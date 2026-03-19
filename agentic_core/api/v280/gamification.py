from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime
import json
import os

router = APIRouter(prefix="/gamification", tags=["Gamification & Quests"])

DATA_DIR = "agentic_core/data"
GAMIFICATION_FILE = os.path.join(DATA_DIR, "gamification.json")
QUEST_FILE = os.path.join(DATA_DIR, "quests.json")

os.makedirs(DATA_DIR, exist_ok=True)

class UserStats(BaseModel):
    user_id: str
    xp: int = 0
    level: int = 1
    badges: List[str] = []
    completed_quests: List[str] = []
    last_updated: datetime.datetime = datetime.datetime.now()

class Quest(BaseModel):
    id: str
    title: str
    description: str
    xp_reward: int
    badge_reward: Optional[str] = None
    category: str # onboarding, exploration, mastery, domain
    status: str = "available" # available, in_progress, completed

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

@router.get("/stats/{user_id}", response_model=UserStats)
async def get_stats(user_id: str):
    store = load_json(GAMIFICATION_FILE, {})
    return store.get(user_id, UserStats(user_id=user_id))

@router.post("/xp")
async def add_xp(user_id: str, amount: int):
    store = load_json(GAMIFICATION_FILE, {})
    stats_data = store.get(user_id, UserStats(user_id=user_id).dict())
    if isinstance(stats_data, dict):
        stats = UserStats(**stats_data)
    else:
        stats = stats_data

    stats.xp += amount
    # Simple leveling logic: level = floor(sqrt(xp/100)) + 1
    new_level = int((stats.xp / 100)**0.5) + 1
    leveled_up = new_level > stats.level
    stats.level = new_level
    stats.last_updated = datetime.datetime.now()

    store[user_id] = stats.dict()
    save_json(GAMIFICATION_FILE, store)
    return {"status": "success", "new_xp": stats.xp, "new_level": stats.level, "leveled_up": leveled_up}

@router.get("/quests")
async def get_quests(user_id: str):
    quests = load_json(QUEST_FILE, [
        {"id": "q-001", "title": "First Pulse", "description": "Visit the Dashboard for the first time.", "xp_reward": 50, "category": "onboarding"},
        {"id": "q-002", "title": "Direct Dialogue", "description": "Issue your first directive to the AI CEO.", "xp_reward": 100, "category": "onboarding"},
        {"id": "q-003", "title": "BTO Architect", "description": "Configure a custom agentic infrastructure.", "xp_reward": 200, "badge_reward": "Architect", "category": "mastery"},
        {"id": "q-004", "title": "Domain Explorer", "description": "Visit all five great domain hubs.", "xp_reward": 500, "badge_reward": "Polymath", "category": "exploration"}
    ])
    return quests

@router.post("/quests/complete")
async def complete_quest(user_id: str, quest_id: str):
    store = load_json(GAMIFICATION_FILE, {})
    stats_data = store.get(user_id, UserStats(user_id=user_id).dict())
    stats = UserStats(**stats_data)

    if quest_id in stats.completed_quests:
        return {"status": "already_completed"}

    quests = await get_quests(user_id)
    quest = next((q for q in quests if q["id"] == quest_id), None)
    if not quest:
        raise HTTPException(status_code=404, detail="Quest not found")

    stats.completed_quests.append(quest_id)
    stats.xp += quest["xp_reward"]
    if quest.get("badge_reward") and quest["badge_reward"] not in stats.badges:
        stats.badges.append(quest["badge_reward"])

    stats.last_updated = datetime.datetime.now()
    store[user_id] = stats.dict()
    save_json(GAMIFICATION_FILE, store)
    return {"status": "quest_completed", "reward": quest["xp_reward"], "badge": quest.get("badge_reward")}
