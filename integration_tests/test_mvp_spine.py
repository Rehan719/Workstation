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
# Skip the local Ollama model under tests so the suite resolves to the always-available native
# floor instantly (no waiting on real local inference). The in-house guarantee is unchanged:
# served_by stays an OWNED resource and any_external stays False.
os.environ.setdefault("AI_DISABLE_LOCAL", "1")

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


# ── Nervous system ────────────────────────────────────────────────────────────

def test_nervous_status(client):
    r = client.get("/api/v1/organism/nervous/status")
    assert r.status_code == 200
    body = r.json()
    assert "arousal_state" in body
    assert body["arousal_state"] in ("HYPERACTIVE", "ALERT", "RESTING", "DORMANT")
    assert "signal_rate_per_second" in body
    assert "reflex_arcs_registered" in body


def test_nervous_signals(client):
    r = client.get("/api/v1/organism/nervous/signals")
    assert r.status_code == 200
    body = r.json()
    assert "signals" in body
    assert isinstance(body["signals"], list)


def test_nervous_stimulate(client):
    r = client.post("/api/v1/organism/nervous/stimulate", json={
        "signal_type": "sensory",
        "source": "test_suite",
        "payload": "integration test stimulation",
        "intensity": 0.7,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["fired"] is True


# ── Reconfiguration engine ────────────────────────────────────────────────────

def test_reconfig_get(client):
    r = client.get("/api/v1/organism/config")
    assert r.status_code == 200
    body = r.json()
    assert "gateway" in body
    assert "features" in body
    assert "domains" in body
    assert "organism" in body


def test_reconfig_history(client):
    r = client.get("/api/v1/organism/config/history")
    assert r.status_code == 200
    body = r.json()
    assert "history" in body
    assert isinstance(body["history"], list)


def test_reconfig_update(client):
    r = client.post("/api/v1/organism/config/update", json={
        "section": "gateway",
        "key": "temperature_bias",
        "value": "creative",
        "reason": "integration test",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "applied"
    assert body["change"]["new_value"] == "creative"


# ── Genome system ─────────────────────────────────────────────────────────────

def test_genome_list(client):
    r = client.get("/api/v1/organism/genome")
    assert r.status_code == 200
    body = r.json()
    assert "genomes" in body
    assert isinstance(body["genomes"], list)


# ── Auth system ───────────────────────────────────────────────────────────────

def test_auth_status(client):
    r = client.get("/api/v1/auth/status")
    assert r.status_code == 200
    body = r.json()
    assert "auth_enabled" in body
    assert "mode" in body
    assert body["mode"] in ("single-user", "multi-user")


def test_auth_me_single_user(client):
    """In single-user mode, /me returns a non-authed descriptor — no token needed."""
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 200
    body = r.json()
    # In single-user mode: auth_enabled=False and a message field
    assert "auth_enabled" in body or "username" in body


def test_auth_login(client):
    """Default admin credentials must yield tokens."""
    r = client.post("/api/v1/auth/token", data={
        "username": "admin",
        "password": "workstation2026",
    })
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


def test_auth_login_bad_password(client):
    r = client.post("/api/v1/auth/token", data={
        "username": "admin",
        "password": "wrongpassword",
    })
    assert r.status_code == 401


def test_auth_refresh(client):
    login = client.post("/api/v1/auth/token", data={
        "username": "admin", "password": "workstation2026"
    })
    refresh_token = login.json()["refresh_token"]
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body


# ── VSB Spawn Pipeline ────────────────────────────────────────────────────────

def test_vsb_list(client):
    r = client.get("/api/v1/vsb")
    assert r.status_code == 200
    body = r.json()
    assert "entities" in body
    assert isinstance(body["entities"], list)


# ── Nine Cognitive Engines ────────────────────────────────────────────────────

def test_cognitive_engines_list(client):
    r = client.get("/api/v1/cognitive/engines")
    assert r.status_code == 200
    body = r.json()
    assert "engines" in body
    assert body["total"] == 9
    layers = {e["layer"] for e in body["engines"]}
    assert "foundational" in layers
    assert "meta" in layers


def test_cognitive_cascade(client):
    """Cascade must run without API key — engines process internally."""
    r = client.post("/api/v1/cognitive/cascade", json={
        "problem": "How do we reduce hospital readmission rates?",
        "domain": "care",
        "include_mjm": True,
    })
    assert r.status_code == 200
    body = r.json()
    assert "cascade" in body
    assert "status" in body
    assert body["status"] == "complete"
    assert body["engines_run"] == 9


def test_cognitive_single_engine(client):
    r = client.post("/api/v1/cognitive/engine", json={
        "engine_id": "aqal",
        "input": {"goals": ["solve climate change"], "constraints": ["budget limits"]},
        "domain": "enterprise",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["engine_id"] == "aqal"
    assert "result" in body


def test_cognitive_unknown_engine(client):
    r = client.post("/api/v1/cognitive/engine", json={
        "engine_id": "nonexistent",
        "input": "test",
    })
    assert r.status_code == 400


# ── Intelligence Engines ──────────────────────────────────────────────────────

def test_intelligence_status(client):
    r = client.get("/api/v1/intelligence/status")
    assert r.status_code == 200
    body = r.json()
    assert "engines_available" in body
    assert "BDP" in body["engines_available"]
    assert "SPI" in body["engines_available"]
    assert body["bdp_stages"] == 8
    assert body["spi_stages"] == 8


@_ai_only
def test_intelligence_solve(client):
    r = client.post("/api/v1/intelligence/solve", json={
        "problem": "How can a small care home improve resident wellbeing on a limited budget?",
        "domain": "care",
    })
    assert r.status_code == 200
    body = r.json()
    assert "synthesis" in body
    _assert_real_response(body["synthesis"])
    assert body["engines_used"] == ["UltimateCognitiveCascade", "MJMOrchestratorV4", "AIGateway"]


# ── QEP — Quran Education Platform ───────────────────────────────────────────

def test_qep_status(client):
    r = client.get("/api/v1/qep/status")
    assert r.status_code == 200
    body = r.json()
    assert "components" in body
    assert "hifz_sm2" in body["components"]
    assert "constraints" in body


def test_qep_hifz_schedule(client):
    r = client.post("/api/v1/qep/hifz/schedule", json={
        "uid": "test_user_001",
        "surah_number": 1,
        "ayaat_range": [1, 7],
    })
    assert r.status_code == 200
    body = r.json()
    assert body["ayaat_scheduled"] == 7
    assert len(body["schedule"]) == 7


def test_qep_hifz_review(client):
    """SM-2 review must return updated interval based on quality score."""
    r = client.post("/api/v1/qep/hifz/review", json={
        "uid": "test_user_001",
        "ayah_ref": "1:1",
        "quality": 4,
    })
    assert r.status_code == 200
    body = r.json()
    assert "new_interval_days" in body
    assert body["new_interval_days"] >= 1
    assert "next_review_date" in body


def test_qep_hifz_progress(client):
    r = client.get("/api/v1/qep/hifz/progress/test_user_001")
    assert r.status_code == 200
    body = r.json()
    assert "total_ayaat_in_schedule" in body
    assert "due_today" in body


@_ai_only
def test_genome_encode(client):
    r = client.post("/api/v1/organism/genome/encode", json={
        "entity_name": "AI Medical Diagnostics Platform",
        "domain": "care",
        "realm": "health",
        "description": "AI-powered early disease detection using medical imaging",
    })
    assert r.status_code == 200
    body = r.json()
    assert "genome_id" in body
    assert "traits" in body
    assert len(body["traits"]) == 10
    assert "fitness_score" in body
    assert 0.0 <= body["fitness_score"] <= 1.0


# ── Organism Status ───────────────────────────────────────────────────────────

def test_organism_status(client):
    r = client.get("/api/v1/organism/status")
    assert r.status_code == 200
    body = r.json()
    assert "composite_health" in body
    assert "mode" in body
    assert "systems" in body
    assert body["mode"] in ("FULL_POWER", "NOMINAL", "DEGRADED", "EMERGENCY")
    assert 0.0 <= body["composite_health"] <= 1.0


def test_organism_health_summary(client):
    r = client.get("/api/v1/organism/health-summary")
    assert r.status_code == 200
    body = r.json()
    assert "composite_health" in body
    assert "should_throttle" in body
    assert "circadian_cycle" in body


def test_organism_lifecycle(client):
    r = client.get("/api/v1/organism/lifecycle")
    assert r.status_code == 200
    body = r.json()
    assert "lifecycle_stages_reached" in body
    assert "projects" in body
    assert "vsb_entities" in body


def test_organism_signals(client):
    r = client.get("/api/v1/organism/signals?n=10")
    assert r.status_code == 200
    body = r.json()
    assert "arousal_state" in body
    assert "signals" in body
    assert isinstance(body["signals"], list)


# ── Change Control Agency ─────────────────────────────────────────────────────

def test_cca_list_all(client):
    r = client.get("/api/v1/cca")
    assert r.status_code == 200
    body = r.json()
    assert "changes" in body
    assert "total" in body


def test_cca_queue(client):
    r = client.get("/api/v1/cca/queue")
    assert r.status_code == 200
    body = r.json()
    assert "queue" in body
    assert "total" in body


def test_cca_submit_and_get(client):
    r = client.post("/api/v1/cca/submit", json={
        "title": "Test: Enable experimental domain routing",
        "change_type": "config_minor",
        "description": "Enable A/B routing for the science domain to test new prompts.",
        "rationale": "Improve science domain response quality.",
        "affected_systems": ["gateway", "science"],
        "submitted_by": "test_suite",
        "rollback_plan": "Revert config flag to false.",
    })
    assert r.status_code == 200
    body = r.json()
    assert "cca_id" in body
    assert "impact_tier" in body
    assert body["impact_tier"] == "LOW"
    # LOW tier auto-approved when organism healthy
    assert body["status"] in ("submitted", "approved")

    # Retrieve the change
    cca_id = body["cca_id"]
    r2 = client.get(f"/api/v1/cca/{cca_id}")
    assert r2.status_code == 200
    assert r2.json()["cca_id"] == cca_id


def test_mgmt_ems_generate(client):
    """EMS endpoint — no AI key needed for route resolution."""
    if not _AI_AVAILABLE:
        pytest.skip("Skipped — no AI key")
    r = client.post("/api/v1/mgmt/ems/generate", json={
        "organisation_name": "GreenTech Solutions Ltd",
        "domain": "technology",
        "sector": "technology",
    })
    assert r.status_code == 200
    body = r.json()
    assert "framework" in body
    assert body["standard"] == "ISO 14001:2015"
    assert len(body["framework"]) > 200


# ── New IDBO routers — smoke coverage (added autonomous Cycle 2) ──────────────
# These verify each new router is mounted and its primary non-AI GET endpoint
# returns 200 with a sane payload. AI-narrated fields are not asserted (they may
# be live or a labelled fallback depending on the running environment).

def test_board_status(client):
    r = client.get("/api/v1/board/status")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_business_plan_get(client):
    r = client.get("/api/v1/business-plan", params={"scope": "workstation"})
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_economy_entity_types(client):
    r = client.get("/api/v1/economy/entity-types")
    assert r.status_code == 200
    body = r.json()
    assert body  # non-empty list/dict of entity types


def test_forge_resources(client):
    r = client.get("/api/v1/forge/resources")
    assert r.status_code == 200
    assert r.json()


def test_forge_run_in_house_provenance(client):
    # W1-d.2: a Forge pipeline records which OWNED resource served each AI stage (in-house-first).
    r = client.post("/api/v1/forge/run",
                    json={"objective": "pytest forge provenance", "stages": [{"type": "laboratory"}]})
    assert r.status_code == 200
    prov = r.json()["ai_provenance"]
    assert prov["posture"] == "in-house-first"
    assert prov["any_external"] is False
    assert set(prov["served_by"]) <= {"native", "ollama"} and sum(prov["served_by"].values()) >= 1


def test_genesis_journey_in_house_provenance(client):
    # W1-d.2: the Genesis Concept→Commercialisation journey runs its synthesis stages in-house.
    r = client.post("/api/v1/genesis/journey", json={"problem": "pytest genesis provenance"})
    assert r.status_code == 200
    prov = r.json()["ai_provenance"]
    assert prov["posture"] == "in-house-first"
    assert prov["any_external"] is False
    assert set(prov["served_by"]) <= {"native", "ollama"}


def test_compliance_frameworks(client):
    r = client.get("/api/v1/compliance/frameworks")
    assert r.status_code == 200
    assert r.json()


def test_transformation_realisation(client):
    r = client.get("/api/v1/transformation/realisation")
    assert r.status_code == 200
    body = r.json()
    assert "overall_realisation" in body
    assert "pillars" in body and len(body["pillars"]) > 0


def test_resource_fabric_list(client):
    r = client.get("/api/v1/resources")
    assert r.status_code == 200
    assert r.json()


def test_sovereign_evolution_roadmap(client):
    r = client.get("/api/v1/sovereign-evolution/roadmap")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_heartbeat_status(client):
    r = client.get("/api/v1/heartbeat/status")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_cognition_wiring(client):
    r = client.get("/api/v1/cognition/wiring")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_living_plan_state(client):
    r = client.get("/api/v1/plan/state")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


def test_frontier_reality_status(client):
    r = client.get("/api/v1/frontier/reality/status")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


# ── Integration surface — the 18 previously-broken endpoints (Cycle 2) ────────

def test_integration_ai_quotas(client):
    r = client.get("/api/v1/ai/quotas")
    assert r.status_code == 200
    assert "providers" in r.json()


def test_integration_evidence_graph(client):
    r = client.get("/api/v1/evidence/graph")
    assert r.status_code == 200
    body = r.json()
    assert "nodes" in body and "edges" in body


def test_integration_git_history(client):
    r = client.get("/api/v1/workstation/git-history")
    assert r.status_code == 200
    assert "commits" in r.json()


def test_integration_global_search(client):
    r = client.get("/api/v250/search/global", params={"q": "vsb"})
    assert r.status_code == 200
    body = r.json()
    assert "results" in body and "by_type" in body


def test_integration_evolution_metrics(client):
    r = client.get("/api/v240/evolution/metrics")
    assert r.status_code == 200
    body = r.json()
    assert "pillar_breakdown" in body


# ── POST-path coverage — operational workflows (added autonomous Cycle 6) ─────
# Deterministic (non-AI) workflow endpoints. Verify the real request→response
# contract, not just that the router is mounted.

def test_compliance_check_pass(client):
    r = client.post("/api/v1/compliance/check",
                    json={"subject": "a halal community meal-prep service for elderly families"})
    assert r.status_code == 200
    body = r.json()
    assert body["overall"] == "pass"
    assert len(body["verdicts"]) >= 5


def test_compliance_check_fail(client):
    r = client.post("/api/v1/compliance/check",
                    json={"subject": "a payday loan charging riba interest plus gambling"})
    assert r.status_code == 200
    assert r.json()["overall"] == "fail"


def test_economy_cycle(client):
    r = client.post("/api/v1/economy/cycle", json={})
    assert r.status_code == 200
    cycle = r.json()["cycle"]
    assert "vsb_id" in cycle and "intake_revenue" in cycle


def test_resource_compose(client):
    r = client.post("/api/v1/resources/compose",
                    json={"name": "test-composition", "resource_ids": ["genesis"]})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "test-composition"
    assert len(body["resources"]) >= 1


def test_resource_fabric_native_swarm_cascade(client):
    # W1-d: native AI resources are first-class in the fabric, and bespoke swarm cascades are
    # reconfigurable, reusable, re-runnable resources that run on Workstation's OWN resources.
    fab = client.get("/api/v1/resources?resource_class=ai_native").json()
    ids = [r["id"] for r in fab["resources"]]
    assert "native_orchestrator" in ids and "native_swarm" in ids
    # define a bespoke, reusable cascade (user design control)
    d = client.post("/api/v1/resources/swarm/define",
                    json={"name": "pytest cascade", "context": "test",
                          "stages": [{"role": "analyst", "instruction": "Analyse."},
                                     {"role": "synthesiser", "instruction": "Synthesise."}]}).json()
    sid = d["id"]
    assert d["reusable"] is True and len(d["stages"]) == 2
    assert any(c["id"] == sid for c in client.get("/api/v1/resources/swarm").json()["cascades"])
    # run the SAVED cascade on owned resources — in-house only
    run = client.post("/api/v1/resources/swarm/run", json={"swarm_id": sid}).json()
    assert run["stages"] == 2
    assert run["any_external"] is False
    assert all(s["served_by"] in ("native", "ollama") for s in run["trace"])
    # unknown saved id → 404
    assert client.post("/api/v1/resources/swarm/run", json={"swarm_id": "nope"}).status_code == 404


def test_integration_user_activity(client):
    r = client.post("/api/v260/user/activity",
                    json={"user_id": "pytest", "action": "view", "detail": "spine-test"})
    assert r.status_code == 200
    assert r.json()["recorded"] is True


def test_integration_bounty_submit(client):
    r = client.post("/api/security/bounty/submit",
                    json={"title": "test finding", "severity": "low", "description": "smoke"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "received" and body["severity"] == "low"


# ── Business-plan lifecycle — Chief/Board flagship feature (autonomous Cycle 7) ─
# Full set→objective→review→progress flow in an isolated scope (no real-data
# pollution), plus the missing-objective 404 path.

def test_business_plan_lifecycle(client):
    import uuid
    # unique scope per run → fully isolated + idempotent (the plan store persists to data/)
    scope = f"pytest-bp-{uuid.uuid4().hex[:8]}"
    # 1. Chief sets the plan's strategic layers
    r = client.post("/api/v1/business-plan/set",
                    json={"scope": scope, "mission": "M", "vision": "V", "strategy": "S"})
    assert r.status_code == 200
    assert r.json()["mission"] == "M"
    # 2. add a timelined objective
    r = client.post("/api/v1/business-plan/objective",
                    json={"scope": scope, "title": "Test objective", "timeline": "Q3 2026"})
    assert r.status_code == 200
    obj = r.json()
    oid = obj["id"]
    assert obj["progress_pct"] == 0
    # 3. review it to 80%
    r = client.post(f"/api/v1/business-plan/objective/{oid}/review",
                    json={"scope": scope, "progress_pct": 80, "status": "in_progress"})
    assert r.status_code == 200
    assert r.json()["progress_pct"] == 80
    # 4. progress summary reflects 80%
    r = client.get("/api/v1/business-plan/progress", params={"scope": scope})
    assert r.status_code == 200
    body = r.json()
    assert body["overall_progress"] == 80.0
    assert body["objectives"] == 1
    # 5. reviewing a missing objective → 404
    r = client.post("/api/v1/business-plan/objective/nope/review",
                    json={"scope": scope, "progress_pct": 50})
    assert r.status_code == 404


# ── Genesis → Business-Plan wiring (Phase 2) ──────────────────────────────────
# Every established VSB IDBO auto-seeds a living business plan with objectives
# mapped to its Concept→Design→Commercialisation lifecycle.

def test_genesis_establish_seeds_business_plan(client):
    r = client.post("/api/v1/genesis/establish",
                    json={"problem": "pytest VSB business-plan seed check", "owner_id": "pytest", "entity_type": "ltd"})
    assert r.status_code == 200
    vsb = r.json()["vsb_id"]
    bp = client.get("/api/v1/business-plan", params={"scope": vsb}).json()
    assert bp["mission"].startswith("Deliver:")
    assert len(bp["objectives"]) == 3


# ── Payments — honest, launch-ready rails (Phase 3, test-mode safe) ───────────
# Verifies the rails never fabricate a connection and default to safe simulation.

def test_payments_status_honest(client):
    r = client.get("/api/v310/payments/status")
    assert r.status_code == 200
    b = r.json()
    assert b["mode"] in ("simulation", "test", "live", "live_gated")
    assert isinstance(b["stripe_configured"], bool)
    # SAFETY INVARIANT: live charges are enabled IFF mode is exactly "live"
    # (requires BOTH a live key AND STRIPE_LIVE_ENABLED=true). A live key alone → "live_gated".
    assert b["live_charges_enabled"] == (b["mode"] == "live")
    if b["mode"] == "simulation":
        assert b["stripe_configured"] is False


def test_payments_wallet_no_fabrication(client):
    r = client.get("/api/v310/payments/wallet/pytest")
    assert r.status_code == 200
    b = r.json()
    assert b["currency"] == "WST (virtual)"
    assert isinstance(b["stripe_configured"], bool)


def test_payments_wst_settlement(client):
    # WST settlement never touches Stripe (real money) — safe in any payment mode,
    # including when a live key is present (it stays gated).
    r = client.post("/api/v310/payments/create-session",
                    json={"item_id": "test-item", "price_wst": 100.0, "payment_method": "wst_balance"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "wst_ledger"
    assert body["currency"] == "WST (virtual)"


# ── End-to-end Transformation Orchestration (Chief → Build-to-Order) ──────────
# The whole transformation run THROUGH the VSB delivery org as one verified cascade.

def test_transformation_orchestrate_end_to_end(client):
    r = client.post("/api/v1/transformation/orchestrate",
                    json={"objective": "pytest end-to-end", "scope": "workstation", "owner_id": "Rehan"})
    assert r.status_code == 200
    b = r.json()
    tiers = [s["tier"] for s in b["cascade"]]
    assert tiers[0].startswith("Chief")                                    # starts at the Chief
    assert any("Business Transformation" in t for t in tiers)             # reaches the BTO
    v = b["validation"]
    assert v["verified_stages"] == v["stages"]                            # every stage verified
    assert v["end_to_end_chief_to_bto"] is True
    assert v["validated"] is True
    assert v["biomimetic_signals_fired"] >= 1                             # responsive
    assert b["digital_twin"]["model_id"]                                  # twin generated
    assert b["digital_twin"]["simulation"]["projected_realisation"] is not None  # + simulated
    assert b["governance"]["status"] == "allowed"                        # gaas-governed


def test_transformation_orchestrate_runs(client):
    # run an orchestration, then the history endpoint must list it
    client.post("/api/v1/transformation/orchestrate", json={"objective": "runs test", "scope": "workstation"})
    r = client.get("/api/v1/transformation/orchestrate/runs")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 1
    first = body["runs"][0]
    assert "transformation_id" in first and "validated" in first


def test_transformation_orchestrate_deep_native_swarm(client):
    # deep=true runs the Chief's cognition on Workstation's OWN native swarm (W1-c) — in-house,
    # recording served_by so the whole-transformation run demonstrably uses owned AI resources.
    r = client.post("/api/v1/transformation/orchestrate",
                    json={"objective": "pytest deep native swarm", "scope": "workstation", "deep": True})
    assert r.status_code == 200
    b = r.json()
    nc = b["native_cognition"]
    assert nc and "error" not in nc
    assert nc["any_external"] is False                                   # in-house only
    assert all(s in ("native", "ollama") for s in nc["served_by"])       # owned resources only
    assert b["validation"]["ai_in_house"] is True
    assert b["validation"]["stages"] == 9                                # the owned-swarm stage was added


def test_vsb_list_org_flags(client):
    # an established VSB has a Board + Economy; the list must surface org flags
    client.post("/api/v1/genesis/establish",
                json={"problem": "list-flags test", "owner_id": "pytest", "entity_type": "ltd"})
    r = client.get("/api/v1/vsb")
    assert r.status_code == 200
    ents = r.json()["entities"]
    assert ents
    established = [e for e in ents if e.get("has_board")]
    assert established, "expected at least one established VSB with has_board=True"
    assert "entity_type" in established[0]


# ── Native AI Fabric (W1) — Workstation's OWN in-house AI resources ───────────
# Verifies the platform produces real AI output from its own resources with NO
# external dependency (the headline native-AI mandate).

def test_native_ai_status_in_house_first(client):
    r = client.get("/api/v1/native-ai/status")
    assert r.status_code == 200
    b = r.json()
    assert b["posture"] == "in-house-first"
    assert "native" in b["owned_resources_available"]   # the owned floor is always available
    assert isinstance(b["external_allowed"], bool)


def test_native_ai_complete_no_external_dependency(client):
    r = client.post("/api/v1/native-ai/complete",
                    json={"prompt": "## Understanding\n## Approach\nProblem: a native-AI test", "agent": "t"})
    assert r.status_code == 200
    b = r.json()
    assert b["output"]                       # always a real result
    assert b["is_external"] is False         # in-house-first guarantee — never depends on external


def test_native_ai_swarm_cascade(client):
    r = client.post("/api/v1/native-ai/swarm", json={"agent": "t", "context": "test"})
    assert r.status_code == 200
    b = r.json()
    assert b["stages"] >= 1 and len(b["trace"]) == b["stages"]
    assert b["any_external"] is False


def test_native_engine_structured_and_grounded():
    # W1-e: the native engine returns every requested section, tailored per archetype and grounded
    # in the prompt's content — honestly labelled (not an LLM), never fabricated.
    from agentic_core.ai.native.engine import native_engine
    prompt = ("You are the IDBO Commercialisation engine.\n\n"
              "Concept: a halal zero-waste community meal service for elderly Londoners\n"
              "Domain: care\n\n## Go-To-Market Strategy\n## Revenue Model\n## Key Risks")
    out = native_engine.generate(prompt, "genesis_commercial")
    assert native_engine.is_model is False and native_engine.is_external is False
    assert "Workstation native structured engine" in out          # honest provenance marker
    for section in ("## Go-To-Market Strategy", "## Revenue Model", "## Key Risks"):
        assert section in out                                      # every requested section present
    assert "zero-waste" in out.lower() or "elderly" in out.lower()  # grounded in the actual content
    gtm = out.split("## Go-To-Market Strategy")[1].split("##")[0]
    rev = out.split("## Revenue Model")[1].split("##")[0]
    assert gtm.strip() != rev.strip()                             # archetypes are differentiated
