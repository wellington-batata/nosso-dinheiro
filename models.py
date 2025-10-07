from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base
from sqlalchemy.dialects.postgresql import JSONB


class Transactions(Base):
    __tablename__ = "Transactions"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True)
    description = Column(String, index=False)
    money = Column(Float)
    category = Column(String, index=True)
    subcategory = Column(String, index=True, nullable=True)
    type = Column(String, index=True, nullable=True)  # credit ou debit
    created_at = Column(DateTime, default=datetime.today())
    event_date = Column(DateTime, default=datetime.today())
    is_recurring = Column(Boolean, nullable=True)
    recurrence_type = Column(String, nullable=True)
    auto_generated = Column(Boolean, nullable=True)
    parent_recurring_id = Column(Integer, nullable=True)


class Categorys(Base):
    __tablename__ = 'Categorys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(50), unique=False, nullable=True)  # credit ou debit
    category = Column(String(100), unique=True, nullable=False)
    # Armazena lista JSON de subcategorias
    subcategorys = Column(JSONB, nullable=True)


class TransactionText(BaseModel):
    texto: str


class Message(BaseModel):
    message: str
    success: bool
