from sqlalchemy import Column,String,Float,Boolean,DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    #definign user table content
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.now)
    #defining realtionship : 
    transactions= relationship("Transaction",back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"

    #defining tbale content : 
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)

    amount = Column(Float, nullable=False)
    time = Column(Float, nullable=False)
    v1 = Column(Float)
    v2 = Column(Float)
    v3 = Column(Float)
    v4 = Column(Float)
    v5 = Column(Float)
    v6 = Column(Float)
    v7 = Column(Float)
    v8 = Column(Float)
    v9 = Column(Float)
    v10 = Column(Float)
    v11 = Column(Float)
    v12 = Column(Float)
    v13 = Column(Float)
    v14 = Column(Float)
    v15 = Column(Float)
    v16 = Column(Float)
    v17 = Column(Float)
    v18 = Column(Float)
    v19 = Column(Float)
    v20 = Column(Float)
    v21 = Column(Float)
    v22 = Column(Float)
    v23 = Column(Float)
    v24 = Column(Float)
    v25 = Column(Float)
    v26 = Column(Float)
    v27 = Column(Float)
    v28 = Column(Float)
    is_fraud = Column(Boolean, default=False)
    fraud_probability = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")
    status = Column(String, default="APPROVED")
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="transactions")

# Drop and recreate all tables
from database import engine

Base.metadata.drop_all(bind=engine)    # drops existing tables
Base.metadata.create_all(bind=engine)  # recreates with new structure
print("Tables created successfully")
