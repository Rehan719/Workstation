from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import random

router = APIRouter(prefix="/economic", tags=["Economic Symbiosis"])

@router.get("/wallet/{user_id}")
async def get_wallet(user_id: str):
    return {
        "balance": 52400.0,
        "currency": "WST",
        "staked": 12000.0,
        "transactions": [
            {"id": "tx-1", "type": "STAKE", "amount": 1000, "status": "confirmed"},
            {"id": "tx-2", "type": "BTO_PURCHASE", "amount": -15000, "status": "confirmed"}
        ]
    }

@router.post("/payment/create")
async def create_payment(amount: float, item: str):
    return {
        "payment_intent": f"pi_{random.randint(100000, 999999)}",
        "amount": amount,
        "item": item,
        "status": "pending"
    }

@router.get("/treasury")
async def get_treasury():
    return {
        "total_reserve": 1420500.0,
        "active_yield": "8.4%",
        "liability_fund": 500000.0,
        "status": "solvent"
    }
