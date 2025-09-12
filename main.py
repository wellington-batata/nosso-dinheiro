from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Despesa
from pydantic import BaseModel

from typing import List
from datetime import datetime
from dotenv import load_dotenv

# from openai import OpenAI
from langchain_openai.llms import OpenAI
from langchain.prompts import PromptTemplate

import os
import json

load_dotenv()

# Carregar variáveis de ambiente
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
langOpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                    temperature=0)

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

# Schemas


class DespesaTexto(BaseModel):
    texto: str


class Mensagem(BaseModel):
    message: str
    success: bool

# Função de IA


def analisar_despesa_texto(record: str):
    prompt_template = PromptTemplate.from_template(
        '''
        Extraia as seguintes informações da frase abaixo:
        - descricao
        - valor (número com ponto decimal)
        - categoria
        - data (YYYY-MM-DD; se não houver, usar data de hoje)
        Frase: "{param_record}"
        Responda estritamente em um objeto JSON, por exemplo:
        [
        {{
            "descricao": "Compra no supermercado",
            "valor": 150.75,
            "categoria": "Alimentação",
            "data": "2024-09-05"
        }}
        ]
        Não adicione explicações ou texto adicional.
        '''
    )

    prompt = prompt_template.format(param_record=record)
    print("Prompt enviado à IA:", prompt)
    resp = langOpenAI.invoke(prompt)

    try:
        print("Resposta da IA:", resp)
        return json.loads(resp)
    except (json.JSONDecodeError, AttributeError):
        print("Erro ao decodificar JSON:", resp)
        return None


@app.post("/despesas/nlp", response_model=Mensagem)
def adicionar_despesa_texto(d: DespesaTexto, db: Session = Depends(get_db)):
    dados = analisar_despesa_texto(d.texto)
    if not dados or not isinstance(dados, list) or len(dados) == 0:
        return {"mensagem": "Erro ao processar texto", "id": 0}

    novas_despesas = []
    for item in dados:
        nova_despesa = Despesa(
            descricao=item["descricao"],
            valor=float(item["valor"]),
            categoria=item["categoria"],
            data=datetime.fromisoformat(item["data"]),
            userId=1  # Valor padrão para userId
        )
        print("Nova despesa criada:", nova_despesa)
        novas_despesas.append(nova_despesa)

    db.add_all(novas_despesas)
    db.commit()
    for despesa in novas_despesas:
        db.refresh(despesa)

    return {"message": "Despesa adicionada com sucesso via IA", "success": True}


@app.get("/despesas", response_model=List[dict])
def listar_despesas(userId: int, db: Session = Depends(get_db)):
    despesas = db.query(Despesa).where(Despesa.userId == userId).all()
    return [
        {
            "id": d.id,
            "userId": d.userId,
            "descricao": d.descricao,
            "valor": d.valor,
            "categoria": d.categoria,
            "data": d.data
        }
        for d in despesas
    ]
