"""
Integration tests for the MVP spine endpoints.

Tests verify that each real AI endpoint:
1. Returns a 2xx response
2. Does NOT return a hardcoded/simulated response (checks for content length
   that a real LLM call would produce)
3. Does NOT contain obvious simulation markers

Run with:
    pytest integration_tests/test_mvp_spine.py --noconftest -v

AI-dependent tests are automatically skipped when no provider is configured.
Set ANTHROPIC_API_KEY (or have Ollama running) for the full suite.
"""
import os
import json
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("PROJECTS_DIR", "data/test_projects")
os.environ.setdefault("SYNTHESIS_OUTPUT_DIR", "data/test_synthesis")
os.environ.setdefault("PROPOSALS_DIR", "data/test_proposals")

_AI_AVAILABLE = bool(
    os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
)
_ai_only = pytest.mark.skipif(
    not _AI_AVAILABLE,
    reason="Skipped — no ANTHROPIC_API_KEY or OPENAI_API_KEY set"
)


@pytest.fixture(scope="module")
def client():
    from agentic_core.app_mvp import app
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ── Health ───────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_health_versioned(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200


# ── Projects CRUD ────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def project_id(client):
    r = client.post("/api/v1/projects/", json={
        "title": "Test Integration Project",
        "description": "Created by automated test",
        "realm": "enterprise",
        "domain": "product",
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]
    yield pid
    client.delete(f"/api/v1/projects/{pid}")


def test_create_project(project_id):
    assert project_id


def test_list_projects(client, project_id):
    r = client.get("/api/v1/projects/")
    assert r.status_code == 200
    ids = [p["id"] for p in r.json()]
    assert project_id in ids


def test_get_project(client, project_id):
    r = client.get(f"/api/v1/projects/{project_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["stage"] == "concept"
    assert data["title"] == "Test Integration Project"


def test_projects_stats_summary(client):
    r = client.get("/api/v1/projects/stats/summary")
    assert r.status_code == 200
    body = r.json()
    assert "total_projects" in body
    assert isinstance(body["total_projects"], int)


# ── C-Suite ───────────────────────────────────────────────────────────────────

def test_csuite_cfo_metrics(client):
    """CFO metrics must be computed from real project store, not literals."""
    r = client.get("/api/csuite/cfo/metrics")
    assert r.status_code == 200
    body = r.json()
    # Response has 'revenue' (computed from project store) and a kpis array
    assert "revenue" in body or "portfolio_value" in body, (
        f"Expected revenue or portfolio_value in CFO response, got: {list(body.keys())}"
    )
    # Must not return the old hardcoded value
    assert body.get("revenue") != 1420500
    assert body.get("portfolio_value") != 1420500


def test_biometrics_status(client):
    """Vitals must come from real psutil data including immune system."""
    r = client.get("/api/v1/biometrics/status")
    assert r.status_code == 200
    body = r.json()
    assert "cardiovascular" in body
    assert "cognition" in body
    assert "immune" in body
    assert "metabolic" in body
    flow = body["cardiovascular"]["resource_flow"]
    assert isinstance(flow, (int, float))
    assert 0 <= flow <= 100
    immune = body["immune"]
    assert "health" in immune
    assert 0.0 <= immune["health"] <= 1.0
    assert immune["threat_level"] in ("NOMINAL", "ELEVATED", "HIGH", "CRITICAL")


# ── AI endpoints — skipped without API key ───────────────────────────────────

def _assert_real_response(text: str, min_chars: int = 100):
    assert text, "Response was empty"
    assert len(text) >= min_chars, (
        f"Response too short ({len(text)} chars) — likely a fallback/error: {text!r}"
    )
    for phrase in ["# Simulation", "HARDCODED", "TODO: implement", "random.uniform"]:
        assert phrase.lower() not in text.lower(), f"Simulation marker found: {phrase!r}"


@_ai_only
def test_factory_produce_streams(client):
    """Factory must stream a real AI response."""
    with client.stream("POST", "/api/v1/factory/produce", json={
        "name": "Integration Test Business Model",
        "product_type": "business_model",
        "domain": "enterprise",
        "description": "A SaaS platform for project management",
    }) as resp:
        assert resp.status_code == 200
        accumulated = ""
        for line in resp.iter_lines():
            if line.startswith("data: "):
                try:
                    ev = json.loads(line[6:])
                    if "token" in ev:
                        accumulated += ev["token"].replace("\n", "\n")
                    if ev.get("done"):
                        break
                    if ev.get("error"):
                        pytest.fail(f"Factory error: {ev['error']}")
                except json.JSONDecodeError:
                    pass
        _assert_real_response(accumulated)


@_ai_only
def test_ceo_generate_blueprint(client):
    """CEO blueprint generation must return real AI content."""
    r = client.post("/api/v290/ceo/generate-blueprint", json={
        "intent": "An AI-powered tutoring platform",
        "realm": "enterprise",
        "domain": "education",
        "stage": "concept",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "complete"
    _assert_real_response(body["deliverable"])


@_ai_only
def test_project_run_streams(client, project_id):
    """Project run must stream a real AI output."""
    with client.stream("POST", f"/api/v1/projects/{project_id}/run") as resp:
        assert resp.status_code == 200
        accumulated = ""
        for line in resp.iter_lines():
            if line.startswith("data: "):
                try:
                    ev = json.loads(line[6:])
                    if "token" in ev:
                        accumulated += ev["token"].replace("\n", "\n")
                    if ev.get("done"):
                        break
                    if ev.get("error"):
                        pytest.fail(f"Project run error: {ev['error']}")
                except json.JSONDecodeError:
                    pass
        _assert_real_response(accumulated)


# ── Law domain ────────────────────────────────────────────────────────────────

def test_law_templates(client):
    r = client.get("/api/v1/law/templates")
    assert r.status_code == 200
    body = r.json()
    assert "templates" in body
    assert len(body["templates"]) >= 5
    assert all("id" in t and "name" in t for t in body["templates"])


@_ai_only
def test_law_analyse(client):
    r = client.post("/api/v1/law/analyse", json={
        "document_text": (
            "This Non-Disclosure Agreement is entered into between Party A and Party B. "
            "Party B agrees to keep all information confidential for a period of 1 year. "
            "No limitations on liability are specified."
        ),
        "document_type": "nda",
        "jurisdiction": "England & Wales",
        "analysis_focus": "risk",
    })
    assert r.status_code == 200
    body = r.json()
    assert "analysis" in body
    _assert_real_response(body["analysis"])


@_ai_only
def test_law_generate(client):
    r = client.post("/api/v1/law/generate", json={
        "template_id": "nda",
        "parties": {"party_a": "Workstation Ltd", "party_b": "Client Co"},
        "jurisdiction": "England & Wales",
    })
    assert r.status_code == 200
    body = r.json()
    assert "document" in body
    _assert_real_response(body["document"])


# ── Career domain ─────────────────────────────────────────────────────────────

@_ai_only
def test_career_generate(client):
    """Career document generation must call gateway and return real content."""
    r = client.post("/api/v1/career/generate", json={
        "file_ids": [],
        "company_website": "https://example.com",
        "instructions": "Tailor for a Senior Software Engineer role at a fintech startup.",
        "output_types": ["cover_letter"],
    })
    assert r.status_code == 200
    body = r.json()
    assert "results" in body
    assert len(body["results"]) == 1
    result = body["results"][0]
    assert result["output_type"] == "cover_letter"
    _assert_real_response(result["content"])


@_ai_only
def test_career_job_search(client):
    """Job search must return structured listings."""
    r = client.post("/api/v1/career/job-search", json={
        "query": "Senior Python developer remote",
        "limit": 3,
    })
    assert r.status_code == 200
    body = r.json()
    assert "results" in body
    assert isinstance(body["results"], list)


# ── Science domain ────────────────────────────────────────────────────────────

def test_science_methodologies(client):
    r = client.get("/api/v1/science/methodologies")
    assert r.status_code == 200
    body = r.json()
    assert "methodologies" in body
    assert len(body["methodologies"]) >= 5


@_ai_only
def test_science_synthesise(client):
    r = client.post("/api/v1/science/synthesise", json={
        "research_question": "What is the effect of sleep deprivation on cognitive performance?",
        "domain": "neuroscience",
        "methodology": "systematic_review",
        "depth": "brief",
    })
    assert r.status_code == 200
    body = r.json()
    assert "report" in body
    _assert_real_response(body["report"])


# ── Education domain ──────────────────────────────────────────────────────────

def test_education_frameworks(client):
    r = client.get("/api/v1/education/frameworks")
    assert r.status_code == 200
    body = r.json()
    assert "frameworks" in body
    assert len(body["frameworks"]) >= 5


@_ai_only
def test_education_lesson_plan(client):
    r = client.post("/api/v1/education/lesson-plan", json={
        "subject": "Mathematics",
        "topic": "Quadratic Equations",
        "level": "GCSE Year 10",
        "duration_minutes": 60,
        "class_size": 28,
    })
    assert r.status_code == 200
    body = r.json()
    assert "lesson_plan" in body
    _assert_real_response(body["lesson_plan"])


# ── Care domain ───────────────────────────────────────────────────────────────

def test_care_tools(client):
    r = client.get("/api/v1/care/tools")
    assert r.status_code == 200
    body = r.json()
    assert "tools" in body
    assert len(body["tools"]) >= 5


# ── Evolution engine ──────────────────────────────────────────────────────────

def test_evolution_proposals_empty(client):
    """Evolution proposals endpoint must return a list (may be empty initially)."""
    r = client.get("/api/v191/evolution/proposals")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_evolution_history(client):
    r = client.get("/api/v191/evolution/history")
    assert r.status_code == 200
    body = r.json()
    assert "resolved" in body
    assert "total_approved" in body


@_ai_only
def test_evolution_generate(client):
    """Evolution engine must generate AI-backed proposals."""
    r = client.post("/api/v191/evolution/proposals/generate", json={
        "context": "We have 2 projects in concept stage and good system health."
    })
    assert r.status_code == 200
    body = r.json()
    assert "proposals" in body
    assert len(body["proposals"]) >= 1
    p = body["proposals"][0]
    assert "id" in p and "title" in p and "status" in p
    assert p["status"] == "pending"


# ── Religion domain ───────────────────────────────────────────────────────────

def test_religion_schools(client):
    r = client.get("/api/v1/religion/schools")
    assert r.status_code == 200
    body = r.json()
    assert "madhabs" in body
    assert len(body["madhabs"]) >= 4


# ── Self-healing system ───────────────────────────────────────────────────────

def test_self_healing_status(client):
    r = client.get("/api/v1/organism/self-healing/status")
    assert r.status_code == 200
    body = r.json()
    assert "overall_health" in body
    assert "circuits" in body
    assert 0.0 <= body["overall_health"] <= 1.0


def test_self_healing_log(client):
    r = client.get("/api/v1/organism/self-healing/log")
    assert r.status_code == 200
    assert "events" in r.json()


# ── Agent swarm ───────────────────────────────────────────────────────────────

def test_swarm_agents(client):
    r = client.get("/api/v1/swarm/agents")
    assert r.status_code == 200
    body = r.json()
    assert "agents" in body
    assert len(body["agents"]) >= 8


def test_swarm_runs(client):
    r = client.get("/api/v1/swarm/runs")
    assert r.status_code == 200
    assert "runs" in r.json()


# ── Digital twin ──────────────────────────────────────────────────────────────

def test_twin_models_list(client):
    r = client.get("/api/v1/twin/models")
    assert r.status_code == 200
    body = r.json()
    assert "models" in body
    assert isinstance(body["models"], list)


# ── VSB Studio ────────────────────────────────────────────────────────────────

def test_studio_vsb_list(client):
    r = client.get("/api/v1/studio/vsb")
    assert r.status_code == 200
    body = r.json()
    assert "entities" in body
    assert isinstance(body["entities"], list)


@_ai_only
def test_swarm_delegate(client):
    """Swarm must engage agents and return CEO synthesis."""
    r = client.post("/api/v1/swarm/delegate", json={
        "task": "How should we price a SaaS product for the education market?",
        "agent_ids": ["CFO", "CMO"],
        "domain": "education",
        "realm": "enterprise",
    })
    assert r.status_code == 200
    body = r.json()
    assert "ceo_synthesis" in body
    assert "agent_responses" in body
    _assert_real_response(body["ceo_synthesis"])


@_ai_only
def test_twin_model_generate(client):
    """Digital twin model generation must return real AI spec."""
    r = client.post("/api/v1/twin/model", json={
        "system_name": "Hospital Patient Flow",
        "system_description": "Emergency department intake through to ward admission",
        "domain": "care",
        "model_type": "process",
        "complexity": "simple",
    })
    assert r.status_code == 200
    body = r.json()
    assert "model_id" in body
    assert "model_spec" in body
    _assert_real_response(body["model_spec"])


# ── Management systems ────────────────────────────────────────────────────────

def test_mgmt_standards(client):
    r = client.get("/api/v1/mgmt/standards")
    assert r.status_code == 200
    body = r.json()
    assert "standards" in body
    assert len(body["standards"]) >= 5


# ── Capital fund ──────────────────────────────────────────────────────────────

def test_fund_status(client):
    r = client.get("/api/v1/fund/status")
    assert r.status_code == 200
    body = r.json()
    assert "total_capital" in body
    assert "available" in body
    assert "fund_health" in body


def test_fund_portfolio(client):
    r = client.get("/api/v1/fund/portfolio")
    assert r.status_code == 200
    body = r.json()
    assert "total_capital" in body
    assert "allocations" in body


# ── Marketplace ───────────────────────────────────────────────────────────────

def test_marketplace_listings(client):
    r = client.get("/api/v1/marketplace/listings")
    assert r.status_code == 200
    # Existing marketplace router returns a list; new capital_fund router returns dict
    assert isinstance(r.json(), (list, dict))
