from fastapi import APIRouter
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json
import os

router = APIRouter(prefix="/marketplace/v2", tags=["Living Marketplace"])

DATA_DIR = "agentic_core/data"
WALLET_FILE = os.path.join(DATA_DIR, "creator_wallets.json")
LISTINGS_FILE = os.path.join(DATA_DIR, "user_listings.json")

os.makedirs(DATA_DIR, exist_ok=True)

class MarketplaceListing(BaseModel):
    id: str
    name: str
    creator_id: str
    description: str
    price_wst: float = 0.0
    type: str # tool, reactor, realm
    original_id: Optional[str] = None # For remix tracking
    rating: float = 5.0

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            try: return json.load(f)
            except: return default
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

@router.get("/listings")
async def get_listings():
    return load_json(LISTINGS_FILE, [
        {"id": "usr-001", "name": "Global News Synth", "creator_id": "AlphaUser", "price_wst": 150, "type": "tool", "rating": 4.8},
        {"id": "usr-002", "name": "Bio-Ethics Guard", "creator_id": "BetaDoc", "price_wst": 0, "type": "reactor", "rating": 4.9}
    ])

@router.post("/remix")
async def remix_listing(listing_id: str, user_id: str):
    listings = await get_listings()
    original = next((l for l in listings if l["id"] == listing_id), None)
    if not original: return {"error": "Original not found"}

    new_listing = original.copy()
    new_listing["id"] = f"remix-{listing_id}-{user_id}"
    new_listing["name"] = f"{original['name']} (Remix)"
    new_listing["creator_id"] = user_id
    new_listing["original_id"] = listing_id

    # Save simulation
    all_usr = load_json(LISTINGS_FILE, [])
    all_usr.append(new_listing)
    save_json(LISTINGS_FILE, all_usr)
    return {"status": "remixed", "new_id": new_listing["id"]}

@router.get("/wallet/{user_id}")
async def get_creator_wallet(user_id: str):
    wallets = load_json(WALLET_FILE, {})
    return wallets.get(user_id, {"balance_wst": 0, "transactions": []})

@router.post("/purchase")
async def purchase_listing(listing_id: str, buyer_id: str):
    # Simulated purchase logic: 70% to creator, 30% to platform
    listings = await get_listings()
    item = next((l for l in listings if l["id"] == listing_id), None)
    if not item: return {"error": "Item not found"}

    price = item.get("price_wst", 0)
    creator_share = price * 0.7

    wallets = load_json(WALLET_FILE, {})
    creator_id = item["creator_id"]

    c_wallet = wallets.get(creator_id, {"balance_wst": 0, "transactions": []})
    c_wallet["balance_wst"] += creator_share
    c_wallet["transactions"].append({"type": "sale", "item": item["name"], "amount": creator_share})

    wallets[creator_id] = c_wallet
    save_json(WALLET_FILE, wallets)
    return {"status": "purchased", "creator_share": creator_share}
