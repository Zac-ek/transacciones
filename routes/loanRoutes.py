from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from validations import get_current_user
import crud.loan
import config.db
import schemas.loans
import models.loan

loan = APIRouter()

models.loan.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@loan.get("/loan/", response_model=List[schemas.loans.Loan], tags=["Loans"])
async def read_loans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.loan.get_loans(db=db, skip=skip, limit=limit)

@loan.post("/loan/", response_model=schemas.loans.Loan, tags=["Loans"])
async def create_loan(loan_data: schemas.loans.LoanCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return crud.loan.create_loan(db=db, loan=loan_data)

@loan.put("/loan/{id}", response_model=schemas.loans.Loan, tags=["Loans"])
async def update_loan(id: int, loan_data: schemas.loans.LoanUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_loan = crud.loan.update_loan(db=db, loan_id=id, loan=loan_data)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

@loan.delete("/loan/{id}", response_model=schemas.loans.Loan, tags=["Loans"])
async def delete_loan(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_loan = crud.loan.delete_loan(db=db, loan_id=id)
    if db_loan is None:
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan
