from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas

def get_transactions(db: Session, category: str = None, transaction_type: str = None):
    """Fetches transactions with optional filtering."""
    query = db.query(models.Transaction)
    if category:
        query = query.filter(models.Transaction.category == category)
    if transaction_type:
        query = query.filter(models.Transaction.type == transaction_type)
    return query.all()


def get_transaction_by_id(db: Session, transaction_id: int):
    """Helper to find a single transaction."""
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()


def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    """Saves a new financial record to the database."""
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, db_transaction: models.Transaction, updated_data: schemas.TransactionCreate):
    """Updates an existing record using setattr for efficiency."""
    for key, value in updated_data.dict().items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, db_transaction: models.Transaction):
    """Removes a record from the database."""
    db.delete(db_transaction)
    db.commit()
    return True


def get_financial_summary(db: Session):
    """Calculates totals and category breakdowns using SQL aggregations."""
    total_income = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == "income").scalar() or 0.0
    total_expense = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == "expense").scalar() or 0.0
    
    category_data = db.query(
        models.Transaction.category, 
        func.sum(models.Transaction.amount)
    ).group_by(models.Transaction.category).all()
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "current_balance": total_income - total_expense,
        "category_breakdown": {cat: amt for cat, amt in category_data}
    }