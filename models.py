from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base
from sqlalchemy.dialects.postgresql import JSONB


class Expenses(Base):
    __tablename__ = "Expenses"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True)
    description = Column(String, index=False)
    money = Column(Float)
    category = Column(String, index=True)
    subcategory = Column(String, index=True, nullable=True)
    event_date = Column(DateTime, default=datetime.today())


class Categorys(Base):
    __tablename__ = 'Categorys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(100), unique=True, nullable=False)
    # Armazena lista JSON de subcategorias
    subcategorys = Column(JSONB, nullable=True)


class ExpensesText(BaseModel):
    texto: str


class Message(BaseModel):
    message: str
    success: bool
