from fastapi import FastAPI, Depends
import json
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_openai.llms import OpenAI
from datetime import datetime
from typing import List
from models import Expenses, Message, ExpensesText
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from tools.date_now import tratar_data

# from openai import OpenAI
load_dotenv()

# Carregar variáveis de ambiente
langOpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

# Inicializa o agente com a tool tratar_data_tool


@tool("tratar_data")
def tratar_data_tool(data_str: str = None) -> str:
    """
    Trata datas: se não houver data, retorna a data atual.
    Se a data vier incompleta (apenas mês e dia), completa com o ano atual.
    """
    return tratar_data(data_str)


tools = [tratar_data_tool]
agent = initialize_agent(
    tools=tools,
    llm=langOpenAI,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agente Financeiro - API")

# Dependência do DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Função de IA

def analisar_despesa_texto(param_text: str):

    date_now = datetime.now().strftime("%Y-%m-%d")

    prompt_date = PromptTemplate.from_template(
        '''
    Considere que a data de hoje é {date}.
    Extraia e converta qualquer expressão de tempo do texto abaixo para o formato YYYY-MM-DD.
    Se não houver expressão de tempo, retorne a data atual.
    Texto: "{param_text}"
    Responda apenas com a data.
    '''
    )

    print("Prompt data:", prompt_date)

    chain_data = prompt_date | langOpenAI
    the_date = chain_data.invoke({"date": date_now, "param_text": param_text})

    print("Data extraída:", the_date)

    prompt_template = PromptTemplate.from_template(
        '''
        Extraia as seguintes informações do texto abaixo:
        - description (descrição da despesa)
        - value (número com ponto decimal)
        - category
        - date (YYYY-MM-DD; use esta data {date})
        texto: "{param_record}"
        Responda estritamente em um objeto JSON, por exemplo:
        [
        {{
            "description": "Compra no supermercado",
            "value": 150.75,
            "category": "Alimentação",
            "event_date": "2024-09-05"
        }}
        ]
        '''
    )

    prompt = prompt_template.format(param_record=param_text, date=the_date)
    print("Prompt enviado à IA:", prompt)

    try:
        resp = agent.run(prompt)
        print("Resposta da IA:", resp)
        return json.loads(resp)
    except (json.JSONDecodeError, AttributeError):
        print("Erro ao decodificar JSON:", resp)
        return None


@app.post("/expenses", response_model=Message)
def adicionar_despesa_texto(d: ExpensesText, userId: int, db: Session = Depends(get_db)):
    dados = analisar_despesa_texto(d.texto)
    if not dados or not isinstance(dados, list) or len(dados) == 0:
        return {"mensagem": "Erro ao processar texto", "id": 0}

    novas_despesas = []
    for item in dados:
        nova_despesa = Expenses(
            description=item["description"],
            money=float(item["value"]),
            category=item["category"],
            event_date=datetime.fromisoformat(item["event_date"]),
            userId=userId
        )
        novas_despesas.append(nova_despesa)

    db.add_all(novas_despesas)
    db.commit()
    for despesa in novas_despesas:
        db.refresh(despesa)

    return {"message": "Despesa adicionada com sucesso via IA", "success": True}


@app.get("/expenses", response_model=List[dict])
def listar_despesas(userId: int, db: Session = Depends(get_db)):
    despesas = db.query(Expenses).where(Expenses.userId == userId).all()
    return [
        {
            "id": d.id,
            "userId": d.userId,
            "description": d.description,
            "money": d.money,
            "category": d.category,
            "event_date": d.event_date
        }
        for d in despesas
    ]
