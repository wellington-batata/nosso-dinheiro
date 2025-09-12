from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True)
    descricao = Column(String, index=False)
    valor = Column(Float)
    categoria = Column(String, index=True)
    data = Column(DateTime, default=datetime.today())
