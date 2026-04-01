from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String, default="viewer")  # viewer, analyst, admin


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income or expense
    category = Column(String, index=True)
    date = Column(Date, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))