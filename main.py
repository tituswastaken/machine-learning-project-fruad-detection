from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routers import auth, transactions


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fraud Detection API",
    description="Real-time fraud detection system with JWT authentication",
    version="1.0.0"
)

# C
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }