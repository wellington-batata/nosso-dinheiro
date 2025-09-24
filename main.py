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
from models import Transactions, Message, TransactionText
from models import Transactions, Message, TransactionText
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session

from tools.date_now import tratar_data
from prompt_template import pt_date, pt_transaction
from tools.categorys import listar_categorias, montar_prompt as montar_prompt_categorys

# from openai import OpenAI
load_dotenv()

# Carregar variáveis de ambiente
langOpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                    temperature=0)


print(f"Modelo do LangOpenAI: {langOpenAI.model_name}")

# Dependência do DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tool("tratar_data")
def tratar_data_tool(data_str: str = None) -> str:
    """
    Trata datas: se não houver data, retorna a data atual.
    Se a data vier incompleta (apenas mês e dia), completa com o ano atual.
    """
    return tratar_data(data_str)


@tool("tratar_categorias")
def tratar_categorias_tool(input: str) -> str:
    """
    Categorizar: retorna a lista de categorias válidas e suas subcategorias.
    Deve usar apenas o nome da categoria e apenas UMA das subcategoria que melhor correspondem ao termo.
    """
    db = SessionLocal()
    categorias = listar_categorias(db)
    db.close()
    return montar_prompt_categorys(categorias)


tools = [tratar_data_tool, tratar_categorias_tool]
agent = initialize_agent(
    tools=tools,
    llm=langOpenAI,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agente Financeiro - API")


# Função de IA

def analisar_despesa_texto(param_text: str):

    date_now = datetime.now().strftime("%Y-%m-%d")

    prompt_date = PromptTemplate.from_template(pt_date)

    print("Prompt data:", prompt_date)

    chain_data = prompt_date | langOpenAI
    the_date = chain_data.invoke({"date": date_now, "param_text": param_text})

    print("Data extraída:", the_date)

    prompt_template = PromptTemplate.from_template(pt_transaction)

    prompt = prompt_template.format(param_record=param_text, date=the_date)
    print("Prompt enviado à IA:", prompt)

    try:
        resp = agent.run(prompt)
        print("Resposta da IA:", resp)
        return json.loads(resp)
    except (json.JSONDecodeError, AttributeError):
        print("Erro ao decodificar JSON:", resp)
        return None


@app.post("/Transactions", response_model=Message)
def adicionar_despesa_texto(d: TransactionText, userId: int, db: Session = Depends(get_db)):
    dados = analisar_despesa_texto(d.texto)
    if not dados or not isinstance(dados, list) or len(dados) == 0:
        return {"message": "Erro ao processar texto", "id": -1}

    novas_despesas = []
    for item in dados:
        nova_despesa = Transactions(
            description=item["description"],
            money=float(item["value"]),
            category=item["category"],
            subcategory=item["subcategory"],
            event_date=datetime.fromisoformat(item["event_date"]),
            userId=userId
        )
        novas_despesas.append(nova_despesa)

    db.add_all(novas_despesas)
    db.commit()
    for despesa in novas_despesas:
        db.refresh(despesa)

    return {"message": "Despesa adicionada com sucesso via IA", "success": True}


@app.get("/Transactions", response_model=List[dict])
def listar_despesas(userId: int, db: Session = Depends(get_db)):
    despesas = db.query(Transactions).where(
        Transactions.userId == userId).all()
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
