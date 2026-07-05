from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Transaction, User
from schemas import TransactionInput, TransactionResponse
from dependencies import get_current_user
import numpy as np
import joblib
import uuid
from datetime import datetime


router = APIRouter(prefix="/transactions", tags=["Transactions"])

#loading models: 
model = joblib.load("fraud_detection_model.pkl")
scaler_time = joblib.load("scaler_time.pkl")
scaler_amount = joblib.load("scaler_amount.pkl")

#api requests : 

#add a transaction and return the output : 
@router.post("/",response_model=TransactionResponse,status_code=status.HTTP_201_CREATED)
def process_transaction(
    input : TransactionInput,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    #store data in such a format that the model expects  :
    data = np.array([[
        input.Time,
        input.V1, input.V2, input.V3,
        input.V4, input.V5, input.V6,
        input.V7, input.V8, input.V9,
        input.V10, input.V11, input.V12,
        input.V13, input.V14, input.V15,
        input.V16, input.V17, input.V18,
        input.V19, input.V20, input.V21,
        input.V22, input.V23, input.V24,
        input.V25, input.V26, input.V27,
        input.V28, input.Amount

    ]])


    #setting time and date to lower values (between 0 and 1)
    data[0, 0] = scaler_time.transform([[input.Time]])[0][0]
    data[0, -1] = scaler_amount.transform([[input.Amount]])[0][0]

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    is_fraud = bool(prediction)
    fraud_probability =round(float(probability),4)

    risk_level = "High" if fraud_probability > 0.7 else "MEDIUM" if fraud_probability > 0.3 else "LOW"
    status_val = "Flagged" if is_fraud else "APPROVED"

    transaction = Transaction(
        user_id=current_user.id,
        amount=input.Amount,
        time=input.Time,
        v1=input.V1, v2=input.V2, v3=input.V3,
        v4=input.V4, v5=input.V5, v6=input.V6,
        v7=input.V7, v8=input.V8, v9=input.V9,
        v10=input.V10, v11=input.V11, v12=input.V12,
        v13=input.V13, v14=input.V14, v15=input.V15,
        v16=input.V16, v17=input.V17, v18=input.V18,
        v19=input.V19, v20=input.V20, v21=input.V21,
        v22=input.V22, v23=input.V23, v24=input.V24,
        v25=input.V25, v26=input.V26, v27=input.V27,
        v28=input.V28,
        is_fraud=is_fraud,
        fraud_probability=fraud_probability,
        risk_level=risk_level,
        status=status_val,
        timestamp=datetime.now()
    )


    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


# now get endpoint to get all saved transactions in db :

@router.get("/",response_model=list[TransactionResponse])
def get_transactions(
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
    ):

    transactions = db.query(Transaction)\
        .filter(Transaction.user_id == current_user.id)\
        .order_by(Transaction.timestamp)\
        .all()
    
    return transactions


@router.get("/{transaction_id}",response_model=TransactionResponse)
def get_transaction(
    transaction_id : str,
    db : Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
    ):

    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction


@router.get("/stats/summary")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Transaction)\
        .filter(Transaction.user_id == current_user.id)\
        .count()

    fraud = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.is_fraud == True
    ).count()

    high_risk = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.risk_level == "HIGH"
    ).count()

    return {
        "total_transactions": total,
        "fraud_detected": fraud,
        "fraud_rate": round((fraud / total * 100), 2) if total > 0 else 0,
        "high_risk_count": high_risk
    }    

    






