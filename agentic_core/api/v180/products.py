from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
import os

router = APIRouter(prefix="/products", tags=["BTO Products"])

PRODUCTS_FILE = "packages/shared/data/btoProducts.json"

@router.get("/", response_model=List[Dict[str, Any]])
async def get_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r") as f:
        return json.load(f)

@router.get("/{product_id}")
async def get_product(product_id: str):
    if not os.path.exists(PRODUCTS_FILE):
        raise HTTPException(status_code=404, detail="Products not found")
    with open(PRODUCTS_FILE, "r") as f:
        products = json.load(f)
        product = next((p for p in products if p["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
