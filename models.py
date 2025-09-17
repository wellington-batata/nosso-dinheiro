from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


class Expenses(Base):
    __tablename__ = "Expenses"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, index=True)
    description = Column(String, index=False)
    money = Column(Float)
    category = Column(String, index=True)
    event_date = Column(DateTime, default=datetime.today())


class ExpensesText(BaseModel):
    texto: str


class Message(BaseModel):
    message: str
    success: bool
