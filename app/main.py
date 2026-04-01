from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from fastapi.responses import StreamingResponse

from . import models, schemas, database, crud

# Initialize Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Personal Finance System API",
    description="A robust backend for financial tracking with RBAC and Analytics.",
    version="1.0.0"
)

# --- ROLE SECURITY DEPENDENCIES ---

def verify_role(x_user_role: str = Header(None)):
    if not x_user_role:
        raise HTTPException(status_code=400, detail="X-User-Role header missing")
    return x_user_role.lower()

def require_admin(role: str = Depends(verify_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only Admins can perform this action")
    return role

def require_analyst_or_admin(role: str = Depends(verify_role)):
    if role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions for analytics")
    return role

# --- ROUTES ---

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Finance Tracker API is online", "docs": "/docs"}

@app.post("/transactions/", response_model=schemas.Transaction, tags=["Transactions"])
def create_entry(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(database.get_db),
    role: str = Depends(require_admin)
):
    return crud.create_transaction(db=db, transaction=transaction, user_id=1)

@app.get("/transactions/", response_model=List[schemas.Transaction], tags=["Transactions"])
def list_entries(
    category: str = None, 
    transaction_type: str = None, 
    db: Session = Depends(database.get_db)
):
    return crud.get_transactions(db, category, transaction_type)

@app.get("/transactions/summary/", tags=["Analytics"])
def get_summary(
    db: Session = Depends(database.get_db),
    role: str = Depends(require_analyst_or_admin)
):
    return crud.get_financial_summary(db)

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction, tags=["Transactions"])
def update_entry(
    transaction_id: int, 
    updated_data: schemas.TransactionCreate, 
    db: Session = Depends(database.get_db),
    role: str = Depends(require_admin)
):
    db_entry = crud.get_transaction_by_id(db, transaction_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud.update_transaction(db, db_entry, updated_data)

@app.delete("/transactions/{transaction_id}", tags=["Transactions"])
def delete_entry(
    transaction_id: int, 
    db: Session = Depends(database.get_db),
    role: str = Depends(require_admin)
):
    db_entry = crud.get_transaction_by_id(db, transaction_id)
    if not db_entry:
        raise HTTPException(status_code=404, detail="Transaction not found")
    crud.delete_transaction(db, db_entry)
    return {"message": f"Successfully deleted transaction {transaction_id}"}

@app.get("/transactions/export/csv", tags=["Analytics"])
def export_csv(
    db: Session = Depends(database.get_db), 
    role: str = Depends(require_analyst_or_admin)
):
    transactions = crud.get_transactions(db)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Amount", "Type", "Category", "Date", "Description"])
    
    for t in transactions:
        writer.writerow([t.id, t.amount, t.type, t.category, t.date, t.description])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=finance_report.csv"}
    )