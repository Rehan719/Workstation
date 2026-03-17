from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

router = APIRouter(prefix="/user", tags=["Personalization"])

class UserActivity(BaseModel):
    action: str
    target_module: str
    metadata: Dict[str, Any] = {}
    dwell_time: float = 0.0 # seconds
    interaction_speed: float = 1.0 # 1.0 is baseline
    error_count: int = 0

class UserPreferences(BaseModel):
    theme: str = "legacy"
    smart_sidebar_enabled: bool = True
    notifications_enabled: bool = True
    priority_modules: List[str] = []
    density_preference: str = "auto" # comfortable, compact, auto

import json
import os

# v146.0 PERSISTENCE LAYER (Simulated with JSON for Perfection)
DATA_DIR = "agentic_core/data"
PREFS_FILE = os.path.join(DATA_DIR, "user_preferences.json")
LOG_FILE = os.path.join(DATA_DIR, "activity_log.json")

os.makedirs(DATA_DIR, exist_ok=True)

def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except:
                return default
    return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)

@router.get("/preferences", response_model=UserPreferences)
async def get_preferences(user_id: str = "guardian"):
    store = load_json(PREFS_FILE, {})
    return store.get(user_id, UserPreferences())

@router.post("/preferences")
async def update_preferences(prefs: UserPreferences, user_id: str = "guardian"):
    store = load_json(PREFS_FILE, {})
    store[user_id] = prefs.dict()
    save_json(PREFS_FILE, store)
    return {"status": "success", "updated_at": datetime.datetime.now()}

@router.post("/activity")
async def log_activity(activity: UserActivity, user_id: str = "guardian"):
    log = load_json(LOG_FILE, [])
    log.append({
        "user_id": user_id,
        "action": activity.action,
        "module": activity.target_module,
        "dwell_time": activity.dwell_time,
        "interaction_speed": activity.interaction_speed,
        "error_count": activity.error_count,
        "timestamp": datetime.datetime.now()
    })
    save_json(LOG_FILE, log)
    return {"status": "recorded"}

# v146.0 CUSTOM A/B TESTING FRAMEWORK
AB_CONFIG_FILE = os.path.join(DATA_DIR, "ab_tests.json")

class ABTest(BaseModel):
    test_id: str
    variants: List[str]
    active: bool = True

@router.get("/ab-tests")
async def get_active_tests():
    return load_json(AB_CONFIG_FILE, [
        {"test_id": "sidebar-order", "variants": ["static", "predictive"], "active": True},
        {"test_id": "onboarding-flow", "variants": ["sequential", "adaptive"], "active": True}
    ])

@router.get("/recommendations")
async def get_recommendations(user_id: str = "guardian"):
    log = load_json(LOG_FILE, [])
    counts = {}
    dwell_total = {}
    errors = 0

    for entry in log:
        if entry["user_id"] == user_id:
            m = entry["module"]
            counts[m] = counts.get(m, 0) + 1
            dwell_total[m] = dwell_total.get(m, 0) + entry.get("dwell_time", 0)
            errors += entry.get("error_count", 0)

    sorted_modules = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    recommended = [m for m, _ in sorted_modules[:3]]

    if not recommended:
        recommended = ["dashboard", "ceo", "bto"]

    return {
        "recommended_modules": recommended,
        "reasoning": "Based on your recent engagement patterns."
    }
