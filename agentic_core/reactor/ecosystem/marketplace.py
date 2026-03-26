import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select

logger = logging.getLogger(__name__)

class AgentRecord(SQLModel, table=True):
    """v0.2: Agent Marketplace Database Schema."""
    id: str = Field(primary_key=True)
    name: str
    creator: str
    blueprint_json: str
    rating: float = 0.0
    votes: int = 0
    version: int = 1
    timestamp: str

class AgentMarketplace:
    """v0.2: Agent Marketplace Registry (SQLite-backed)."""
    def __init__(self, db_path: str = "agentic_core/data/marketplace.db"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(self.engine)

    def publish_agent(self, blueprint: Dict[str, Any], creator: str):
        """v0.2: Publishes or versions an agent."""
        import json
        agent_id = blueprint.get("id", f"pub-{os.urandom(4).hex()}")

        with Session(self.engine) as session:
            existing = session.get(AgentRecord, agent_id)
            if existing:
                existing.version += 1
                existing.blueprint_json = json.dumps(blueprint)
                existing.timestamp = datetime.utcnow().isoformat()
                session.add(existing)
            else:
                record = AgentRecord(
                    id=agent_id,
                    name=blueprint.get("name", "Unnamed Agent"),
                    creator=creator,
                    blueprint_json=json.dumps(blueprint),
                    timestamp=datetime.utcnow().isoformat()
                )
                session.add(record)
            session.commit()
        return agent_id

    def list_agents(self) -> List[Dict[str, Any]]:
        with Session(self.engine) as session:
            statement = select(AgentRecord)
            results = session.exec(statement).all()
            return [r.dict() for r in results]

    def rate_agent(self, agent_id: str, rating: int):
        """v0.2: Rate an agent in the database."""
        with Session(self.engine) as session:
            record = session.get(AgentRecord, agent_id)
            if record:
                record.votes += 1
                record.rating = (record.rating * (record.votes - 1) + rating) / record.votes
                session.add(record)
                session.commit()
                return True
        return False

    def delete_agent(self, agent_id: str):
        """v0.3: Delete an agent from the marketplace."""
        with Session(self.engine) as session:
            record = session.get(AgentRecord, agent_id)
            if record:
                session.delete(record)
                session.commit()
                return True
        return False

marketplace = AgentMarketplace()
