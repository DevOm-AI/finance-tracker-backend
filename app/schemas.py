from pydantic import BaseModel
from datetime import date
from typing import Optional


class TransactionBase(BaseModel):
    amount: float
    type: str  # income or expense
    category: str
    date: date
    description: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 