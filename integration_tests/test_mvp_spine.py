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
    """CFO metrics report real counts and DO NOT synthesise a valuation.

    W410 - this test was titled "must be computed from real project store, not literals" and
    asserted that `revenue` was present and was not one specific old constant. It therefore
    REQUIRED the presence of a field that was itself invented: revenue came from project counts
    multiplied by hardcoded stage values (concept $1,000 / prototype $5,000 / commercialise
    $15,000), under a docstring claiming "no hardcoded literals". The test guarded the wrong
    property and passed throughout.
    """
    r = client.get("/api/csuite/cfo/metrics")
    assert r.status_code == 200
    body = r.json()

    # The real things must be reported.
    assert "portfolio" in body, list(body.keys())
    for key in ("total_projects", "by_stage", "complete", "total_outputs"):
        assert key in body["portfolio"], body["portfolio"]
    assert "token_balance" in body

    # No synthesised money. A valuation may exist only when something actually values a project.
    assert body.get("valuation") is None, body.get("valuation")
    for invented in ("revenue", "growth", "liquidity", "unrealised_gain", "realised_gain"):
        assert invented not in body, (
            f"{invented} is back in the CFO payload; it was derived from invented multipliers"
        )


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


def test_employment_services(client):
    # Employment domain brought to parity with the other domains: a service catalogue + clean tools.
    r = client.get("/api/v1/employment/services")
    assert r.status_code == 200
    body = r.json()
    assert "services" in body and body["total"] >= 4
    ids = {s["id"] for s in body["services"]}
    assert {"cv", "cover_letter", "interview_prep", "career_path"} <= ids


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


def test_user_isolation_when_auth_enabled(client, monkeypatch):
    # §17.5 absolute invariant — user isolation. Single-user mode (default) stays open; with
    # AUTH_ENABLED=true every generated VSB is owner-stamped SERVER-SIDE (a client cannot claim
    # another owner) and scoped: another user cannot list or read it (404, never a confirming 403),
    # unauthenticated calls get 401. The admin bootstrap has NO hardcoded default password.
    from agentic_core.auth import core as auth_core
    if not auth_core._AUTH_DEPS_OK:
        import pytest as _pytest
        _pytest.skip("auth crypto deps not installed")
    users = auth_core._load_users()
    for uname, pw in (("alice-iso", "pw-alice"), ("bob-iso", "pw-bob")):
        users[uname] = {"user_id": uname, "username": uname,
                        "hashed_password": auth_core._pwd_ctx.hash(pw), "role": "user",
                        "created_at": "2026-01-01T00:00:00Z", "api_keys": []}
    auth_core._save_users(users)
    monkeypatch.setenv("AUTH_ENABLED", "true")
    assert client.get("/api/v1/vsb").status_code == 401       # fail-closed without a token

    def _hdr(u, p):
        r = client.post("/api/v1/auth/token", data={"username": u, "password": p})
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['access_token']}"}
    alice, bob = _hdr("alice-iso", "pw-alice"), _hdr("bob-iso", "pw-bob")

    est = client.post("/api/v1/genesis/establish", json={
        "problem": "isolation invariant test", "domain": "enterprise", "name": "IsoInvariantCo",
        "concept": "c", "design": "d", "commercialisation": "m",
        "owner_id": "someone-else"}, headers=alice).json()    # the client-claimed owner must be IGNORED
    vid = est.get("vsb_id")
    assert vid
    mine = client.get(f"/api/v1/vsb/{vid}", headers=alice)
    assert mine.status_code == 200
    assert mine.json().get("owner_id") == "alice-iso"          # server-side stamp won
    assert client.get(f"/api/v1/vsb/{vid}", headers=bob).status_code == 404   # scoped out, not 403
    ids_a = {e.get("vsb_id") for e in client.get("/api/v1/vsb", headers=alice).json()["entities"]}
    ids_b = {e.get("vsb_id") for e in client.get("/api/v1/vsb", headers=bob).json()["entities"]}
    assert vid in ids_a and vid not in ids_b
    # no hardcoded admin default: the known constant must be gone from the bootstrap code
    import inspect as _inspect
    assert "workstation2026" not in _inspect.getsource(auth_core)


def test_develop_actions_apply_cycle_over_cycle(client):
    # §5 DEVELOP (W269) — "each tier manages, appraises and DEVELOPS the tier below": the appraisal
    # chain now covers ALL SIX edges (chief→board, board→ceo, ceo→csuite, csuite→coe, ceo→bto,
    # bto→build), each Development Action persists, and the NEXT cycle's tier prompts APPLY them —
    # previously Development Actions had zero consumers and two edges were missing.
    r1 = client.post("/api/v1/swarm/cascade", json={
        "mission": "w269 develop loop contract", "domain": "enterprise"}).json()
    assert set(r1["appraisals"].keys()) == {
        "chief_appraises_board", "board_appraises_ceo", "ceo_appraises_csuite",
        "csuite_appraises_coe", "ceo_appraises_bto", "bto_appraises_build"}   # all six edges
    r2 = client.post("/api/v1/swarm/cascade", json={
        "mission": "w269 develop loop contract round 2", "domain": "enterprise"}).json()
    da = r2["development_applied"]
    assert set(da.keys()) == set(r1["appraisals"].keys())     # every tier received a development action
    assert all(v == r1["run_id"] for v in da.values())        # each traceable to the run that set it


def test_cascade_appraisals_measured_and_persisted(client):
    # §5 (W268) — the appraise/develop pass is grounded in MEASURED outcomes (the real QMS gate runs
    # BEFORE the appraisals; tier calls accrue real operational-excellence rows) and cascade runs
    # PERSIST (appraisals + Development Actions survive the response, queryable at /cascade/runs).
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w268 measured appraisal contract", "domain": "enterprise"}).json()
    assert set(r["appraisals"].keys()) >= {"chief_appraises_board", "board_appraises_ceo",
                                           "ceo_appraises_csuite", "bto_appraises_build"}
    assert r["quality"].get("qms_gate_passed") is not None      # the gate ran (before the appraisals)
    runs = client.get("/api/v1/swarm/cascade/runs").json()
    top = runs["runs"][0]
    assert top["run_id"] == r["run_id"]                          # this run persisted
    assert top["appraisals"] and top["quality"].get("delivery_coverage") is not None
    ops = client.get("/api/v1/operations/rankings").json()["rankings"]
    tier_rows = [x for x in ops if str(x["resource"]).startswith(("agent:cascade_", "agent:appraise_"))]
    assert tier_rows, "cascade tier calls accrued no operational-excellence rows"


def test_pervsb_swarm_reconfigurable_and_live_grounded(client):
    # §7 user design control × §5 (W267) — the VSB's OWN delivery org is genuinely reconfigurable:
    # PUT /resources/swarm/{sid} edits stages/org (id + vsb_id preserved; the entity's native_swarm
    # summary syncs; UEG-logged), and a VSB-bound run grounds in the LIVING VSB's CURRENT state —
    # never the frozen establish-time snapshot.
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w267 swarm design-control test", "domain": "enterprise", "name": "SwarmDesignCo",
        "concept": "c", "design": "d", "commercialisation": "m"}).json()
    vid = est["vsb_id"]
    sw = client.get(f"/api/v1/resources/swarm?vsb_id={vid}").json()["cascades"]
    assert sw, "the established VSB has no delivery cascade"
    sid = sw[0]["id"]
    upd = client.put(f"/api/v1/resources/swarm/{sid}", json={
        "stages": [{"role": "ai-ceo", "instruction": "Frame the objective."},
                   {"role": "halal-compliance-officer", "instruction": "Verify halal compliance."},
                   {"role": "build-to-order", "instruction": "Assemble the delivery plan."}],
        "org": ["Chief (owner twin)", "AI CEO", "Halal Compliance", "Build-to-Order"]}).json()
    assert [s["role"] for s in upd["stages"]] == ["ai-ceo", "halal-compliance-officer", "build-to-order"]
    assert upd["id"] == sid and upd.get("vsb_id") == vid          # identity preserved
    ent = client.get(f"/api/v1/vsb/{vid}").json()
    assert ent["native_swarm"]["stages"] == ["ai-ceo", "halal-compliance-officer", "build-to-order"]
    assert ent["native_swarm"].get("reconfigured_at")             # the entity summary synced
    run = client.post("/api/v1/resources/swarm/run", json={"swarm_id": sid}).json()
    assert run["grounded_in_live_vsb"] is True and run["vsb_id"] == vid
    assert len(run.get("trace", [])) == 3                          # the EDITED stages ran
    assert client.put("/api/v1/resources/swarm/nope", json={"name": "x"}).status_code == 404
    assert client.put(f"/api/v1/resources/swarm/{sid}", json={"stages": []}).status_code == 400


def test_delivery_moves_the_living_plan(client):
    # §5 loop closure (W266) — the roadmap "updates as the plan progresses": (A) a genuinely
    # QMS-governed orchestration advances the objective planned→in_progress (never auto-'done');
    # (B) a VALIDATED transformation whose mandate came FROM the plan writes an auditable review
    # back onto the driving objective. Previously the ONLY progress mutator was the manual review UI.
    import uuid as _uuid
    scope = f"vsb:w266-{_uuid.uuid4().hex[:8]}"
    client.post("/api/v1/board/chief/instruct", json={
        "instruction": "Deliver the winter pilot menu", "scope": scope})
    p = client.get("/api/v1/business-plan", params={"scope": scope}).json()
    obj = ((p.get("plan") or p)["objectives"])[0]
    assert obj["status"] == "planned"
    # (A) governed orchestration advances the status honestly
    o = client.post(f"/api/v1/business-plan/objective/{obj['id']}/orchestrate",
                    json={"scope": scope}).json()
    if (o["tree"]["governance"] or {}).get("qms_passed"):
        assert o["status"] == "in_progress" and o["status_advanced"] is True
    else:   # an ungoverned run must leave the plan untouched
        assert o["status"] == "planned" and o["status_advanced"] is False
    # (B) a plan-driven validated transformation writes back onto the driving objective
    scope2 = f"vsb:w266t-{_uuid.uuid4().hex[:8]}"
    client.post("/api/v1/board/chief/instruct", json={
        "instruction": "Scale the delivery kitchen", "scope": scope2})
    t = client.post("/api/v1/transformation/orchestrate", json={"scope": scope2}).json()
    if (t.get("validation") or {}).get("validated"):
        assert t.get("plan_objective_advanced")
        p2 = client.get("/api/v1/business-plan", params={"scope": scope2}).json()
        obj2 = ((p2.get("plan") or p2)["objectives"])[0]
        assert obj2["status"] == "in_progress"
        assert any("transformation" in r for r in obj2.get("reviews", []))


def test_chief_instruction_becomes_living_plan_objectives(client):
    # §5 apex closure (W265) — the Owner's most important input no longer evaporates into prose:
    # POST /board/chief/instruct parses the CEO action plan's TITLE|KPI|TIMELINE|OWNER_ROLE lines
    # into REAL objectives on the scoped living business plan (tagged with the directive), falling
    # back to the instruction itself as one objective when the model yields no machine lines — the
    # delegation ALWAYS lands on the roadmap.
    import uuid as _uuid
    scope = f"vsb:w265-{_uuid.uuid4().hex[:8]}"
    r = client.post("/api/v1/board/chief/instruct", json={
        "instruction": "Launch the halal meal-kit pilot in London by winter", "scope": scope}).json()
    assert r["objectives_added"] >= 1 and r["business_plan_scope"] == scope
    p = client.get("/api/v1/business-plan", params={"scope": scope}).json()
    objs = (p.get("plan") or p).get("objectives", [])
    tagged = [o for o in objs if o.get("directive_id") == r["directive_id"]]
    assert tagged, "no plan objective carries the Chief's directive"
    assert tagged[0]["status"] == "planned" and tagged[0]["id"].startswith("obj-")


def test_apex_board_runs_on_native_fabric(client):
    # §5×§6×§11 apex closure (W270) — the Board (the organism's HIGHEST direction) now runs on the
    # same governed native fabric as every lower tier: provenance recorded (which OWNED resource
    # served the apex, in-house-first), the chief directive passes the gaas.v5 gate (or bypass is
    # LOUDLY logged — never silent), the direction is sealed into the tamper-evident UEG ledger,
    # and /board/directive persists (previously write-only prose).
    r = client.post("/api/v1/board/chief/instruct", json={
        "instruction": "w270 apex fabric contract — expand the scholarship engine"}).json()
    prov = r["ai_provenance"]
    assert prov["served_by"] and prov["posture"] == "in-house-first"
    assert r["governance"]["status"] in ("allowed", "passed", "ungated_bypass_logged")
    ev = client.get("/api/v1/gaas/ueg/events?limit=200").json()
    payloads = [e.get("data") or {} for e in ev.get("events", [])]   # hash-chain nodes nest the event
    sealed = [p for p in payloads if p.get("type") == "board.chief_instruct"
              and p.get("directive_id") == r["directive_id"]]
    assert sealed and sealed[0]["served_by"], "apex direction not sealed into the UEG ledger"
    d = client.post("/api/v1/board/directive", json={
        "topic": "w270 directive persistence", "domain": "enterprise"}).json()
    assert d["kind"] == "board_directive" and d["ai_provenance"]["served_by"]
    recent = client.get("/api/v1/board/status").json().get("recent_directives", [])
    assert any(x.get("kind") == "board_directive" and
               x.get("topic") == "w270 directive persistence" for x in recent)


def test_all_four_management_systems_compute(client):
    # §5 living management systems (W271) — ALL FOUR now COMPUTE over the run's own telemetry:
    # DCMS commits real versioned artifacts, QMS runs the real stateful gate, and BMS unit
    # economics + EMS carbon are computed from the run's measured artifact count and a
    # duration-derived energy estimate (simulated constants HONESTLY caveated) — previously
    # BMS/EMS were catalogue-attested but never engaged.
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w271 four living systems contract", "domain": "enterprise"}).json()
    ms = r["management_systems"]
    assert ms["document_control"] and r["quality"].get("qms_gate_passed") is not None
    bms = ms["bms"]
    assert isinstance(bms["cost_per_insight_usd"], (int, float)) and bms["insights_count"] >= 4
    assert bms["status"] in ("EFFICIENT", "REVISE") and "estimate" in bms["caveat"]
    ems = ms["ems"]
    assert isinstance(ems["total_co2_kg"], (int, float)) and ems["total_co2_kg"] > 0
    assert ems["efficiency_gain"] > 0 and "simulated" in ems["caveat"]


def test_cascade_bto_requisitions_real_fabric(client):
    # §5×§7 (W272) — the BTO tier REQUISITIONS the Resource Fabric for real: the deterministic
    # word-overlap matcher selects light facilities from the mission + programme, their REAL handlers
    # RUN inside the cascade, Build-to-Order assembles from the genuine outputs, and the managing
    # tiers see live fabric telemetry — previously the BTO only DESCRIBED facilities in prose.
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "optimise the allocation of compute resources and verify regulatory compliance "
                   "for the halal delivery platform", "domain": "enterprise"}).json()
    fr = r["fabric_requisitions"]
    assert fr, "no fabric facility was requisitioned for a mission that plainly matches two"
    for f in fr:
        assert f["ran"].startswith("/api/") and f["match_hits"] >= 2 and f["output"]
    rids = {f["resource"] for f in fr}
    assert rids & {"compliance", "resource_optimizer"}   # the deterministic match is stable
    top = client.get("/api/v1/swarm/cascade/runs").json()["runs"][0]
    assert top["run_id"] == r["run_id"]
    assert [x["resource"] for x in top["fabric_requisitions"]] == [f["resource"] for f in fr]


def test_composition_lifecycle_params_and_gate(client):
    # §7 (W273) — a saved composition is a LIVING design with an honest run path: PUT reconfigures
    # in place (re-simulated, version bumps, identity preserved), DELETE retires it, per-RUN params
    # reach the REAL engines, registry type-placeholders never leak into real runs as literal
    # values, and a design whose simulation failed (QMS or usage-area) runs WITH an explicit
    # warning — never silently, never hard-blocked (the catalogue's declared areas are narrower
    # than legitimate composition practice, so warn-not-block is the honest calibration).
    comp = client.post("/api/v1/resources/compose", json={
        "name": "w273 living design", "usage_area": "synthesis",
        "resource_ids": ["petri_dish"], "config": {}}).json()
    cid = comp["id"]
    r = client.post(f"/api/v1/resources/compositions/{cid}/run", json={
        "objective": "culture a halal-nutrition specimen",
        "params": {"petri_dish": {"iterations": 2}}}).json()
    rr = next(x for x in r["real_resource_runs"] if x["resource"] == "petri_dish")
    assert rr["passages"] == 2                                # the per-RUN override reached the engine
    assert r["run_params_applied"] == ["petri_dish"]
    assert "str (" not in rr.get("output", "")                # no placeholder-string leak
    if not r["commit_ready"]:
        assert r["quality_warning"]                           # failed simulation warns, never silent
    upd = client.put(f"/api/v1/resources/compositions/{cid}", json={
        "config": {"petri_dish": {"medium": "rich"}}}).json()
    assert upd["version"] == 2 and upd["id"] == cid           # reconfigured in place, identity kept
    assert upd["resources"][0]["config"]["medium"] == "rich"
    bad = client.post("/api/v1/resources/compose", json={
        "name": "w273 unsupported", "usage_area": "science",
        "resource_ids": ["petri_dish"], "config": {}}).json()
    assert bad["model"]["usage_area_supported_by_all"] is False
    warned = client.post(f"/api/v1/resources/compositions/{bad['id']}/run",
                         json={"objective": "x"}).json()
    assert warned["usage_area_supported"] is False            # the structural signal is surfaced…
    assert warned["quality_warning"] and "usage area" in warned["quality_warning"]   # …and explained
    assert warned.get("real_resource_runs") is not None       # …but the run was NOT blocked
    assert client.delete(f"/api/v1/resources/compositions/{cid}").json()["deleted"] == cid
    assert client.get(f"/api/v1/resources/compositions/{cid}").status_code == 404
    client.delete(f"/api/v1/resources/compositions/{bad['id']}")   # tidy the second design


def test_marketplace_attribution_owner_scoped(client, monkeypatch):
    # §14×§12 (W311) — marketplace mutations are OWNER-SCOPED and attribution is unspoofable:
    # creator_id is server-stamped under auth; a listing can only be revenue-attributed to a VSB
    # the caller owns (404 never 403); PATCH/DELETE are owner-only; creator_id immutable by patch.
    import agentic_core.auth.core as ac
    monkeypatch.setenv("AUTH_ENABLED", "true")
    users = ac._load_users()
    for u in ("w311a", "w311b"):
        users[u] = {"username": u, "hashed_password": ac._pwd_ctx.hash("pw12345678"), "role": "user"}
    ac._save_users(users)

    def hdr(u):
        t = client.post("/api/v1/auth/token",
                        data={"username": u, "password": "pw12345678"}).json()["access_token"]
        return {"Authorization": f"Bearer {t}"}

    ha, hb = hdr("w311a"), hdr("w311b")
    va = client.post("/api/v1/genesis/establish", json={
        "problem": "w311a venture", "domain": "enterprise", "concept": "A.", "design": "D.",
        "commercialisation": "C.", "ship_output": False}, headers=ha).json()["vsb_id"]
    l1 = client.post("/api/v1/marketplace/listings", json={
        "name": "w311 halal pack", "price_wst": 10,
        "creator_id": "someone_else", "vsb_id": va}, headers=ha).json()
    assert l1["creator_id"] == "w311a"                       # spoofed creator ignored
    assert client.post("/api/v1/marketplace/listings", json={
        "name": "spoof", "price_wst": 5, "vsb_id": va}, headers=hb).status_code == 404
    lid = l1["id"]
    assert client.patch(f"/api/v1/marketplace/listings/{lid}",
                        json={"price_wst": 1}, headers=hb).status_code == 404
    assert client.delete(f"/api/v1/marketplace/listings/{lid}", headers=hb).status_code == 404
    assert client.patch(f"/api/v1/marketplace/listings/{lid}",
                        json={"price_wst": 12}, headers=ha).status_code == 200
    assert client.patch(f"/api/v1/marketplace/listings/{lid}",
                        json={"creator_id": "hax"}, headers=ha).json()["creator_id"] == "w311a"
    client.delete(f"/api/v1/marketplace/listings/{lid}", headers=ha)


def test_taxonomy_is_canonical():
    # §17.1 (W311) — ONE module owns the Realm × Domain taxonomy; the BTO catalog (previously a
    # drifted five-realm list) serves the canon.
    from agentic_core.taxonomy import REALMS, DOMAINS
    from agentic_core.catalog.bto import _build_component
    assert REALMS == ("enterprise", "learning", "developing", "scholarship")
    assert DOMAINS == ("religion", "science", "education", "law", "employment", "care")
    assert _build_component("realms")["available"] == ["Enterprise", "Learning", "Developing", "Scholarship"]
    assert set(_build_component("domains")["available"]) == {"Religion", "Science", "Education",
                                                             "Law", "Employment", "Care"}


def test_genome_consequential_evolution_loop(client):
    # §8 (W310) — the genome is CONSEQUENTIAL: evolution proposals are evidence-based (basis named)
    # and route to the arms-length CCA at MEDIUM tier (never auto-approved — the Owner keeps the
    # gate); mutations apply ONLY on approval, land traceably on the entity, mark the CCA
    # implemented, mark the shipped repo stale (drift honesty), and the shipped IDENTITY expresses
    # the applied mutations.
    import json as _json
    from agentic_core.config import data_path
    j = client.post("/api/v1/genesis/journey", json={
        "problem": "w310 genome venture", "domain": "enterprise",
        "establish": True, "ship_output": True}).json()
    vid = (j.get("established_vsb") or {}).get("vsb_id")
    assert vid
    ev = client.post(f"/api/v1/vsb/{vid}/evolve", json={"trigger": "w310"}).json()
    cca = ev.get("evolution_pending_cca")
    props = ev.get("proposals") or []
    assert cca and props and all(p.get("basis") or p.get("expected_impact") for p in props)
    ch = client.get(f"/api/v1/cca/{cca}").json()
    assert ch["impact_tier"] == "MEDIUM" and ch["status"] == "submitted"   # never auto-approved
    pre = client.post(f"/api/v1/vsb/{vid}/evolution/apply").json()
    assert pre["applied"] is False and "cca_status" in str(pre.get("reason"))
    client.post(f"/api/v1/cca/{cca}/review",
                json={"override_decision": "approved", "reviewer_notes": "w310 owner approval"})
    ap = client.post(f"/api/v1/vsb/{vid}/evolution/apply").json()
    assert ap["applied"] is True and ap["mutations_applied"] > 0
    assert client.get(f"/api/v1/cca/{cca}").json()["status"] == "implemented"
    ship = _json.loads((data_path("vsb_repos") / f"{vid}.ship.json").read_text(encoding="utf-8"))
    assert ship.get("stale") is True
    client.post(f"/api/v1/vsb/{vid}/repo")
    idmd = (data_path("vsb_repos") / vid / "IDENTITY.md").read_text(encoding="utf-8")
    assert "Applied mutations (CCA-approved)" in idmd
    # applying twice is an honest no-op (nothing pending)
    again = client.post(f"/api/v1/vsb/{vid}/evolution/apply").json()
    assert again["applied"] is False and again["reason"] == "no_pending_evolution"


def test_birth_is_alive_and_consequences(client):
    # §3×§8×§12 (W309) — birth is ALIVE: the newborn's first §11 screen + first governed economy
    # cycle run AT establishment; a FAIL-screened entity's distributions are HELD until a re-screen
    # clears it; autonomous drift AFTER a ship marks the repo honestly STALE.
    import json as _json
    from agentic_core.config import atomic_write_json, data_path, load_json_tolerant
    e = client.post("/api/v1/genesis/establish", json={
        "problem": "w309 living birth venture", "domain": "enterprise",
        "concept": "A halal community textile venture with clear operations.",
        "design": "Design body.", "commercialisation": "Commercial plan."}).json()
    vid = e["vsb_id"]
    bv = e.get("birth_vitals") or {}
    assert (bv.get("first_screen") or {}).get("overall") in ("pass", "review", "fail")
    fc = bv.get("first_cycle") or {}
    assert fc.get("cycle") == 1 or fc.get("cycle_ran") is False     # ran, or held honestly
    ship_p = data_path("vsb_repos") / f"{vid}.ship.json"
    assert _json.loads(ship_p.read_text(encoding="utf-8")).get("stale") is False   # vitals BEFORE ship
    # autonomous drift after the ship → stale, with the reason. W340 — drift requires MATERIAL
    # change (a zero-activity maintenance cycle no longer marks stale), so seed real activity.
    from agentic_core.economy.living_vsbs import operate_vsb
    from agentic_core.economy.revenue import record_event as _rec_ev
    _rec_ev(vid, "revenue", 250.0, "marketplace", ref="w309-drift")
    op = operate_vsb(vid)
    assert op and op.get("error") is None
    ship2 = _json.loads(ship_p.read_text(encoding="utf-8"))
    assert ship2.get("stale") is True and "cycle" in str(ship2.get("stale_reason", ""))
    # a FAIL screen HOLDS the economy — §11 teeth in §12
    hp = data_path("vsb_compliance_history.json")
    h = load_json_tolerant(hp, {}) or {}
    h[vid] = {"overall": "fail", "last_at": "2026-08-22T00:00:00Z", "history": []}
    atomic_write_json(hp, h)
    held = operate_vsb(vid)
    assert held.get("cycle_ran") is False and held.get("held") == "compliance_fail_hold"
    # ...and the hold LIFTS when a re-screen clears it (this entity screens pass/review)
    from agentic_core.organism.heartbeat import screen_living_vsb
    res = screen_living_vsb(vid)
    if res and res.get("overall") != "fail":
        lifted = operate_vsb(vid)
        assert lifted.get("held") is None and lifted.get("error") is None


def test_offering1_gated_and_develop_loop(client):
    # §10×§11×§3A (W308) — Offering-1 is GATED: every domain-tool / refine response passes the same
    # living QMS + compliance gate (FLAG, never block — the output always arrives, its real posture
    # rides on the provenance), and the DEVELOP loop is real: refined content persists as the next
    # deliverable version VERBATIM instead of evaporating in the UI.
    r = client.post("/api/v1/education/feedback", json={
        "student_work": "An essay on rivers and their role in trade across history, "
                        "with substantive discussion of the Thames.", "criteria": "clarity"})
    assert r.status_code == 200
    qa = (r.json().get("ai_provenance") or {}).get("quality_assurance") or {}
    assert "qms_gate_passed" in qa and "compliance_overall" in qa    # gated, output intact
    rf = client.post("/api/v1/refine", json={
        "previous": "A draft about community gardens with several substantive paragraphs "
                    "of real content to refine further today.", "instruction": "tighten"}).json()
    assert "qms_gate_passed" in ((rf.get("ai_provenance") or {}).get("quality_assurance") or {})
    body = ("# Dev Loop\n\n## Objective\nSubstantive deliverable content well beyond the stub floor, "
            "discussing the halal community meal service in specific operational detail across "
            "procurement, kitchen operations and delivery routes.\n\n## Next Steps\nIterate.")
    d = client.post("/api/v1/deliverables/produce", json={
        "type": "brief", "brief": "w308 dev", "content": body}).json()
    d2 = client.post(f"/api/v1/deliverables/{d['id']}/regenerate", json={
        "content": body + "\n\n## Refinement\nW308-REFINED-MARKER."}).json()
    assert len(d2["versions"]) == len(d["versions"]) + 1
    assert "W308-REFINED-MARKER" in d2["content"]
    assert d2["ai_provenance"]["served_by"] == "verbatim-ingest"
    # the brief-driven regeneration path is untouched
    d3 = client.post(f"/api/v1/deliverables/{d['id']}/regenerate", json={"brief": "w308 regen"}).json()
    assert d3["ai_provenance"]["served_by"] != "verbatim-ingest"


def test_qms_defect_loop_and_measured_bar(client):
    # §10 (W307) — the QMS is genuinely stateful and honest: defects are PERSISTENT + TRACEABLE,
    # the non-conformance rate is a REAL rate (failures / gates run), the §8.7/§10.2
    # defect→correction→re-verify loop closes only on a genuine pass (and reopens on a failed
    # re-verify), and the quality record measures the §10 bar PER-CRITERION instead of implying
    # a 16-criterion measurement that never ran.
    base = client.get("/api/v1/vbs/qms/defects").json()["summary"]
    assert client.post("/api/v1/vbs/qms/gate", json={"coverage": 0.2, "stubs_found": False}).json()["passed"] is False
    assert client.post("/api/v1/vbs/qms/gate", json={"coverage": 0.99, "stubs_found": False}).json()["passed"] is True
    d = client.get("/api/v1/vbs/qms/defects", params={"status": "open"}).json()
    s = d["summary"]
    assert s["gates_run"] == base["gates_run"] + 2 and s["defects_total"] == base["defects_total"] + 1
    # W316 — the rate is FAILURES over gates run (a failed re-verify counts as a failure)
    assert s["gates_run"] > 0 and abs(s["non_conformance_rate"] - round(s["gate_failures"] / s["gates_run"], 4)) < 1e-9
    new = [x for x in d["defects"] if x["id"].startswith("DEF-")]
    assert new and new[0]["label"] and new[0]["status"] == "open"
    did = new[0]["id"]
    # correction alone never closes; re-verify on real metrics does
    cor = client.post(f"/api/v1/vbs/qms/defects/{did}/correct", json={"correction": "regenerated"}).json()
    assert cor["defect"]["status"] == "corrected"
    rev = client.post(f"/api/v1/vbs/qms/defects/{did}/reverify", json={"coverage": 0.97, "stubs_found": False}).json()
    assert rev["passed"] is True and rev["defect"]["status"] == "closed"
    # a failed re-verify REOPENS
    client.post("/api/v1/vbs/qms/gate", json={"coverage": 0.1, "stubs_found": True})
    d2 = client.get("/api/v1/vbs/qms/defects", params={"status": "open"}).json()["defects"][0]
    client.post(f"/api/v1/vbs/qms/defects/{d2['id']}/correct", json={"correction": "attempt"})
    rev2 = client.post(f"/api/v1/vbs/qms/defects/{d2['id']}/reverify", json={"coverage": 0.3, "stubs_found": False}).json()
    assert rev2["passed"] is False and rev2["defect"]["status"] == "open"
    # §10 (W316) — the failed re-verification RAISED the failure count (since `s`: the 0.1 gate
    # fail + this failed re-verify = exactly 2). Previously it only inflated the denominator,
    # so WORSE corrections produced a BETTER reported rate.
    s2 = client.get("/api/v1/vbs/qms/defects").json()["summary"]
    assert s2["gate_failures"] == s["gate_failures"] + 2
    assert abs(s2["non_conformance_rate"] - round(s2["gate_failures"] / s2["gates_run"], 4)) < 1e-9
    # the bar is measured per-criterion, honest about what was NOT measured
    body = ("# W307\n\n## Objective\nSubstantive content long enough to clear the stub floor — the "
            "living QMS measures what it can and declares the rest unmeasured, never implied.\n\n"
            "## Context\nQuality.\n\n## Key Factors\nEvidence.\n\n## Approach\nHonesty.\n\n## Next Steps\nCommit.")
    dl = client.post("/api/v1/deliverables/produce", json={
        "type": "brief", "brief": "w307 bar", "content": body}).json()
    bm = dl["quality_assurance"]["quality"]["bar_measured"]
    assert bm["measured"] >= 4 and bm["not_measured"] > 0
    assert bm["criteria"]["compliant"]["measured"] is True
    assert bm["criteria"]["best-in-class"]["met"] is None    # never claimed unmeasured criteria
    # §10 (W316) — the close leg can MEASURE instead of self-attest: reverify with the corrected
    # delivery's CONTENT re-runs the same instruments; the basis is recorded honestly either way.
    client.post(f"/api/v1/vbs/qms/defects/{d2['id']}/correct", json={"correction": "second attempt"})
    rev3 = client.post(f"/api/v1/vbs/qms/defects/{d2['id']}/reverify", json={"content": body}).json()
    assert rev3["defect"]["reverify_basis"] == "measured_from_content"
    assert rev3["passed"] is True and rev3["defect"]["status"] == "closed"
    assert rev2["defect"]["reverify_basis"] == "caller_attested"   # the legacy leg says what it is
    # and a fresh assure_delivery failure carries the REAL delivery reference for that measured leg
    stub_d = client.post("/api/v1/deliverables/produce", json={
        "type": "brief", "brief": "w316 stub", "content": "TODO"}).json()
    ref_defs = [x for x in client.get("/api/v1/vbs/qms/defects").json()["defects"]
                if (x.get("delivery_ref") or {}).get("content_sha3")]
    assert ref_defs and stub_d.get("id")


def test_deliverables_accept_verbatim_content(client):
    # §4.9 (W306) — 'any selectable format' is reachable for work already produced elsewhere:
    # /produce with content= carries it VERBATIM (no regeneration, honest provenance), still runs
    # the same §10/§11 assure_delivery gate, and every live export renders it.
    body = ("# W306 Verbatim Journey\n\n## Concept\nA halal textile venture — MARKER-W306-VERBATIM.\n\n"
            "## Commercialisation\nDirect-to-community launch.")
    d = client.post("/api/v1/deliverables/produce", json={
        "type": "report", "title": "W306 verbatim", "brief": "w306 verbatim ingest",
        "content": body}).json()
    assert d["content"] == body                                # verbatim — never regenerated
    prov = d.get("ai_provenance") or {}
    assert prov.get("served_by") == "verbatim-ingest" and prov.get("is_external") is False
    assert "Concept" in d.get("sections", [])                  # sections derived from the headings
    assert d.get("quality_assurance")                          # the §10/§11 gate still ran
    exp = client.get(f"/api/v1/deliverables/{d['id']}/export", params={"format": "slides"})
    assert exp.status_code == 200 and "MARKER-W306-VERBATIM" in exp.text
    # and the generated path is untouched: no content → the fabric generates as before
    g = client.post("/api/v1/deliverables/produce", json={
        "type": "brief", "brief": "w306 generated-path regression"}).json()
    assert g.get("ai_provenance", {}).get("served_by") != "verbatim-ingest" and g.get("content")


def test_candidates_selected_on_simulated_evidence(client):
    # §4.5 (W305) — "modelled, SIMULATED" is true: every stage-5 candidate is forward-simulated
    # through the owned model-free digital-twin pattern, a simulation-derived score joins the
    # ranking with DECLARED weights (60/40), and the selection basis names both components —
    # text proxies no longer carry selection alone.
    j = client.post("/api/v1/genesis/journey", json={
        "problem": "w305 halal textile venture", "domain": "enterprise"}).json()
    s5 = j.get("stage_5_model_simulate_rank") or {}
    cands = s5.get("candidates") or []
    assert len(cands) == 3
    for c in cands:
        assert "simulation_score" in c and "modelled_score" in c and c.get("simulation")
        assert abs(c["score"] - round(0.6 * c["modelled_score"] + 0.4 * c["simulation_score"], 3)) < 1e-9
    assert "60%" in s5.get("method", "")                      # the weights are DECLARED
    basis = s5.get("selection_basis", "")
    assert "modelled" in basis and "simulated" in basis


def test_full_journey_record_survives_establishment(client):
    # §4 (W304) — the entity keeps ALL SEVEN of the journey's stage outputs (previously 3): the
    # §4.3 research, §4.5 selected candidate with its real scores, §4.7 operational intelligence,
    # and the §5 stage verifications survive as entity.genesis_journey (untruncated); the repo
    # carries OPERATIONS.md + EVIDENCE.md; operational intelligence seeds a REAL plan objective.
    # Standalone /establish renders honest 'not provided' stubs — never invented content.
    import pathlib
    j = client.post("/api/v1/genesis/journey", json={
        "problem": "w304 halal orchard co-op", "domain": "care",
        "establish": True, "ship_output": False}).json()
    vid = (j.get("established_vsb") or {}).get("vsb_id")
    assert vid
    gj = client.get(f"/api/v1/vsb/{vid}").json().get("genesis_journey") or {}
    assert len(str(gj.get("research", ""))) > 100
    assert len(str(gj.get("operations", ""))) > 100
    assert (gj.get("selected_candidate") or {}).get("id")
    assert len(gj.get("stage_verifications") or {}) >= 4
    m = client.post(f"/api/v1/vsb/{vid}/repo").json()
    root = pathlib.Path(m["repo_root"])
    assert "Not provided" not in (root / "OPERATIONS.md").read_text(encoding="utf-8")
    evd = (root / "EVIDENCE.md").read_text(encoding="utf-8")
    assert "Selected Candidate" in evd and "Stage Verifications" in evd
    plan = client.get("/api/v1/business-plan", params={"scope": vid}).json()
    objs = (plan.get("plan") or plan).get("objectives", [])
    assert any(o.get("source") == "genesis_journey.operations" for o in objs)
    est2 = client.post("/api/v1/genesis/establish", json={
        "problem": "w304 standalone", "domain": "care", "name": "W304Solo",
        "concept": "c", "design": "d", "commercialisation": "m", "ship_output": False}).json()
    m2 = client.post(f"/api/v1/vsb/{est2['vsb_id']}/repo").json()
    root2 = pathlib.Path(m2["repo_root"])
    assert "Not provided at establishment" in (root2 / "OPERATIONS.md").read_text(encoding="utf-8")


def test_newborn_ships_its_living_body_and_journey_carries_identity(client, monkeypatch):
    # §4 (W302) — the ONE continuous workflow is real: establishment ships the newborn's WHOLE §13
    # body at birth (repo+website+webapp+mobile+board-pack, no manual clicks; opt-out honest), and
    # the journey THREADS USER IDENTITY so establish no longer crashes into 'establishment
    # deferred' under auth — the entity belongs to the authenticated user.
    from agentic_core.config import data_path
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w302 halal tutoring venture", "domain": "education", "name": "W302ShipCo",
        "concept": "c", "design": "d", "commercialisation": "m"}).json()
    iship = est.get("initial_ship") or {}
    assert iship.get("shipped") is True and len(iship.get("surfaces", [])) == 5
    assert (data_path("vsb_repos") / f"{est['vsb_id']}.ship.json").exists()
    est2 = client.post("/api/v1/genesis/establish", json={
        "problem": "w302 no-ship", "domain": "care", "name": "W302NoShip",
        "concept": "c", "design": "d", "commercialisation": "m", "ship_output": False}).json()
    assert est2.get("initial_ship") is None                   # opt-out ships nothing, honestly
    assert not (data_path("vsb_repos") / f"{est2['vsb_id']}.ship.json").exists()
    # the journey path under AUTH: no 'establishment deferred', the user owns the newborn
    from agentic_core.auth import core as auth_core
    if not auth_core._AUTH_DEPS_OK:
        import pytest as _pytest
        _pytest.skip("auth crypto deps not installed")
    users = auth_core._load_users()
    users["w302-iso"] = {"user_id": "w302-iso", "username": "w302-iso",
                         "hashed_password": auth_core._pwd_ctx.hash("pw-302"), "role": "user",
                         "created_at": "2026-01-01T00:00:00Z", "api_keys": []}
    auth_core._save_users(users)
    monkeypatch.setenv("AUTH_ENABLED", "true")
    tok = client.post("/api/v1/auth/token", data={"username": "w302-iso", "password": "pw-302"})
    H = {"Authorization": f"Bearer {tok.json()['access_token']}"}
    j = client.post("/api/v1/genesis/journey",
                    json={"problem": "w302 auth journey", "domain": "care", "establish": True},
                    headers=H).json()
    ev = j.get("established_vsb") or {}
    assert "error" not in ev and ev.get("vsb_id")             # the deferred crash is gone
    d = client.get(f"/api/v1/vsb/{ev['vsb_id']}", headers=H).json()
    assert d.get("owner_id") == "w302-iso"                    # the USER owns the newborn
    assert (ev.get("initial_ship") or {}).get("shipped") is True


def test_genesis_blueprint_reaches_the_entity_surfaces(client):
    # §4×§13 (W301) — the blueprint key-shape mismatch is FIXED: writers store flat
    # concept/design/commercialisation while every §13 reader expected phase_* keys, so each
    # established entity silently shipped a GENERIC body (the challenge fallback masked it).
    # The canonical _blueprint accessor accepts both shapes — the journey's REAL content now
    # reaches the repo docs and the website.
    import pathlib
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w301 halal community nutrition", "domain": "care", "name": "W301BlueCo",
        "concept": "CONCEPT-MARKER-ALPHA halal meal planning for elders",
        "design": "DESIGN-MARKER-BRAVO modular cold-chain service design",
        "commercialisation": "COMMERCIAL-MARKER-CHARLIE subscription with zakat-aligned pricing"}).json()
    vid = est["vsb_id"]
    m = client.post(f"/api/v1/vsb/{vid}/repo").json()
    root = pathlib.Path(m["repo_root"])
    allmd = " ".join(p.read_text(encoding="utf-8", errors="replace") for p in root.rglob("*.md"))
    assert "CONCEPT-MARKER-ALPHA" in allmd
    assert "DESIGN-MARKER-BRAVO" in allmd
    assert "COMMERCIAL-MARKER-CHARLIE" in allmd
    client.post(f"/api/v1/vsb/{vid}/website")
    web = " ".join(p.read_text(encoding="utf-8", errors="replace")
                   for p in (root / "web").rglob("*.html"))
    assert "CONCEPT-MARKER-ALPHA" in web or "halal meal planning for elders" in web
    # legacy phase_* shaped blueprints still read correctly (the fallback path)
    from agentic_core.api.vsb import _blueprint
    legacy = {"genesis_blueprint": {"phase_1_conceptualisation": {"concept": "LEGACY-C"},
                                    "phase_2_design_development": "LEGACY-D",
                                    "phase_3_commercialisation": "LEGACY-M"}}
    got = _blueprint(legacy)
    assert (got["concept"], got["design"], got["commercialisation"]) == ("LEGACY-C", "LEGACY-D", "LEGACY-M")


def test_pervsb_apex_governance_scoped(client):
    # §14 (W300) — apex governance reaches the USER'S OWN entity: /board/status?scope=<vsb_id>
    # returns THAT entity's board (honest 404 for unknown scopes; the workstation apex unchanged),
    # a scoped chief instruction lands objectives on the ENTITY's plan and appears in ITS
    # directive history, and a scoped deliberation grounds the strategy director in the SCOPED
    # plan (previously hardcoded to the workstation plan).
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w300 halal venture", "domain": "care", "name": "W300ApexCo",
        "concept": "c", "design": "d", "commercialisation": "m"}).json()
    vid = est["vsb_id"]
    s = client.get(f"/api/v1/board/status?scope={vid}").json()
    assert "W300ApexCo" in s["board"] and s["scope"] == vid and s["chief"]
    assert client.get("/api/v1/board/status").json()["board"].startswith("Workstation")
    assert client.get("/api/v1/board/status?scope=vsb-nonexistent").status_code == 404
    r = client.post("/api/v1/board/chief/instruct", json={
        "instruction": "w300: launch the halal pilot", "scope": vid}).json()
    assert r["objectives_added"] >= 1 and r["business_plan_scope"] == vid
    s2 = client.get(f"/api/v1/board/status?scope={vid}").json()
    assert any(d.get("business_plan_scope") == vid for d in s2["recent_directives"])
    d = client.post("/api/v1/board/directive", json={
        "topic": "strengthen the strategy and mission objectives of the plan",
        "domain": "care", "scope": vid}).json()
    strat = d.get("director_inputs", {}).get("dir_strategy", {})
    assert "objectives by status" in strat.get("live_grounding", "")   # scoped, not apex-hardcoded


def test_self_serve_signup_owner_gated(client, monkeypatch):
    # §14 (W297) — self-serve signup is a MECHANISM whose switch stays with the Owner: 409 while
    # auth is off (signup is meaningless), 403 while the flag is off (accounts stay Owner-curated),
    # and when the Owner enables it: validated, duplicate-safe, and NEVER able to mint an admin.
    # /auth/config reports the truth so the UI never renders signup theatre.
    from agentic_core.auth import core as auth_core
    if not auth_core._AUTH_DEPS_OK:
        import pytest as _pytest
        _pytest.skip("auth crypto deps not installed")
    cfg = client.get("/api/v1/auth/config").json()
    assert cfg["auth_enabled"] is False and cfg["self_serve_signup_enabled"] is False
    assert client.post("/api/v1/auth/signup",
                       json={"username": "w297a", "password": "longpass297"}).status_code == 409
    monkeypatch.setenv("AUTH_ENABLED", "true")
    assert client.post("/api/v1/auth/signup",
                       json={"username": "w297a", "password": "longpass297"}).status_code == 403
    monkeypatch.setenv("SELF_SERVE_SIGNUP_ENABLED", "true")
    assert client.get("/api/v1/auth/config").json()["self_serve_signup_enabled"] is True
    assert client.post("/api/v1/auth/signup",
                       json={"username": "w297a", "password": "short"}).status_code == 422
    import uuid as _uuid
    uname = f"w297-{_uuid.uuid4().hex[:6]}"
    r = client.post("/api/v1/auth/signup", json={"username": uname, "password": "longpass297"}).json()
    assert r["role"] == "user"                                # NEVER admin via self-serve
    assert client.post("/api/v1/auth/signup",
                       json={"username": uname, "password": "longpass297"}).status_code == 409
    tok = client.post("/api/v1/auth/token", data={"username": uname, "password": "longpass297"})
    assert tok.status_code == 200                             # the new user genuinely signs in


def test_pervsb_management_surfaces_tenant_isolated(client, monkeypatch):
    # §14×§17.5 (W295) — tenant isolation now covers the per-VSB MANAGEMENT surfaces (repo ·
    # website · board-pack · review-gates · genome · ship · evolve · shipped-repo read), which
    # previously had NO scoping: any user could manage any entity. Another tenant gets 404 —
    # never a confirming 403 — on every surface; the owner is fully served; and the economy
    # cycle attributes to the LIVING entity's registration, not the request's "Rehan" default.
    from agentic_core.auth import core as auth_core
    if not auth_core._AUTH_DEPS_OK:
        import pytest as _pytest
        _pytest.skip("auth crypto deps not installed")
    users = auth_core._load_users()
    for uname, pw in (("alice-295", "pw-alice"), ("bob-295", "pw-bob")):
        users[uname] = {"user_id": uname, "username": uname,
                        "hashed_password": auth_core._pwd_ctx.hash(pw), "role": "user",
                        "created_at": "2026-01-01T00:00:00Z", "api_keys": []}
    auth_core._save_users(users)
    monkeypatch.setenv("AUTH_ENABLED", "true")

    def _hdr(u, p):
        r = client.post("/api/v1/auth/token", data={"username": u, "password": p})
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['access_token']}"}
    alice, bob = _hdr("alice-295", "pw-alice"), _hdr("bob-295", "pw-bob")
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w295 halal venture", "domain": "care", "name": "W295IsoCo",
        "concept": "c", "design": "d", "commercialisation": "m"}, headers=alice).json()
    vid = est["vsb_id"]
    assert client.post(f"/api/v1/vsb/{vid}/repo", headers=alice).status_code == 200
    checks = [("POST", f"/api/v1/vsb/{vid}/repo"), ("GET", f"/api/v1/vsb/{vid}/repo"),
              ("POST", f"/api/v1/vsb/{vid}/website"), ("POST", f"/api/v1/vsb/{vid}/board-pack"),
              ("GET", f"/api/v1/vsb/{vid}/review-gates"), ("GET", f"/api/v1/vsb/{vid}/genome"),
              ("POST", f"/api/v1/vsb/{vid}/repo/ship"), ("POST", f"/api/v1/vsb/{vid}/evolve"),
              ("GET", f"/api/v1/vsb/{vid}/repo/ship")]
    for m, u in checks:
        resp = client.request(m, u, headers=bob, json={} if m == "POST" else None)
        assert resp.status_code == 404, f"{m} {u} leaked: {resp.status_code}"
    ship = client.post(f"/api/v1/vsb/{vid}/repo/ship", headers=alice).json()
    assert ship.get("coherent_whole") is True                 # the owner is fully served
    # W320 — under auth the economy router requires a session (anonymous → 401) and is
    # owner-scoped, so the cycle runs AS the owner; attribution stays honest.
    anon = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "revenue": 500})
    assert anon.status_code == 401                            # anonymous writes refused under auth
    cyc = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "revenue": 500},
                      headers=alice).json()
    att = cyc.get("attribution") or {}
    assert att.get("basis", "").startswith("living_registration")   # honest attribution
    assert att.get("owner") == "alice-295"                    # the ENTITY's owner, not "Rehan"


def test_capital_compounds_and_proposals_commercialise(client):
    # §12 (W294) — two loops closed: the waterfall's capital_fund stage COMPOUNDS into the shared
    # Sovereign Capital Fund (previously only a ledger row — three disconnected WST pools), and a
    # cascade-PROPOSED offering CURATES into the live marketplace by a deliberate act (§11-screened
    # with TEETH: haram content blocks with the verdicts; the cascade proposes, never publishes).
    import uuid as _uuid
    from agentic_core.economy.living_vsbs import register, operate_one
    from agentic_core.economy.revenue import record_event
    vid = f"vsb-w294-{_uuid.uuid4().hex[:6]}"
    register(vid, name="W294 Halal Ventures", domain="care")
    record_event(vid, "revenue", 1000.0, "marketplace_sale", ref="seed")
    before = client.get("/api/v1/fund/status").json()
    tb = before.get("total_capital") or (before.get("fund") or {}).get("total_capital") or 0
    for _ in range(40):
        op = operate_one() or {}
        if op.get("vsb_id") == vid:
            break
    assert op.get("revenue_recognised_wst") == 1000.0
    after = client.get("/api/v1/fund/status").json()
    ta = after.get("total_capital") or (after.get("fund") or {}).get("total_capital") or 0
    assert ta > tb                                            # the endowment genuinely compounded
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w294 catalogue proposals", "domain": "enterprise"}).json()
    cur = client.post(f"/api/v1/swarm/catalogue/proposed/{r['run_id']}/curate", json={
        "item": "Halal Meal Planning Service",
        "description": "transparent community nutrition benefit",
        "price_wst": 25, "vsb_id": vid}).json()
    assert cur["listing"].get("id") and cur["listing"].get("vsb_id") == vid   # sales feed the VSB
    bad = client.post(f"/api/v1/swarm/catalogue/proposed/{r['run_id']}/curate",
                      json={"item": "Alcohol subscription box", "price_wst": 10})
    assert bad.status_code == 409                             # §11 has TEETH on publication
    assert client.post("/api/v1/swarm/catalogue/proposed/nope/curate",
                       json={"item": "x"}).status_code == 404
    pc = client.get("/api/v1/swarm/catalogue/proposed").json()["proposed"]
    mine = next(p for p in pc if p["run_id"] == r["run_id"])
    assert mine["status"] == "curated" and len(mine.get("curated", [])) == 1


def test_economy_fed_by_real_work(client):
    # §12×§5 (W293) — the economic organism is FED by the enterprise's REAL work: the fabricated
    # flat 1000-WST tick is GONE. An idle entity runs an honest ZERO-revenue maintenance cycle; a
    # marketplace sale attributed to the VSB and a QMS-passed VSB-scoped cascade delivery (declared
    # simulated tariff + BMS cost estimate) are recorded as events; the next autonomous cycle
    # consumes exactly that intake, exactly once. Virtual WST only.
    import uuid as _uuid
    from agentic_core.economy.living_vsbs import register, operate_one
    from agentic_core.economy.revenue import pending_summary
    vid = f"vsb-w293-{_uuid.uuid4().hex[:6]}"
    register(vid, name="W293 Halal Ventures", domain="care")

    def _tick():
        for _ in range(40):
            op = operate_one() or {}
            if op.get("vsb_id") == vid:
                return op
        raise AssertionError("round-robin never reached the test VSB")
    op0 = _tick()
    assert op0["revenue_basis"] == "no_activity_maintenance_cycle"   # honest zero, not fabricated
    assert op0["revenue_recognised_wst"] == 0.0
    lst = client.post("/api/v1/marketplace/listings", json={
        "name": "W293 Halal Meal Plan", "price_wst": 40, "vsb_id": vid}).json()
    lid = lst.get("id") or (lst.get("listing") or {}).get("id")
    from agentic_core.commercial.token_ledger import TokenLedger, UserTier
    TokenLedger().initialize_user("w293buyer", UserTier.PRO)
    rec = client.post(f"/api/v1/marketplace/listings/{lid}/purchase",
                      json={"user_id": "w293buyer", "quantity": 2}).json()
    assert rec.get("revenue_recognised_for") == vid                  # the sale reached the books
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w293 deliver for the entity", "domain": "enterprise", "scope": vid}).json()
    if r["quality"].get("qms_gate_passed"):
        assert (r.get("economic_event") or {}).get("revenue_wst") == 250.0   # the declared tariff
    expected = pending_summary(vid)["pending_revenue_wst"]
    assert expected >= 80.0                                          # at least the sale landed
    op1 = _tick()
    assert op1["revenue_basis"] == "recognised_events"
    assert op1["revenue_recognised_wst"] == expected                 # exactly the real intake
    assert pending_summary(vid)["pending_events"] == 0               # consumed exactly once


def test_vsb_repo_cascades_rerunnable(client):
    # §13 (W291) — the repo's AI-swarm cascades are RE-RUNNABLE: POST /repo/cascade executes the
    # REAL §5 org cascade SCOPED to this VSB (Chief/CEO ground in ITS living plan — W280), binds
    # the run summary back INTO the repo (resources/runs/<id>.json + a commit), and a missing repo
    # is an honest 404 — the repo is an operating surface, not a snapshot.
    import pathlib
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w291 halal venture", "domain": "care", "name": "W291CascCo",
        "concept": "c", "design": "d", "commercialisation": "m", "ship_output": False}).json()
    vid = est["vsb_id"]
    assert client.post(f"/api/v1/vsb/{vid}/repo/cascade", json={}).status_code == 404
    m = client.post(f"/api/v1/vsb/{vid}/repo").json()
    from agentic_core.api.business_plan import parse_objective_lines, _load as _bpl, _save as _bps
    plan = _bpl(vid)
    plan.setdefault("objectives", []).extend(
        parse_objective_lines("Grow the W291 pilot | pilot live | next review | AI CEO"))
    _bps(plan)
    oid = _bpl(vid)["objectives"][-1]["id"]
    r = client.post(f"/api/v1/vsb/{vid}/repo/cascade",
                    json={"mission": "w291 operate the entity", "objective_id": oid}).json()
    assert r["run"]["business_plan_scope"] == vid             # scoped to THIS entity's plan
    rr = r["repo_run"]
    assert (rr.get("plan_binding") or {}).get("result") in ("review_written", "qms_failed_no_advance")
    runfile = pathlib.Path(m["repo_root"]) / "resources" / "runs" / f"{rr['run_id']}.json"
    assert runfile.exists()                                   # the run is bound INTO the repo
    assert "cascade:" in r["version_control"]["message"]      # and committed


def test_vsb_repo_ships_as_one_whole_and_tracks_evolution(client):
    # §13 (W290) — the canonical output ships as ONE COHERENT WHOLE (repo + website + webapp +
    # mobile + board pack regenerated from CURRENT entity data under a unified manifest, one
    # repo-level commit, UEG-sealed), and the repo TRACKS the life: evolution re-ships it by
    # default, or honestly marks it STALE on opt-out — never silently outdated.
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w290 halal community venture", "domain": "care",
        "name": "W290ShipCo", "concept": "c", "design": "d", "commercialisation": "m"}).json()
    vid = est["vsb_id"]
    s = client.post(f"/api/v1/vsb/{vid}/repo/ship").json()
    assert s["shipped"] and set(s["surfaces"]) == {"repo", "website", "webapp", "mobile", "board_pack"}
    assert s["coherent_whole"] is True and s["version_control"]["commits_total"] >= 1
    ev = client.post(f"/api/v1/vsb/{vid}/evolve", json={"trigger": "w290 refresh"}).json()
    assert (ev.get("repo_refresh") or {}).get("action") == "re_shipped"
    ev2 = client.post(f"/api/v1/vsb/{vid}/evolve",
                      json={"trigger": "w290 stale", "refresh_repo": False}).json()
    assert (ev2.get("repo_refresh") or {}).get("action") == "marked_stale"
    g = client.get(f"/api/v1/vsb/{vid}/repo/ship").json()
    assert g["stale"] is True and "generation" in g["stale_reason"]
    events = client.get("/api/v1/gaas/ueg/events?limit=200").json()["events"]
    assert any(e.get("data", {}).get("type") == "vsb.repo.ship" for e in events)


def test_vsb_repo_genuinely_version_controlled(client):
    # §13 (W289) — "shipped as a coherent, VERSION-CONTROLLED whole" is true now: the entity repo
    # is git-init'd on first generation (nested safely under gitignored data/), every generation
    # commits with a structured message (surface · QMS · compliance · seal), the prior manifest
    # appends to history instead of being silently overwritten, and compliance/QUALITY.md is the
    # REAL sealed record (§10 figures + §11 per-framework verdicts), not a pointer stub.
    import pathlib
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w289 halal community nutrition venture", "domain": "care",
        "name": "W289RepoCo", "concept": "c", "design": "d", "commercialisation": "m", "ship_output": False}).json()
    vid = est["vsb_id"]
    m1 = client.post(f"/api/v1/vsb/{vid}/repo").json()
    assert m1["version_control"]["mechanism"] in ("git", "hash-chain")   # honest either way
    assert m1["version_control"]["commits_total"] >= 1
    assert m1["manifest_history"] == []                       # first generation — no lineage yet
    m2 = client.post(f"/api/v1/vsb/{vid}/repo").json()
    assert m2["version_control"]["commits_total"] > m1["version_control"]["commits_total"]
    assert len(m2["manifest_history"]) == 1                   # the prior manifest is lineage now
    assert "QMS" in m2["version_control"]["message"] and "compliance" in m2["version_control"]["message"]
    root = pathlib.Path(m2["repo_root"])
    q = (root / "compliance" / "QUALITY.md").read_text(encoding="utf-8")
    assert "Document-control seal" in q and "sharia_halal" in q   # the REAL sealed record
    w = client.post(f"/api/v1/vsb/{vid}/website").json()
    assert w["version_control"]["commits_total"] > m2["version_control"]["commits_total"]


def test_continuous_compliance_beat(client):
    # §11 (W288) — "continuously live": the heartbeat's opt-in auto_compliance beat re-screens the
    # least-recently-screened LIVING VSB over its CURRENT text (an entity screened at establishment
    # is re-evaluated as it evolves), persists per-VSB history, and honours honesty at the edges
    # (no living VSBs → None, never a fabricated reading). Also: the previously-DEAD auto_economy
    # flag is genuinely consulted now (it was settable and reported but never checked in beat()).
    import asyncio as _aio, uuid as _uuid
    from agentic_core.organism.heartbeat import heartbeat
    from agentic_core.economy.living_vsbs import register
    loop = _aio.get_event_loop()
    vid = f"vsb-w288-{_uuid.uuid4().hex[:6]}"
    try:
        heartbeat.configure(auto_compliance=True, auto_economy=False)
        register(vid, name="Halal community nutrition venture", domain="care")
        loop.run_until_complete(heartbeat.beat())
        assert heartbeat.last_compliance and heartbeat.last_compliance["overall"] in ("pass", "review", "fail")
        from agentic_core.config import data_path, load_json_tolerant
        hist = load_json_tolerant(data_path("vsb_compliance_history.json"), {})
        assert vid in hist and hist[vid]["history"]           # per-VSB history persisted
        r_off = loop.run_until_complete(heartbeat.beat())     # auto_economy off → no operate action
        assert "operate_vsb" not in r_off.get("actions", [])
        heartbeat.configure(auto_economy=True)
        r_on = loop.run_until_complete(heartbeat.beat())      # on → the flag genuinely gates
        assert "operate_vsb" in r_on.get("actions", [])
    finally:
        heartbeat.configure(auto_compliance=False, auto_economy=False)
    r = client.post("/api/v1/heartbeat/configure", json={"auto_compliance": True}).json()
    assert client.get("/api/v1/heartbeat/status").json()["auto_compliance"] is True
    client.post("/api/v1/heartbeat/configure", json={"auto_compliance": False})


def test_compliance_sealed_ueg_immune_and_routed(client):
    # §11×§6 (W287) — verdicts are CONSEQUENTIAL now: the screen runs BEFORE the QMS seal (the
    # sealed quality record carries the §11 verdicts — previously computed after, so every sealed
    # record omitted them), every screen seals a compliance.screen UEG event, a FAIL registers
    # with the immune system, and a FAIL on a MATERIAL label routes to Change Control at MEDIUM
    # tier (never auto-approved — a genuine human decision). Flag-not-block preserved throughout.
    import asyncio as _aio
    from agentic_core.vbs.quality import assure_delivery
    loop = _aio.get_event_loop()
    r = loop.run_until_complete(assure_delivery(
        "a cascade delivery promoting alcohol sales and gambling revenue " + "x" * 200,
        ["Section"], label="cascade"))
    q = r["quality"]
    assert q["compliance"]["overall"] == "fail"
    assert q.get("compliance_routed_to_cca") is True          # material fail → arms-length review
    assert q.get("quality_record_hash")                       # still sealed (flag, not block)
    ev = client.get("/api/v1/gaas/ueg/events?limit=100").json()["events"]
    comp = [e["data"] for e in ev if e.get("data", {}).get("type") == "compliance.screen"]
    assert comp and comp[-1]["verdicts"].get("sharia_halal") == "fail"   # sealed to the UEG
    cca = client.get("/api/v1/cca/queue").json()
    items = cca.get("queue", cca.get("changes", []))
    routed = [x for x in items if "Compliance FAIL" in str(x.get("title", ""))]
    assert routed and routed[0]["impact_tier"] == "MEDIUM"    # above LOW auto-approve
    assert routed[0]["status"] != "approved"                  # held for a genuine decision
    r2 = loop.run_until_complete(assure_delivery(
        "a halal community nutrition programme with transparent pricing " + "y" * 150,
        ["Section"], label="cascade"))
    assert "compliance_routed_to_cca" not in r2["quality"]    # a pass routes nothing
    # the cascade's persisted run record + UEG seal carry the compliance verdict (swarm.py side)
    rc = client.post("/api/v1/swarm/cascade", json={
        "mission": "w287 compliance-sealed cascade", "domain": "enterprise"}).json()
    top = client.get("/api/v1/swarm/cascade/runs").json()["runs"][0]
    assert top["run_id"] == rc["run_id"]
    assert "compliance_overall" in top["quality"]


def test_ethical_engine_real_per_dimension(client):
    # §11 (W286) — the Ethical framework EVALUATES now (the old screen hardcoded 'pass — no
    # violations detected' without checking anything): four explainable dimensions (human ·
    # environment · quality · value), ambiguity → review, un-assessable dimensions say
    # 'not_assessed' honestly (never a fabricated pass), and the caller's PRECOMPUTED QMS
    # metrics thread into the quality dimension without any circular call.
    from agentic_core.compliance.ethical_engine import evaluate_ethics
    r = evaluate_ethics("a scheme to exploit vulnerable users with hidden fees")
    assert r["overall"] == "fail"                          # extractive value framing
    assert any(d["dimension"] == "human" and d["status"] == "review" for d in r["dimensions"])
    r2 = evaluate_ethics("dumping contaminated waste to cut costs while helping the community")
    assert any(d["dimension"] == "environment" and d["status"] == "review" for d in r2["dimensions"])
    r3 = evaluate_ethics("WATER")                          # a short charity-cause subject
    assert any(d["status"] == "not_assessed" for d in r3["dimensions"])   # honest, not a fake pass
    r4 = evaluate_ethics("a comprehensive technical migration of the database layer executed "
                         "thoroughly with zero stated societal framing whatsoever")
    assert r4["overall"] == "review"                       # no stated benefit → review, not pass
    r5 = evaluate_ethics("x" * 300, {"delivery_coverage": 0.9, "stub_found": False})
    assert any(d["dimension"] == "quality" and d["status"] == "pass" for d in r5["dimensions"])
    from agentic_core.api.compliance import screen_compliance
    e = next(v for v in screen_compliance("a plan to exploit users")["verdicts"]
             if v["framework"] == "ethical")
    assert e["status"] in ("review", "fail") and "human: review" in e["reason"]
    assert "(engine-backed)" in e["reason"]                # the registry claim is now true


def test_compliance_engines_genuinely_invoked(client):
    # §11 (W285) — the '(engine-backed)' label is TRUE now: the Halal and UK-Legal ENGINES are
    # actually INVOKED (the old screen imported them and appended the label without a single
    # call), with worst-of merging (an engine pass never downgrades a rule fail), the UK engine's
    # SHA3-512 audit hash in the reason, an HONEST '(built-in rules)' label when an engine cannot
    # run, and the phantom 'RegulatoryComplianceMonitor' purged from the framework registry.
    from agentic_core.api.compliance import screen_compliance
    import agentic_core.api.compliance as C
    r = screen_compliance("a venture selling alcohol at events")
    h = next(v for v in r["verdicts"] if v["framework"] == "sharia_halal")
    assert h["status"] == "fail" and "HARAM_ELEMENT_ALCOHOL" in h["reason"]   # the ENGINE's code
    assert "(engine-backed)" in h["reason"]
    r2 = screen_compliance("the plan involves unfair dismissal of staff")
    l2 = next(v for v in r2["verdicts"] if v["framework"] == "uk_legal")
    assert l2["status"] == "fail" and "STATUTORY_BREACH: ERA1996" in l2["reason"]
    assert "audit " in l2["reason"]                       # the engine's SHA3-512 audit hash
    r3 = screen_compliance("a halal-certified community meal service with transparent pricing")
    h3 = next(v for v in r3["verdicts"] if v["framework"] == "sharia_halal")
    assert h3["status"] == "pass" and "(engine-backed)" in h3["reason"]   # pass keeps the suffix
    orig = C._halal_engine
    try:
        C._halal_engine = lambda: (_ for _ in ()).throw(RuntimeError("down"))
        r4 = screen_compliance("gambling ring")
        h4 = next(v for v in r4["verdicts"] if v["framework"] == "sharia_halal")
        assert h4["status"] == "fail"                     # the built-in rule verdict stands
        assert "(built-in rules)" in h4["reason"] and "engine-backed" not in h4["reason"]
    finally:
        C._halal_engine = orig
    fw = client.get("/api/v1/compliance/frameworks").json()["frameworks"]
    assert all("RegulatoryComplianceMonitor" not in f["engine"] for f in fw)   # phantom purged
    assert any("invoked" in f["engine"] for f in fw)      # the registry says what genuinely runs


def test_tree_planner_swarm_planned_with_honest_floor(client):
    # §6 (W283) — the workflow-tree decomposition is PLANNED BY the swarm's own intelligence only
    # when a REAL owned model genuinely served: under the deterministic floor the planner label is
    # honest ("deterministic_template" — zero wasted planning calls), a valid model-produced DAG
    # yields "swarm_planned", and a structurally invalid plan (two roots) falls back.
    import asyncio as _aio
    from agentic_core.ai.native.orchestrator import orchestrator
    import agentic_core.ai.native.model_resource as mr
    loop = _aio.get_event_loop()
    r = loop.run_until_complete(orchestrator.orchestrate_tree("w283 planner honesty contract"))
    assert r["planner"] == "deterministic_template"       # AI_DISABLE_LOCAL → the honest floor
    assert len(r["nodes"]) >= 4 and r["final"]            # the template tree still genuinely ran
    orig_complete, orig_up = orchestrator.complete, mr.ollama_up
    try:
        mr.ollama_up = lambda: True

        async def _good(prompt, **kw):
            return {"served_by": "ollama:x", "is_external": False, "output":
                    "frame | framing analyst | Frame the goal | -\n"
                    "research | researcher | Gather facts | frame\n"
                    "synth | synthesiser | Combine | frame,research"}
        orchestrator.complete = _good
        nodes, planner = loop.run_until_complete(orchestrator._plan_tree_adaptive("g", 10.0))
        assert planner == "swarm_planned" and [n["id"] for n in nodes] == ["frame", "research", "synth"]

        async def _bad(prompt, **kw):
            return {"served_by": "ollama:x", "output": "a | r | t | -\nb | r | t | -"}
        orchestrator.complete = _bad
        _, planner2 = loop.run_until_complete(orchestrator._plan_tree_adaptive("g", 10.0))
        assert planner2 == "deterministic_template"       # invalid DAG → deterministic fallback
    finally:
        orchestrator.complete, mr.ollama_up = orig_complete, orig_up


def test_delegate_standard_catalogue_landing_and_stage_models(client):
    # §5×§6 (W282) — three seams closed: /swarm/delegate joins the W268+ standard (provenance +
    # per-call ops rows + QMS-gated synthesis + honest homeostasis demand); the cascade's
    # Products/Services catalogue LANDS as persisted PROPOSED offerings (the cascade proposes,
    # the Owner curates — never auto-published; unparseable floor output honestly persists raw
    # with zero items); and bespoke swarm stages route to a NAMED owned model.
    d = client.post("/api/v1/swarm/delegate", json={
        "task": "w282 delegate standard contract", "domain": "enterprise"}).json()
    assert d["ai_provenance"]["served_by"] and "qms_gate_passed" in d["quality"]
    assert d["homeostasis"] is not None
    from agentic_core.api.operational_excellence import _load as _ops
    assert len([x for x in _ops() if x.get("ref") == d["run_id"]]) >= 3   # each call accrued a row
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w282 catalogue landing contract", "domain": "enterprise"}).json()
    assert isinstance(r["catalogue_items_proposed"], list)
    pc = client.get("/api/v1/swarm/catalogue/proposed").json()["proposed"]
    assert pc[0]["run_id"] == r["run_id"] and pc[0]["status"] == "proposed"
    assert pc[0]["raw"]                                       # raw preserved even when items parse 0
    import asyncio as _aio
    from agentic_core.ai.native.orchestrator import orchestrator
    s = _aio.get_event_loop().run_until_complete(orchestrator.swarm("w282", [
        {"role": "a", "instruction": "say hi", "model": "native"},
        {"role": "b", "instruction": "say more"}]))
    assert s["trace"][0]["requested_model"] == "native"       # the named stage routing recorded
    assert "requested_model" not in s["trace"][1]             # auto stays unlabelled (honest)


def test_tier_identity_and_founder_modelled_chief(client):
    # §5 (W281) — tiers have PERSISTENT identity (each carries its accumulated record — runs
    # served + its manager's last appraisal — into the next cascade; no more re-prompted-from-
    # scratch officers), and the Chief twin reasons from the FOUNDER'S LIVED RECORD (standing
    # canon values + the Owner's actual remembered instructions), iterating with every directive.
    client.post("/api/v1/board/chief/instruct", json={
        "instruction": "w281 founder memory: prioritise the halal certification pilot"})
    from agentic_core.api.board import founder_profile
    fp = founder_profile()
    assert "halal ethics" in fp and "never fabricate" in fp        # the Owner's standing values
    assert "certification pilot" in fp                             # the twin REMEMBERS instructions
    r1 = client.post("/api/v1/swarm/cascade", json={
        "mission": "w281 identity contract run 1", "domain": "enterprise"}).json()
    r2 = client.post("/api/v1/swarm/cascade", json={
        "mission": "w281 identity contract run 2", "domain": "enterprise"}).json()
    ia = r2["tier_identity_applied"]
    assert set(ia.keys()) == set(r1["appraisals"].keys())          # every tier carried its identity
    assert all(v >= 1 for v in ia.values())                        # accumulated from run 1 onward
    from agentic_core.config import data_path, load_json_tolerant
    store = load_json_tolerant(data_path("tier_identity.json"), {})
    assert store["bto_appraises_build"]["runs"] >= 2               # the record persists + accumulates
    assert store["bto_appraises_build"]["last_appraisal"]          # grounded in the real appraisal


def test_cascade_sees_and_moves_the_living_plan(client):
    # §5 (W280) — the cascade's Chief genuinely OWNS the living Business Plan: `scope` selects the
    # plan that grounds the apex tiers (its real objectives injected into the Chief/CEO prompts),
    # and an `objective_id`-bound run writes a review back (with the run id + the BTO's fabric
    # requisitions) and advances planned→in_progress ONLY on a QMS-passed run — never auto-done.
    import uuid as _uuid
    scope = f"w280-{_uuid.uuid4().hex[:8]}"
    from agentic_core.api.business_plan import parse_objective_lines, _load as _bpl, _save as _bps
    plan = _bpl(scope)
    plan.setdefault("objectives", []).extend(
        parse_objective_lines("Deliver the W280 org pilot | pilot live | next review | AI CEO"))
    _bps(plan)
    oid = _bpl(scope)["objectives"][-1]["id"]
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w280 plan-grounded cascade contract", "domain": "enterprise",
        "scope": scope, "objective_id": oid}).json()
    assert r["business_plan_scope"] == scope
    pb = r["plan_binding"]
    obj = next(o for o in _bpl(scope)["objectives"] if o["id"] == oid)
    if pb["result"] == "review_written":                   # the QMS gate passed this run
        assert pb["advanced"] is True and obj["status"] == "in_progress"
        assert obj["reviews"][-1]["org_cascade_run"]["run_id"] == r["run_id"]
    else:                                                  # honest: a failed gate never advances
        assert pb["result"] == "qms_failed_no_advance" and obj["status"] == "planned"
    top = client.get("/api/v1/swarm/cascade/runs").json()["runs"][0]
    assert top["run_id"] == r["run_id"]
    assert (top.get("plan_binding") or {}).get("objective_id") == oid   # binding persisted


def test_board_deliberates_as_specialists(client):
    # §5 (W279) — the Board's directive is a REAL specialist deliberation: relevant directors are
    # selected deterministically (mandate-word overlap — the reason IS the overlap), EACH
    # contributes through its own AI call grounded in LIVE readings of the systems it owns, and
    # the Chief synthesises over the directors' ACTUAL inputs — no single-call invented
    # 'Director Inputs'.
    r = client.post("/api/v1/board/directive", json={
        "topic": "strengthen the delivery operations and build quality of the resource facilities",
        "domain": "enterprise"}).json()
    engaged = r["directors_engaged"]
    assert engaged and set(engaged) & {"dir_operations", "dir_technology"}   # relevant specialists
    di = r["director_inputs"]
    assert set(di.keys()) == set(engaged)
    for v in di.values():
        assert v["live_grounding"] and v["input"]           # every input grounded in a live reading
    assert sum(r["ai_provenance"]["served_by"].values()) == len(engaged) + 1   # directors + chair
    # an off-mandate topic still deliberates via the default strategy/operations mandate holders
    r2 = client.post("/api/v1/board/directive", json={"topic": "zzz qqq", "domain": "x"}).json()
    assert set(r2["directors_engaged"]) == {"dir_strategy", "dir_operations"}
    recent = client.get("/api/v1/board/status").json().get("recent_directives", [])
    assert any(x.get("director_inputs") for x in recent)     # the deliberation persisted


def test_organism_governs_native_path_and_cascade_tempo(client):
    # §6×§8 (W278) — the native path re-joined the living organism: repeated model failures open
    # the self-healing circuit breaker (the router then skips honestly) and raise immune threat;
    # and the cascade's homeostatic posture is BEHAVIORAL — honest demand (~22 calls, not 8) is
    # reported, and the granted parallelism decides whether the C-Suite runs concurrently.
    from agentic_core.ai.native.orchestrator import _organism_report, _breaker_open
    import uuid as _uuid
    m = f"w278-{_uuid.uuid4().hex[:6]}"
    assert _breaker_open(m) is False
    for _ in range(6):
        _organism_report(m, False)
    assert _breaker_open(m) is True                       # failures opened the breaker
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w278 organism tempo contract", "domain": "enterprise"}).json()
    ha = r["homeostasis_adaptation"]
    assert ha["demand_nodes_reported"] >= 20              # honest demand, not the old 8
    assert ha["csuite_concurrent"] == (ha["granted_parallel"] > 1)   # posture IS behavior
    assert len(r["level_2_csuite"]) == 5 and len(r["level_3_coe"]) == 5
    # under granted headroom the officers genuinely run concurrently (same code path, bounded)
    from unittest.mock import patch
    from agentic_core.ai.native.homeostasis import homeostasis
    real = homeostasis.assess
    with patch.object(homeostasis, "assess",
                      side_effect=lambda **kw: {**real(**kw), "max_parallel": 3}):
        r2 = client.post("/api/v1/swarm/cascade", json={
            "mission": "w278 concurrent contract", "domain": "enterprise"}).json()
    assert r2["homeostasis_adaptation"]["csuite_concurrent"] is True
    assert len(r2["level_2_csuite"]) == 5 and len(r2["appraisals"]) == 6


def test_native_memory_genuinely_used(client):
    # §6 (W277) — the native memory is USED, not ceremonial: retrieval is scored token-overlap
    # (the old whole-prompt substring match never matched a real prompt), irrelevant memories are
    # excluded, the store is capped (most recent kept), and the gateway injects recall with an
    # HONEST label telling the model exactly what the lines are.
    from agentic_core.ai.memory import memory
    memory.add_memory("User: plan a halal meal-kit delivery venture in London | "
                      "AI: certification and cold-chain logistics first")
    memory.add_memory("User: what is the capital of France | AI: Paris")
    r = memory.query_memory("design the halal meal delivery launch with certification steps")
    assert r and "halal" in r[0].lower()                      # scored recall genuinely fires
    assert all("France" not in x for x in r)                  # irrelevant excluded
    assert memory.query_memory("unrelated quantum zebra blockchain") == []   # no false recall
    assert len(memory._load()) <= memory.MAX_MEMORIES         # the store is capped
    from agentic_core.ai.gateway import ModelGateway
    aug = ModelGateway()._augment("halal meal delivery certification plan")
    assert aug.startswith("[native memory recall")            # honest provenance label
    assert "use only if relevant" in aug


def test_owned_model_lifecycle(client):
    # §6 (W276) — the owned-model registry is a managed ESTATE, not a static enumeration:
    # EVALUATE runs honest probes (under AI_DISABLE_LOCAL the target cannot serve → can_serve
    # False and score None — never fabricated), PROMOTE requires genuine discovery (409 otherwise),
    # RETIRE/REINSTATE persist and drive the active estate, and every transition seals to the UEG.
    lc = client.get("/api/v1/native-ai/lifecycle").json()
    assert "effective_default" in lc and isinstance(lc["active_estate"], list)
    ev = client.post("/api/v1/native-ai/lifecycle/evaluate", json={"model": "llama3.2"}).json()
    assert ev["can_serve"] is False and ev["score"] is None      # honest under AI_DISABLE_LOCAL
    assert len(ev["probes"]) == 3 and all(p["served_by"] for p in ev["probes"])
    assert client.post("/api/v1/native-ai/lifecycle/promote",
                       json={"model": "llama3.2"}).status_code == 409   # undiscovered → refused
    rt = client.post("/api/v1/native-ai/lifecycle/retire", json={"model": "llama3.2"}).json()
    assert "llama3.2" in rt["retired"]
    ri = client.post("/api/v1/native-ai/lifecycle/reinstate", json={"model": "llama3.2"}).json()
    assert "llama3.2" not in ri["retired"]
    lc2 = client.get("/api/v1/native-ai/lifecycle").json()
    assert lc2["evaluations"], "the evaluation did not persist"
    events = client.get("/api/v1/gaas/ueg/events?limit=200").json()["events"]
    kinds = [e.get("data", {}).get("type", "") for e in events]
    assert sum(1 for k in kinds if k.startswith("native_ai.model.")) >= 3   # transitions sealed


def test_native_learning_loop_closed(client):
    # §6 (W275) — the learning loop is CLOSED, not one-way exile: model scores are RECENCY-WINDOWED
    # (recovery inside the window is possible), the router POSITIVELY selects the measured-best
    # owned model (not merely avoiding failures), a long-untried demoted model earns a probation
    # retry (exile is never permanent), the run's REAL QMS verdict feeds routing as a
    # model_quality row, and the apex Board accrues operational rows like every other tier.
    from agentic_core.api.operational_excellence import record_outcome, model_health, _load as _ops
    from agentic_core.ai.native.orchestrator import _reorder_by_health
    import uuid as _uuid
    a, b = f"ollama:w275a-{_uuid.uuid4().hex[:4]}", f"ollama:w275b-{_uuid.uuid4().hex[:4]}"
    for i in range(6):
        record_outcome("model_attempt", "model:t", served_by=a, success=True, duration_ms=900)
        record_outcome("model_attempt", "model:t", served_by=b, success=(i == 0), duration_ms=400)
    order = _reorder_by_health([b, a, "native"])
    assert order[0] == a and order[-1] == b            # positive selection + windowed demotion
    for _ in range(40):                                # b recovers INSIDE the window
        record_outcome("model_attempt", "model:t", served_by=b, success=True, duration_ms=400)
    assert _reorder_by_health([b, a, "native"])[0] == b   # recovery is possible — no permanent exile
    h = model_health()
    assert h[b]["window_runs"] <= 40 and h[b]["success_rate"] >= 0.9 and h[b]["last_at"]
    # the cascade's REAL QMS verdict feeds routing…
    r = client.post("/api/v1/swarm/cascade", json={
        "mission": "w275 quality loop contract", "domain": "enterprise"}).json()
    mq = [x for x in _ops() if x["kind"] == "model_quality" and x.get("ref") == r["run_id"]]
    assert mq and mq[0]["success"] == bool(r["quality"].get("qms_gate_passed"))
    # …and the apex Board accrues operational rows like every other tier
    client.post("/api/v1/board/chief/instruct", json={"instruction": "w275 board rows contract"})
    assert any(x["kind"] == "ai_call" and str(x["resource"]).startswith("agent:board")
               for x in _ops())


def test_composition_runs_persist_feed_selection_and_move_the_plan(client):
    # §7×§5×§6 (W274) — a composition run is a first-class event: it PERSISTS (queryable history),
    # every real facility run accrues its own operational-excellence row (fabric:<resource> — measured
    # facility performance feeds selection), and a run bound to a living-plan objective writes a
    # review back + advances planned→in_progress ONLY on a QMS-passed run (W266 semantics, never
    # auto-done, a failed gate never advances).
    import uuid as _uuid
    scope = f"w274-{_uuid.uuid4().hex[:8]}"
    from agentic_core.api.business_plan import parse_objective_lines, _load as _bpl, _save as _bps
    plan = _bpl(scope)
    plan.setdefault("objectives", []).extend(
        parse_objective_lines("Deliver the W274 pilot | pilot live | next review | AI CEO"))
    _bps(plan)
    oid = _bpl(scope)["objectives"][-1]["id"]
    comp = client.post("/api/v1/resources/compose", json={
        "name": "w274 delivery rig", "usage_area": "synthesis",
        "resource_ids": ["petri_dish"], "config": {}}).json()
    r = client.post(f"/api/v1/resources/compositions/{comp['id']}/run", json={
        "objective": "deliver the pilot", "objective_id": oid, "scope": scope}).json()
    assert r["run_id"].startswith("cr-")
    pb = r["plan_binding"]
    obj = next(o for o in _bpl(scope)["objectives"] if o["id"] == oid)
    if pb["result"] == "review_written":                       # the QMS gate passed this run
        assert pb["advanced"] is True and obj["status"] == "in_progress"
        assert obj["reviews"][-1]["composition_run"]["run_id"] == r["run_id"]
    else:                                                      # honest: a failed gate never advances
        assert pb["result"] == "qms_failed_no_advance" and obj["status"] == "planned"
    runs = client.get("/api/v1/resources/compositions/runs").json()["runs"]
    assert runs[0]["run_id"] == r["run_id"]                    # the run persisted, newest first
    assert [x["resource"] for x in runs[0]["real_resources"]] == ["petri_dish"]
    ops = client.get("/api/v1/operations/rankings").json()["rankings"]
    assert any(str(x["resource"]) == "fabric:petri_dish" for x in ops)   # facility outcomes accrued
    client.delete(f"/api/v1/resources/compositions/{comp['id']}")


def test_every_generated_vsb_carries_board_and_economy(client):
    # §3.3 invariant (Living Plan, bold): "Every generated VSB carries its own Board + a Chief that is
    # the digital twin of its owner" — plus a living economy in its legal form, living-entity
    # registration, and a seeded business plan. Previously only Genesis /establish delivered this; the
    # SSE /vsb/spawn and Studio spawn paths produced governance-orphaned entities. Assert ALL paths.
    import re as _re
    # 1) Studio spawn (non-streaming)
    s = client.post("/api/v1/studio/vsb/spawn", json={
        "solution_name": "InvariantCo", "challenge": "invariant check", "realm": "enterprise",
        "domain": "enterprise", "project_id": "inv-1"}).json()
    assert s.get("has_board") is True
    assert (s.get("economy") or {}).get("entity_type")     # living economy attached
    assert s.get("living")                                  # registered as a living entity
    # 2) SSE /vsb/spawn cascade — the stream emits a governance event and the persisted entity is enriched
    r = client.post("/api/v1/vsb/spawn", json={
        "challenge": "invariant check spawn", "domain": "enterprise", "entity_type": "waqf_ltd_hybrid"})
    assert r.status_code == 200 and '"governance"' in r.text
    m = _re.search(r'"vsb_id": "(vsb-[a-f0-9]+)"', r.text)
    assert m, "spawn stream did not announce a vsb_id"
    ent = client.get(f"/api/v1/vsb/{m.group(1)}").json()
    ent = ent.get("entity", ent)
    assert ent.get("board"), "spawned VSB has no Board (invariant broken)"
    assert (ent.get("economy") or {}).get("entity_type") == "waqf_ltd_hybrid"
    assert ent.get("living") and ent.get("business_plan_scope")


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


def test_auth_login(client, monkeypatch):
    """W252 secure bootstrap: there is NO hardcoded admin default — an admin created with a random
    password (ADMIN_PASSWORD unset) is claimed by setting the env var (self-heal at login)."""
    import secrets as _secrets
    from agentic_core.auth import core as auth_core
    if not auth_core._AUTH_DEPS_OK:
        import pytest as _pytest
        _pytest.skip("auth crypto deps not installed")
    # force the bootstrap state: admin with a random password, flagged random-unset
    users = auth_core._load_users()
    users["admin"] = {"user_id": "admin", "username": "admin",
                      "hashed_password": auth_core._pwd_ctx.hash(_secrets.token_urlsafe(24)),
                      "password_source": "random-unset", "role": "admin",
                      "created_at": "2026-01-01T00:00:00Z", "api_keys": []}
    auth_core._save_users(users)
    # the operator sets ADMIN_PASSWORD → login self-heals and issues tokens
    monkeypatch.setenv("ADMIN_PASSWORD", "test-admin-pw-252")
    r = client.post("/api/v1/auth/token", data={"username": "admin", "password": "test-admin-pw-252"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert "access_token" in body and "refresh_token" in body
    assert body["token_type"] == "bearer"
    assert auth_core._get_user("admin").get("password_source") == "env"   # claimed
    # and a second login with the same env password still works (no re-heal needed)
    assert client.post("/api/v1/auth/token",
                       data={"username": "admin", "password": "test-admin-pw-252"}).status_code == 200


def test_auth_login_bad_password(client):
    r = client.post("/api/v1/auth/token", data={
        "username": "admin",
        "password": "wrongpassword",
    })
    assert r.status_code == 401


def test_auth_refresh(client):
    from agentic_core.auth import core as auth_core
    if not auth_core._AUTH_DEPS_OK:
        import pytest as _pytest
        _pytest.skip("auth crypto deps not installed")
    users = auth_core._load_users()
    users["refresh-tester"] = {"user_id": "refresh-tester", "username": "refresh-tester",
                               "hashed_password": auth_core._pwd_ctx.hash("pw-refresh"), "role": "user",
                               "created_at": "2026-01-01T00:00:00Z", "api_keys": []}
    auth_core._save_users(users)
    login = client.post("/api/v1/auth/token", data={
        "username": "refresh-tester", "password": "pw-refresh"
    })
    assert login.status_code == 200, login.text
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
    body = r.json()
    prov = body["ai_provenance"]
    assert prov["posture"] == "in-house-first"
    assert prov["any_external"] is False
    assert set(prov["served_by"]) <= {"native", "ollama"}
    # W109 — continual operational delivery within the LIVING QMS: the journey's buildable + go-to-market
    # delivery is QMS-gated, held to the §10 bar, recorded within the §8 organism (same shared capability).
    qa = body["quality_assurance"]; q = qa["quality"]; bio = qa["biomimetic"]
    assert isinstance(q["qms_gate_passed"], bool) and 0.0 <= q["delivery_coverage"] <= 1.0
    assert q["qms_min_coverage"] == 0.95 and len(q["bar"]) >= 12 and {"verified", "safe"} <= set(q["bar"])
    assert len(bio["layers"]) == 7 and "immune" in bio and bio.get("circadian")


def test_compliance_frameworks(client):
    r = client.get("/api/v1/compliance/frameworks")
    assert r.status_code == 200
    assert r.json()
    # §11 — the federated check flags prohibited content (Halal) and clears clean content
    clean = client.post("/api/v1/compliance/check", json={"subject": "a halal community meal service"}).json()
    assert clean["overall"] == "pass" and clean["compliant"] is True
    haram = client.post("/api/v1/compliance/check", json={"subject": "fund it via riba interest-bearing loans"}).json()
    assert haram["overall"] == "fail" and haram["compliant"] is False
    assert any(v["framework"] == "sharia_halal" and v["status"] == "fail" for v in haram["verdicts"])


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


def test_cockpit_bto_and_ledger_backends(client):
    # Guards the VSB Cockpit's Build-to-Order configurator + Economy ledger backends.
    # 1. BTO components catalogue is offered for selection.
    comp = client.get("/api/v1/bto/components").json()
    ids = {c["id"] for c in comp["components"]}
    assert {"vsb", "csuite", "coe", "products"} <= ids
    # 2. BTO configure assembles a blueprint from exactly the selected components.
    bp = client.post("/api/v1/bto/configure",
                     json={"entity_name": "Cockpit Test Co", "components": ["vsb", "csuite", "coe"], "product_resources": []}).json()
    assert bp["blueprint_id"] and bp["component_count"] == 3
    assert set(bp["components"].keys()) == {"vsb", "csuite", "coe"}
    # 3. Economy ledger for an established VSB is virtual WST with a balances breakdown (honest, no real money).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "ledger lock-in", "domain": "care", "owner_id": "pytest"}).json()
    client.post("/api/v1/economy/cycle", json={"vsb_id": est["vsb_id"]})   # seed a cycle so the ledger has entries
    led = client.get(f"/api/v1/economy/ledger/{est['vsb_id']}").json()
    assert led["currency"] == "WST (virtual)"
    assert "balances" in led and led.get("total_revenue", 0) >= 0


def test_resource_compose(client):
    r = client.post("/api/v1/resources/compose",
                    json={"name": "test-composition", "resource_ids": ["genesis"]})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "test-composition"
    assert len(body["resources"]) >= 1
    # W111 — a committed configuration is modelled + QMS-gated + document-controlled under the QMS
    assert body["model"]["pipeline"] and isinstance(body["commit_ready"], bool)
    assert body["quality_assurance"]["quality"]["document_controlled"] is True


def test_resource_compose_model_and_simulate_before_commit(client):
    # §7 — the platform MODELS + SIMULATES a configuration BEFORE commit (user design control), gated by
    # the living QMS; nothing is saved by the preview, and usage-area incompatibility blocks commit.
    sim = client.post("/api/v1/resources/compose/simulate",
                      json={"name": "concept-rig", "resource_ids": ["bdp", "ddpie", "genesis"],
                            "usage_area": "design"}).json()
    assert sim["saved"] is False
    m = sim["model"]
    assert m["pipeline"] and m["combined_capabilities"] and m["usage_area_supported_by_all"] is True
    q = sim["simulation"]["quality"]
    assert isinstance(q["qms_gate_passed"], bool) and len(q["bar"]) >= 12
    assert sim["simulation"]["biomimetic"]["layers"] and sim["commit_ready"] is True
    # an incompatible selection (gaas_v5 supports governance/delivery/evolution, not 'design') is caught
    bad = client.post("/api/v1/resources/compose/simulate",
                      json={"name": "bad", "resource_ids": ["bdp", "gaas_v5"], "usage_area": "design"}).json()
    assert len(bad["model"]["incompatibilities"]) == 1 and bad["model"]["usage_area_supported_by_all"] is False
    assert bad["commit_ready"] is False
    # user design control over PARAMETER VALUES: setting a param removes it from unset_params (§7)
    cfg = client.post("/api/v1/resources/compose/simulate",
                      json={"name": "cfg", "resource_ids": ["bdp"], "usage_area": "synthesis",
                            "config": {"bdp": {"challenge": "reduce food waste"}}}).json()
    assert "challenge" not in (cfg["model"]["unset_params"].get("bdp") or [])
    assert cfg["resources"][0]["config"]["challenge"] == "reduce food waste"
    # the preview saved nothing; empty/unknown selections are rejected
    assert client.post("/api/v1/resources/compose/simulate", json={"name": "x", "resource_ids": []}).status_code == 400
    assert client.post("/api/v1/resources/compose/simulate", json={"name": "x", "resource_ids": ["nope"]}).status_code == 400


def test_resource_composition_run_on_native_swarm(client):
    # §7↔§6↔§5 — a committed configuration is RERUNNABLE on Workstation's OWN native swarm: each composed
    # resource (incl. the §5 org-cascade resource) becomes a stage, the user's reconfigured params feed in,
    # it runs in-house-first, and the combined run is QMS-gated + document-controlled (§10/§8).
    # §5 org-structure design control is reachable through the §7 fabric: the org resource exposes
    # csuite_roles (which C-Suite officers) as a reconfigurable parameter.
    org_res = client.get("/api/v1/resources/vsb_org_swarm").json()
    assert "csuite_roles" in org_res["reconfigurable_params"]
    comp = client.post("/api/v1/resources/compose",
                       json={"name": "run-rig", "resource_ids": ["bdp", "vsb_org_swarm"],
                             "usage_area": "commercialisation",
                             "config": {"bdp": {"challenge": "a halal meal service"},
                                        "vsb_org_swarm": {"csuite_roles": "CSO, CFO, Policy"}}}).json()
    cid = comp["id"]
    # the user-designed C-Suite is carried in the saved configuration (and no longer "unset")
    org_cfg = next(r for r in comp["resources"] if r["id"] == "vsb_org_swarm")["config"]
    assert org_cfg["csuite_roles"] == "CSO, CFO, Policy"
    assert "csuite_roles" not in (comp["model"]["unset_params"].get("vsb_org_swarm") or [])
    run = client.post(f"/api/v1/resources/compositions/{cid}/run",
                      json={"objective": "Launch a halal community meal service"}).json()
    assert run["posture"] == "in-house-first" and len(run["trace"]) == 2
    assert run["any_external"] is False                       # ran on OWNED native resources (§6)
    assert all(t["served_by"] in ("native", "ollama") for t in run["trace"])
    assert run["final"]                                       # produced a combined pipeline result
    q = run["quality_assurance"]["quality"]                   # QMS-gated + document-controlled (§10/§8)
    assert isinstance(q["qms_gate_passed"], bool) and q["document_controlled"] is True
    # unknown composition is a 404
    assert client.post("/api/v1/resources/compositions/nope/run", json={}).status_code == 404


def test_incubator_parameterised_evolution(client):
    # §7 Reactor — the Incubator runs a parameterised Temperature/Mutation/Iteration evolution loop, and
    # the fabric exposes those as user design control.
    r = client.post("/api/v1/incubator/evolve",
                    json={"name": "pytest evolve", "base_prompt": "a one-line pitch for a halal meal service",
                          "domain": "enterprise", "variants": 3,
                          "temperature": 0.8, "mutation": 0.6, "iterations": 2}).json()
    assert r["generations_run"] == 2                         # the Iteration loop ran 2 generations
    assert r["variants_evaluated"] == 3 and len(r["leaderboard"]) >= 2
    assert r["winner"]["rank"] == 1 and r["winner"]["response"]
    # iterations are capped (1..4); a single-generation run is the default
    capped = client.post("/api/v1/incubator/evolve",
                         json={"name": "x", "base_prompt": "a tagline", "variants": 2, "iterations": 9}).json()
    assert capped["generations_run"] == 4
    # the §7 fabric surfaces the parameterised loop as reconfigurable params (user design control)
    res = client.get("/api/v1/resources/incubator").json()
    assert {"temperature", "mutation", "iterations"} <= set(res["reconfigurable_params"])


def test_reactor_experimentation_whatif(client):
    # §7 Reactor — Experimentation: project + compare outcomes across user-defined what-if scenarios,
    # in-house, QMS-gated + document-controlled (§10/§8).
    r = client.post("/api/v1/reactor/experiment",
                    json={"subject": "a halal meal-service pricing model", "domain": "enterprise",
                          "scenarios": ["What if we cut price 20%?", "What if we add a subscription tier?"]}).json()
    assert r["scenarios_run"] == 2 and len(r["outcomes"]) == 2
    assert all(o["outcome"] and o["scenario"] for o in r["outcomes"]) and r["comparison"]
    assert r["ai_provenance"]["any_external"] is False        # ran on OWNED resources (§6)
    assert r["quality_assurance"]["quality"]["document_controlled"] is True
    # at least one scenario is required
    assert client.post("/api/v1/reactor/experiment", json={"subject": "x", "scenarios": []}).status_code == 400
    # the §7 fabric exposes the Experimentation resource (user design control)
    res = client.get("/api/v1/resources/experimentation").json()
    assert res["type"] == "experimentation" and "scenarios" in res["reconfigurable_params"]


def test_reactor_studio_visual_analytics(client):
    # §7 Reactor — Studio: 2D/3D visual analytics over a REAL series — deterministic stats (never invented),
    # in-house insight, QMS-gated + document-controlled.
    r = client.post("/api/v1/reactor/studio",
                    json={"title": "signups", "chart_type": "bar",
                          "series": [{"label": "Q1", "value": 120}, {"label": "Q2", "value": 180},
                                     {"label": "Q3", "value": 150}, {"label": "Q4", "value": 240}]}).json()
    a = r["analytics"]
    assert r["dimensions"] == 2 and r["chart_type"] == "bar"
    assert a["count"] == 4 and a["total"] == 690 and a["mean"] == 172.5
    assert a["max"]["label"] == "Q4" and a["max"]["value"] == 240 and a["range"] == 120
    assert r["ai_provenance"]["any_external"] is False         # in-house insight (§6)
    assert r["quality_assurance"]["quality"]["document_controlled"] is True
    # a z magnitude makes it a 3D scatter
    r3 = client.post("/api/v1/reactor/studio",
                     json={"title": "risk-reward", "chart_type": "scatter",
                           "series": [{"label": "A", "value": 3, "z": 10}, {"label": "B", "value": 7, "z": 4}]}).json()
    assert r3["dimensions"] == 3 and r3["chart_type"] == "scatter"
    # at least one point required; the §7 fabric exposes the Studio resource
    assert client.post("/api/v1/reactor/studio", json={"title": "x", "series": []}).status_code == 400
    assert client.get("/api/v1/resources/studio").json()["type"] == "studio"


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
    # 1. Chief sets the plan — incl. the Chief-owned opening (Executive Summary · Concept · Vision)
    r = client.post("/api/v1/business-plan/set",
                    json={"scope": scope, "executive_summary": "ES", "concept": "C",
                          "mission": "M", "vision": "V", "strategy": "S"})
    assert r.status_code == 200
    body = r.json()
    assert body["mission"] == "M"
    assert body["executive_summary"] == "ES" and body["concept"] == "C" and body["vision"] == "V"
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


def test_business_plan_living_roadmap(client):
    # The Chief delivers the plan via Strategy AND a LIVING roadmap — time-phased from the objectives,
    # recomputed each read so it tracks progress (no fabrication; derived only from real objectives).
    import uuid
    scope = f"pytest-rm-{uuid.uuid4().hex[:8]}"
    client.post("/api/v1/business-plan/set", json={"scope": scope, "mission": "M", "vision": "V", "strategy": "S"})
    client.post("/api/v1/business-plan/objective", json={"scope": scope, "title": "Phase A obj", "timeline": "Q3 2026"})
    o2 = client.post("/api/v1/business-plan/objective", json={"scope": scope, "title": "Phase B obj", "timeline": "Q4 2026"}).json()
    client.post(f"/api/v1/business-plan/objective/{o2['id']}/review", json={"scope": scope, "progress_pct": 50})
    rm = client.get("/api/v1/business-plan/roadmap", params={"scope": scope}).json()
    assert rm["living"] is True and rm["phase_count"] == 2
    assert {"Q3 2026", "Q4 2026"} <= {p["timeline"] for p in rm["phases"]}
    assert rm["current_phase"] == "Q3 2026" and 0 < rm["overall_progress_pct"] < 100
    # integrated into the main plan response (the roadmap is part of the living business plan)
    bp = client.get("/api/v1/business-plan", params={"scope": scope}).json()
    assert bp["roadmap"]["living"] is True


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
    # The VSB's Chief-owned plan opens with Executive Summary · Concept · Vision, seeded from Genesis (W92)
    assert "VSB IDBO established to solve" in bp["executive_summary"]
    assert bp["concept"] and bp["vision"]


def test_vsb_repo_generation(client):
    # §13 — the VSB IDBO Entity Repository: scaffold a coherent, version-controlled repo from an established
    # VSB, on the native fabric, QMS-gated + compliance-screened + document-controlled. web/webapp/mobile
    # are HONEST scaffolds (later increments), never claimed as built apps.
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "a halal community meal service", "domain": "care", "owner_id": "pytest"})
    vid = est.json()["vsb_id"]
    m = client.post(f"/api/v1/vsb/{vid}/repo").json()
    assert m["file_count"] >= 8 and m["total_bytes"] > 0
    tree = set(m["tree"])
    assert {"README.md", "BUSINESS_PLAN.md", "ORGANISATION.md", "genome.json",
            "web/index.html", "webapp/README.md", "mobile/manifest.webmanifest"} <= tree
    q = m["quality_assurance"]["quality"]
    assert q["qms_gate_passed"] is True and q["document_controlled"] is True          # §10 + QMS-owned DCMS
    assert q["compliance"]["overall"] in ("pass", "review", "fail")                   # §11 screened
    # the integrated surfaces are present + HONESTLY labelled as scaffolds (no fabricated built apps)
    surf = m["integrated_surfaces"]
    assert "scaffold" in surf["website"].lower() and "scaffold" in surf["mobile"].lower()
    # GET retrieves the manifest; an unknown VSB is a 404
    assert client.get(f"/api/v1/vsb/{vid}/repo").json()["file_count"] == m["file_count"]
    assert client.post("/api/v1/vsb/nope-xyz-404/repo").status_code == 404


def test_vsb_website_generation(client):
    # §13 (D1 increment 2) — the integrated Website: real multi-page static HTML/CSS generated in-house
    # from the entity, written into the repo's web/, QMS-gated + compliance-screened + document-controlled;
    # the pages are served as real HTML (known pages only — no path traversal).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "a halal community meal service", "domain": "care", "owner_id": "pytest"})
    vid = est.json()["vsb_id"]
    m = client.post(f"/api/v1/vsb/{vid}/website").json()
    assert m["kind"] == "static_website" and m["page_count"] == 3
    paths = {p["path"] for p in m["pages"]} | {a["path"] for a in m["assets"]}
    assert {"web/index.html", "web/about.html", "web/solution.html", "web/styles.css"} <= paths
    q = m["quality_assurance"]["quality"]
    assert q["qms_gate_passed"] is True and q["document_controlled"] is True
    assert q["compliance"]["overall"] in ("pass", "review", "fail")
    assert m["ai_provenance"]["any_external"] is False                 # copy generated in-house (§6)
    # generated pages are served as real HTML; styles too; unknown page is 404 (no traversal)
    pg = client.get(f"/api/v1/vsb/{vid}/website/page/index")
    assert pg.status_code == 200 and pg.text.strip().lower().startswith("<!doctype html") and "<nav>" in pg.text
    assert client.get(f"/api/v1/vsb/{vid}/website/page/styles").status_code == 200
    assert client.get(f"/api/v1/vsb/{vid}/website/page/evil").status_code == 404
    assert client.get(f"/api/v1/vsb/{vid}/website").json()["page_count"] == 3
    assert client.post("/api/v1/vsb/nope-xyz-404/website").status_code == 404


def test_vsb_webapp_generation(client):
    # §13 (D1 increment 3) — the interactive Web app: a real client-side app (HTML + CSS + vanilla JS +
    # data.json) data-driven from the entity, written into the repo's webapp/, QMS-gated + compliance-
    # screened + document-controlled; the files are served so the app runs in-browser (known files only).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "a halal community meal service", "domain": "care", "owner_id": "pytest"})
    vid = est.json()["vsb_id"]
    m = client.post(f"/api/v1/vsb/{vid}/webapp").json()
    assert m["kind"] == "client_web_app" and m["interactive"] is True
    paths = {f["path"] for f in m["files"]}
    assert {"webapp/index.html", "webapp/app.js", "webapp/data.json", "webapp/styles.css"} <= paths
    q = m["quality_assurance"]["quality"]
    assert q["qms_gate_passed"] is True and q["document_controlled"] is True
    assert q["compliance"]["overall"] in ("pass", "review", "fail")
    # served as real, runnable client-side files; data-driven; known files only (no traversal)
    idx = client.get(f"/api/v1/vsb/{vid}/webapp/page/index")
    assert idx.status_code == 200 and 'src="app.js"' in idx.text
    js = client.get(f"/api/v1/vsb/{vid}/webapp/page/app.js")
    assert js.status_code == 200 and js.headers["content-type"].startswith("text/javascript")
    assert "function render" in js.text and "data.json" in js.text
    dj = client.get(f"/api/v1/vsb/{vid}/webapp/page/data.json").json()
    assert dj["name"] and "business_plan" in dj and isinstance(dj["resources"], list)
    assert client.get(f"/api/v1/vsb/{vid}/webapp/page/evil").status_code == 404
    assert client.get(f"/api/v1/vsb/{vid}/webapp").json()["interactive"] is True
    assert client.post("/api/v1/vsb/nope-xyz-404/webapp").status_code == 404


def test_vsb_mobile_pwa_generation(client):
    # §13 (D1 increment 4) — the Phone app: a real installable PWA (manifest + service worker + icon +
    # mobile-first interactive app) generated from the entity into the repo's mobile/, QMS-gated +
    # compliance-screened + document-controlled; served with correct content-types so it runs in-browser.
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "a halal community meal service", "domain": "care", "owner_id": "pytest"})
    vid = est.json()["vsb_id"]
    m = client.post(f"/api/v1/vsb/{vid}/mobile").json()
    assert m["kind"] == "installable_pwa" and m["installable"] is True and m["offline_capable"] is True
    paths = {f["path"] for f in m["files"]}
    assert {"mobile/index.html", "mobile/app.js", "mobile/manifest.webmanifest", "mobile/sw.js",
            "mobile/icon.svg", "mobile/styles.css", "mobile/data.json"} <= paths
    q = m["quality_assurance"]["quality"]
    assert q["qms_gate_passed"] is True and q["document_controlled"] is True
    assert q["compliance"]["overall"] in ("pass", "review", "fail")
    # served PWA files with correct content-types; manifest + SW registration present
    idx = client.get(f"/api/v1/vsb/{vid}/mobile/page/index")
    assert idx.status_code == 200 and 'rel="manifest"' in idx.text and "serviceWorker" in idx.text
    man = client.get(f"/api/v1/vsb/{vid}/mobile/page/manifest.webmanifest")
    assert man.headers["content-type"].startswith("application/manifest+json")
    assert man.json()["display"] == "standalone" and man.json()["icons"]
    sw = client.get(f"/api/v1/vsb/{vid}/mobile/page/sw.js")
    assert sw.status_code == 200 and "caches.open" in sw.text
    assert client.get(f"/api/v1/vsb/{vid}/mobile/page/icon.svg").headers["content-type"].startswith("image/svg+xml")
    # known files only; manifests retrievable; unknown VSB is a 404
    assert client.get(f"/api/v1/vsb/{vid}/mobile/page/evil").status_code == 404
    assert client.get(f"/api/v1/vsb/{vid}/mobile").json()["installable"] is True
    assert client.post("/api/v1/vsb/nope-xyz-404/mobile").status_code == 404


def test_vsb_board_pack(client):
    # §17.3 — the Living Business System's on-demand Board Pack: assembled FRESH from the VSB's live data
    # (Constitutional · Strategic · Action · Operational) + an in-house AI-CEO narrative, QMS-gated +
    # compliance-screened + DCS-registered (document-controlled via the QMS-owned DCMS).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "a halal community meal service", "domain": "care", "owner_id": "pytest"})
    vid = est.json()["vsb_id"]
    m = client.post(f"/api/v1/vsb/{vid}/board-pack").json()
    assert m["kind"] == "board_pack"
    assert set(m["layers"]) == {"constitutional", "strategic", "action_plan", "operational"}
    assert all(k in m["layers"]["constitutional"] for k in ("mission", "vision", "values"))
    assert m["narrative"]
    assert m["dcs_registered"] is True and isinstance(m["dcs_hash"], str) and len(m["dcs_hash"]) == 128
    q = m["quality_assurance"]["quality"]
    assert q["qms_gate_passed"] is True and q["compliance"]["overall"] in ("pass", "review", "fail")
    assert m["ai_provenance"]["any_external"] is False
    # GET latest + history; unknown VSB is a 404
    assert client.get(f"/api/v1/vsb/{vid}/board-pack").json()["dcs_hash"] == m["dcs_hash"]
    assert client.get(f"/api/v1/vsb/{vid}/board-packs").json()["total"] >= 1
    assert client.post("/api/v1/vsb/nope-xyz-404/board-pack").status_code == 404
    assert client.get("/api/v1/vsb/nope-xyz-404/board-pack").status_code == 404


def test_vsb_review_gates_mode3(client):
    # §17.4 Mode 3 — optional human review gates at any Concept→Commercialisation stage (set in the VSB
    # genome). Configurable per-VSB; each config + decision is append-only DCS-audited (§17.5).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "a halal community meal service", "domain": "care", "owner_id": "pytest"})
    vid = est.json()["vsb_id"]
    g0 = client.get(f"/api/v1/vsb/{vid}/review-gates").json()
    assert g0["mode"].startswith("Mode 3") and g0["stages"] == [] and len(g0["lifecycle"]) == 8
    # set gates on two stages (genome config) — DCS-registered
    s = client.post(f"/api/v1/vsb/{vid}/review-gates", json={"stages": ["design", "commercialise"]}).json()
    assert set(s["stages"]) == {"design", "commercialise"} and isinstance(s["dcs_hash"], str) and len(s["dcs_hash"]) == 128
    assert client.post(f"/api/v1/vsb/{vid}/review-gates", json={"stages": ["nope"]}).status_code == 400
    # a gated stage is pending + blocks progress; a non-gated stage does not gate
    st = client.get(f"/api/v1/vsb/{vid}/review-gates/design").json()
    assert st["gated"] is True and st["status"] == "pending" and st["blocks_progress"] is True
    assert client.get(f"/api/v1/vsb/{vid}/review-gates/build").json()["status"] == "not_gated"
    # human approves the design gate -> approved, no longer blocks (decision DCS-audited)
    d = client.post(f"/api/v1/vsb/{vid}/review-gates/design/decision", json={"decision": "approve", "note": "ok"}).json()
    assert d["status"] == "approved" and d["blocks_progress"] is False and len(d["dcs_hash"]) == 128
    assert client.get(f"/api/v1/vsb/{vid}/review-gates/design").json()["status"] == "approved"
    # deciding on a non-gated stage is rejected; unknown VSB/stage are 404
    assert client.post(f"/api/v1/vsb/{vid}/review-gates/build/decision", json={"decision": "approve"}).status_code == 400
    assert client.get("/api/v1/vsb/nope-xyz-404/review-gates").status_code == 404
    assert client.get(f"/api/v1/vsb/{vid}/review-gates/zzz").status_code == 404


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
    """The name promised more than the test checked.

    W401 - it asserted only the currency string and a boolean type, and passed happily while the
    endpoint reported the PLATFORM capital fund as every user's personal balance: any id, including
    ones with no account, came back with the same 10,000,000 WST. A test called "no_fabrication"
    must actually check the number it is named after.
    """
    r = client.get("/api/v310/payments/wallet/pytest")
    assert r.status_code == 200
    b = r.json()
    assert b["currency"] == "WST (virtual)"
    assert isinstance(b["stripe_configured"], bool)

    # An id with no ledger must NOT be handed a balance.
    ghost = client.get("/api/v310/payments/wallet/definitely-no-such-user-xyz").json()
    assert ghost["known_user"] is False, ghost
    assert ghost["wst_balance"] is None, ghost

    # Two different unknown ids must not share one balance — that was exactly the bug.
    other = client.get("/api/v310/payments/wallet/another-no-such-user-abc").json()
    assert other["wst_balance"] is None, other

    # The platform pool may be reported, but never under a name that reads as the user's money.
    assert "platform_capital_fund_available" in ghost
    assert ghost.get("wst_available") is None


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
    # Build-to-Order yields first-class operational delivery resources + the products/services catalogue
    assert b["operational_delivery_resources"]                            # the resources assembled
    cat = b["products_services_catalogue"]
    assert cat and all(p.get("name") for p in cat)                       # real catalogue items
    assert not any(str(p.get("name", "")).startswith(("_", ".")) for p in cat)  # no __pycache__/dotdirs leaked
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


def test_established_vsb_gets_own_native_swarm(client):
    # W2: every established VSB is given its OWN reconfigurable native swarm (its in-house
    # delivery org), persisted, filed under the VSB in the fabric, and runnable on owned resources.
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "pytest per-vsb swarm", "domain": "care", "owner_id": "pytest"}).json()
    vid = est["vsb_id"]
    ent = client.get(f"/api/v1/vsb/{vid}").json()
    ns = ent["native_swarm"]
    assert ns["cascade_id"] and ns["org"] and len(ns["stages"]) >= 3
    # auto-derived name must not leak the native engine's provenance marker
    assert "native structured engine" not in ent["name"].lower()
    # the cascade is filed under THIS vsb in the fabric
    mine = client.get(f"/api/v1/resources/swarm?vsb_id={vid}").json()
    assert any(c["id"] == ns["cascade_id"] for c in mine["cascades"])
    # and runs on OWNED resources only
    run = client.post("/api/v1/resources/swarm/run", json={"swarm_id": ns["cascade_id"]}).json()
    assert run["stages"] == len(ns["stages"])
    assert run["any_external"] is False
    assert all(s["served_by"] in ("native", "ollama") for s in run["trace"])
    # the list surfaces the org flag
    row = next(e for e in client.get("/api/v1/vsb").json()["entities"] if e["vsb_id"] == vid)
    assert row["has_native_swarm"] is True


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


def test_avatar_status_always_online_in_house(client):
    # W3: the avatar runs on the native fabric — it is ALWAYS online regardless of providers.
    r = client.get("/api/v1/avatar/status")
    assert r.status_code == 200
    b = r.json()
    assert b["online"] is True and b["native"] is True and b["posture"] == "in-house-first"


def test_avatar_chat_in_house_provenance(client):
    # W3: a chat turn answers in-house and reports which OWNED resource served it.
    r = client.post("/api/v1/avatar/chat", json={"message": "Summarise my context.", "context": "ceo"})
    assert r.status_code == 200
    b = r.json()
    assert b["response"] and b["served_by"] in ("native", "ollama")
    assert b["is_external"] is False


def test_avatar_chat_grounded_in_vsb(client):
    # W3: when a vsb_id is supplied, the avatar is grounded in that live entity (no error,
    # in-house, and the grounded_in id echoed back).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "avatar grounding test", "domain": "care", "owner_id": "pytest"}).json()
    r = client.post("/api/v1/avatar/chat",
                    json={"message": "What is this venture's mission?", "context": "vsb", "vsb_id": est["vsb_id"]})
    assert r.status_code == 200
    b = r.json()
    assert b["grounded_in"] == est["vsb_id"]
    assert b["is_external"] is False and b["response"]


def test_deliverables_living_lifecycle(client):
    # W4: a living deliverable is produced on the native fabric (in-house), persisted, listed,
    # and is re-runnable / reconfigurable (versioned history).
    types = client.get("/api/v1/deliverables/types").json()
    assert any(t["id"] == "report" for t in types["types"])
    d = client.post("/api/v1/deliverables/produce",
                    json={"type": "report", "title": "pytest deliverable",
                          "brief": "a halal meal service for elderly Londoners", "domain": "care"}).json()
    did = d["id"]
    assert len(d["sections"]) >= 4 and d["content"]
    assert d["living"] is True and len(d["versions"]) == 1
    assert d["ai_provenance"]["is_external"] is False
    assert d["ai_provenance"]["served_by"] in ("native", "ollama")
    assert any(x["id"] == did for x in client.get("/api/v1/deliverables").json()["deliverables"])
    # W108 — continual operational delivery within the LIVING QMS: the produced deliverable is gated by
    # the OWNED QMS, held to the §10 Solution-Quality Bar, recorded within the §8 biomimetic organism.
    qa = d["quality_assurance"]; q = qa["quality"]; bio = qa["biomimetic"]
    assert isinstance(q["qms_gate_passed"], bool) and 0.0 <= q["delivery_coverage"] <= 1.0
    assert q["qms_min_coverage"] == 0.95 and q["qms_non_conformance_rate"] >= 0.0
    assert len(q["bar"]) >= 12 and {"verified", "compliant", "safe", "ranked"} <= set(q["bar"])
    assert len(bio["layers"]) == 7 and {"Genome", "Immune", "Endocrine"} <= set(bio["layers"])
    assert "immune" in bio and bio.get("circadian")
    assert d["versions"][0]["quality_assurance"]["quality"]["qms_gate_passed"] == q["qms_gate_passed"]
    # the list summary surfaces the QMS gate (for the UI badge)
    summ = [x for x in client.get("/api/v1/deliverables").json()["deliverables"] if x["id"] == did][0]
    assert "qms_gate_passed" in summ
    # re-run / reconfigure → appends a new version (living), itself QMS-gated
    r = client.post(f"/api/v1/deliverables/{did}/regenerate", json={"brief": "add a zero-waste angle"}).json()
    assert len(r["versions"]) == 2 and r["brief"] == "add a zero-waste angle"
    assert r["quality_assurance"]["quality"] and r["versions"][1].get("quality_assurance")
    assert client.get("/api/v1/deliverables/nope").status_code == 404
    # the user can EXPORT the living deliverable as a downloadable Markdown document
    exp = client.get(f"/api/v1/deliverables/{did}/export")
    assert exp.status_code == 200 and exp.headers["content-type"].startswith("text/markdown")
    assert "attachment" in exp.headers.get("content-disposition", "")
    assert exp.text.startswith("# ") and "own AI fabric" in exp.text
    assert client.get("/api/v1/deliverables/nope/export").status_code == 404
    # §4.9 — selectable IN-HOUSE export formats are real renders (not faked), bad formats rejected
    fmt_ct = {"html": "text/html", "slides": "text/html", "txt": "text/plain", "json": "application/json"}
    for fmt, ct in fmt_ct.items():
        r = client.get(f"/api/v1/deliverables/{did}/export", params={"format": fmt})
        assert r.status_code == 200 and r.headers["content-type"].startswith(ct), (fmt, r.status_code)
        assert f".{ 'slides.html' if fmt=='slides' else fmt }" in r.headers.get("content-disposition", "")
    assert "<h1>" in client.get(f"/api/v1/deliverables/{did}/export", params={"format": "html"}).text
    assert client.get(f"/api/v1/deliverables/{did}/export", params={"format": "mp4"}).status_code == 400  # never faked
    of = client.get("/api/v1/deliverables/output-formats").json()
    from agentic_core.api.deliverables import (_PDF_OK, _DOCX_OK, _PPTX_OK, _XLSX_OK,
                                               _PNG_OK)   # live iff lib installed
    # Kept as EXACT equality on purpose: this is the honesty guard that no format is advertised as
    # live unless it can actually be produced. W372 added svg (dependency-free, always live) and
    # png (Pillow-gated, exactly like pdf/docx/pptx/xlsx).
    expected = {"md", "html", "slides", "txt", "json", "video-html"}   # video-html live since W264
    expected |= {"svg"}                                               # W372 — no dependency needed
    expected |= {"pdf"} if _PDF_OK else set()
    expected |= {"docx"} if _DOCX_OK else set()
    expected |= {"pptx"} if _PPTX_OK else set()
    expected |= {"xlsx"} if _XLSX_OK else set()
    expected |= {"png"} if _PNG_OK else set()                         # W372
    assert set(of["live_ids"]) == expected
    if _PDF_OK:   # real in-house PDF via fpdf2 (pure-python)
        pr = client.get(f"/api/v1/deliverables/{did}/export", params={"format": "pdf"})
        assert pr.status_code == 200 and pr.headers["content-type"].startswith("application/pdf")
        assert pr.content[:5] == b"%PDF-"
    else:
        assert "pdf" in of["catalogue_not_yet_produced"]
    if _DOCX_OK:   # real in-house Word doc via python-docx (.docx is a zip → PK header)
        dr = client.get(f"/api/v1/deliverables/{did}/export", params={"format": "docx"})
        assert dr.status_code == 200 and "wordprocessingml" in dr.headers["content-type"]
        assert dr.content[:2] == b"PK"
    else:
        assert "docx" in of["catalogue_not_yet_produced"]
    if _PPTX_OK:   # real in-house PowerPoint via python-pptx (.pptx is a zip → PK header)
        ppr = client.get(f"/api/v1/deliverables/{did}/export", params={"format": "pptx"})
        assert ppr.status_code == 200 and "presentationml" in ppr.headers["content-type"]
        assert ppr.content[:2] == b"PK"
    else:
        assert "pptx" in of["catalogue_not_yet_produced"]
    if _XLSX_OK:   # real in-house Excel via openpyxl (.xlsx is a zip → PK header)
        xr = client.get(f"/api/v1/deliverables/{did}/export", params={"format": "xlsx"})
        assert xr.status_code == 200 and "spreadsheetml" in xr.headers["content-type"]
        assert xr.content[:2] == b"PK"
    else:
        assert "xlsx" in of["catalogue_not_yet_produced"]
    assert "mp4" in of["catalogue_not_yet_produced"]   # AV stays catalogue — never faked


def test_operations_learning_loop(client):
    # W5: running a swarm records a real outcome that surfaces in rankings + summary (honest).
    sid = client.post("/api/v1/resources/swarm/define",
                      json={"name": "ops pytest", "stages": [{"role": "a", "instruction": "x"}]}).json()["id"]
    client.post("/api/v1/resources/swarm/run", json={"swarm_id": sid})
    summ = client.get("/api/v1/operations/summary").json()
    assert summ["total_runs"] >= 1 and "swarm_run" in summ["kinds"]
    assert 0.0 <= summ["success_rate"] <= 1.0 and 0.0 <= summ["in_house_rate"] <= 1.0
    ranks = client.get("/api/v1/operations/rankings").json()["rankings"]
    mine = [r for r in ranks if r["resource"] == "swarm:ops pytest"]
    assert mine and mine[0]["runs"] >= 1 and 0.0 <= mine[0]["success_rate"] <= 1.0
    assert client.get("/api/v1/operations/outcomes?kind=swarm_run").json()["total"] >= 1


def test_deliverables_per_vsb_filter(client):
    # A deliverable produced for a VSB is filed under it and retrievable by vsb_id (per-VSB
    # living deliverables, surfaced in the VSBSpawnStudio panel).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "per-vsb deliverable", "domain": "care", "owner_id": "pytest"}).json()
    vid = est["vsb_id"]
    d = client.post("/api/v1/deliverables/produce",
                    json={"type": "brief", "brief": "opportunity brief", "vsb_id": vid}).json()
    assert d["vsb_id"] == vid
    lst = client.get(f"/api/v1/deliverables?vsb_id={vid}").json()
    assert any(x["id"] == d["id"] for x in lst["deliverables"])
    assert all(x.get("vsb_id") == vid for x in lst["deliverables"])   # the filter is honest


def test_orchestrator_adapts_to_model_health(client):
    # The learning APPLICATION: a model resource with a clearly-poor recorded track record is
    # deprioritised below the always-available native floor (so we stop wasting time on it).
    # Native is never demoted; infra-level model_attempt records stay out of the user-facing views.
    from agentic_core.api.operational_excellence import model_health
    from agentic_core.ai.native.orchestrator import _reorder_by_health
    for _ in range(6):
        client.post("/api/v1/operations/record",
                    json={"kind": "model_attempt", "resource": "model:flaky", "served_by": "flaky",
                          "duration_ms": 25000, "success": False})
    h = model_health()
    assert h["flaky"]["runs"] >= 6 and h["flaky"]["success_rate"] < 0.6
    order = _reorder_by_health(["flaky", "native"])
    assert order.index("native") < order.index("flaky")              # flaky demoted below the floor
    assert _reorder_by_health(["native"]) == ["native"]              # native untouched
    # model_attempt records are infra-level — excluded from the user-facing rankings + summary
    assert not any(r["resource"] == "model:flaky" for r in client.get("/api/v1/operations/rankings").json()["rankings"])
    assert "model_attempt" not in client.get("/api/v1/operations/summary").json()["kinds"]
    # the learning surface exposes the poor model as deprioritised
    mh = client.get("/api/v1/operations/model-health").json()
    flaky = next((m for m in mh["models"] if m["name"] == "flaky"), None)
    assert flaky and flaky["deprioritised"] is True


def test_domains_in_house_provenance(client):
    # The WHOLE Domains suite (Law/Science/Care/Education/Religion/Employment) runs AI-mediated
    # responses on Workstation's OWN native fabric and reports in-house provenance (like Forge/Genesis).
    law = client.post("/api/v1/law/analyse",
                      json={"document_text": "A short NDA between two parties.", "analysis_focus": "risk"}).json()
    sci = client.post("/api/v1/science/hypothesis", json={"research_question": "does X reduce Y?"}).json()
    care = client.post("/api/v1/care/handover",
                       json={"patient_summary": "stable", "current_situation": "routine"}).json()
    edu = client.post("/api/v1/education/lesson-plan",
                      json={"subject": "Maths", "topic": "fractions", "level": "KS3"}).json()
    rel = client.post("/api/v1/religion/halal-review",
                      json={"product_name": "Snack", "product_description": "a cereal bar"}).json()
    car = client.post("/api/v1/career/job-search", json={"query": "developer"}).json()
    for r in (law, sci, care, edu, rel, car):
        p = r["ai_provenance"]
        assert p["posture"] == "in-house-first" and p["is_external"] is False
        assert p["served_by"] in ("native", "ollama")


def test_native_engine_web_app_archetypes():
    # The native floor gives website/app/service section types tailored scaffolds (not the bland
    # generic fallback), improving the quality of those living deliverables even with no model.
    from agentic_core.ai.native.engine import native_engine
    prompt = ("Produce a website.\nConcept: a halal meal service for elderly Londoners\nDomain: care\n\n"
              "## Hero\n## Value Proposition\n## Features\n## How It Works\n## Service Overview")
    out = native_engine.generate(prompt, "deliverable:website")
    for sec in ("## Hero", "## Value Proposition", "## Features", "## How It Works", "## Service Overview"):
        seg = out.split(sec)[1].split("##")[0]
        assert "Native structured content for" not in seg   # not the generic fallback
        assert "Structured" in seg                          # a dedicated archetype frame


def test_deliverables_leverage_own_omnimedia(client):
    # The deliverables pipeline LEVERAGES Workstation's own omnimedia factory for its output-format
    # catalogue, and omnimedia is registered as a first-class Resource-Fabric resource (so existing
    # in-house capabilities are surfaced into the unified fabric the swarm/delivery draws from).
    of = client.get("/api/v1/deliverables/output-formats").json()
    from agentic_core.api.deliverables import _PDF_OK, _DOCX_OK, _PPTX_OK, _XLSX_OK
    assert {"md", "html", "slides", "txt", "json"} <= set(of["live_ids"])    # real in-house renders
    assert ("pdf" in of["live_ids"]) == _PDF_OK                              # pdf live iff fpdf2 present
    assert ("docx" in of["live_ids"]) == _DOCX_OK                            # docx live iff python-docx present
    assert ("pptx" in of["live_ids"]) == _PPTX_OK                            # pptx live iff python-pptx present
    assert ("xlsx" in of["live_ids"]) == _XLSX_OK                            # xlsx live iff openpyxl present
    assert "mp4" in of["catalogue_not_yet_produced"]   # AV stays catalogue — never faked
    assert "omnimedia" in of["source"]
    fab = client.get("/api/v1/resources?resource_class=output_media").json()
    assert any(r["id"] == "omnimedia" for r in fab["resources"])


def test_deliverables_binary_export_edge_inputs_no_crash():
    # The binary renderers must NEVER 500 on edge content (control chars / NULL bytes / unicode):
    # openpyxl + python-docx reject control chars, so deliverables._xml_safe strips them. Guards that fix.
    from agentic_core.api import deliverables as D
    assert D._xml_safe("a\x00b\x1fc\x08d") == "abcd"   # control chars stripped; tab/newline kept
    edge = {"id": "t", "title": "T\x00\x07", "type": "report",
            "brief": "b\x1f", "content": "## Sec\x00\nbody \x08 \x1b\n报告 \U0001F4CA — dash"}
    for ok, fn, sig in [(D._PDF_OK, D._pdf_bytes, b"%PDF-"), (D._DOCX_OK, D._docx_bytes, b"PK"),
                        (D._PPTX_OK, D._pptx_bytes, b"PK"), (D._XLSX_OK, D._xlsx_bytes, b"PK")]:
        if not ok:   # the lib may be absent under system-python; CI installs it via requirements
            continue
        out = fn(edge)
        assert isinstance(out, (bytes, bytearray)) and out[:len(sig)] == sig


def test_federation_mesh_surfaced(client):
    # Workstation's OWN federation mesh (agentic_core.mesh, previously 0 importers) is now reachable
    # and a first-class Resource-Fabric resource — honest: single-node peers are flagged simulated.
    m = client.get("/api/v1/mesh/status").json()
    assert m["operational"] is True
    assert "bft" in m["consensus"]["type"].lower()
    assert m["discovery"]["simulated"] is True
    assert "consensus" in m["modules"] and "discovery" in m["modules"]
    fab = client.get("/api/v1/resources?resource_class=federation").json()
    assert any(r["id"] == "federation_mesh" for r in fab["resources"])


def test_mega_project_synthesis_in_house_no_fabrication(client):
    # mega_project surfaced into the fabric, REDONE honestly on the native fabric (the original
    # MegaProjectSynthesizer returned hardcoded "$1.5T valuation / 450% ROI / 98.5% confidence").
    r = client.post("/api/v1/mega-project/synthesise",
                    json={"concept": "a carbon-negative shipping network", "domain": "enterprise"}).json()
    assert len(r["sections"]) >= 5 and r["deliverable"]
    assert r["ai_provenance"]["is_external"] is False
    assert "1.5 Trillion" not in r["deliverable"] and "450%" not in r["deliverable"]  # not fabricated
    fab = client.get("/api/v1/resources?resource_class=process_intelligence").json()
    assert any(x["id"] == "mega_project" for x in fab["resources"])


def test_swarm_cascade_in_house_provenance(client):
    # The FULL VSB org cascade — Chief of the Board (founder's digital twin) -> Board of Directors ->
    # AI CEO -> C-Suite -> Centres of Excellence -> Business Transformation Office -> Build-to-Order
    # (operational delivery resources) -> Products/Services catalogue — runs on the native fabric and
    # reports in-house provenance across EVERY tier.
    r = client.post("/api/v1/swarm/cascade",
                    json={"mission": "launch a halal meal service", "domain": "enterprise"}).json()
    for k in ("level_0_chief_of_board", "level_0b_board_resolution", "level_1_ceo_directive",
              "level_2_csuite", "level_3_coe", "level_4_business_transformation_office",
              "level_5_build_to_order", "products_services_catalogue"):
        assert r.get(k), f"cascade missing tier '{k}'"
    assert r["org_hierarchy"][0] == "Chief of the Board of Directors"
    assert "Build-to-Order" in r["org_hierarchy"] and "Business Transformation Office" in r["org_hierarchy"]
    p = r["ai_provenance"]
    assert p["posture"] == "in-house-first" and p["any_external"] is False
    assert set(p["served_by"]) <= {"native", "ollama"}
    # §5 fine-resolution — each apex tier delivers its specific function
    assert "Strategy" in r["level_0_chief_of_board"] and "Roadmap" in r["level_0_chief_of_board"]
    assert "Action Plan" in r["level_0b_board_resolution"]
    # §5 — the AI CEO INTEGRATES the living management systems (real DCMS document-control of decisions)
    ms = r["management_systems"]
    assert {"bms", "qms", "ems", "dcms"} <= set(ms["integrated"])
    assert all(len(h) == 128 for h in ms["document_control"].values())   # real SHA3-512 versioned artifacts
    assert {"ceo_directive", "board_action_plan", "bto_programme", "build_to_order"} <= set(ms["document_control"])
    # §5 — arms-length Change-Control / constitutional governance over the whole delivery
    assert r["governance"]["arms_length"] is True and r["governance"]["status"] in ("allowed", "blocked", "ungoverned")
    # §6 — verifiable hash-chained provenance for the entire org delivery
    assert r["ueg_hash"] and len(r["ueg_hash"]) == 128
    # §5 — the full specialist C-Suite is selectable (user design control), and EACH officer drives its CoE
    ros = r["csuite_roster"]
    assert ros["each_drives_coe"] is True
    assert {"CSO", "CFO", "CTO", "CPO", "COO", "CIO", "CLO", "Forecasting", "Policy"} <= set(ros["available"])
    assert set(ros["engaged"]) <= set(ros["available"]) and len(ros["engaged"]) >= 3
    for officer in ros["engaged"]:
        assert officer in r["level_2_csuite"]                 # the officer's functional plan
        assert f"{officer} CoE" in r["level_3_coe"]           # and the CoE that officer drives
    # §5 — each tier manages, APPRAISES and DEVELOPS the tier below (arms-length upward appraisal pass)
    appr = r["appraisals"]
    assert {"chief_appraises_board", "board_appraises_ceo", "ceo_appraises_csuite", "bto_appraises_build"} <= set(appr)
    assert all(appr[k] for k in appr)
    # §10 Solution-Quality Bar + continual operational delivery within the LIVING QMS (real gate)
    q = r["quality"]
    assert isinstance(q["qms_gate_passed"], bool) and 0.0 <= q["delivery_coverage"] <= 1.0
    assert q["qms_min_coverage"] == 0.95 and q["qms_non_conformance_rate"] >= 0.0
    assert len(q["bar"]) >= 12 and {"verified", "compliant", "ranked", "safe"} <= set(q["bar"])
    # the QMS document-controls the quality record through its OWNED DCMS (QMS ⊃ DCMS, ISO 9001 §7.5)
    assert isinstance(q.get("quality_record_hash"), str) and len(q["quality_record_hash"]) == 128
    assert q.get("document_controlled") is True
    # §11 — live compliance woven into EVERY delivery (not bolted on): Halal·Legal·Regulatory·EHS·Ethical
    comp = q["compliance"]
    assert isinstance(comp["compliant"], bool) and comp["overall"] in ("pass", "review", "fail")
    assert {v["framework"] for v in comp["verdicts"]} >= {"sharia_halal", "uk_legal", "ehs", "ethical"}
    # §8 — the biomimetic living-organism substrate the cascade runs within (live immune + circadian)
    bio = r["biomimetic"]
    assert len(bio["layers"]) == 7 and {"Genome", "Immune", "Endocrine"} <= set(bio["layers"])
    assert "immune" in bio and bio.get("circadian")


def test_swarm_cascade_user_reconfigurable_org(client):
    # §5 "reconfigurable with user design control": the user chooses which specialist C-Suite officers
    # run (each still drives its own CoE). Honest: only known C-Suite roles are engaged.
    r = client.post("/api/v1/swarm/cascade",
                    json={"mission": "open a community clinic", "domain": "care",
                          "csuite_roles": ["CFO", "Policy", "Forecasting"]}).json()
    assert r["csuite_roster"]["engaged"] == ["CFO", "Policy", "Forecasting"]
    assert set(r["level_2_csuite"]) == {"CFO", "Policy", "Forecasting"}
    assert {"CFO CoE", "Policy CoE", "Forecasting CoE"} <= set(r["level_3_coe"])
    assert r["ai_provenance"]["any_external"] is False        # still fully in-house (§6)


def test_resource_optimizer_surfaced(client):
    # Workstation's own adaptive resource optimiser (agentic_core.optimizer, previously orphaned) is
    # now reachable + a fabric resource; capacity is an honestly-flagged single-node simulated baseline.
    a = client.post("/api/v1/optimizer/allocate",
                    json={"domain": "science", "requirements": {"CPU": 8, "RAM": 2048}, "tier": "standard"}).json()
    assert a["status"] == "SUCCESS" and a["pool_id"] and a["simulated_capacity"] is True
    inv = client.get("/api/v1/optimizer/inventory").json()
    assert inv["simulated"] is True and "compute" in inv["inventory"]
    fab = client.get("/api/v1/resources?resource_class=digital_resource").json()
    assert any(x["id"] == "resource_optimizer" for x in fab["resources"])
    # robustness: STRING requirement values (what a web form / key-value field posts) must NOT 500 —
    # they are coerced to numbers (the engine compares them against capacity).
    s = client.post("/api/v1/optimizer/allocate",
                    json={"domain": "science", "requirements": {"CPU": "8", "RAM": "2048"}, "tier": "standard"})
    assert s.status_code == 200, s.text
    assert s.json()["status"] == "SUCCESS"


def test_collective_truth_consensus_surfaced(client):
    # Workstation's own truth-consensus engine (agentic_core.collective, previously orphaned):
    # reputation-weighted consensus over the SUBMITTED claims — real logic, fabricates nothing.
    r = client.post("/api/v1/collective/consensus", json={"threshold": 0.85, "claims": [
        {"claim": "halal supply is verified", "confidence": 0.95, "reputation": 2.0},
        {"claim": "halal supply is verified", "confidence": 0.9, "reputation": 1.0},
        {"claim": "price is optimal", "confidence": 0.4, "reputation": 1.0}]}).json()
    assert r["claims"] == 2 and r["accepted"] == 1
    by = {x["claim"]: x for x in r["results"]}
    assert by["halal supply is verified"]["accepted"] is True
    assert by["price is optimal"]["accepted"] is False
    fab = client.get("/api/v1/resources?resource_class=process_intelligence").json()
    assert any(x["id"] == "truth_consensus" for x in fab["resources"])


# The user-reachable domain-tool surface — the reusable <DomainTool> frontend component posts to
# exactly these endpoints/keys. This locks them in: each returns its text result + honest in-house
# provenance (no external dependency), so a regression to any tool's contract fails CI.
_DOMAIN_TOOLS = [
    ("/api/v1/law/analyse", {"document_text": "This agreement is between A and B for consulting services."}, "analysis"),
    ("/api/v1/law/generate", {"template_id": "nda", "parties": {"party_a": "Workstation Ltd", "party_b": "Client Co"}, "jurisdiction": "England & Wales"}, "document"),
    ("/api/v1/science/synthesise", {"research_question": "Does X improve Y?"}, "report"),
    ("/api/v1/science/literature", {"research_question": "Does X improve Y?"}, "outline"),
    ("/api/v1/care/handover", {"patient_summary": "72yo M, community-acquired pneumonia.", "current_situation": "Stable post-op, observations within range."}, "handover"),
    ("/api/v1/care/care-plan", {"patient_profile": {"age": "78", "condition": "COPD"}, "care_needs": ["breathlessness management", "falls prevention"], "setting": "community", "duration_weeks": "6", "care_model": "person_centred"}, "care_plan"),
    ("/api/v1/care/risk-assess", {"tool": "news2", "patient_data": {"resp_rate": "22", "spo2": "93", "pulse": "112"}, "clinical_context": "post-op day 2"}, "assessment"),
    ("/api/v1/education/lesson-plan", {"subject": "Biology", "topic": "Cells", "level": "GCSE"}, "lesson_plan"),
    ("/api/v1/education/curriculum", {"subject": "Mathematics", "level": "GCSE"}, "curriculum"),
    ("/api/v1/education/assessment", {"subject": "Biology", "topic": "Photosynthesis", "level": "GCSE", "assessment_type": "quiz", "learning_objectives": ["explain light-dependent reactions"]}, "assessment"),
    ("/api/v1/religion/fatwa-research", {"question": "What are the conditions for fasting while travelling?"}, "research"),
    ("/api/v1/religion/quran-tafsir", {"surah": 1, "ayah_start": 1}, "tafsir"),
    ("/api/v1/religion/halal-review", {"product_name": "Gummy sweets", "product_description": "Chewy fruit sweets", "ingredients": ["bovine gelatin", "glucose syrup"], "target_markets": ["UK"]}, "assessment"),
    ("/api/v1/employment/cv", {"target_role": "Senior Data Engineer", "experience": "5 years building ETL pipelines in Python", "skills": ["Python", "Spark"], "seniority": "senior"}, "cv"),
    ("/api/v1/employment/cover-letter", {"target_role": "Product Manager", "company": "Acme", "highlights": "launched 3 products", "tone": "professional"}, "cover_letter"),
    ("/api/v1/employment/interview-prep", {"target_role": "Backend Engineer", "seniority": "mid", "competencies": ["system design"]}, "prep"),
    ("/api/v1/employment/career-path", {"current_role": "QA Analyst", "target_role": "SDET", "experience_years": 4, "constraints": "evenings only"}, "roadmap"),
    ("/api/v1/employment/application", {"target_role": "Band 5 Staff Nurse", "organisation": "NHS Trust", "person_spec": "Essential: NMC registration; person-centred care.", "experience": "3 years on a surgical ward", "questions": ["Describe handling a deteriorating patient."], "word_limit": 500}, "statement"),
]


@pytest.mark.parametrize("endpoint,payload,result_key", _DOMAIN_TOOLS)
def test_domain_tools_reachable_in_house(client, endpoint, payload, result_key):
    r = client.post(endpoint, json=payload)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get(result_key), f"{endpoint} missing '{result_key}'"
    prov = body.get("ai_provenance") or {}
    assert prov.get("posture") == "in-house-first"
    assert prov.get("is_external") is False


# Robustness guard: edge inputs (empty strings, empty dicts/lists, non-numeric where numbers are
# expected, zero reputation) must NEVER 500 — a 422 is acceptable, a 500 is a bug. This locks the whole
# AI surface against the crash class we hit in care/handover (W22) and the optimizer (W25).
_EDGE_PROBES = [
    ("/api/v1/law/generate", {"template_id": "nonexistent", "parties": {}}),
    ("/api/v1/care/care-plan", {"patient_profile": {}, "care_needs": [], "duration_weeks": "0"}),
    ("/api/v1/care/risk-assess", {"tool": "", "patient_data": {}}),
    ("/api/v1/education/curriculum", {"subject": "", "level": "", "duration_weeks": "0"}),
    ("/api/v1/religion/halal-review", {"product_name": "", "product_description": "", "ingredients": []}),
    ("/api/v1/employment/application", {"target_role": "", "questions": [], "word_limit": "0"}),
    ("/api/v1/optimizer/allocate", {"domain": "x", "requirements": {"CPU": "lots", "RAM": ""}}),
    ("/api/v1/collective/consensus", {"claims": [{"claim": "x", "confidence": 0.9, "reputation": 0}]}),
    ("/api/v1/mega-project/synthesise", {"concept": "", "domain": ""}),
    ("/api/v1/refine", {"previous": "", "instruction": ""}),
    ("/api/v1/avatar/chat", {"message": "", "context": "", "language": ""}),  # empty multimodal turn must not 500
    ("/api/v1/business-plan/objective", {"scope": "edge-probe", "title": ""}),  # blank objective must not 500
    # newer in-house-fabric capabilities must survive degenerate inputs (empty graph / no agents / no sources)
    ("/api/v1/native-ai/topology", {"nodes": [], "edges": []}),
    ("/api/v1/native-ai/quorum", {"agents": 0}),
    ("/api/v1/native-ai/entropy", {"sources": []}),
    ("/api/v1/native-ai/consensus", {"votes": [], "total_nodes": 0}),
    ("/api/v1/native-ai/decide", {"actions": []}),
    ("/api/v1/native-ai/intent", {"text": ""}),
    ("/api/v1/native-ai/rigor", {"metric_name": "", "value": 0.0, "baseline": 0.0}),
    ("/api/v1/native-ai/tree", {"goal": ""}),               # centerpiece: empty goal must not 500
    ("/api/v1/native-ai/transduce", {"input_signal": 0.0}),  # zero signal
    ("/api/v1/native-ai/entailment", {"premise": "", "hypothesis": ""}),
    ("/api/v1/native-ai/validate", {"prediction": "", "actual": "", "task_type": "SEMANTIC"}),
]


@pytest.mark.parametrize("endpoint,payload", _EDGE_PROBES)
def test_endpoints_no_500_on_edge_inputs(client, endpoint, payload):
    r = client.post(endpoint, json=payload)
    assert r.status_code < 500, f"{endpoint} 500'd on edge input: {r.text[:200]}"


def test_ai_calls_recorded_to_learning_loop(client):
    # Every in-house AI tool call (via _ai_provenance.ai_text) records a real outcome into the
    # operational-excellence learning loop, so rankings/summary reflect ACTUAL platform usage —
    # which OWNED resource served each domain tool — not just swarm runs.
    client.post("/api/v1/science/synthesise", json={"research_question": "does X affect Y?"})
    summ = client.get("/api/v1/operations/summary").json()
    assert "ai_call" in summ["kinds"]
    assert 0.0 <= summ["in_house_rate"] <= 1.0
    ranks = client.get("/api/v1/operations/rankings").json()["rankings"]
    agent_rows = [r for r in ranks if str(r["resource"]).startswith("agent:")]
    assert agent_rows and all(0.0 <= r["success_rate"] <= 1.0 for r in agent_rows)


def test_avatar_guided_navigation_whitelisted(client):
    # §5/§9 — the avatar guides/navigates users to platform areas: a deterministic keyword match
    # over a WHITELISTED catalogue of REAL routes (it can never invent a destination), each
    # suggestion carrying an honest match reason; no keywords → no forced suggestions.
    from agentic_core.avatars.api import ALLOWED_NAVIGATION_ROUTES
    r = client.post("/api/v1/avatar/chat", json={
        "message": "How do I adjust my economy waterfall and see the charity distribution?",
        "context": "general"}).json()
    areas = r.get("suggested_areas") or []
    assert areas and any(a["route"] == "/economy" for a in areas)
    for a in areas:
        assert a["route"] in ALLOWED_NAVIGATION_ROUTES      # whitelist-only — never a fabricated route
        assert a["because"].startswith("matched: ")          # honest match provenance
    r2 = client.post("/api/v1/avatar/chat", json={"message": "thank you, that was helpful",
                                                  "context": "general"}).json()
    assert (r2.get("suggested_areas") or []) == []            # nothing matched → nothing suggested


def test_genesis_establish_stream_births_a_real_vsb(client):
    # §5 — users WATCH the VSB being born: the SSE /establish/stream emits one event per REAL
    # completed step (naming → attestation → genome → board → economy → living → plan → swarm →
    # operational) and the persisted entity carries everything the events claimed.
    import json as _json
    import re as _re
    r = client.post("/api/v1/genesis/establish/stream", json={
        "problem": "stream-birth contract test", "domain": "enterprise", "name": "StreamBirthCo",
        "concept": "c", "design": "d", "commercialisation": "m"})
    assert r.status_code == 200
    events = [_json.loads(l[6:]) for l in r.text.splitlines() if l.startswith("data: ")]
    stages = [e["stage"] for e in events]
    for required in ("init", "named", "governance", "board", "economy", "living", "plan", "complete"):
        assert required in stages, f"birth stream missing the {required} stage"
    assert stages[-1] == "complete"
    vid = _re.search(r'"vsb_id": "(vsb-[a-f0-9]+)"', r.text).group(1)
    ent = client.get(f"/api/v1/vsb/{vid}").json()
    # every event reflected a real attachment — the persisted entity proves it
    assert ent.get("board") and ent.get("economy") and ent.get("living") and ent.get("business_plan_scope")
    assert ent.get("name") == "StreamBirthCo" and ent.get("status") == "operational"


def test_streaming_surfaces_in_house_first(client, monkeypatch):
    # §6 mandate — the last three user-reachable streaming surfaces ran the legacy EXTERNAL-FIRST
    # gateway.stream cascade. gateway.stream is now in-house-first (owned local model → opt-in
    # external → the guaranteed native floor), so ALL streams complete with NO external key and
    # never end in a bare error line.
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("AI_ALLOW_EXTERNAL", raising=False)
    # 1) Business-Plan Wizard stream
    r1 = client.post("/api/v310/entrepreneur/generate-plan/stream", json={
        "creation_id": "w254-test", "target_market": "UK elders", "funding_goal": 50000,
        "description": "halal meal kits"})
    assert r1.status_code == 200 and len(r1.text) > 200
    assert "Error:" not in r1.text[:200]
    # 2) Projects concept→commercialise stream
    p = client.post("/api/v1/projects/", json={"title": "W254 stream", "description": "stream test",
                                               "realm": "enterprise", "domain": "general"}).json()
    r2 = client.post(f"/api/v1/projects/{p['id']}/run")
    assert r2.status_code == 200 and len(r2.text) > 200
    assert "Error:" not in r2.text[:200]
    # 3) Synthesis Studio stream
    r3 = client.post("/api/v1/synthesis/stream", json={
        "instructions": "summarise a halal meal-kit plan", "content_ids": [], "output_type": "report"})
    assert r3.status_code == 200 and len(r3.text) > 200
    assert "Error:" not in r3.text[:200]


def test_video_html_render_live_and_honest(client):
    # §4.9 'Video' — a REAL deterministic render now exists: /export?format=video-html produces a
    # self-contained, SELF-PLAYING animated HTML artifact of the deliverable's own sections
    # (auto-advance + progress bar; no dependencies; nothing fabricated). mp4/mp3 remain HONESTLY in
    # the not-yet catalogue until real media encoding exists.
    d = client.post("/api/v1/deliverables/produce", json={
        "type": "report", "title": "W264 Video Render", "brief": "halal meal-kit strategy",
        "domain": "enterprise"}).json()
    did = d.get("id") or (d.get("deliverable") or {}).get("id")
    r = client.get(f"/api/v1/deliverables/{did}/export?format=video-html")
    assert r.status_code == 200
    assert "setInterval" in r.text and 'class="scene"' in r.text      # genuinely self-playing scenes
    assert "W264 Video Render" in r.text                               # the deliverable's own content
    f = client.get("/api/v1/deliverables/output-formats").json()
    assert "video-html" in f["live_ids"]                               # live — a real render
    assert "mp4" in f["catalogue_not_yet_produced"]                    # media encoding stays honest
    # the fabricated legacy economics module is out of the live tree
    import importlib.util as _ilu
    assert _ilu.find_spec("agentic_core.governance.economy") is None


def test_tree_autonomously_draws_fabric_resources(client):
    # §6↔§7 "the fabric is the bus" — the native swarm's workflow tree autonomously SELECTS matching
    # fabric resources (deterministic capability-word overlap; LIGHT bounded handlers only) and runs
    # their REAL engine, folding the genuine result into the node with honest provenance. Each
    # resource is drawn ONCE per run; a goal with no capability match draws nothing.
    t = client.post("/api/v1/native-ai/tree",
                    json={"goal": "Check halal compliance and regulatory assurance for a meal service"}).json()
    assert "compliance" in (t.get("fabric_resources_drawn") or [])
    drew = [n for n in t.get("nodes", []) if n.get("fabric")]
    assert len(drew) == 1                                          # once per run, not per node
    assert drew[0]["fabric"]["ran"] == "/api/v1/compliance/check"  # the REAL engine ran
    assert drew[0]["fabric"]["match_hits"] >= 2                    # honest deterministic match score
    assert "[fabric:compliance" in drew[0]["output"]               # the genuine result folded in
    t2 = client.post("/api/v1/native-ai/tree",
                     json={"goal": "Write a short story about a lighthouse keeper"}).json()
    assert (t2.get("fabric_resources_drawn") or []) == []          # no match → no forced draws


def test_v191_evolution_approvals_route_through_change_control(client):
    # The v191 evolution fragment previously self-approved self-modification proposals OUTSIDE all
    # governance. Approving now files a REAL Change Control request (arms-length): LOW auto-approves
    # through the CCA when the organism is healthy; higher impact HOLDS under_change_control until
    # the CCA decides; the proposal mirrors the governed outcome; re-approval never duplicates.
    from agentic_core.api.v191 import evolution as ev
    import uuid as _uuid
    lo, hi = f"w261-lo-{_uuid.uuid4().hex[:6]}", f"w261-hi-{_uuid.uuid4().hex[:6]}"
    props = ev._load()
    props += [
        {"id": lo, "title": "Tune cache TTL", "description": "raise TTL", "impact": "Low",
         "rationale": "r", "status": "pending"},
        {"id": hi, "title": "Swap orchestrator core", "description": "replace engine", "impact": "High",
         "rationale": "r", "status": "pending"},
    ]
    ev._save(props)
    a1 = client.post(f"/api/v191/evolution/proposals/{lo}/approve").json()
    assert a1.get("cca_id")                                     # a real CCA record exists even for LOW
    a2 = client.post(f"/api/v191/evolution/proposals/{hi}/approve").json()
    assert a2["status"] == "under_change_control" and a2.get("cca_id")   # held for the governed decision
    client.post(f"/api/v1/cca/{a2['cca_id']}/review",
                json={"override_decision": "approved", "reviewer_notes": "owner"})
    st = {p["id"]: p["status"] for p in client.get("/api/v191/evolution/proposals?status=all").json()}
    assert st[hi] == "approved"                                  # mirrors the CCA's governed outcome
    again = client.post(f"/api/v191/evolution/proposals/{lo}/approve").json()
    assert "no duplicate" in (again.get("note") or "").lower()   # idempotent — no duplicate CCA


def test_cca_twin_prevalidation_gates_major_changes(client):
    # §17.5 absolute invariant — digital-twin pre-validation before MAJOR change. An approved
    # HIGH-tier change is twin-simulated at approval; /implement REFUSES (409) a major change with
    # no recorded pre-validation; an explicit POST /{id}/twin-prevalidate unblocks it. The verdict
    # source is honest: a real model marker, or the organism health gate (never an echoed marker).
    from agentic_core.api import change_control as cca
    sub = client.post("/api/v1/cca/submit", json={
        "title": "W253 rotate signing keys", "change_type": "security_change",
        "description": "rotate the platform signing keys", "rationale": "invariant test"}).json()
    cid = sub["cca_id"]
    assert sub["impact_tier"] == "HIGH"
    ap = client.post(f"/api/v1/cca/{cid}/review",
                     json={"override_decision": "approved", "reviewer_notes": "owner"}).json()
    assert ap["decision"] == "approved"
    rec = client.get(f"/api/v1/cca/{cid}").json()
    tp = rec.get("twin_prevalidation") or {}
    assert tp.get("verdict") in ("pass", "fail")                      # ran at approval
    assert tp.get("source") in ("twin_marker", "health_gate_default")  # honest provenance
    assert any(a["event"].startswith("twin_prevalidation_") for a in rec["audit_trail"])
    if tp["verdict"] == "pass":
        assert client.post(f"/api/v1/cca/{cid}/implement").status_code == 200
    # a major change approved WITHOUT a recorded pre-validation is refused (409)
    sub2 = client.post("/api/v1/cca/submit", json={
        "title": "W253 policy amendment", "change_type": "policy_amendment",
        "description": "amend the distribution policy", "rationale": "t"}).json()
    cid2 = sub2["cca_id"]
    r2 = cca._load_change(cid2)
    r2["status"] = "approved"
    r2.pop("twin_prevalidation", None)
    cca._save_change(r2)
    assert client.post(f"/api/v1/cca/{cid2}/implement").status_code == 409
    pv = client.post(f"/api/v1/cca/{cid2}/twin-prevalidate").json()
    assert (pv.get("twin_prevalidation") or {}).get("verdict") in ("pass", "fail")
    if pv["twin_prevalidation"]["verdict"] == "pass":
        assert client.post(f"/api/v1/cca/{cid2}/implement").status_code == 200


def test_cca_immune_reconfigurator(client):
    # The arms-length Change Control Agency is wired to the Immune system + the Reconfiguration engine:
    # under threat the immune system proposes a SAFE, reversible defensive reconfiguration which the CCA
    # governs (audits + auto-approves) and applies via the reconfiguration engine. NOMINAL → no action.
    n = client.post("/api/v1/cca/immune-reconfigure", json={}).json()
    assert n["governed_by"].startswith("Change Control Agency")
    # ELEVATED → tighten generation (benign, reversible) — governed + applied via the reconfig engine
    e = client.post("/api/v1/cca/immune-reconfigure", json={"simulate_threat": "ELEVATED"}).json()
    assert e["status"] == "implemented" and e["applied"]
    assert e["reconfiguration"]["section"] == "gateway" and e["reconfiguration"]["key"] == "temperature_bias"
    rec = client.get(f"/api/v1/cca/{e['cca_id']}").json()
    assert rec["change_type"] == "immune_reconfiguration" and rec["immune_threat_at_submit"] == "ELEVATED"
    assert any(a["event"] == "implemented" for a in rec["audit_trail"])
    # CRITICAL containment is MEDIUM-tier + flagged for Board ratification
    cr = client.post("/api/v1/cca/immune-reconfigure", json={"simulate_threat": "CRITICAL"}).json()
    assert cr["impact_tier"] == "MEDIUM" and cr["requires_ratification"] is True
    # a submitted change records the live immune threat that governed the decision
    assert "immune_threat_at_submit" in rec
    # reset the risky lever so the suite leaves clean organism state
    client.post("/api/v1/organism/config/update",
                json={"section": "organism", "key": "immune_quarantine", "value": False, "reason": "test reset"})


def test_vbs_living_systems_integrated_in_house(client):
    # The OWNED VBS management systems (agentic_core/vbs) are real, reachable, and INTEGRATED into the
    # in-house AI: genuine ops (real QMS gates, SHA3-512 DCMS versioning) + the native workflow-tree
    # synthesis is GOVERNED by the real VBS QMS + DCMS. Honest: real computation, nothing fabricated.
    sysz = client.get("/api/v1/vbs/systems").json()
    assert sysz["owned"] is True and sysz["count"] == 5
    assert {s["id"] for s in sysz["systems"]} == {"bms", "qms", "ems", "dcms", "backbone"}
    # QMS: a REAL gate — high coverage + no stubs passes; low coverage + stubs fails
    assert client.post("/api/v1/vbs/qms/gate", json={"coverage": 0.97, "stubs_found": False}).json()["passed"] is True
    assert client.post("/api/v1/vbs/qms/gate", json={"coverage": 0.4, "stubs_found": True}).json()["passed"] is False
    # DCMS: REAL SHA3-512 versioning — same id, distinct content -> distinct hash + version bump
    a = client.post("/api/v1/vbs/dcms/commit", json={"artifact_id": "t-vbs", "content": {"v": 1}}).json()
    b = client.post("/api/v1/vbs/dcms/commit", json={"artifact_id": "t-vbs", "content": {"v": 2}}).json()
    assert a["algo"] == "sha3_512" and a["hash"] != b["hash"] and b["version"] == a["version"] + 1
    # W110 — the QMS OWNS the DCMS (ISO 9001 §7.5): document control is a function OF the QMS, not a sibling
    import asyncio as _aio
    from agentic_core.vbs.registry import qms as _qms, dcms as _dcms
    assert _qms.dcms is _dcms                                   # one DCMS instance, owned by the QMS
    _h = _aio.run(_qms.control_document("t-qms-owns-dcms", {"v": 1}, "pytest"))
    assert isinstance(_h, str) and len(_h) == 128              # QMS places a doc under control via its DCMS
    dc = client.get("/api/v1/vbs/qms/document-control").json()
    assert dc["qms_owns_dcms"] is True and dc["owned_subsystem"].startswith("DCMS")
    assert dc["controlled_documents"] >= 1 and dc["audit_integrity"] == 1.0
    cat = {s["id"]: s for s in sysz["systems"]}                 # catalogue declares ownership both ways
    assert "dcms" in (cat["qms"].get("owns") or []) and cat["dcms"].get("owned_by") == "qms"
    # INTEGRATED INTO THE IN-HOUSE AI: the native workflow tree's output is governed by VBS QMS + DCMS
    tree = client.post("/api/v1/native-ai/tree", json={"goal": "Build a halal compliance service"}).json()
    gov = tree.get("governance")
    assert gov and gov["governed_by"].startswith("VBS QMS + DCMS")
    assert isinstance(gov["qms_passed"], bool) and gov["dcms_algo"] == "sha3_512" and len(gov["dcms_hash"]) == 128


def test_data_dir_configurable(client):
    # Persistence is routed through the configured DATA_DIR (default 'data') so a deployment can point
    # all data at a durable volume (survives redeploys). Default behaviour is unchanged.
    # W394 — BOTH halves are checked in a fresh subprocess now, and symmetrically.
    # The default half used to be asserted in-process, which only holds when the ambient environment
    # happens to carry no DATA_DIR. That made the test depend on the developer's shell: it was the
    # long-standing "known local failure", and it would have started failing in CI the moment
    # conftest began isolating DATA_DIR. A test of "what happens with no DATA_DIR" must actually run
    # with no DATA_DIR.
    import os
    import subprocess
    import sys

    probe = "from agentic_core.config import data_path; print(data_path('vsb_entities'))"

    clean_env = {k: v for k, v in os.environ.items() if k not in ("DATA_DIR", "WORKSTATION_DATA_DIR")}
    default_out = subprocess.check_output(
        [sys.executable, "-c", probe], env=clean_env, text=True).strip().replace("\\", "/")
    assert default_out.endswith("data/vsb_entities"), default_out
    assert "_test_store" not in default_out, default_out       # the suite's isolation must not leak

    env = {**os.environ, "DATA_DIR": "custom_data_root"}
    out = subprocess.check_output(
        [sys.executable, "-c", probe], env=env, text=True).strip().replace("\\", "/")
    assert out.endswith("custom_data_root/vsb_entities"), out


def test_hot_stores_atomic_and_corruption_tolerant(tmp_path):
    # W257 — the W241 hardening pattern is SHARED (config.atomic_write_json / load_json_tolerant)
    # and adopted by the heartbeat-touched stores (living_vsbs · ledger · vsb entities · deliverables ·
    # forge · operational_excellence · capital_fund · marketplace · business_plan): a reader never
    # sees a half-written file; a corrupt file loads as its recoverable prefix or the default.
    import json as _json
    import inspect as _inspect
    from agentic_core.config import atomic_write_json, load_json_tolerant
    p = tmp_path / "store.json"
    atomic_write_json(p, {"a": 1})
    assert _json.loads(p.read_text(encoding="utf-8")) == {"a": 1}
    # corrupt trailing garbage → the recoverable prefix, not an exception
    p.write_text('{"a": 1}][{"garbage', encoding="utf-8")
    assert load_json_tolerant(p, {}) == {"a": 1}
    p.write_text("total trash", encoding="utf-8")
    assert load_json_tolerant(p, {"d": True}) == {"d": True}
    assert not [f for f in tmp_path.iterdir() if f.suffix == ".tmp"]   # no stray temp files
    # regression guard: the hot stores actually route through the shared atomic writer
    import agentic_core.economy.living_vsbs as lv
    import agentic_core.economy.ledger as lg
    import agentic_core.api.vsb as vb
    import agentic_core.api.deliverables as dl
    import agentic_core.api.capital_fund as cf
    for mod in (lv, lg, vb, dl, cf):
        assert "atomic_write_json" in _inspect.getsource(mod), f"{mod.__name__} not atomic"


def test_memory_store_corruption_tolerant(tmp_path):
    # §6 robustness — the native AI memory store the gateway writes after EVERY completion must
    # tolerate a corrupt/interleaved file (e.g. concurrent appenders from separate processes) rather
    # than raising and breaking every downstream AI call. On corruption it recovers the valid JSON
    # prefix, self-heals the file, and keeps writing atomically.
    import json as _json
    from agentic_core.ai.memory import VectorMemory
    f = tmp_path / "memory.json"
    # a complete valid list followed by interleaved trailing garbage (the real "Extra data" shape)
    good = _json.dumps([{"text": "alpha", "metadata": {}}, {"text": "beta", "metadata": {}}])
    f.write_text(good + '][{"text": "garbage', encoding="utf-8")
    m = VectorMemory.__new__(VectorMemory)
    m.storage_path = str(f)
    recovered = m._load()                      # recovers the valid prefix, drops the garbage
    assert [e["text"] for e in recovered] == ["alpha", "beta"]
    m.add_memory("gamma")                      # append survives + heals the file
    healed = _json.loads(f.read_text(encoding="utf-8"))    # file is valid JSON again
    assert [e["text"] for e in healed] == ["alpha", "beta", "gamma"]
    assert m.query_memory("beta") == ["beta"]


def test_spa_serving_when_built(client):
    # Single-service SPA serving: when the frontend is built (dist present), the backend serves the app
    # at / and falls back to the SPA shell for client routes, while /api still 404s as JSON and /health
    # works. Skipped in CI / pure-API dev (no build) so it never affects the lightweight suite.
    import pathlib
    from agentic_core.app_mvp import _FRONTEND_DIST  # always module-level
    if not (pathlib.Path(_FRONTEND_DIST) / "index.html").is_file():
        import pytest
        pytest.skip("frontend not built (no dist) — single-service SPA serving inactive")
    root = client.get("/")
    assert root.status_code == 200 and ("<!doctype" in root.text.lower() or "<html" in root.text.lower())
    assert client.get("/native-ai").status_code == 200            # client route -> SPA shell
    assert client.get("/api/v1/__definitely_not_a_route__").status_code == 404   # API 404 preserved (JSON)
    assert client.get("/health").json().get("status") == "healthy"


def test_native_fabric_selfcheck(client):
    # Fabric integrity: every integrated capability's backing agentic_core module actually IMPORTS.
    # Guards the whole integration arc — a broken integration would flip all_live to false.
    b = client.get("/api/v1/native-ai/selfcheck").json()
    assert b["posture"] == "in-house-first"
    assert b["total"] >= 12 and b["live"] == b["total"] and b["all_live"] is True
    assert all(m["live"] is True for m in b["modules"])


def test_native_capabilities_catalogue(client):
    # The in-house AI fabric publishes a discoverable catalogue of its OWNED capabilities — each backed
    # by a real, integrated agentic_core module. Consolidates the integration sweep into one surface.
    r = client.get("/api/v1/native-ai/capabilities")
    assert r.status_code == 200
    b = r.json()
    assert b["posture"] == "in-house-first" and b["count"] >= 12
    caps = b["capabilities"]
    assert all(c["in_house"] is True and c["name"] and c["endpoint"] and c["source"] and c["description"] for c in caps)
    # the genuinely-integrated real modules are represented
    sources = {c["source"] for c in caps}
    for s in ("cognition.minimax_optimizer", "quorum.sensing", "nlp.nli_engine",
              "signaling.empirical_transduction", "statistics.live_rigor_monitor", "crypto.entropy_pool"):
        assert s in sources, f"missing capability source {s}"


def test_native_topology_betti_in_house(client):
    # Owned graph-topology analysis (agentic_core/topology.TopologyDefense, with beta0 FIXED to real
    # connected components): REAL Betti numbers of the 1-complex — tree -> beta1=0, cycle -> beta1=1,
    # fracture (disconnection) -> beta0>1.
    tree = client.post("/api/v1/native-ai/topology",
                       json={"nodes": ["a", "b", "c", "d"], "edges": [["a", "b"], ["b", "c"], ["c", "d"]]}).json()
    cyc = client.post("/api/v1/native-ai/topology",
                      json={"nodes": ["a", "b", "c"], "edges": [["a", "b"], ["b", "c"], ["c", "a"]]}).json()
    frac = client.post("/api/v1/native-ai/topology",
                       json={"nodes": ["a", "b", "c", "d"], "edges": [["a", "b"]]}).json()
    assert tree["beta0_components"] == 1 and tree["beta1_cycles"] == 0    # connected tree, no cycles
    assert cyc["beta0_components"] == 1 and cyc["beta1_cycles"] == 1      # one independent cycle
    assert frac["beta0_components"] == 3                                  # disconnected -> 3 components
    assert "topology" in tree["method"]


def test_native_entropy_pool_in_house(client):
    # Owned entropy pool (agentic_core/crypto.EntropyPool): REAL SHA3-512 + XOR entropy mixing — a
    # deterministic seed for fixed sources (reproducible in-house seeding), not a PRNG call.
    src = [{"size": 100, "source": "a", "content_hash": "h1", "timestamp": 1},
           {"size": 200, "source": "b", "content_hash": "h2", "timestamp": 2}]
    r = client.post("/api/v1/native-ai/entropy", json={"sources": src}).json()
    assert isinstance(r["seed"], int) and r["bits_harvested"] == 256 and r["sources_mixed"] == 2
    assert len(r["pool_integrity"]) == 16 and "sha3" in r["algo"]
    # deterministic for the same fixed-timestamp sources; different sources -> different seed
    assert client.post("/api/v1/native-ai/entropy", json={"sources": src}).json()["seed"] == r["seed"]
    other = client.post("/api/v1/native-ai/entropy",
                        json={"sources": [{"size": 1, "source": "x", "content_hash": "z", "timestamp": 9}]}).json()
    assert other["seed"] != r["seed"]


def test_native_quorum_sensing_in_house(client):
    # Owned biomimetic swarm quorum sensing (agentic_core/quorum.QuorumSensing): REAL AI-2 density
    # threshold — the swarm flips to COOPERATIVE once aggregate concentration crosses the threshold.
    coop = client.post("/api/v1/native-ai/quorum", json={"agents": 6, "secretion": 10, "threshold": 50}).json()
    indep = client.post("/api/v1/native-ai/quorum", json={"agents": 3, "secretion": 10, "threshold": 50}).json()
    assert coop["behavior_mode"] == "COOPERATIVE" and coop["cooperative"] is True
    assert indep["behavior_mode"] == "INDEPENDENT" and indep["cooperative"] is False
    assert coop["concentration"] > indep["concentration"] and "quorum" in coop["method"]


def test_native_nlp_intent_entailment_in_house(client):
    # Owned NLP (agentic_core/nlp.NLIEngine): REAL regex intent inference + word-overlap entailment —
    # deterministic, not LLM, no external dependency.
    i = client.post("/api/v1/native-ai/intent", json={"text": "build and generate an app"}).json()
    assert i["intent"] == "BUILD_APP" and 0.0 <= i["confidence"] <= 1.0 and "all_scores" in i
    d = client.post("/api/v1/native-ai/intent", json={"text": "deploy this release to the cloud"}).json()
    assert d["intent"] == "DEPLOY_APP"
    e_same = client.post("/api/v1/native-ai/entailment",
                         json={"premise": "the cat sat on the mat", "hypothesis": "the cat sat on the mat"}).json()
    e_none = client.post("/api/v1/native-ai/entailment",
                         json={"premise": "the cat sat on the mat", "hypothesis": "quantum rocket science"}).json()
    assert e_same["label"] == "ENTAILED" and e_none["label"] == "NEUTRAL"
    assert "nlp" in e_same["method"]


def test_operations_degradation_detection_in_house(client):
    # The owned PerformanceDegradationDetector (agentic_core/self_improvement) is wired into the learning
    # loop: REAL telemetry degradation detection (>12.7% latency rise OR >9.3% accuracy drop over cycles)
    # bucketed from recorded outcomes — real arithmetic over real runs, not a guess.
    for _ in range(12):
        client.post("/api/v1/science/synthesise", json={"research_question": "x?"})
    r = client.get("/api/v1/operations/degradation", params={"cycles": 3, "window": 3})
    assert r.status_code == 200, r.text
    b = r.json()
    assert isinstance(b["degraded"], bool) and b["score"] in (0.0, 1.0)
    assert b["cycles_built"] == 3 and "PerformanceDegradationDetector" in b["method"]
    assert b["thresholds"]["latency_rise"] == 0.127 and b["thresholds"]["accuracy_drop"] == 0.093


def test_chief_orchestrates_objective_in_house(client):
    # The Chief delivers a business-plan OBJECTIVE via the autonomous in-house workflow TREE — grounded
    # in the plan, governed (QMS/validation/minimax/consensus/signal), sealed into the UEG chain, and
    # recorded as an auditable review on the objective. The whole living-organism pipeline, end to end.
    scope = "test-chief-tree"
    obj = client.post("/api/v1/business-plan/objective",
                      json={"scope": scope, "title": "Launch a halal compliance service",
                            "kpi": "10 pilots", "timeline": "Q3 2026"}).json()
    oid = obj["id"]
    r = client.post(f"/api/v1/business-plan/objective/{oid}/orchestrate", json={"scope": scope})
    assert r.status_code == 200, r.text
    b = r.json()
    assert b["objective_id"] == oid and b["grounded_in"] == scope
    assert b["tree"]["node_count"] >= 4 and b["tree"]["final"]
    assert b["tree"]["ueg_hash"] and len(b["tree"]["ueg_hash"]) == 128
    assert b["tree"]["decision"]["recommendation"] in ("proceed", "refine", "hold")
    # the run is recorded as an auditable review (with the orchestration provenance) on the objective
    plan = client.get("/api/v1/business-plan", params={"scope": scope}).json()
    o = next(o for o in plan["objectives"] if o["id"] == oid)
    assert any("workflow-tree" in rv.get("note", "") and "orchestration" in rv for rv in o.get("reviews", []))
    # 404 for an unknown objective
    assert client.post("/api/v1/business-plan/objective/nope/orchestrate", json={"scope": scope}).status_code == 404


def test_native_biomimetic_signaling_in_house(client):
    # Owned biomimetic signal transduction (agentic_core/signaling.EmpiricalSignalTransduction): a REAL
    # Hill-equation sigmoidal cascade — strong signals propagate (peak>=0.5), weak ones stay
    # sub-threshold; latency decreases as the signal strengthens (real kinetics, not a constant).
    strong = client.post("/api/v1/native-ai/transduce", json={"input_signal": 0.8}).json()
    weak = client.post("/api/v1/native-ai/transduce", json={"input_signal": 0.2}).json()
    assert strong["propagated"] is True and weak["propagated"] is False
    assert strong["peak_intensity"] > weak["peak_intensity"] and "Hill" in strong["method"]
    assert strong["latency_s"] < weak["latency_s"]
    # the workflow tree carries a real biomimetic signal_response over its consensus strength
    t = client.post("/api/v1/native-ai/tree", json={"goal": "Build a halal compliance service"}).json()
    sr = t.get("signal_response")
    assert sr and 0.0 <= sr["peak_intensity"] <= 1.0 and isinstance(sr["propagated"], bool) and "Hill" in sr["method"]


def test_native_swarm_consensus_in_house(client):
    # The owned swarm ConsensusEngine (agentic_core/swarm) is integrated (it was DEAD — a missing
    # Optional import — now fixed): REAL threshold vote-tally — a choice wins at >= threshold of total
    # nodes, else no consensus. Plus the workflow tree's INDEPENDENT owned checks vote + reach consensus.
    won = client.post("/api/v1/native-ai/consensus", json={"total_nodes": 4, "votes": [
        {"voter": "a", "choice": "go"}, {"voter": "b", "choice": "go"},
        {"voter": "c", "choice": "go"}, {"voter": "d", "choice": "stop"}]}).json()
    assert won["reached"] is True and won["choice"] == "go"          # 3/4 >= 0.66
    split = client.post("/api/v1/native-ai/consensus", json={"total_nodes": 4, "votes": [
        {"voter": "a", "choice": "x"}, {"voter": "b", "choice": "x"},
        {"voter": "c", "choice": "y"}, {"voter": "d", "choice": "z"}]}).json()
    assert split["reached"] is False and split["choice"] is None     # 2/4 < 0.66
    # the tree carries a real consensus across its OWN independent owned signals
    t = client.post("/api/v1/native-ai/tree", json={"goal": "Build a halal compliance service"}).json()
    con = t.get("consensus")
    assert con and "swarm" in con["method"] and isinstance(con["reached"], bool)
    assert set(con["votes"].keys()) == {"qms", "validation", "minimax", "immune"}
    assert 0.0 <= con["proceed_fraction"] <= 1.0


def test_native_statistical_rigor_in_house(client):
    # The owned statistical-rigor capability (agentic_core/statistics.LiveRigorMonitor) is integrated:
    # REAL scipy 95% CI + one-sample t-test over a live metric series (not a fabricated confidence),
    # each validation sealed into the owned UEG provenance chain.
    last = None
    for v in [0.82, 0.80, 0.85, 0.79, 0.88, 0.83]:
        last = client.post("/api/v1/native-ai/rigor",
                           json={"metric_name": "rate_x", "value": v, "baseline": 0.6}).json()
    assert last["ci_95"][0] <= last["ci_95"][1] and "scipy" in last["method"]
    assert 0.0 <= last["p_value"] <= 1.0 and isinstance(last["significant"], bool)
    # a series clearly above baseline 0.6 yields a tiny p-value (real t-test, not fabricated)
    assert last["p_value"] < 0.05
    # a non-significant metric produces a numpy bool internally — the owned UEG chain must STILL
    # serialise it and stay cryptographically valid (regression for the numpy-serialisation fix)
    client.post("/api/v1/native-ai/rigor", json={"metric_name": "flat_y", "value": 0.6, "baseline": 0.6})
    assert client.get("/api/v1/ueg/verify").json()["chain_valid"] is True


def test_native_validation_capability_in_house(client):
    # The owned validation capability (agentic_core/validation.AccuracyValidator) is integrated: REAL
    # difflib semantic similarity / numerical tolerance — not LLM self-grading — exposed standalone AND
    # used by the tree to check the synthesis genuinely INTEGRATES (vs near-copies) its branches.
    hi = client.post("/api/v1/native-ai/validate",
                     json={"prediction": "the quick brown fox", "actual": "the quick brown fox", "task_type": "SEMANTIC"}).json()
    lo = client.post("/api/v1/native-ai/validate",
                     json={"prediction": "totally unrelated content", "actual": "the quick brown fox", "task_type": "SEMANTIC"}).json()
    assert hi["is_accurate"] is True and hi["confidence"] > 0.9
    assert lo["is_accurate"] is False and lo["confidence"] < hi["confidence"]
    num = client.post("/api/v1/native-ai/validate",
                      json={"prediction": 100.0, "actual": 100.5, "task_type": "NUMERICAL"}).json()
    assert num["is_accurate"] is True
    # the workflow tree carries a real difflib synthesis-integration check
    t = client.post("/api/v1/native-ai/tree", json={"goal": "Build a halal compliance service"}).json()
    v = t.get("validation")
    assert v and "difflib" in v["method"]
    assert 0.0 <= v["max_branch_overlap"] <= 1.0 and isinstance(v["integrated"], bool) and v["branches_checked"] >= 1


def test_ueg_provenance_ledger_in_house(client):
    # The in-house AI records its workflow-tree runs to a REAL hash-chained SHA3-512 Merkle-DAG audit
    # ledger (agentic_core/ueg) — cryptographically verifiable, tamper-evident, grows per run.
    t = client.post("/api/v1/native-ai/tree", json={"goal": "Build a halal compliance service"}).json()
    assert t.get("ueg_hash") and len(t["ueg_hash"]) == 128
    v = client.get("/api/v1/ueg/verify").json()
    assert v["chain_valid"] is True and v["algo"] == "sha3_512" and len(v["merkle_root"]) == 128
    r = client.get("/api/v1/ueg/recent", params={"limit": 5}).json()
    assert r["count"] >= 1 and any(e["event_type"] == "native.tree.run" for e in r["events"])
    # a second run keeps the chain cryptographically valid (real append-only integrity)
    client.post("/api/v1/native-ai/tree", json={"goal": "Design an education service"})
    assert client.get("/api/v1/ueg/verify").json()["chain_valid"] is True


def test_native_minimax_decision_in_house(client):
    # The OWNED cognition module (agentic_core/cognition.MinimaxOptimizer) is integrated into the
    # in-house AI as a REAL maximin decision capability — game-theory over actions under worst-case
    # stressors, not LLM text. Exposed standalone AND used to recommend on every workflow-tree run.
    d = client.post("/api/v1/native-ai/decide",
                    json={"state": {"base_stability": 0.9}, "actions": ["expand", "hold", "retreat"]})
    assert d.status_code == 200, d.text
    db = d.json()
    assert db["selected_action"] in ["expand", "hold", "retreat"]
    assert 0.0 <= db["consistency_score"] <= 1.0 and "minimax" in db["method"]
    # the workflow tree carries a real minimax decision grounded in its OWN run signals
    t = client.post("/api/v1/native-ai/tree", json={"goal": "Build a halal compliance service"}).json()
    dec = t.get("decision")
    assert dec and dec["recommendation"] in ("proceed", "refine", "hold")
    assert 0.0 <= dec["consistency"] <= 1.0 and "minimax" in dec["method"]
    assert dec["stressors"] and len(dec["stressors"]) >= 3


def test_native_workflow_tree_in_house(client):
    # The native swarm AUTONOMOUSLY decomposes a goal into a workflow TREE (DAG) and runs it
    # in-house-first per node, with PARALLEL branches + dependency ordering — orchestrated as a
    # living-organism cascade (biobus signals + immune-throttled parallelism). No fabrication:
    # every node reports which OWNED resource served it; nothing external in the test env.
    r = client.post("/api/v1/native-ai/tree",
                    json={"goal": "Build and launch a halal compliance review service"})
    assert r.status_code == 200, r.text
    b = r.json()
    assert b["posture"] == "in-house-first"
    # a real TREE, not a linear chain: >=4 nodes and at least one level fans out (>1 node in parallel)
    assert b["node_count"] >= 4 and b["parallel_levels"] >= 1
    # dependency ordering: every node runs only after ALL its dependencies (levels are topo-ordered)
    seen: set = set()
    tree_by_id = {n["id"]: n for n in b["tree"]}
    for level in b["levels"]:
        for nid in level:
            assert all(d in seen for d in tree_by_id[nid]["depends_on"]), f"{nid} ran before its deps"
        seen.update(level)
    # every node served in-house with honest provenance; final synthesis present
    assert b["any_external"] is False
    assert b["nodes"] and all(n["is_external"] is False and n["served_by"] for n in b["nodes"])
    assert b["final"] and isinstance(b["final"], str)
    # adaptive planner expanded the tree for THIS goal: build->implementation, halal/compliance->risk
    ids = set(tree_by_id)
    assert {"frame", "synthesise", "review", "implementation", "risk"} <= ids
    # the fan-out level has the parallel investigation branches depending only on frame
    fanout = next((lv for lv in b["levels"] if len(lv) > 1), [])
    assert all(tree_by_id[nid]["depends_on"] == ["frame"] for nid in fanout)


def test_avatar_vision_in_house_and_honest(client):
    # The avatar accepts an image (multimodal) and analyses it IN-HOUSE FIRST (local Ollama vision
    # model) — never an external dependency. When no vision model is available it stays HONEST:
    # image_understood is False and no description is fabricated; the text answer is still in-house.
    png_1x1 = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
    r = client.post("/api/v1/avatar/chat",
                    json={"message": "What is in this image?", "context": "general", "image_base64": png_1x1})
    assert r.status_code == 200, r.text
    b = r.json()
    assert "image_understood" in b and "image_served_by" in b and "image_is_external" in b
    assert isinstance(b["image_understood"], bool)
    # vision provenance is honest: if analysed at all, in-house (ollama) unless an external key is set
    if b["image_understood"]:
        assert b["image_served_by"] in ("ollama", "openai")
    else:
        assert b["image_served_by"] is None and b["image_is_external"] is False
    # the conversational answer itself is always in-house (native fabric)
    assert b["response"] and b["is_external"] is False


def test_avatar_all_language_in_house(client):
    # All-language, HONESTLY (W326): the avatar accepts a `language` and instructs the fabric to
    # answer in it — but the response reports only the language actually HONOURED. On the
    # deterministic floor (which cannot translate) a requested language is NOT echoed back as an
    # achievement; the answer stays in-house either way. Default (no language) is not forced.
    r = client.post("/api/v1/avatar/chat", json={"message": "Summarise the mission",
                                                 "context": "general", "language": "Arabic"})
    assert r.status_code == 200
    b = r.json()
    assert b["response"] and b["is_external"] is False
    if b["served_by"] == "native":
        assert b["language"] is None          # the floor never claims a translation it didn't do
    else:
        assert b["language"] == "Arabic"      # a capable model honoured it — reported truthfully
    d = client.post("/api/v1/avatar/chat", json={"message": "hi", "context": "general"}).json()
    assert d["language"] is None


def test_refine_iterates_in_house(client):
    # Iterative refinement: ANY tool output can be advanced in-house via /api/v1/refine, building on
    # the previous version. Returns the FULL refined text + honest in-house provenance.
    r = client.post("/api/v1/refine", json={"previous": "## Plan\nA brief care plan.",
                                            "instruction": "Add a falls-prevention section.", "context": "Care Plan"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("refined")
    p = body.get("ai_provenance") or {}
    assert p.get("posture") == "in-house-first" and p.get("is_external") is False


# ── Phase 2 domain-depth endpoints (W208-212) ─────────────────────────────────
# Structural/contract tests — NOT @_ai_only, so they run on the native floor in CI and guard routing +
# the response contract (these would catch a decorator-shadow / 422 regression on a new endpoint).

def _assert_str_field(body: dict, key: str):
    assert key in body, f"missing '{key}' in {list(body)[:8]}"
    assert isinstance(body[key], str) and body[key].strip(), f"'{key}' empty"


def test_law_research_contract(client):
    r = client.post("/api/v1/law/research", json={
        "question": "Can an employer enforce a 12-month non-compete clause?",
        "jurisdiction": "England & Wales", "area_of_law": "employment"})
    assert r.status_code == 200, r.text
    body = r.json()
    _assert_str_field(body, "analysis")
    assert body.get("method") == "IRAC"
    assert "legal advice" in (body.get("disclaimer") or "").lower()


def test_employment_salary_negotiation_contract(client):
    r = client.post("/api/v1/employment/salary-negotiation", json={
        "target_role": "Senior Software Engineer", "seniority": "senior", "offered_salary": "£70,000"})
    assert r.status_code == 200, r.text
    body = r.json()
    _assert_str_field(body, "plan")
    assert body.get("disclaimer")
    # salary_negotiation must be discoverable in the services list
    svc = client.get("/api/v1/employment/services").json()
    assert any(s.get("id") == "salary_negotiation" for s in svc.get("services", []))


def test_science_experiment_design_contract(client):
    r = client.post("/api/v1/science/experiment-design", json={
        "hypothesis": "A daily mindfulness app reduces self-reported anxiety in undergraduates",
        "methodology": "rct", "domain": "psychology"})
    assert r.status_code == 200, r.text
    _assert_str_field(r.json(), "design")


def test_care_safeguarding_contract(client):
    r = client.post("/api/v1/care/safeguarding", json={
        "concern": "An elderly client has unexplained bruising and seems fearful of a relative.",
        "setting": "domiciliary"})
    assert r.status_code == 200, r.text
    body = r.json()
    _assert_str_field(body, "guidance")
    # the safety-critical disclaimer must direct to emergency services
    assert "999" in (body.get("disclaimer") or "")


def test_education_feedback_contract(client):
    r = client.post("/api/v1/education/feedback", json={
        "student_work": "The water cycle is when water goes up and comes down as rain.",
        "task": "Explain the water cycle", "level": "KS2", "subject": "science"})
    assert r.status_code == 200, r.text
    body = r.json()
    _assert_str_field(body, "feedback")
    # marking must be flagged as indicative, never a final/official grade
    assert "indicative" in (body.get("disclaimer") or "").lower()


def test_religion_hadith_study_contract(client):
    r = client.post("/api/v1/religion/hadith-study", json={
        "hadith": "Actions are but by intentions", "focus": "authentication"})
    assert r.status_code == 200, r.text
    body = r.json()
    _assert_str_field(body, "study")
    # high-stakes honesty guard: results must be flagged provisional / to be verified with scholars
    assert "verif" in (body.get("disclaimer") or "").lower()


# ── VSB Economic Model — Owner-adjustable profit waterfall (W215, virtual-only) ───────────────────

def test_economy_waterfall_owner_sovereignty(client):
    import uuid as _uuid
    vid = f"test-waterfall-{_uuid.uuid4().hex[:10]}"   # unique per run — no dependence on persisted state
    # default comes from the entity template, summing to 1.0
    d = client.get(f"/api/v1/economy/waterfall?vsb_id={vid}&entity_type=waqf_ltd_hybrid").json()
    assert d["source"] == "entity_template"
    assert abs(sum(d["waterfall"].values()) - 1.0) < 0.01
    # the Owner adjusts the proportions (more to charity) — accepted, normalised, persisted
    r = client.post("/api/v1/economy/waterfall", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
        "proportions": {"owner": 0.10, "self_investment": 0.25, "capital_fund": 0.20,
                        "user_projects": 0.15, "charity": 0.30}})
    assert r.status_code == 200, r.text
    assert r.json()["source"] == "owner_override"
    # the override is now the effective waterfall
    d2 = client.get(f"/api/v1/economy/waterfall?vsb_id={vid}&entity_type=waqf_ltd_hybrid").json()
    assert d2["source"] == "owner_override"
    assert d2["waterfall"]["charity"] == 0.30


def test_native_ai_ensemble(client):
    # §6 — model-ensemble orchestration: run across multiple owned models in parallel, then synthesise
    r = client.post("/api/v1/native-ai/ensemble", json={
        "prompt": "one-line halal meal idea", "models": ["ollama:llama3.2", "native"]}).json()
    assert r.get("models_run") == ["ollama:llama3.2", "native"]
    members = r.get("members") or []
    assert len(members) == 2
    assert all(m.get("output") and m.get("served_by") for m in members)   # each member ran + reports provenance
    assert (r.get("synthesis") or {}).get("output")                       # consensus synthesis produced
    # composable in the §7 fabric
    comp = client.post("/api/v1/resources/compose", json={
        "name": "Ens", "usage_area": "synthesis", "resource_ids": ["native_ensemble"],
        "config": {"native_ensemble": {"prompt": "plan", "models": "native"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run", json={"objective": "o"}).json()
    ne = next((x for x in (run.get("real_resource_runs") or []) if x["resource"] == "native_ensemble"), None)
    assert ne and ne.get("output")


def test_native_ai_model_discovery_and_named_routing(client):
    # §6 — owned models as composable resources: the catalogue + named-model routing
    m = client.get("/api/v1/native-ai/models").json()
    assert isinstance(m.get("local_models"), list)        # discovered local models (empty under AI_DISABLE_LOCAL)
    tier_ids = [t["id"] for t in m.get("tiers", [])]
    assert "auto" in tier_ids and "native" in tier_ids    # the always-present tiers
    # routing to a SPECIFIC named model is honored (tried first), with the floor as graceful fallback
    r = client.post("/api/v1/native-ai/complete", json={"prompt": "x", "model": "ollama:llama3.2"}).json()
    assert (r.get("resources_tried") or [])[0] == "ollama:llama3.2"
    assert r.get("output")   # always a real in-house result (floor guarantees it)
    # the ollama resource row advertises its discovered local models
    res = client.get("/api/v1/native-ai/resources").json()
    ollama = next((x for x in res["resources"] if x["name"] == "ollama"), {})
    assert "local_models" in ollama


def test_native_ai_model_preference(client):
    # §6/§7 — model-tier preference (user design control over which OWNED tier serves)
    # model=native forces the deterministic floor (tries only "native")
    rn = client.post("/api/v1/native-ai/complete", json={"prompt": "summarise", "model": "native"}).json()
    assert rn.get("served_by") == "native"
    assert rn.get("resources_tried") == ["native"]
    # model=local requires the local model first, with the floor as graceful fallback (tries ollama, then native)
    rl = client.post("/api/v1/native-ai/complete", json={"prompt": "summarise", "model": "local"}).json()
    assert (rl.get("resources_tried") or [])[0] == "ollama"
    assert rl.get("output")   # always a real in-house result (floor guarantees it)


def test_fabric_pi_engines_run_real_staged(client):
    # §7 — ALL FOUR headline PI engines (BDP/SPI/APIE/DDPIE) run their REAL multi-stage pipeline when composed
    comp = client.post("/api/v1/resources/compose", json={
        "name": "PIengines", "usage_area": "synthesis", "resource_ids": ["bdp", "spi", "apie", "ddpie"],
        "config": {"bdp": {"rigor": "rigorous"}, "spi": {}, "apie": {"rigor": "rigorous"}, "ddpie": {}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "launch a halal meal-kit for elders"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    for eng in ("bdp", "spi", "apie", "ddpie"):
        assert eng in rr, f"{eng} did not run as a real engine"
        assert (rr[eng].get("stages") or 0) >= 2   # a multi-stage pipeline ran (not a single prompt)
        assert rr[eng].get("output")


def test_fabric_nexus_and_genesis_run_real(client):
    # §7 — the last two PI cognition orchestrators the vision names run their REAL engine when composed:
    # Synthesis Nexus (4-layer chain) + Genesis (Concept→Commercialisation journey, bounded establish=False).
    comp = client.post("/api/v1/resources/compose", json={
        "name": "NexusGenesis", "usage_area": "synthesis", "resource_ids": ["nexus", "genesis"],
        "config": {"nexus": {"activity": "auto"}, "genesis": {"realm": "enterprise"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "a halal meal-kit subscription for elders"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    assert "nexus" in rr and "genesis" in rr
    assert (rr["nexus"].get("stages") or 0) >= 2 and rr["nexus"].get("output")        # the 4-layer chain ran
    assert rr["nexus"].get("ran") == "/api/v1/intelligence/nexus"
    assert rr["genesis"].get("status") == "complete" and rr["genesis"].get("output")  # the journey ran
    assert rr["genesis"].get("ran") == "/api/v1/genesis/journey"


def test_fabric_genome_runs_real(client):
    # §7 — composing the genome resource runs its REAL encode engine (a trait vector), not a prompt stage
    comp = client.post("/api/v1/resources/compose", json={
        "name": "GenomePipe", "usage_area": "synthesis", "resource_ids": ["genome"],
        "config": {"genome": {"entity_name": "ZeroWaste Care"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "a halal zero-waste meal service"}).json()
    g = next((x for x in (run.get("real_resource_runs") or []) if x["resource"] == "genome"), None)
    assert g is not None
    assert str(g.get("genome_id", "")).startswith("genome-")
    assert g.get("dominant_trait")   # a real trait vector was produced


def test_fabric_native_ai_resources_run_real(client):
    # §6↔§7 — the OWNED native AI resources (orchestrator + swarm) run their REAL logic when composed,
    # reporting which owned resource actually served (provenance), not a generic prompt stage.
    comp = client.post("/api/v1/resources/compose", json={
        "name": "Native AI Pipeline", "usage_area": "synthesis",
        "resource_ids": ["native_orchestrator", "native_swarm"],
        "config": {"native_orchestrator": {"prompt": "outline a zero-waste meal plan"},
                   "native_swarm": {"stages": "research the need\ndesign the plan\ndeliver the output"}}}).json()
    cid = comp["id"]
    run = client.post(f"/api/v1/resources/compositions/{cid}/run", json={"objective": "zero-waste community meals"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    assert "native_orchestrator" in rr and "native_swarm" in rr
    assert rr["native_orchestrator"].get("served_by")            # honest provenance (native floor / ollama / external)
    assert rr["native_swarm"].get("stages_run") == 3 and rr["native_swarm"].get("output")


def test_fabric_musculoskeletal_facilities_run_real(client):
    # §7↔§6 — the musculoskeletal facilities run their REAL engine when composed, now driven by the
    # OWNED native swarm: Reactor + Factory (previously the legacy external-first stream) report
    # served_by; the Optimizer runs the deterministic allocator; the Simulator (digital twin) runs a
    # native-driven forward simulation. Each is a genuine engine run, not a generic prompt stage.
    comp = client.post("/api/v1/resources/compose", json={
        "name": "Facilities", "usage_area": "science",
        "resource_ids": ["reactor", "factory", "resource_optimizer", "digital_twin"],
        "config": {"reactor": {"domain": "science"},
                   "factory": {"product_type": "technical_spec", "name": "DesertFarm Spec"},
                   "resource_optimizer": {"requirements": {"CPU": 8, "RAM": 2048}, "tier": "pro"},
                   "digital_twin": {"system": "drip-irrigation grid", "scenario": "drought stress"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "optimise a desert farm"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    for fac in ("reactor", "factory", "resource_optimizer", "digital_twin"):
        assert fac in rr, f"{fac} did not run as a real engine"
        assert not rr[fac].get("error"), rr[fac].get("error")
        assert rr[fac].get("output")
    # Reactor + Factory + Simulator are now driven by the native swarm (in-house provenance)
    assert rr["reactor"].get("served_by") and rr["factory"].get("served_by")
    assert rr["digital_twin"].get("served_by")
    assert rr["reactor"].get("ran") == "/api/v1/reactor/composite"   # the composite Reactor (vision definition)
    assert rr["factory"].get("ran") == "/api/v1/factory/produce"


def test_fabric_reactor_is_composite(client):
    # §7 vision — "A Reactor = Incubator + Experimentation + Studio". Composing the Reactor runs all
    # THREE real sub-engines as one orchestrated run on the native swarm (not a single domain sim).
    comp = client.post("/api/v1/resources/compose", json={
        "name": "CompositeReactor", "usage_area": "science", "resource_ids": ["reactor"],
        "config": {"reactor": {"subject": "a drought-resistant irrigation schedule", "variants": 2,
                               "iterations": 1, "scenarios": "Pursue now\nDefer one season"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "optimise a desert farm"}).json()
    r = next((x for x in (run.get("real_resource_runs") or []) if x["resource"] == "reactor"), None)
    assert r is not None and not r.get("error")
    assert r.get("ran") == "/api/v1/reactor/composite"
    assert r.get("sub_facilities") == ["incubator", "experimentation", "studio"]   # the three sub-engines
    assert (r.get("generations_run") or 0) >= 1      # Incubator evolution ran
    assert (r.get("scenarios_run") or 0) >= 2        # Experimentation what-ifs ran
    assert r.get("output")


def test_generator_facility_live(client):
    # §7 — the Generator facility is first-class + live: produce ONE targeted artefact in a chosen
    # format on the OWNED native swarm, with provenance. Reconfigurable + rerunnable.
    r = client.post("/api/v1/generator/produce", json={
        "artefact_type": "schema", "spec": "a user account record", "format": "json", "domain": "technology"}).json()
    assert r["artefact_type"] == "schema" and r["format"] == "json"
    assert r["served_by"] and r["output"]


def test_fabric_all_eight_facilities_run_real(client):
    # §7 — ALL EIGHT musculoskeletal digital-resource facilities the vision names run their REAL engine
    # when composed (Engines · Reactors · Petri dishes · Incubators · Laboratories · Factories ·
    # Generators · Simulators) — each reconfigurable, rerunnable, reusable, driven by the native swarm.
    facilities = {
        "bdp": {"rigor": "standard"},                                  # Engines
        "reactor": {"domain": "science"},                              # Reactors
        "petri_dish": {"specimen": "drought-resistant seed"},          # Petri dishes
        "incubator": {"base_prompt": "irrigation scheduling", "variants": 2},  # Incubators
        "synthesis_studio": {"brief": "a halal desert-farm co-op", "max_stages": 2},  # Laboratories
        "factory": {"product_type": "operational_plan", "name": "Farm Ops"},   # Factories
        "generator": {"artefact_type": "config", "spec": "irrigation controller", "format": "yaml"},  # Generators
        "digital_twin": {"system": "drip grid", "scenario": "heatwave"},       # Simulators
    }
    comp = client.post("/api/v1/resources/compose", json={
        "name": "All8 Facilities", "usage_area": "science",
        "resource_ids": list(facilities.keys()), "config": facilities}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "stand up a halal desert-farm co-op"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    for fac in facilities:
        assert fac in rr, f"{fac} did not run as a real engine when composed"
        assert not rr[fac].get("error"), f"{fac}: {rr[fac].get('error')}"
        assert rr[fac].get("output"), f"{fac} produced no output"
    # the Engine ran a multi-stage pipeline; the Laboratory ran its genuine cascade
    assert (rr["bdp"].get("stages") or 0) >= 2
    assert (rr["synthesis_studio"].get("stages_run") or 0) >= 1


def test_fabric_organism_systems_run_real(client):
    # §8↔§7 — the biomimetic organism systems run their REAL engine/reading when composed (the living
    # substrate the composition runs ON), not generic prompt stages: constitutional gate · live immune /
    # self-healing health · ATP metabolism · circadian phase · a real nervous signal · evolution-office.
    systems = ["gaas_v5", "nervous_system", "immune", "self_healing", "metabolic", "circadian", "genome"]
    comp = client.post("/api/v1/resources/compose", json={
        "name": "Organism", "usage_area": "governance", "resource_ids": systems,
        "config": {"genome": {"entity_name": "OrganismCo"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "govern a halal venture under homeostasis"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    for sysid in systems:
        assert sysid in rr, f"{sysid} did not run as a real organism engine"
        assert not rr[sysid].get("error"), f"{sysid}: {rr[sysid].get('error')}"
        assert rr[sysid].get("output"), f"{sysid} produced no reading"
    # real organism readings (not fabricated): immune health, self-healing health, gaas governance verdict
    assert rr["immune"].get("health") is not None
    assert rr["self_healing"].get("overall_health") is not None
    assert rr["gaas_v5"].get("ran") == "/api/v1/gaas/intercept"
    assert rr["metabolic"].get("mode")        # FULL_POWER / NOMINAL / DEGRADED / EMERGENCY
    assert rr["nervous_system"].get("signal_fired") is True


def test_fabric_enterprise_layer_runs_real(client):
    # §5/§12↔§7 — the enterprise/org layer runs its REAL engine/reading when composed (bounded, no state
    # proliferation): live treasury · the genuine tiered-governance verdict · the real Products Catalogue
    # (relevance-matched) · a real Build-to-Order blueprint.
    res_ids = ["capital_fund", "change_control", "products_catalogue", "build_to_order"]
    comp = client.post("/api/v1/resources/compose", json={
        "name": "Enterprise", "usage_area": "commercialisation", "resource_ids": res_ids,
        "config": {"build_to_order": {"entity_name": "MealKitCo", "components": "vsb,csuite"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "launch a halal meal-kit subscription for elders"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    for rid in res_ids:
        assert rid in rr, f"{rid} did not run as a real enterprise engine"
        assert not rr[rid].get("error"), f"{rid}: {rr[rid].get('error')}"
        assert rr[rid].get("output"), f"{rid} produced no reading"
    # real readings/verdicts (not fabricated)
    assert rr["capital_fund"].get("available") is not None          # live virtual treasury
    assert rr["change_control"].get("impact_tier") in ("LOW", "MEDIUM", "HIGH", "CRITICAL")  # real tier
    assert (rr["products_catalogue"].get("total_products") or 0) >= 1   # the real catalogue
    assert rr["build_to_order"].get("blueprint_id")                 # a real blueprint assembled


def test_fabric_remaining_resources_run_real(client):
    # §7 — the LAST previously-prompt-only registry resources run their real engine/reading when
    # composed: compliance (federated verdict), truth_consensus (real consensus over configured
    # claims), mega_project (bounded native synthesis), omnimedia (live output-formats reading),
    # federation_mesh (live mesh status — simulated peers honestly flagged).
    res_ids = ["compliance", "truth_consensus", "mega_project", "omnimedia", "federation_mesh"]
    comp = client.post("/api/v1/resources/compose", json={
        "name": "Remaining", "usage_area": "governance", "resource_ids": res_ids,
        "config": {"truth_consensus": {"claims": "halal certification is required\nthe product is compliant"}}}).json()
    run = client.post(f"/api/v1/resources/compositions/{comp['id']}/run",
                      json={"objective": "launch a halal meal-kit"}).json()
    rr = {x["resource"]: x for x in (run.get("real_resource_runs") or [])}
    for rid in res_ids:
        assert rid in rr, f"{rid} did not run as a real engine"
        assert not rr[rid].get("error"), f"{rid}: {rr[rid].get('error')}"
        assert rr[rid].get("output"), f"{rid} produced no output"
    assert rr["compliance"].get("overall") in ("pass", "review", "fail")   # a genuine federated verdict
    assert rr["truth_consensus"].get("claims") == 2                        # real consensus over MY claims
    assert rr["omnimedia"].get("live_formats")                             # the real producible formats
    assert rr["federation_mesh"].get("operational") is True


def test_invariants_sweep_the_never_tested_absolutes(client):
    # §17.5 (W345) — live verdicts for the five invariants no round ever tested. Each leg asserts
    # what the code genuinely guarantees (per the W331 honest restatement) — nothing aspirational.
    import json as _json
    import threading
    from agentic_core.config import data_path

    # (1) ARMS-LENGTH FALSIFICATION — drive the AI-CEO-tier surfaces AT the Board/genome and
    # prove none of them mutates it: the only mutation path is the CCA-approved apply.
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "w345 invariant venture", "ship_output": False}).json()
    vid = est["vsb_id"]
    before = client.get(f"/api/v1/vsb/{vid}").json()
    board0 = _json.dumps(before.get("board"), sort_keys=True)
    genome0 = _json.dumps(before.get("genome_spec"), sort_keys=True)
    # attack a: the swarm write-back path (updates native_swarm ONLY)
    sw = [s for s in client.get("/api/v1/resources/swarm").json()["cascades"]
          if s.get("vsb_id") == vid]
    if sw:
        client.put(f"/api/v1/resources/swarm/{sw[0]['id']}", json={"name": "w345 attack rename"})
    # attack b: evolution apply WITHOUT approval
    ev = client.post(f"/api/v1/vsb/{vid}/evolve", json={"trigger": "w345"}).json()
    pre = client.post(f"/api/v1/vsb/{vid}/evolution/apply").json()
    assert pre.get("applied") is False                       # never without the Owner's CCA
    # attack c: a chief instruction (delegation, not board mutation)
    client.post("/api/v1/board/chief/instruct",
                json={"instruction": "w345 probe", "owner": "Rehan", "scope": vid,
                      "cascade_to_ceo": False})
    after = client.get(f"/api/v1/vsb/{vid}").json()
    assert _json.dumps(after.get("board"), sort_keys=True) == board0       # board untouched
    assert _json.dumps(after.get("genome_spec"), sort_keys=True) == genome0  # genome untouched

    # (2) TWIN PRE-VALIDATION fires on a HIGH-tier change (the §17.5 major-change gate):
    # a real twin verdict with an honest source (model marker, or the organism health gate on
    # the deterministic floor).
    from agentic_core.api.change_control import SubmitChangeRequest, submit_change
    sub = _ensure_loop().run_until_complete(submit_change(SubmitChangeRequest(
        title="w345 genome edit probe", change_type="genome_edit",
        description="w345 invariant probe — a deliberately HIGH-tier change",
        rationale="w345 invariant sweep", affected_systems=["genome"])))
    cid = sub["cca_id"] if isinstance(sub, dict) else getattr(sub, "cca_id", None)
    assert cid
    tp = client.post(f"/api/v1/cca/{cid}/twin-prevalidate").json()
    v = tp.get("twin_prevalidation") or {}
    assert v.get("verdict") in ("pass", "fail") and v.get("source")

    # (3) SIGNAL-BUS ATOMICITY — 8 threads × 50 concurrent fire_signal: never raises, and the
    # organism context stays coherent afterwards.
    from agentic_core.organism.biobus import biobus
    _errs = []
    def _blast():
        try:
            for i in range(50):
                biobus.fire_signal("reflex", "w345.blast", f"s{i}", 0.4)
        except Exception as e:
            _errs.append(e)
    _threads = [threading.Thread(target=_blast) for _ in range(8)]
    for t in _threads: t.start()
    for t in _threads: t.join()
    assert not _errs
    ctx = biobus.organism_context()
    assert "composite_health" in ctx and "immune" in ctx

    # (4) PLAN FRESHNESS (the honestly-restated invariant: assembled fresh on demand) — a
    # just-added objective is visible on the immediately-following read.
    client.post("/api/v1/business-plan/objective", json={
        "scope": vid, "title": "W345-FRESHNESS-MARKER", "kpi": "visible immediately"})
    plan = client.get("/api/v1/business-plan", params={"scope": vid}).json()
    assert any(o.get("title") == "W345-FRESHNESS-MARKER" for o in plan.get("objectives", []))

    # (5) SINGLE ROUTER-MOUNT POINT — every include_router call in the live tree belongs to
    # app_mvp (agent_hub is a helper the same app calls; _archive excluded).
    import re as _re
    import subprocess as _sp
    _files = _sp.run(["git", "grep", "-l", "include_router("], capture_output=True, text=True,
                     cwd=".").stdout.split()
    _offenders = []
    for _p in _files:
        if not _p.startswith("agentic_core/") or "app_mvp" in _p or "agent_hub" in _p:
            continue
        _src = open(_p, encoding="utf-8", errors="replace").read()
        if _re.search(r"^\s*\w+\.include_router\(", _src, _re.M):
            _offenders.append(_p)
    assert _offenders == [], _offenders


def test_dockerfile_copies_every_boot_path_package():
    # §16 deployment honesty (W354) — the shipped image must contain every LOCAL package app_mvp
    # imports at boot. The old Dockerfile COPYied only agentic_core + core, omitting config/ (used
    # by ai/memory + ai/logger + ~10 more) and src/ (the tool registry), so the image died at
    # import. This test is the standing contract: whatever app_mvp pulls in at boot must be COPYied.
    import sys, pathlib
    import agentic_core.app_mvp  # noqa: F401 — the exact production boot import
    repo = pathlib.Path(__file__).resolve().parent.parent
    # exclude the test harness itself (it runs inside pytest, which imports the test module +
    # conftest + integration_tests — none of which ship in the production image)
    _harness = {"integration_tests", "conftest", "test_mvp_spine", "tests"}
    boot_local = set()
    for m in list(sys.modules):
        top = m.split(".")[0]
        if top == "agentic_core" or top in _harness:
            continue
        spec = getattr(sys.modules.get(m), "__spec__", None)
        origin = getattr(spec, "origin", None) if spec else None
        if origin and str(repo) in str(origin) and "site-packages" not in str(origin) \
                and ("\\venv\\" not in str(origin) and "/venv/" not in str(origin)):
            boot_local.add(top)
    dockerfile = (repo / "Dockerfile").read_text(encoding="utf-8")
    import re as _re
    copied = set(_re.findall(r"^COPY\s+(?:\./)?([A-Za-z_][\w]*)\b", dockerfile, _re.M))
    copied.add("agentic_core")
    missing = {p for p in boot_local if p not in copied}
    assert not missing, f"Dockerfile omits boot-path packages (image would die at import): {missing}"
    # and the two the old image specifically dropped are present
    assert "config" in copied and "src" in copied


def test_store_concurrency_and_session_scoping(client, monkeypatch):
    # §12/§13/§17.5 (W348-W351) — the store layer is correct under concurrent writers, and the
    # avatar session store is owner-scoped. The Round-10 concurrency audit measured lost writes
    # in the money path (confirmed sales exceeding balance; recognised revenue dropped) and an
    # unscoped session store; a shared cross-process store_lock + a single UEG instance close them.
    import threading
    # (1) revenue events: 120 concurrent records → none dropped, full amount intact
    from agentic_core.economy.revenue import record_event, _load as _rev_load
    def _rec(i): record_event("vsb-conc-t", "revenue", 10.0, "probe", ref=f"c{i}")
    ts = [threading.Thread(target=_rec, args=(i,)) for i in range(120)]
    for t in ts: t.start()
    for t in ts: t.join()
    got = [e for e in _rev_load() if e["vsb_id"] == "vsb-conc-t"]
    assert len(got) == 120 and round(sum(e["amount_wst"] for e in got), 2) == 1200.0
    # (2) living registrations: 24 concurrent → all persisted. Cleaned up afterward so the shared
    # module registry is left as found (operate_one() rotates the GLOBAL registry, so leftover
    # entities would skew a sibling test's rotation-fairness assertion).
    from agentic_core.economy import living_vsbs as lv
    rs = [threading.Thread(target=lv.register, args=(f"vsb-cr-{i}",), kwargs={"name": f"R{i}"})
          for i in range(24)]
    for t in rs: t.start()
    for t in rs: t.join()
    assert sum(1 for k in lv._load() if k.startswith("vsb-cr-")) == 24
    from agentic_core.config import store_lock as _sl, atomic_write_json as _awj
    with _sl(lv._STORE):
        _d = lv._load()
        for _k in [k for k in _d if k.startswith("vsb-cr-")]:
            _d.pop(_k, None)
        _awj(lv._STORE, _d)
    # (3) marketplace money path under 6×2 concurrent purchases of a 100-WST listing: confirmations
    #     never exceed the balance, and the ledgers agree (charges == receipts == sales).
    lid = client.post("/api/v1/marketplace/listings", json={
        "name": "Conc probe", "description": "an honest halal test product",
        "price_wst": 100.0, "category": "product"}).json()["id"]
    from agentic_core.app_mvp import app as _app   # threads need their own client on the same app
    import glob as _glob
    from agentic_core.config import data_path as _dp2      # resolve via the app, not an env var (CI sets none)
    _rcpt_glob = str(_dp2("marketplace/receipts") / "*.json")
    _rcpt_before = len(_glob.glob(_rcpt_glob))                    # the receipts dir is module-shared
    codes = []
    def _buy():
        cc = TestClient(_app)
        for _ in range(2):
            codes.append(cc.post(f"/api/v1/marketplace/listings/{lid}/purchase",
                                 json={"user_id": "conc-buyer", "quantity": 1}).status_code)
    bs = [threading.Thread(target=_buy) for _ in range(6)]
    for t in bs: t.start()
    for t in bs: t.join()
    confirms = codes.count(200)
    assert codes.count(500) == 0                                  # no crash-after-charge
    from agentic_core.commercial.token_ledger import TokenLedger
    rec = TokenLedger().ledgers.get("conc-buyer", {})
    # the money invariant: charged for EXACTLY the confirmations, no more, no less; balance +
    # consumed conserves the starting allowance (never oversold, never charged-without-confirm).
    assert round(rec.get("total_consumed", -1), 2) == confirms * 100.0
    assert round(rec.get("balance", 0) + rec.get("total_consumed", 0), 2) == 1100.0
    assert len(_glob.glob(_rcpt_glob)) - _rcpt_before == confirms   # one NEW receipt per charge
    assert client.get(f"/api/v1/marketplace/listings/{lid}").json()["sales_count"] == confirms
    # (4) UEG chain: 6×20 concurrent appends via fresh loggers → all stored, chain valid. The
    #     truncation-detection leg runs on a THROWAWAY UEG path (not the shared module ledger,
    #     which later tests append to and verify) so it can't poison sibling tests.
    import json as _json, os as _os, tempfile as _tf
    from agentic_core.gaas.v5 import UEGLogger
    _tmp_ueg = _os.path.join(_tf.mkdtemp(), "throwaway_ueg.json")
    def _log():
        for i in range(20):
            UEGLogger(_tmp_ueg).log({"type": "conc.probe", "n": i})
    ls = [threading.Thread(target=_log) for _ in range(6)]
    for t in ls: t.start()
    for t in ls: t.join()
    g = UEGLogger(_tmp_ueg)
    n_before = len(_json.load(open(g.storage_path, encoding="utf-8"))["nodes"])
    assert n_before >= 120 and g.verify_chain().get("valid") is True   # no lost events under load
    graph = _json.load(open(g.storage_path, encoding="utf-8"))
    graph["nodes"] = graph["nodes"][:20]
    graph["root_hash"] = graph["nodes"][-1]["hash"]
    open(g.storage_path, "w", encoding="utf-8").write(_json.dumps(graph))
    assert g.verify_chain().get("valid") is False                # silent loss is detected
    # (5) avatar session store owner-scoped under auth
    monkeypatch.setenv("AUTH_ENABLED", "true")
    from agentic_core.auth import core as ac
    for u in ("s350a", "s350b"):
        us = ac._load_users(); us[u] = {"username": u, "role": "user",
                                        "hashed_password": ac._pwd_ctx.hash("pw")}; ac._save_users(us)
    tok = {u: {"Authorization": "Bearer " + client.post(
        "/api/v1/auth/token", data={"username": u, "password": "pw"}).json()["access_token"]}
        for u in ("s350a", "s350b")}
    sid = client.post("/api/v1/avatar/chat", headers=tok["s350a"],
                      json={"session_id": None, "message": "private", "context": "general"}).json()["session_id"]
    assert client.get("/api/v1/avatar/sessions").status_code == 401           # anon denied
    assert client.get(f"/api/v1/avatar/session/{sid}/history", headers=tok["s350b"]).status_code == 404
    assert client.delete(f"/api/v1/avatar/session/{sid}", headers=tok["s350b"]).status_code == 404
    assert client.get(f"/api/v1/avatar/session/{sid}/history", headers=tok["s350a"]).status_code == 200
    monkeypatch.setenv("AUTH_ENABLED", "false")


def test_evolution_auto_apply_loop_end_to_end(client):
    # §8 (W346) — the ONE leg of the sovereign-evolution loop never driven in eight rounds: the
    # Owner-enabled `evolution_auto_apply` lever applying a CCA-APPROVED proposal ON THE BEAT,
    # with the post-apply re-ship closing the loop (approval stays Owner-gated — the lever only
    # automates the post-approval application; proposals here emerge from REAL journey evidence).
    import json as _json
    from agentic_core.config import data_path
    j = client.post("/api/v1/genesis/journey", json={
        "problem": "w346 loop venture", "domain": "enterprise",
        "establish": True, "ship_output": True}).json()
    vid = (j.get("established_vsb") or {}).get("vsb_id")
    assert vid
    ev = client.post(f"/api/v1/vsb/{vid}/evolve", json={"trigger": "w346"}).json()
    cca = ev.get("evolution_pending_cca")
    assert cca and (ev.get("proposals") or [])                     # REAL evidence-based proposals
    client.post(f"/api/v1/cca/{cca}/review",
                json={"override_decision": "approved", "reviewer_notes": "w346 owner approval"})
    # the lever is OFF by default — a beat must NOT apply
    from agentic_core.organism.heartbeat import heartbeat
    from agentic_core.organism.reconfiguration import _load_config, _save_config
    loop = _ensure_loop()
    beat0 = loop.run_until_complete(heartbeat.beat())
    assert "evolution_applied" not in (beat0.get("actions") or [])
    cfg = _load_config() or {}
    cfg.setdefault("organism", {})["evolution_auto_apply"] = True
    _save_config(cfg)
    try:
        heartbeat.configure(auto_evolve=True, auto_ship=True)
        heartbeat._beats_since_evolve = 999                        # force the paced evolve tick
        applied = False
        for _ in range(3):
            beat = loop.run_until_complete(heartbeat.beat())
            applied = applied or ("evolution_applied" in (beat.get("actions") or []))
            if applied:
                break
        assert applied                                             # the lever genuinely consumes
    finally:
        heartbeat.configure(auto_evolve=False, auto_ship=False)
        cfg["organism"]["evolution_auto_apply"] = False
        _save_config(cfg)
    vsb = _json.loads((data_path("vsb_entities") / f"{vid}.json").read_text(encoding="utf-8")) \
        if (data_path("vsb_entities") / f"{vid}.json").exists() else \
        client.get(f"/api/v1/vsb/{vid}").json()
    assert vsb.get("applied_mutations")                            # mutations genuinely landed
    assert client.get(f"/api/v1/cca/{cca}").json()["status"] == "implemented"


def test_two_authenticated_users_memory_isolated(client, monkeypatch):
    # §17.5 invariant 1 (W343) — the AUTH-ON acceptance test for the round's headline: the
    # Round-8 audit ran the memory-bleed reproduction anonymous; this proves the fix under real
    # authentication. User A's confidential chat must (1) never surface in user B's shipped
    # website, (2) live in A's OWN namespace, (3) be unrecallable by B's queries in BOTH stores.
    # Route wiring matters: without owner_id threading, authenticated chat landed in the shared
    # platform namespace — scoping without teeth.
    monkeypatch.setenv("AUTH_ENABLED", "true")
    from agentic_core.auth import core as ac
    users = ac._load_users()
    for u in ("alice343", "bob343"):
        users[u] = {"username": u, "role": "user", "hashed_password": ac._pwd_ctx.hash("pw-" + u)}
    ac._save_users(users)
    tok = {u: {"Authorization": "Bearer " + client.post(
        "/api/v1/auth/token", data={"username": u, "password": "pw-" + u}).json()["access_token"]}
        for u in ("alice343", "bob343")}
    A, B = tok["alice343"], tok["bob343"]
    SECRET = "KILIMANJARO-SAFFRON merger valuation"
    client.post("/api/v1/ai/query", headers=A, json={
        "query": f"Confidential: prepare talking points for the {SECRET}. Never disclose."})
    # A's memory is in A's namespace; B cannot recall it in either store
    from agentic_core.ai.memory import memory
    assert any("KILIMANJARO" in r for r in
               memory.query_memory("saffron merger valuation talking points", owner_id="alice343"))
    assert all("KILIMANJARO" not in r for r in
               memory.query_memory("saffron merger valuation talking points", owner_id="bob343"))
    from agentic_core.ai.ceo.memory_v01 import memory_v01
    memory_v01.add_exchange("AVATAR[general]: my private board notes ORCHID-NINE", "ok",
                            owner_id="alice343")
    assert all("ORCHID-NINE" not in d for d in
               memory_v01.query("private board notes", owner_id="bob343"))
    assert any("ORCHID-NINE" in d for d in
               memory_v01.query("private board notes", owner_id="alice343"))
    # B ships a website — A's secret never reaches B's public surfaces
    est = client.post("/api/v1/genesis/establish", headers=B,
                      json={"problem": "b343 pottery cooperative", "ship_output": False}).json()
    vid = est["vsb_id"]
    assert client.post(f"/api/v1/vsb/{vid}/website", headers=B).status_code == 200
    m = client.get(f"/api/v1/vsb/{vid}/repo", headers=B).json()
    files = ({f["path"]: f.get("content", "") for f in m["files"]}
             if isinstance(m.get("files"), list) else (m.get("files") or {}))
    assert "KILIMANJARO" not in " ".join(str(v) for v in files.values())
    monkeypatch.setenv("AUTH_ENABLED", "false")


def test_round8_product_loop_contracts(client):
    # Round-8 Batch C — the operate→drift→re-ship loop made convergent and visible:
    # W340 (a zero-activity maintenance cycle no longer marks the shipped repo stale — the audit
    # measured perpetual 5-surface re-ship churn per beat; ties in the operate rotation break by
    # fewest cycles so bursts cannot starve later-registered entities — observed 23×/8×/7×),
    # W338 (an OWNER-driven economic cycle marks drift too — previously only autonomous cycles
    # did, so a user-run cycle silently outdated the shipped body).
    from agentic_core.economy import living_vsbs as lv
    from agentic_core.economy.revenue import record_event
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "w8c date-farm cooperative", "ship_output": False}).json()
    vid = est["vsb_id"]
    client.post(f"/api/v1/vsb/{vid}/repo/ship")
    lv.operate_vsb(vid)                                       # zero activity
    assert client.get(f"/api/v1/vsb/{vid}/repo/ship").json().get("stale") is False
    record_event(vid, "revenue", 500.0, "marketplace", ref="w8c")
    lv.operate_vsb(vid)                                       # real activity
    assert client.get(f"/api/v1/vsb/{vid}/repo/ship").json().get("stale") is True
    client.post(f"/api/v1/vsb/{vid}/repo/ship")
    client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "revenue": 800.0})
    s3 = client.get(f"/api/v1/vsb/{vid}/repo/ship").json()
    assert s3.get("stale") is True and "owner-driven" in str(s3.get("stale_reason", ""))
    # burst-fair rotation
    for n in ("c1", "c2", "c3"):
        lv.register(f"vsb-w8c-{n}", f"W8C {n}", entity_type="waqf_ltd_hybrid", owner="Rehan")
    from collections import Counter
    ops = [(lv.operate_one() or {}).get("vsb_id") for _ in range(9)]
    cnt = Counter(o for o in ops if o and o.startswith("vsb-w8c"))
    assert len(cnt) == 3 and max(cnt.values()) - min(cnt.values()) <= 1


def test_round8_honesty_batch_contracts(client, monkeypatch):
    # Round-8 Batch B — five confirmed findings closed, each asserted at its exact failure point:
    # W335 (the avatar's external gate was key-presence only — user media shipped to OpenAI with
    # AI_ALLOW_EXTERNAL off), W336 (floor outputs never contained the user's input; refine
    # discarded the draft), W339 (self_investment never depleted — post() moved `accounts` while
    # the check read `balances`), W342 (a 'fine wine subscription club' survived the §11 screen).
    import base64
    monkeypatch.setenv("OPENAI_API_KEY", "sk-fake-w8b")
    monkeypatch.setenv("AI_ALLOW_EXTERNAL", "false")
    r = client.post("/api/v1/avatar/transcribe",
                    files={"file": ("a.webm", b"x", "audio/webm")})
    assert r.status_code == 503 and "nothing was sent externally" in r.json()["detail"]
    assert client.post("/api/v1/avatar/speak", json={"text": "hi"}).status_code == 503
    img = base64.b64encode(b"img").decode()
    r3 = client.post("/api/v1/avatar/chat", json={
        "session_id": None, "message": "what is this?", "context": "general",
        "image_base64": img}).json()
    assert r3.get("image_is_external") is False        # never sent with the flag off
    # W336 — groundedness + draft preservation
    out = str(client.post("/api/v1/science/synthesise", json={
        "research_question": "How does mycorrhizal-networking affect olive groves?",
        "domain": "agronomy"}).json())
    assert "mycorrhizal" in out.lower() or "olive" in out.lower()
    DRAFT = "W8B-DRAFT-MARKER: my careful section.\nSecond section."
    ref = client.post("/api/v1/refine", json={
        "previous": DRAFT, "instruction": "add a risk section"}).json()["refined"]
    assert "W8B-DRAFT-MARKER" in ref and "Second section." in ref
    # W339 — the self_investment fund genuinely depletes
    from agentic_core.economy import living_vsbs as lv
    from agentic_core.economy.revenue import record_event
    lv.register("vsb-w8b", "W8B", entity_type="waqf_ltd_hybrid", owner="Rehan")
    record_event("vsb-w8b", "revenue", 1000.0, "marketplace", ref="w8b")
    lv.operate_vsb("vsb-w8b")
    flags = [lv.spend_self_investment("vsb-w8b", f"p{i}", amount=50.0).get("funded")
             for i in range(12)]
    assert any(f is False for f in flags)              # the fund runs dry — honestly
    # W342 — the adversarial vocabulary
    from agentic_core.api.compliance import screen_compliance
    assert screen_compliance("a fine wine subscription club")["overall"] == "fail"
    assert screen_compliance("an online casino with lottery draws")["overall"] == "fail"
    assert screen_compliance("a spiritual retreat centre")["overall"] != "fail"


def test_memory_no_cross_tenant_bleed_into_shipped_copy(client):
    # §17.5 invariant 1 (W332/W333) — the native memory was one GLOBAL pool with identity-blind
    # APIs: the audit reproduced one user's confidential prompt landing verbatim in another user's
    # git-committed public website (recall injected into copy generation, engine echoed it as the
    # subject). Two lines of defence: (1) generation-class callers whose output ships/persists no
    # longer inject cross-request recall (augment=False); (2) memory is tenant-stamped and recall
    # is scoped to the caller's namespace + platform. This proves both.
    SECRET = "ZANZIBAR-ORCHID acquisition takeover bid"
    client.post("/api/v1/ai/query", json={
        "query": f"Confidential: hero tagline for the {SECRET}. Do not disclose the target."})
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "a honey cooperative for local beekeepers", "ship_output": False}).json()
    vid = est["vsb_id"]
    assert client.post(f"/api/v1/vsb/{vid}/website").status_code == 200
    m = client.get(f"/api/v1/vsb/{vid}/repo").json()
    files = ({f["path"]: f.get("content", "") for f in m["files"]}
             if isinstance(m.get("files"), list) else (m.get("files") or {}))
    allcopy = " ".join(str(v) for v in files.values())
    assert "ZANZIBAR" not in allcopy and "takeover" not in allcopy   # the secret never ships
    # memory tenancy: every entry stamped; cross-tenant recall blocked, same-tenant preserved
    from agentic_core.ai.memory import memory
    import os, json as _json
    # resolve via the app's own store path — CI runs without a DATA_DIR env var (CI-caught)
    raw = _json.loads(open(memory.storage_path, encoding="utf-8").read())
    assert all((e.get("metadata") or {}).get("owner_id") for e in raw)
    memory.add_memory("User: my private alpha-strategy margin secret | AI: ok", owner_id="user-a")
    assert all("alpha-strategy" not in r
               for r in memory.query_memory("private margin strategy secret", owner_id="user-b"))
    assert any("alpha-strategy" in r
               for r in memory.query_memory("private margin strategy secret", owner_id="user-a"))


def test_service_contracts_and_self_investment_consumer(client):
    # §15×§12 (W330) — the inter-entity organ beyond one verb: entity A COMMISSIONS entity B
    # (offer → accept → deliver via a REAL cascade scoped to the provider → settle via the
    # existing gaas-gated transfer primitive, the provider's next cycle recognising the intake).
    # And 'reinvests in its own growth' is real: the waterfall's self_investment stage — the only
    # stage with no consumer — now funds the entity's OWN development actions (honest unfunded
    # record when the balance is empty; development never blocks).
    a = client.post("/api/v1/genesis/establish",
                    json={"problem": "w330t client venture", "ship_output": False}).json()["vsb_id"]
    b = client.post("/api/v1/genesis/establish",
                    json={"problem": "w330t provider venture", "ship_output": False}).json()["vsb_id"]
    ctr = client.post("/api/v1/economy/contracts", json={
        "client_vsb": a, "provider_vsb": b,
        "brief": "produce a halal supply-chain playbook", "price_wst": 120.0}).json()
    assert ctr.get("status") == "offered"
    cid = ctr["id"]
    assert client.post(f"/api/v1/economy/contracts/{cid}/accept").json().get("status") == "accepted"
    dl = client.post(f"/api/v1/economy/contracts/{cid}/deliver").json()
    assert dl.get("status") == "delivered"
    assert (dl.get("delivery") or {}).get("run_id")           # a REAL provider-scoped cascade ran
    from agentic_core.economy.revenue import record_event
    record_event(a, "revenue", 5000.0, "marketplace", ref="w330t-fund")
    from agentic_core.economy import living_vsbs as lv
    lv.operate_vsb(a)                                         # fund the client's reserve
    st = client.post(f"/api/v1/economy/contracts/{cid}/settle").json()
    assert st.get("status") == "settled"
    assert (st.get("settlement") or {}).get("transfer_id")    # the existing primitive moved it
    from agentic_core.economy.living_vsbs import spend_self_investment
    sp = spend_self_investment(a, "w330t evolution")
    assert sp.get("funded") is True and sp.get("spent_wst", 0) > 0
    assert spend_self_investment("vsb-none-w330t", "x").get("funded") is False


def test_avatar_grounding_live_and_honest(client):
    # §9 (W325) — the avatar is enterprise-aware for REAL: grounding carries the entity's LIVE
    # figures (economy cycles/distributable/holds + the latest §11 verdict), and grounded_in is
    # asserted ONLY when a grounding block actually built (previously the request's vsb_id was
    # echoed back even for a missing entity, and grounding held only static header fields).
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "w325t halal courier venture", "ship_output": False}).json()
    vid = est.get("vsb_id")
    from agentic_core.economy import living_vsbs as lv
    lv.operate_vsb(vid)
    r = client.post("/api/v1/avatar/chat", json={
        "session_id": None, "message": "How is our economy doing?",
        "context": "ceo", "vsb_id": vid}).json()
    assert r.get("grounded_in") == vid
    from agentic_core.avatars.api import _vsb_grounding
    g = _vsb_grounding(vid)
    assert "operating cycles" in g and "compliance screen" in g   # LIVE, not just headers
    r2 = client.post("/api/v1/avatar/chat", json={
        "session_id": None, "message": "hello", "context": "ceo",
        "vsb_id": "vsb-does-not-exist"}).json()
    assert r2.get("grounded_in") is None                          # never asserted for nothing
    # the platform surface sends vsb_id + language now (frontend contract, grep-verified)
    hook = open("apps/workstation-superapp/src/hooks/useAvatarSession.ts", encoding="utf-8").read()
    assert "resolveGroundingVsb()" in hook and "prefLanguageName()" in hook
    assert "speechSynthesis" in hook and "SpeechRecognition" in hook   # in-house voice both ways
    panel = open("apps/workstation-superapp/src/components/avatar/ConversationPanel.tsx",
                 encoding="utf-8").read()
    assert "setSpeakReplies" in panel                             # the toggle is REACHABLE


def test_stream_on_control_plane_and_status_measured(client):
    # §6 (W323) — three fixes to the native mandate's honesty: (1) gateway.stream previously ran
    # OUTSIDE the control plane (no learning-loop records, no circuit breaker) on three live §4
    # surfaces — a streamed serve now records a model_attempt outcome; (2) /native-ai/status
    # previously reported mode=real_model from the optimistic selection head while the floor
    # actually served — mode now follows the MEASURED most-recent server; (3) the owned model's
    # self-inflicted 25s whole-body cap is gone (streaming per-chunk timeout + adaptive budget).
    r = client.post("/api/v1/synthesis/stream",
                    json={"instructions": "w323t probe", "output_type": "report",
                          "content_ids": []})
    assert r.status_code == 200 and len(r.text) > 0
    from agentic_core.api.operational_excellence import model_health
    nat = (model_health() or {}).get("native") or {}
    assert nat.get("window_runs", 0) >= 1                    # the stream serve was RECORDED
    st = client.get("/api/v1/native-ai/status").json()
    assert st.get("mode_measured") == "deterministic_floor"  # measured, not predicted
    assert st.get("mode") == "deterministic_floor"
    assert "mode_predicted" in st and "mode_note" in st      # the prediction stays visible
    src = open("agentic_core/ai/native/orchestrator.py", encoding="utf-8").read()
    assert "asyncio.wait_for(_stream_generate()" in src      # adaptive whole-attempt budget
    assert '"stream": False' not in src                      # the bare 25s cap is gone


def test_tamper_evidence_is_genuinely_evident(client):
    # §13 (W327) — the 'tamper-evident' claims were not: /api/v1/ueg/verify walked parent links
    # without recomputing content hashes (mutation passed as chain_valid), DCMS was a write-only
    # in-memory seal (constant 1.0 integrity), and both ledgers accepted tail truncation. Now:
    # every entry's hash is RECOMPUTED, tails are anchored, DCMS persists what it sealed and
    # verifies by recomputation — proven here by actually tampering.
    import asyncio
    import json as _json
    from agentic_core.ueg.registry import ueg_ledger
    loop = _ensure_loop()
    ueg_ledger.merkle_root = ueg_ledger._load_last_root()
    for i in range(4):
        loop.run_until_complete(ueg_ledger.log_event(f"w327t-{i}", {"n": i}))
    assert client.get("/api/v1/ueg/verify").json()["chain_valid"] is True
    path = ueg_ledger.log_path
    lines = open(path, encoding="utf-8").read().splitlines()
    mid = _json.loads(lines[len(lines) // 2])
    mid["payload"]["data"]["tampered"] = True          # mutate a MIDDLE payload, hash untouched
    lines[len(lines) // 2] = _json.dumps(mid)
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    v1 = client.get("/api/v1/ueg/verify").json()
    assert v1["chain_valid"] is False
    assert "content_hash" in str(v1.get("detail", {}).get("reason", ""))
    # repair by rewriting the untampered lines, then TRUNCATE the tail
    del mid["payload"]["data"]["tampered"]
    lines[len(lines) // 2] = _json.dumps(mid)
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    assert client.get("/api/v1/ueg/verify").json()["chain_valid"] is True
    open(path, "w", encoding="utf-8").write("\n".join(lines[:-2]) + "\n")
    ueg_ledger.merkle_root = ueg_ledger._load_last_root()
    v2 = client.get("/api/v1/ueg/verify").json()
    assert v2["chain_valid"] is False
    assert "anchor" in str(v2.get("detail", {}).get("reason", ""))
    # restore a coherent head for later tests
    for i in range(2):
        loop.run_until_complete(ueg_ledger.log_event(f"w327t-restore-{i}", {"n": i}))
    # DCMS — persistent, verifiable, honestly measured
    from agentic_core.vbs.registry import dcms
    loop.run_until_complete(dcms.commit_artifact("w327t-doc", {"body": "sealed"}, "test"))
    va = dcms.verify_artifact("w327t-doc")
    assert va["valid"] is True and va["versions"][0]["basis"] == "recomputed"
    dcms.registry["w327t-doc"][0]["content"] = '{"body": "TAMPERED"}'
    assert dcms.verify_artifact("w327t-doc")["valid"] is False
    assert dcms.get_audit_integrity() < 1.0            # measured, never a constant
    assert "w327t-doc" in type(dcms)("x").registry     # persists across instances


def test_marketplace_screened_and_birth_verdict_substance_aware(client):
    # §11 (W322) — compliance INSIDE the WST economy: (1) the marketplace previously had ZERO
    # screening — a haram listing went live and was purchasable; now every listing's public text
    # is screened, FAIL → held (invisible + unpurchasable), a clean edit is the ONLY way off hold,
    # and status/compliance are never patchable around the screen. (2) the birth verdict screens
    # the entity's SUBSTANCE (challenge/concept/plan), not just clean-sounding header fields —
    # and the FAIL holds the economy (the W309 teeth).
    bad = client.post("/api/v1/marketplace/listings", json={
        "name": "Premium interest-bearing loans",
        "description": "High-interest riba lending with gambling bonus spins and alcohol rewards",
        "price_wst": 10.0, "category": "service", "tags": ["riba", "casino"]}).json()
    assert bad.get("status") == "held"
    assert (bad.get("compliance") or {}).get("overall") == "fail"
    lid = bad["id"]
    assert all(l["id"] != lid for l in client.get("/api/v1/marketplace/listings").json())
    assert client.post(f"/api/v1/marketplace/listings/{lid}/purchase",
                       json={"user_id": "u322", "quantity": 1}).status_code == 409
    ok = client.patch(f"/api/v1/marketplace/listings/{lid}", json={
        "name": "Halal community meal service",
        "description": "Ethical halal-certified meal delivery for the community",
        "tags": ["halal", "community"]}).json()
    assert ok.get("status") == "active"                       # a clean re-screen releases
    again = client.patch(f"/api/v1/marketplace/listings/{lid}", json={
        "description": "now with interest-bearing riba loans and casino gambling"}).json()
    assert again.get("status") == "held"                      # a failing edit re-holds
    direct = client.patch(f"/api/v1/marketplace/listings/{lid}", json={"status": "active"}).json()
    assert direct.get("status") == "held"                     # never patchable around the screen
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "Launch an interest-based riba lending desk with casino gambling revenue",
        "name": "Crescent Community Services", "ship_output": False}).json()
    fs = (est.get("birth_vitals") or {}).get("first_screen") or {}
    assert fs.get("overall") == "fail"                        # SUBSTANCE caught behind a clean name
    from agentic_core.economy import living_vsbs as lv
    assert lv.operate_vsb(est["vsb_id"]).get("held") == "compliance_fail_hold"


def test_resource_fabric_designs_tenant_scoped(client, monkeypatch):
    # §14×§7 (W324) — the ENTIRE user-design surface (/api/v1/resources/*) previously had zero
    # auth and zero tenant scoping: full anonymous CRUD of every tenant's compositions and swarm
    # cascades under AUTH_ENABLED=true, cascade-to-VSB binding unchecked, and update_swarm wrote
    # back into other tenants' VSB records. W252 pattern: server-stamped owner, 404-never-403,
    # binding requires VSB access, auth-off unguarded.
    monkeypatch.setenv("AUTH_ENABLED", "true")
    from agentic_core.auth import core as ac
    users = ac._load_users()
    for u in ("alice324t", "bob324t"):
        users[u] = {"username": u, "role": "user", "hashed_password": ac._pwd_ctx.hash("pw-" + u)}
    ac._save_users(users)
    tok = {u: {"Authorization": "Bearer " + client.post(
        "/api/v1/auth/token", data={"username": u, "password": "pw-" + u}).json()["access_token"]}
        for u in ("alice324t", "bob324t")}
    A, B = tok["alice324t"], tok["bob324t"]
    comp = client.post("/api/v1/resources/compose", headers=A, json={
        "name": "W324t design", "usage_area": "governance",
        "resource_ids": ["compliance"], "config": {}}).json()
    cid = comp["id"]
    assert comp.get("owner_id") == "alice324t"
    assert all(x["id"] != cid for x in
               client.get("/api/v1/resources/compositions", headers=B).json()["compositions"])
    assert client.get(f"/api/v1/resources/compositions/{cid}", headers=B).status_code == 404
    assert client.put(f"/api/v1/resources/compositions/{cid}",
                      json={"name": "hijack"}, headers=B).status_code == 404
    assert client.delete(f"/api/v1/resources/compositions/{cid}", headers=B).status_code == 404
    assert client.post(f"/api/v1/resources/compositions/{cid}/run",
                       json={"objective": "x"}, headers=B).status_code == 404
    assert client.get(f"/api/v1/resources/compositions/{cid}", headers=A).status_code == 200
    est = client.post("/api/v1/genesis/establish", headers=A,
                      json={"problem": "w324t venture", "ship_output": False}).json()
    vid = est.get("vsb_id")
    mine = [s for s in client.get("/api/v1/resources/swarm", headers=A).json()["cascades"]
            if s.get("vsb_id") == vid]
    assert mine and mine[0].get("owner_id") == "alice324t"     # Genesis stamps the entity's owner
    sid = mine[0]["id"]
    assert all(s.get("vsb_id") != vid for s in
               client.get("/api/v1/resources/swarm", headers=B).json()["cascades"])
    assert client.put(f"/api/v1/resources/swarm/{sid}",
                      json={"name": "hijacked org"}, headers=B).status_code == 404
    assert client.post("/api/v1/resources/swarm/define", headers=B, json={
        "name": "evil", "stages": [{"role": "x", "instruction": "y"}],
        "vsb_id": vid}).status_code == 404                     # binding requires VSB access
    assert client.post("/api/v1/resources/swarm/run",
                       json={"swarm_id": sid}, headers=B).status_code == 404
    monkeypatch.setenv("AUTH_ENABLED", "false")
    assert client.get(f"/api/v1/resources/compositions/{cid}").status_code == 200


def _ensure_loop():
    """Get-or-create the main-thread event loop: an earlier test's asyncio.run() unsets it, and
    Python 3.12's get_event_loop() then raises instead of creating one."""
    import asyncio
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def test_immune_quarantine_contains_for_real_and_organism_lives(client):
    # §8 (W318) — the CRITICAL immune lever was WRITE-ONLY (set, audited 'implemented', read by
    # nothing). Now: while immune_quarantine holds, OPEN circuits are genuinely CONTAINED (no
    # half-open probes; the heartbeat's proactive heal holds), the engagement is UEG-logged, the
    # CCA audit names the wired CONSUMER (the honesty rule: no consumer → never 'implemented'),
    # and release restores normal recovery. Then the organism is WATCHED living: real beats tend
    # entities (economy · compliance · stale re-ship) — observed, not just code-read.
    import asyncio
    import collections
    from agentic_core.organism.self_healing import self_healer
    for _ in range(8):
        self_healer.record_failure("w318t-probe")
    assert self_healer.is_open("w318t-probe") is True
    r = client.post("/api/v1/cca/immune-reconfigure", json={"simulate_threat": "CRITICAL"}).json()
    assert r.get("status") == "implemented"
    cca = client.get(f"/api/v1/cca/{r['cca_id']}").json()
    impl = [e for e in (cca.get("audit_trail") or []) if e.get("event") == "implemented"]
    assert impl and "self_healing" in str(impl[0].get("consumer", ""))
    _old_recovery = self_healer._recovery
    try:
        self_healer._recovery = 0.0                       # without quarantine this would half-open
        assert self_healer.is_open("w318t-probe") is True  # containment HOLDS
        assert self_healer.attempt_heal().get("quarantine_hold") is True
        assert "QUARANTINED" in str(self_healer.status())
        ev = client.get("/api/v1/gaas/ueg/events", params={"limit": 150}).json()
        types = [((e.get("data") or {}).get("type"))
                 for e in (ev.get("events") or ev.get("nodes") or [])]
        assert "immune.quarantine_engaged" in types
        from agentic_core.organism.reconfiguration import update_config, ConfigUpdateRequest
        _ensure_loop().run_until_complete(update_config(ConfigUpdateRequest(
            section="organism", key="immune_quarantine", value=False, reason="w318t release")))
        assert self_healer.is_open("w318t-probe") is False  # recovery resumes on release
    finally:
        self_healer._recovery = _old_recovery
    # the organism, WATCHED: 3 real beats with the Owner-gated autonomy flags on
    client.post("/api/v1/genesis/establish", json={"problem": "w318t watch venture"})
    from agentic_core.organism.heartbeat import heartbeat
    heartbeat.configure(auto_economy=True, auto_compliance=True, auto_ship=True)
    seen: collections.Counter = collections.Counter()
    try:
        for _ in range(3):
            beat = _ensure_loop().run_until_complete(heartbeat.beat())
            for a in (beat.get("actions") or []):
                seen[a] += 1
    finally:
        heartbeat.configure(auto_economy=False, auto_compliance=False, auto_ship=False)
    assert seen.get("operate_vsb", 0) > 0                  # the economy genuinely tended
    assert seen.get("compliance_rescreen", 0) > 0          # §11 continuously live
    # (the §13 drift→re-ship loop is asserted deterministically in the W319 stale-repo test —
    # here re-ship targets the suite-wide OLDEST stale repo, which need not be ours)


def test_purchase_is_caller_bound_under_auth(client, monkeypatch):
    # §14 (W317) — /purchase previously deducted WST from ANY caller-supplied user_id: Bob could
    # spend Alice's tokens by naming her. Under auth the purchase binds to the authenticated
    # caller (server-side); single-user mode keeps the request value (back-compat).
    monkeypatch.setenv("AUTH_ENABLED", "true")
    from agentic_core.auth import core as ac
    users = ac._load_users()
    for u in ("alice317t", "bob317t"):
        users[u] = {"username": u, "role": "user", "hashed_password": ac._pwd_ctx.hash("pw-" + u)}
    ac._save_users(users)
    tok = {u: {"Authorization": "Bearer " + client.post(
        "/api/v1/auth/token", data={"username": u, "password": "pw-" + u}).json()["access_token"]}
        for u in ("alice317t", "bob317t")}
    from agentic_core.commercial.token_ledger import TokenLedger, UserTier
    led = TokenLedger()
    led.initialize_user("alice317t", UserTier.FREE)
    a0 = led.get_ledger_report("alice317t").get("balance")
    lst = client.post("/api/v1/marketplace/listings", headers=tok["alice317t"],
                      json={"name": "W317t item", "description": "probe",
                            "price_wst": 5.0, "category": "tool"}).json()
    lid = lst.get("listing_id") or lst.get("id")
    r = client.post(f"/api/v1/marketplace/listings/{lid}/purchase", headers=tok["bob317t"],
                    json={"user_id": "alice317t", "quantity": 1}).json()
    assert r.get("user_id") == "bob317t"                            # bound to the CALLER
    assert TokenLedger().get_ledger_report("alice317t").get("balance") == a0


def test_establish_paths_share_one_plan_core_and_ship_clean_copy(client):
    # §4×§5 (W315) — SSE establish (the UI's primary path) previously birthed entities whose
    # Chief-owned Business Plan opened with an EMPTY concept and lost the §4.7 ops objective
    # (the seeding logic lived only inline in the blocking path). One shared core now serves
    # BOTH paths; and shipped PUBLIC website copy is scaffold-CLEANED (the native floor's
    # provenance markers / markdown headings no longer land on public pages).
    import json as _json
    import pathlib
    body = {"problem": "w315t halal logistics venture",
            "concept": "CONCEPT-W315T-XRAY smart halal cold-chain",
            "design": "modular design", "commercialisation": "b2b subscriptions",
            "operations": "run cold-chain audits weekly", "ship_output": False}
    r = client.post("/api/v1/genesis/establish/stream", json=body)
    vid = None
    for line in r.text.splitlines():
        if line.startswith("data: "):
            ev = _json.loads(line[6:])
            if ev.get("stage") == "init":
                vid = (ev.get("data") or {}).get("vsb_id")
    assert vid
    from agentic_core.api import business_plan as bp_mod
    plan = bp_mod._load(vid)
    assert "CONCEPT-W315T-XRAY" in (plan.get("concept") or "")
    assert "w315t halal logistics" in (plan.get("executive_summary") or "")
    ops = [o for o in plan.get("objectives", []) if o.get("source") == "genesis_journey.operations"]
    assert len(ops) == 1                                           # seeded once, never duplicated
    e2 = client.post("/api/v1/genesis/establish", json=body).json()
    v2 = e2.get("vsb_id") or (e2.get("entity") or {}).get("vsb_id")
    p2 = bp_mod._load(v2)
    assert "CONCEPT-W315T-XRAY" in (p2.get("concept") or "")       # blocking-path parity
    w = client.post(f"/api/v1/vsb/{v2}/website").json()
    root = pathlib.Path(w["repo_root"])
    html = "".join((root / "web" / f).read_text(encoding="utf-8")
                   for f in ("index.html", "about.html", "solution.html")
                   if (root / "web" / f).exists())
    assert html                                                    # pages genuinely shipped
    assert "Native Structured Engine" not in html
    assert "_[" not in html and "## " not in html                  # scaffold never on public pages


def test_stale_repo_loop_closes_and_records_honestly(client):
    # §13 (W319) — the STALE flag was write-only: nothing surfaced, re-shipped, or logged a stale
    # repo. Now: staleness is surfaced on every manifest read; the stale mark and the §11 economy
    # hold are UEG-logged; the Owner-gated heartbeat auto_ship re-ships the oldest stale repo on
    # the beat; the ship-level version-control record aggregates the surfaces' REAL results
    # (previously it fabricated 'QMS fail · compliance None' even when every surface passed);
    # and the repo cascade re-run EXECUTES the stored swarm design instead of discarding it.
    import asyncio
    est = client.post("/api/v1/genesis/establish", json={"problem": "w319t loop venture"}).json()
    vid = est.get("vsb_id") or (est.get("entity") or {}).get("vsb_id")
    assert vid and est.get("initial_ship", {}).get("shipped")
    from agentic_core.economy import living_vsbs as lv
    from agentic_core.economy.revenue import record_event as _rec319
    _rec319(vid, "revenue", 250.0, "marketplace", ref="w319t-drift")   # W340 — drift needs MATERIAL change
    lv.operate_vsb(vid)                                            # autonomous drift
    m = client.get(f"/api/v1/vsb/{vid}/repo").json()
    ss = m.get("ship_status") or {}
    assert ss.get("stale") is True and "operating cycle" in str(ss.get("stale_reason"))
    ev = client.get("/api/v1/gaas/ueg/events", params={"limit": 250}).json()
    types = [((e.get("data") or {}).get("type")) for e in (ev.get("events") or ev.get("nodes") or [])]
    assert "vsb.repo.stale" in types
    from agentic_core.organism.heartbeat import heartbeat
    heartbeat.configure(auto_ship=True)
    try:
        # auto_ship re-ships ONE stale repo per beat, OLDEST first — in a full-suite context other
        # entities' older stale repos are served before ours, so beat until ours refreshes.
        reshipped_any = False
        for _ in range(8):
            beat = _ensure_loop().run_until_complete(heartbeat.beat())
            reshipped_any = reshipped_any or ("reshipped_stale_repo" in (beat.get("actions") or []))
            s2 = client.get(f"/api/v1/vsb/{vid}/repo/ship").json()
            if s2.get("stale") is False:
                break
        assert reshipped_any
    finally:
        heartbeat.configure(auto_ship=False)                       # never leave the flag on
    assert s2.get("stale") is False
    msg = (s2.get("version_control") or {}).get("message", "")
    assert "compliance None" not in msg and "QMS" in msg           # honest aggregate, not fabricated
    ev2 = client.get("/api/v1/gaas/ueg/events", params={"limit": 300}).json()
    t2 = [((e.get("data") or {}).get("type")) for e in (ev2.get("events") or ev2.get("nodes") or [])]
    assert "vsb.repo.reshipped_on_drift" in t2
    casc = client.post(f"/api/v1/vsb/{vid}/repo/cascade", json={}).json()
    sca = (casc.get("repo_run") or {}).get("stored_config_applied") or {}
    assert len(sca.get("csuite_roles") or []) >= 3                 # the stored swarm design ran
    assert casc.get("repo_run", {}).get("run_id")
    from agentic_core.config import data_path, atomic_write_json, load_json_tolerant
    hist = load_json_tolerant(data_path("vsb_compliance_history.json"), {}) or {}
    hist[vid] = {"overall": "fail"}
    atomic_write_json(data_path("vsb_compliance_history.json"), hist)
    lv.operate_vsb(vid)                                            # the teeth engage...
    ev3 = client.get("/api/v1/gaas/ueg/events", params={"limit": 300}).json()
    t3 = [((e.get("data") or {}).get("type")) for e in (ev3.get("events") or ev3.get("nodes") or [])]
    assert "economy.compliance_fail_hold" in t3                    # ...tamper-evidently


def test_economy_deliverables_and_defects_tenant_scoped(client, monkeypatch):
    # §14 (W320) — the three cross-tenant surfaces the Round-6 audit confirmed OPEN are closed:
    # (1) the economy router (Bob could DRAIN Alice's reserve via /transfer and read/mutate her
    # ledger/waterfall/board-pack); (2) Living Deliverables (no owner concept — any user could
    # read/export/refine any tenant's confidential work); (3) the QMS defect store (global
    # unauthenticated read+mutate). W252 pattern: server-stamped owner, 404-never-403,
    # auth-off unguarded.
    monkeypatch.setenv("AUTH_ENABLED", "true")
    from agentic_core.auth import core as ac
    users = ac._load_users()
    for u in ("alice320t", "bob320t"):
        users[u] = {"username": u, "role": "user", "hashed_password": ac._pwd_ctx.hash("pw-" + u)}
    ac._save_users(users)
    tok = {}
    for u in ("alice320t", "bob320t"):
        r = client.post("/api/v1/auth/token", data={"username": u, "password": "pw-" + u})
        tok[u] = {"Authorization": f"Bearer {r.json()['access_token']}"}
    A, B = tok["alice320t"], tok["bob320t"]
    est = client.post("/api/v1/genesis/establish",
                      json={"problem": "w320t alice venture", "ship_output": False}, headers=A).json()
    vid = est.get("vsb_id") or (est.get("entity") or {}).get("vsb_id")
    assert vid
    # economy router scoped — the drain vector closed
    assert client.get("/api/v1/economy/status", params={"vsb_id": vid}, headers=B).status_code == 404
    assert client.get("/api/v1/economy/status", params={"vsb_id": vid}, headers=A).status_code == 200
    assert client.post("/api/v1/economy/transfer", headers=B,
                       json={"from_vsb": vid, "to_vsb": "vsb-b320t", "amount": 50.0}).status_code == 404
    assert client.get(f"/api/v1/economy/ledger/{vid}", headers=B).status_code == 404
    assert client.get("/api/v1/economy/board-pack", params={"vsb_id": vid}, headers=B).status_code == 404
    lv = client.get("/api/v1/economy/living-vsbs", headers=B).json()
    assert all(v.get("vsb_id") != vid for v in lv.get("living_vsbs", []))
    # deliverables owned + confidential
    good = ("## Executive Summary\nA substantive body of real work with enough content to pass "
            "the substance floor of the quality gate for this contract test.\n## Analysis\n"
            "Detailed real analysis follows here with specifics and structure.\n"
            "## Recommendations\nConcrete next steps.")
    d = client.post("/api/v1/deliverables/produce", headers=A,
                    json={"type": "report", "brief": "alice confidential", "content": good}).json()
    assert d.get("owner_id") == "alice320t"
    assert all(x["id"] != d["id"] for x in
               client.get("/api/v1/deliverables", headers=B).json()["deliverables"])
    assert client.get(f"/api/v1/deliverables/{d['id']}", headers=B).status_code == 404
    assert client.get(f"/api/v1/deliverables/{d['id']}/export",
                      params={"format": "md"}, headers=B).status_code == 404
    assert client.get(f"/api/v1/deliverables/{d['id']}/export",
                      params={"format": "md"}, headers=A).status_code == 200
    assert client.post(f"/api/v1/deliverables/{d['id']}/regenerate",
                       json={"content": "## X\nhijack"}, headers=B).status_code == 404
    # QMS defects owner-stamped + scoped
    client.post("/api/v1/deliverables/produce", headers=A,
                json={"type": "report", "brief": "alice stub", "content": "TODO"})
    adefs = client.get("/api/v1/vbs/qms/defects", headers=A).json()["defects"]
    bdefs = client.get("/api/v1/vbs/qms/defects", headers=B).json()["defects"]
    mine = [x for x in adefs if x.get("owner_id") == "alice320t"]
    assert mine
    assert all(x.get("owner_id") != "alice320t" for x in bdefs)
    assert client.post(f"/api/v1/vbs/qms/defects/{mine[0]['id']}/correct",
                       json={"correction": "hijack"}, headers=B).status_code == 404
    # single-user mode unguarded (back-compat)
    monkeypatch.setenv("AUTH_ENABLED", "false")
    assert client.get("/api/v1/economy/status", params={"vsb_id": vid}).status_code == 200
    assert client.get(f"/api/v1/deliverables/{d['id']}").status_code == 200


def test_materiality_hold_preserves_the_held_revenue(client):
    # §12 (W313) — a materiality hold PRESERVES the recognised revenue it holds: previously
    # consume_pending ran BEFORE the governance gates, so the hold destroyed the money and the CCA
    # approval authorised a distribution of nothing. Peek-then-consume: events consume ONLY after
    # every gate passes; the hold intercepts EVERY cycle (rotation still advances); approval
    # releases the SAME recognised money exactly once. Also: waterfall template bounds bind to the
    # VSB's STORED entity type — a nonprofit can no longer smuggle an owner share by claiming
    # entity_type='sole' at set time.
    from agentic_core.economy import living_vsbs as lv
    from agentic_core.economy.revenue import record_event, peek_pending
    lv.register("vsb-w313t", "W313 Contract", entity_type="waqf_ltd_hybrid", owner="Rehan")
    record_event("vsb-w313t", "revenue", 400000.0, "marketplace", ref="w313t")
    r1 = lv.operate_vsb("vsb-w313t")
    assert r1.get("cycle_ran") is False
    assert (r1.get("governance") or {}).get("status") == "held_for_change_control"
    assert peek_pending("vsb-w313t")["revenue"] == 400000.0        # PRESERVED, not destroyed
    assert r1.get("pending_preserved_wst") == 400000.0             # the record names it
    reg = lv._load()["vsb-w313t"]
    assert reg.get("last_operated") and reg.get("last_hold") == "held_for_change_control"
    r1b = lv.operate_vsb("vsb-w313t")                              # hold intercepts EVERY cycle
    assert r1b.get("cycle_ran") is False
    assert peek_pending("vsb-w313t")["revenue"] == 400000.0
    cca_id = (r1.get("governance") or {}).get("cca_id")
    rv = client.post(f"/api/v1/cca/{cca_id}/review",
                     json={"override_decision": "approved", "reviewer_notes": "w313t owner approval"})
    assert rv.status_code == 200
    r2 = lv.operate_vsb("vsb-w313t")
    if r2.get("cycle_ran") is False and (r2.get("governance") or {}).get("cca_id"):
        # CI-hardening: a same-second duplicate hold once shadowed the approval (tie-break now
        # fixed product-side); if a residual hold remains, approve IT and retry once — the money
        # must still be fully preserved at this point.
        assert peek_pending("vsb-w313t")["revenue"] == 400000.0
        client.post(f"/api/v1/cca/{(r2['governance'])['cca_id']}/review",
                    json={"override_decision": "approved", "reviewer_notes": "w313t dup owner approval"})
        r2 = lv.operate_vsb("vsb-w313t")
    assert r2.get("revenue_recognised_wst") == 400000.0, f"post-approval operate: {r2}"
    assert (r2.get("distributable_wst") or 0) > 0
    assert peek_pending("vsb-w313t")["revenue"] == 0.0             # consumed exactly once
    # entity-type spoof closed
    lv.register("vsb-w313t-np", "W313 NP", entity_type="nonprofit", owner="Rehan")
    w = client.post("/api/v1/economy/waterfall", json={
        "vsb_id": "vsb-w313t-np", "entity_type": "sole",
        "proportions": {"owner": 0.4, "self_investment": 0.3, "capital_fund": 0.1,
                        "user_projects": 0.1, "charity": 0.1}})
    assert w.status_code == 400                                    # bounds from the STORED type
    g = client.get("/api/v1/economy/waterfall",
                   params={"vsb_id": "vsb-w313t-np", "entity_type": "sole"}).json()
    assert g.get("entity_type") == "nonprofit"
    assert g.get("entity_type_source") == "living_registry"


def test_economy_cycles_governed_and_ueg_logged(client):
    # VSB_ECONOMIC_LEGAL_MODEL §3/§4 (binding): every distribution passes the gaas.v5 gate, EVERY
    # cycle's split is UEG-logged with per-stage amounts, and MATERIAL distributions are held for
    # Change Control approval (consumed on use). Previously the heartbeat path ran ungated+unlogged
    # and the API path's failure fallback was silent.
    import uuid as _uuid
    vid = f"w249-gov-{_uuid.uuid4().hex[:8]}"
    # 1) sub-materiality cycle: gated + an explicit economy.cycle_split UEG event with amounts
    r = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                                   "revenue": 10000, "costs": 0}).json()
    assert (r.get("governance") or {}).get("status") in ("allowed", "passed")
    assert r.get("cycle") and r["cycle"]["distributable_profit"] > 0
    ev = client.get("/api/v1/gaas/ueg/events?limit=25").json()
    evs = ev if isinstance(ev, list) else ev.get("events", [])
    splits = [(e.get("data") or e) for e in evs if (e.get("data") or e).get("type") == "economy.cycle_split"]
    assert splits, "no economy.cycle_split UEG event was logged"
    assert any(s.get("splits_wst") for s in splits)     # per-stage amounts present, not a bare checkpoint
    # 2) MATERIAL cycle: held for Change Control; owner approval unblocks exactly one cycle
    vid2 = f"w249-mat-{_uuid.uuid4().hex[:8]}"
    held = client.post("/api/v1/economy/cycle", json={"vsb_id": vid2, "entity_type": "waqf_ltd_hybrid",
                                                      "revenue": 400000, "costs": 0}).json()
    g = held.get("governance") or {}
    assert g.get("status") == "held_for_change_control" and g.get("cca_id")
    assert held.get("cycle") is None                    # the distribution did NOT run while held
    ap = client.post(f"/api/v1/cca/{g['cca_id']}/review",
                     json={"override_decision": "approved", "reviewer_notes": "owner approves"}).json()
    assert (ap.get("status") or ap.get("decision")) in ("approved", "auto_approved")
    ok = client.post("/api/v1/economy/cycle", json={"vsb_id": vid2, "entity_type": "waqf_ltd_hybrid",
                                                    "revenue": 400000, "costs": 0}).json()
    assert ok.get("cycle") and ok["cycle"]["distributable_profit"] >= 250000
    # 3) the always-on heartbeat path is governed too
    from agentic_core.economy.living_vsbs import register, operate_one
    vid3 = f"w249-hb-{_uuid.uuid4().hex[:8]}"
    register(vid3, "HB governed", "waqf_ltd_hybrid", "enterprise", "Rehan")
    # operate the round-robin until our VSB gets its tick (bounded loop; store may hold other VSBs)
    seen = None
    for _ in range(25):
        op = operate_one() or {}
        if op.get("vsb_id") == vid3:
            seen = op
            break
    assert seen is not None, "heartbeat round-robin never reached the registered VSB"
    assert seen.get("governance") == "passed" and not seen.get("error")


def test_economy_double_entry_and_period_close(client):
    # §9.1 — the virtual ledger is genuinely DOUBLE-ENTRY: every movement is a balanced posting, the
    # trial balance holds, the balance sheet balances (assets = liabilities + equity), and the CFO
    # period close rolls income/expenses into retained earnings so the next period starts clean.
    import uuid as _uuid
    vid = f"w256-books-{_uuid.uuid4().hex[:8]}"
    for rev in (10000, 5000):
        r = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                                       "revenue": rev, "costs": 0}).json()
        assert r.get("cycle")
    st = client.get(f"/api/v1/economy/board-pack?vsb_id={vid}").json()["statements"]
    pnl, bs, cf, tb = (st["profit_and_loss"], st["balance_sheet"], st["cash_flow"], st["trial_balance"])
    assert pnl["total_income_wst"] == 15000.0                      # the real cycle intake
    assert pnl["net_profit_wst"] == round(pnl["total_income_wst"] - pnl["total_expenses_wst"], 2)
    assert bs["balanced"] is True and tb["balanced"] is True       # the books genuinely balance
    assert bs["assets_total_wst"] == bs["liabilities_and_equity_total_wst"]
    assert cf["operating_receipts_wst"] == 15000.0                 # cash flow from real postings
    assert "CFO" in st["prepared_by"]
    # period close: net rolls into retained earnings; a second close covers ONLY the new period
    c1 = client.post("/api/v1/economy/close-period", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid"}).json()
    assert c1["retained_earnings_wst"] == c1["close"]["net_profit_wst"] > 0
    client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                               "revenue": 2000, "costs": 0})
    c2 = client.post("/api/v1/economy/close-period", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid"}).json()
    assert 0 < c2["close"]["net_profit_wst"] < c1["close"]["net_profit_wst"]   # new period only
    assert c2["statements"]["balance_sheet"]["balanced"] is True


def test_economy_owner_payments_virtual(client):
    import uuid as _uuid
    vid = f"test-owner-pay-{_uuid.uuid4().hex[:10]}"   # unique per run — no dependence on persisted state
    # a metabolic cycle accrues the Owner's §4 share to the owner-payments ledger
    client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                               "revenue": 10000, "costs": 0})
    st = client.get(f"/api/v1/economy/owner-payments?vsb_id={vid}").json()
    assert st["accrued_total_wst"] > 0 and st["balance_wst"] > 0
    # BINDING safeguard: real-money rails are disabled
    assert st["real_money_enabled"] is False and st["real_money_rails"] == "DISABLED"
    # a virtual payout reduces the balance and moves NO real funds
    bal = st["balance_wst"]
    r = client.post("/api/v1/economy/owner-payments/payout", json={"vsb_id": vid, "amount": round(bal / 2, 2)})
    assert r.status_code == 200, r.text
    assert r.json()["real_money_moved"] is False
    assert r.json()["remaining_balance_wst"] < bal
    # over-payout beyond the balance is rejected
    over = client.post("/api/v1/economy/owner-payments/payout", json={"vsb_id": vid, "amount": 10_000_000})
    assert over.status_code == 400


def test_economy_ventures_investment(client):
    import uuid as _uuid
    vid = f"test-ventures-{_uuid.uuid4().hex[:10]}"   # unique per run
    # candidates are ranked by the venture-scoring method
    cand = client.get("/api/v1/economy/ventures/candidates").json()
    assert len(cand["candidates"]) >= 1
    assert cand["candidates"][0].get("score") is not None
    # a cycle competitively allocates the user_projects stage and records portfolio positions
    cyc = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                                     "revenue": 10000, "costs": 0}).json()["cycle"]
    vi = cyc.get("venture_investment")
    assert vi and len(vi["positions"]) >= 1
    pf = client.get(f"/api/v1/economy/ventures/portfolio?vsb_id={vid}").json()
    assert pf["invested_total"] > 0 and pf["positions_count"] >= 1
    assert "no real funds" in (pf.get("note") or "").lower()


def test_inter_vsb_transfer_federation_seed(client):
    # Federation seed — living VSBs TRANSACT: the sender pays from its reserve fund (double-entry
    # posted, refused on insufficient funds — virtual WST is conserved), the receiver's next cycle
    # consumes the amount as intake revenue (enters its waterfall). gaas-gated + UEG-logged.
    import uuid as _uuid
    from agentic_core.economy.living_vsbs import register
    a, b = f"w262-a-{_uuid.uuid4().hex[:6]}", f"w262-b-{_uuid.uuid4().hex[:6]}"
    register(a, "Sender Co", "waqf_ltd_hybrid", "enterprise", "Rehan")
    register(b, "Receiver Co", "waqf_ltd_hybrid", "enterprise", "Rehan")
    client.post("/api/v1/economy/cycle", json={"vsb_id": a, "entity_type": "waqf_ltd_hybrid",
                                               "revenue": 10000, "costs": 0})     # funds the reserve (2000)
    t = client.post("/api/v1/economy/transfer",
                    json={"from_vsb": a, "to_vsb": b, "amount": 500, "memo": "services"}).json()
    tr = t["transfer"]
    assert tr["transfer_id"].startswith("xfer-") and tr["sender_reserve_fund_after_wst"] == 1500.0
    assert (t["governance"] or {}).get("status") in ("allowed", "passed")
    st = client.get(f"/api/v1/economy/board-pack?vsb_id={a}").json()["statements"]
    assert st["profit_and_loss"]["expenses"].get("transfer_out") == 500.0          # posted in the books
    assert st["balance_sheet"]["balanced"] is True                                 # and they still balance
    nxt = client.post("/api/v1/economy/cycle", json={"vsb_id": b, "entity_type": "waqf_ltd_hybrid",
                                                     "revenue": 1000, "costs": 0}).json()["cycle"]
    assert nxt["inter_vsb_received_wst"] == 500.0 and nxt["intake_revenue"] == 1500.0
    # conservation guards: insufficient 400 · unknown receiver 404 · self-transfer 400
    assert client.post("/api/v1/economy/transfer",
                       json={"from_vsb": a, "to_vsb": b, "amount": 999999}).status_code == 400
    assert client.post("/api/v1/economy/transfer",
                       json={"from_vsb": a, "to_vsb": "ghost-vsb", "amount": 5}).status_code == 404
    assert client.post("/api/v1/economy/transfer",
                       json={"from_vsb": a, "to_vsb": a, "amount": 5}).status_code == 400


def test_charity_owner_directives_and_grant_screening(client, monkeypatch):
    # §5 — the Owner SETS charity directives at runtime (priorities · exclusions · 100%-donation
    # rule) and every subsequent allocation honours them; EVERY grant is compliance-screened before
    # allocation; the live-signals ingestion seam is Owner-gated (403 until enabled — no fabricated
    # feeds).
    import uuid as _uuid
    d = client.post("/api/v1/economy/charity/directives", json={
        "priorities": ["famine_food", "clean_water"], "exclusions": ["dawah"],
        "require_100pct": True}).json()
    assert d["source"] == "owner_set" and "dawah" in d["exclusions"]
    vid = f"w260-char-{_uuid.uuid4().hex[:8]}"
    r = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                                   "revenue": 10000, "costs": 0}).json()
    gb = r["cycle"]["giving_back"]
    ids = [g["id"] for g in gb["grants"]]
    assert "dawah" not in ids                                  # the Owner's exclusion is honoured
    assert "famine_food" in ids                                # the Owner's priority is in the grants
    assert all(g.get("compliance") in ("pass", "review") for g in gb["grants"])   # screened, not just flagged
    assert "excluded_by_compliance" in gb                      # honest exclusions surface
    monkeypatch.delenv("CHARITY_LIVE_SIGNALS_ENABLED", raising=False)
    assert client.post("/api/v1/economy/charity/signals",
                       json={"signals": [{"id": "x", "cause": "y"}]}).status_code == 403
    # restore the 2026-06-21 defaults so later tests see the standard directive set
    client.post("/api/v1/economy/charity/directives", json={
        "priorities": ["clean_water", "orphan_sponsorship", "conflict_relief", "dawah"],
        "exclusions": [], "require_100pct": True})


def test_ventures_real_candidates_and_returns_recycle(client):
    # §6 — venture investment selects from the platform's REAL projects/VSBs (deterministic metrics
    # from live state, honestly labelled), and RETURNS RECYCLE: a recorded return queues as a pending
    # amount the next metabolic cycle consumes as intake revenue — the compounding ecosystem is real.
    import uuid as _uuid
    vid = f"w259-vent-{_uuid.uuid4().hex[:8]}"
    client.post("/api/v1/projects/", json={"title": "Halal tutoring for children",
                                           "description": "w259", "realm": "education", "domain": "education"})
    cand = client.get(f"/api/v1/economy/ventures/candidates?vsb_id={vid}").json()
    assert cand["using_demo_candidates"] is False              # the platform's REAL candidates
    assert any(c["id"].startswith(("proj:", "vsb:")) for c in cand["candidates"])
    assert cand["candidates"][0].get("metrics_source")         # honest metric provenance
    r = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                                   "revenue": 10000, "costs": 0}).json()
    vi = r["cycle"]["venture_investment"]
    assert vi["using_demo_candidates"] is False and vi["positions"]
    pf = client.get(f"/api/v1/economy/ventures/portfolio?vsb_id={vid}").json()
    hid = pf["holdings"][0]["id"]
    ret = client.post("/api/v1/economy/ventures/return",
                      json={"vsb_id": vid, "holding_id": hid, "amount": 500, "memo": "exit gain"}).json()
    assert ret["returned_wst"] == 500.0 and ret["pending_returns_wst"] >= 500.0
    nxt = client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                                     "revenue": 1000, "costs": 0}).json()["cycle"]
    assert nxt["venture_returns_recycled_wst"] == 500.0        # the return entered THIS waterfall
    assert nxt["intake_revenue"] == 1500.0
    assert client.post("/api/v1/economy/ventures/return",
                       json={"vsb_id": vid, "holding_id": "nope", "amount": 5}).status_code == 404


def test_genesis_established_vsb_is_living(client):
    # §4 — an established VSB is registered as a LIVING entity the organism autonomously tends
    est = client.post("/api/v1/genesis/establish", json={
        "problem": "autonomous living-entity test", "domain": "enterprise",
        "entity_type": "waqf_ltd_hybrid", "name": "LivingTestCo",
        "concept": "c", "design": "d", "commercialisation": "m"}).json()
    vid = est.get("vsb_id", "")
    assert vid.startswith("vsb-")
    ll = client.get("/api/v1/economy/living-vsbs").json()
    assert ll["total"] >= 1
    row = next((v for v in ll["living_vsbs"] if v["vsb_id"] == vid), None)
    assert row is not None, "established VSB not registered as living"
    assert "operating_cycles" in row and row["status"] == "living"
    assert "no real funds" in (ll.get("note") or "").lower()


def test_genesis_journey_stage_verifications(client):
    # §5 — each stage of the journey is verified/tested/validated on real measured proxies
    r = client.post("/api/v1/genesis/journey", json={"problem": "reduce energy waste in social housing",
                                                     "domain": "enterprise"})
    assert r.status_code == 200, r.text
    sv = r.json().get("stage_verifications") or {}
    for stage in ("concept", "research", "design", "operations", "commercialisation"):
        assert stage in sv, f"missing stage verification: {stage}"
        assert "score" in sv[stage] and "verified" in sv[stage] and "sections_present" in sv[stage]
    assert "/" in (r.json().get("stages_verified") or "")   # e.g. "5/5"


def test_genesis_journey_establish_seam(client):
    # §4→§5 — a journey WITHOUT establish yields no VSB
    r0 = client.post("/api/v1/genesis/journey", json={"problem": "reduce food waste in care homes",
                                                      "domain": "care"})
    assert r0.status_code == 200, r0.text
    assert r0.json().get("established_vsb") is None
    # WITH establish, the journey culminates in a living, operational VSB enterprise (one continuous flow)
    r = client.post("/api/v1/genesis/journey", json={"problem": "reduce food waste in care homes",
                    "domain": "care", "establish": True, "name": "ZeroWaste Care",
                    "entity_type": "waqf_ltd_hybrid"})
    assert r.status_code == 200, r.text
    ev = r.json().get("established_vsb") or {}
    assert ev.get("vsb_id", "").startswith("vsb-")
    assert ev.get("status") == "operational"
    assert "established living enterprise" in r.json().get("deliverable", "")


def test_economy_board_pack(client):
    import uuid as _uuid
    vid = f"test-boardpack-{_uuid.uuid4().hex[:10]}"   # unique per run
    # run a cycle so the pack has real (virtual) figures
    client.post("/api/v1/economy/cycle", json={"vsb_id": vid, "entity_type": "waqf_ltd_hybrid",
                                               "revenue": 10000, "costs": 1000})
    bp = client.get(f"/api/v1/economy/board-pack?vsb_id={vid}&entity_type=waqf_ltd_hybrid").json()
    # all capstone sections present
    for k in ("profit_and_loss", "waterfall", "owner_payments", "venture_portfolio",
              "charitable_giving", "ledger", "governance"):
        assert k in bp, f"board pack missing {k}"
    pl = bp["profit_and_loss"]
    # deterministic — read from THIS vsb's own ledger
    assert pl["total_revenue_wst"] > 0 and pl["total_distributed_wst"] > 0
    assert pl["distribution_by_stage"]["owner"] > 0   # the owner stage was distributed this cycle
    # owner-payments section present + numeric (the accrual itself is covered by its dedicated test;
    # not asserting >0 here avoids coupling to the heavily-shared owner-payments store under full-suite ordering)
    assert isinstance(bp["owner_payments"]["balance_wst"], (int, float))
    assert bp["owner_payments"]["real_money_rails"] == "DISABLED"
    assert "no real funds" in bp["disclaimer"].lower()


def test_economy_waterfall_template_constraints(client):
    # a non-distributing form must reject an owner share > 0
    bad = client.post("/api/v1/economy/waterfall", json={"vsb_id": "np-x", "entity_type": "nonprofit",
        "proportions": {"owner": 0.5, "self_investment": 0.2, "capital_fund": 0.1,
                        "user_projects": 0.1, "charity": 0.1}})
    assert bad.status_code == 400
    assert bad.json()["detail"]["violations"]
    # a capital-preserving form must reject a zero capital_fund
    bad2 = client.post("/api/v1/economy/waterfall", json={"vsb_id": "wq-x", "entity_type": "waqf",
        "proportions": {"owner": 0.1, "self_investment": 0.3, "capital_fund": 0.0,
                        "user_projects": 0.2, "charity": 0.4}})
    assert bad2.status_code == 400


def test_cca_ui_contract_shapes(client):
    """Round-11 ledger cluster 1 — the Change Control Agency page's EXACT contract, guarded so
    shape drift breaks CI instead of silently emptying the governance surface:
      - GET /api/v1/cca (NO trailing slash — the SPA catch-all intercepts '/api/v1/cca/' into a
        404 before FastAPI's slash-redirect can fire) returns {"changes": [...]} whose rows carry
        cca_id / impact_tier / lowercase status (never id / tier / UPPERCASE);
      - POST /{id}/review REQUIRES a ReviewDecision body (bodiless = 422, the old UI's bug);
      - submit signals auto-approval via status, not an auto_approved key;
      - the detail GET carries the description the expand pane renders."""
    r = client.post("/api/v1/cca/submit", json={
        "title": "UI-contract guard", "description": "cca ui contract probe",
        "change_type": "config_major", "submitted_by": "workstation-ui"})
    assert r.status_code == 200, r.text
    sub = r.json()
    cid = sub["cca_id"]
    try:
        assert "auto_approved" not in sub and sub["status"] in (
            "submitted", "under_review", "approved")
        # Trailing slash is NOT forgiven when the built SPA is served (its catch-all route
        # intercepts '/api/v1/cca/' before the slash-redirect — true in production and local dev).
        # Without dist/ (CI's backend job) the 307 redirect fires instead — so assert the 404
        # only in the SPA-mounted environment; the UI calls the bare path, correct in BOTH.
        import pathlib as _pl
        _spa = _pl.Path(__file__).resolve().parents[1] / "apps" / "workstation-superapp" / "dist" / "index.html"
        if _spa.exists():
            assert client.get("/api/v1/cca/").status_code == 404
        d = client.get("/api/v1/cca")
        assert d.status_code == 200
        body = d.json()
        assert "changes" in body and "entries" not in body
        row = next(x for x in body["changes"] if x["cca_id"] == cid)
        for key in ("cca_id", "title", "change_type", "impact_tier", "status",
                    "submitted_at", "decision"):
            assert key in row, f"list row lost {key}"
        assert "id" not in row and "tier" not in row
        assert row["status"] == row["status"].lower()
        # bodiless review (the old UI) is rejected; the fixed body is accepted
        assert client.post(f"/api/v1/cca/{cid}/review").status_code == 422
        rev = client.post(f"/api/v1/cca/{cid}/review",
                          json={"override_decision": "approved", "reviewer_notes": "contract guard"})
        assert rev.status_code == 200, rev.text
        assert rev.json()["status"] == "approved"
        det = client.get(f"/api/v1/cca/{cid}").json()
        assert det["description"] == "cca ui contract probe"
    finally:
        # keep the shared change-control store clean for sibling tests
        from agentic_core.config import data_path
        p = data_path("change_control") / f"{cid}.json"
        if p.exists():
            p.unlink()


def test_ui_response_shape_contracts(client):
    """Round-11 regression lock — the response shapes the FRONTEND actually reads.

    Round 11's headline defect class was silent response-shape drift: the Change Control page read
    keys the backend never returned, so the whole governance surface rendered empty with zero
    errors. Nothing guarded that. These assertions fail CI the moment a shape the UI depends on
    changes, instead of the user discovering an empty page.

    Each assertion names the consuming UI so the fix is obvious when it breaks.
    """
    # GovernanceHub AuditTab — "Run Manual Audit" + the stat cards + the event log
    v = client.get("/api/v1/gaas/ueg/verify")
    assert v.status_code == 200
    vj = v.json()
    for key in ("valid", "events", "root_hash"):
        assert key in vj, f"AuditTab stat cards read verify.{key}"
    assert isinstance(vj["valid"], bool) and isinstance(vj["events"], int)

    # Force at least one real UEG event so the row assertions below are NEVER vacuous (a fresh
    # DATA_DIR starts with an empty ledger — an `if rows:` guard would silently assert nothing).
    client.post("/api/v1/gaas/intercept", json={"intent": "ui_shape_contract_probe"})
    ev = client.get("/api/v1/gaas/ueg/events?limit=5")
    assert ev.status_code == 200
    evj = ev.json()
    assert "events" in evj, "AuditTab reads events[]"
    assert evj["events"], "expected at least one UEG event after an intercept"
    row = evj["events"][0]
    for key in ("id", "timestamp", "data", "hash"):
        assert key in row, f"AuditTab event rows read {key}"

    # Deliverables page — the list and the type selector
    # Produce one real deliverable first — otherwise a fresh DATA_DIR yields an empty list and the
    # row-shape assertions below would pass without ever running (a vacuous guard).
    made = client.post("/api/v1/deliverables/produce", json={
        "type": "report", "title": "UI shape contract probe",
        "brief": "a short probe deliverable for the UI response-shape contract"})
    assert made.status_code == 200, made.text
    dl = client.get("/api/v1/deliverables")
    assert dl.status_code == 200
    dlj = dl.json()
    assert "deliverables" in dlj, "Deliverables page reads d.deliverables[]"
    assert dlj["deliverables"], "expected the produced deliverable in the list"
    row = dlj["deliverables"][0]
    for key in ("id", "type", "title", "versions", "served_by"):
        assert key in row, f"Deliverables list rows read {key}"

    types = client.get("/api/v1/deliverables/types")
    assert types.status_code == 200
    assert "types" in types.json(), "Deliverables page reads d.types"

    # SolutionsPlatform readiness check + CEOChat retry both probe this
    st = client.get("/api/v1/native-ai/status")
    assert st.status_code == 200

    # VSBEconomy — BOTH branches of the metabolic cycle must stay distinguishable: a normal cycle
    # returns a cycle object, and a MATERIAL one returns cycle:null + a governance hold. The UI
    # renders the hold card off exactly this shape (it was invisible before Round 11).
    cyc = client.post("/api/v1/economy/cycle", json={
        "vsb_id": "shape-contract-probe", "entity_type": "waqf_ltd_hybrid",
        "revenue": 5000, "costs": 500})
    assert cyc.status_code == 200, cyc.text
    cj = cyc.json()
    assert "cycle" in cj and "governance" in cj, "VSBEconomy reads d.cycle and d.governance"
    if cj["cycle"] is None:
        assert isinstance(cj["governance"], dict) and "status" in cj["governance"], \
            "a held cycle must carry a governance object the hold card can render"
    else:
        for key in ("intake_revenue", "distributable_profit", "circulation"):
            assert key in cj["cycle"], f"the cycle result card reads cycle.{key}"


def test_user_workspace_store(client):
    """§9 — the user's OWN durable workspace (My Work history + interface preferences).

    Before this, history lived in one browser's localStorage: it did not follow the user to another
    device, and on a shared browser one person's work was visible to the next (W352 cleared it on
    identity change — the honest minimum, not the fix). This guards the real store: round-trip,
    the caps, and the auth-off single-user path. Cross-user ISOLATION is proven separately in the
    auth-on probe (a token-bearing client cannot be built in this auth-off suite)."""
    body = {
        "history": [{
            "id": "ws-probe-1", "kind": "domain-tool", "title": "workspace probe",
            "output": "o" * 30_000,           # over the 24k cap
            "input": "i" * 900,               # over the 400 cap
            "versions": [{"output": "v", "refinedAt": 1}] * 9,   # over the 5 cap
            "ts": 1,
        }],
        "prefs": {"fontScale": "large", "tone": "neutral"},
    }
    r = client.put("/api/v1/user/workspace", json=body)
    assert r.status_code == 200, r.text

    g = client.get("/api/v1/user/workspace")
    assert g.status_code == 200
    doc = g.json()
    assert doc["count"] == 1
    assert doc["prefs"]["fontScale"] == "large", "prefs must survive the round trip"
    rec = doc["history"][0]
    # the server enforces its own caps — a client cannot push an unbounded blob into the store
    assert len(rec["output"]) == 24_000, f"output cap not enforced ({len(rec['output'])})"
    assert len(rec["input"]) == 400, f"input cap not enforced ({len(rec['input'])})"
    assert len(rec["versions"]) == 5, f"version cap not enforced ({len(rec['versions'])})"

    # the delete control clears the server copy
    d = client.delete("/api/v1/user/workspace")
    assert d.status_code == 200 and d.json()["cleared"] is True
    assert client.get("/api/v1/user/workspace").json()["count"] == 0

    # a workspace is stored per owner id, so two owners never share a file even in single-user mode
    client.put("/api/v1/user/workspace", json={"history": [{"id": "a", "output": "A"}],
                                              "prefs": {}, "owner_id": "owner-a"})
    client.put("/api/v1/user/workspace", json={"history": [{"id": "b", "output": "B"}],
                                               "prefs": {}, "owner_id": "owner-b"})
    a = client.get("/api/v1/user/workspace?owner_id=owner-a").json()
    b = client.get("/api/v1/user/workspace?owner_id=owner-b").json()
    assert a["history"][0]["output"] == "A" and b["history"][0]["output"] == "B", \
        "workspaces must be per-owner, never a single shared file"


def test_tenancy_matrix_user_data_routes():
    """W364 — the MECHANICAL tenancy matrix: every route on a user-data surface must declare a
    tenancy dependency.

    Round 12 found the projects module had NO ownership at all: under AUTH_ENABLED any signed-in
    user could list, read and permanently DELETE another user's projects. It was missed because
    nothing checked mechanically — each surface was secured by hand, one audit at a time. This test
    enumerates the live route table and fails the moment a user-data route loses (or ships without)
    its tenancy dependency.

    `require_admin` counts as protection — it is a stricter gate than per-owner scoping.
    """
    import inspect
    from agentic_core.app_mvp import app as _app
    from agentic_core.auth.core import get_current_user, require_admin

    # Surfaces that hold or mutate a USER's own data. Platform-wide status/catalogue/config routes
    # are deliberately not listed — they expose no tenant data.
    USER_DATA_PREFIXES = (
        "/api/v1/projects",
        "/api/v1/user/",
        "/api/v1/vsb/",
        "/api/v1/avatar/",
        "/api/v1/deliverables",
    )
    # Honest exemptions: routes on those prefixes that are genuinely not per-user.
    # Each exemption states WHY it holds no tenant data — never a blanket suppression.
    EXEMPT = {
        "/api/v1/projects/stats/summary",           # aggregate counts, no tenant content
        "/api/v1/projects/governance/proposals",    # the SHARED stage-proposal queue (not per-user)
        "/api/v1/projects/governance/proposals/{proposal_id}/vote",  # a vote on that shared queue
        "/api/v1/deliverables/types",               # static catalogue of deliverable types
        "/api/v1/deliverables/output-formats",      # static catalogue of export formats
        "/api/v1/avatar/status",                    # platform availability, not a user's session
        "/api/v1/avatar/speak",                     # stateless text->audio transform, stores nothing
        "/api/v1/avatar/transcribe",                # stateless audio->text transform, stores nothing
    }

    unprotected = []
    for r in _app.routes:
        path = getattr(r, "path", None)
        ep = getattr(r, "endpoint", None)
        methods = getattr(r, "methods", None)
        if not (path and ep and methods):
            continue
        if not path.startswith(USER_DATA_PREFIXES):
            continue
        if path in EXEMPT or path.rstrip("/") in EXEMPT:
            continue
        guarded = False
        try:
            for prm in inspect.signature(ep).parameters.values():
                dep = getattr(prm.default, "dependency", None)
                if dep in (get_current_user, require_admin):
                    guarded = True
                    break
        except (ValueError, TypeError):
            guarded = True   # un-introspectable — do not fabricate a failure
        if not guarded:
            unprotected.append(f"{','.join(sorted(methods - {'HEAD', 'OPTIONS'}))} {path}")

    assert not unprotected, (
        "user-data routes without a tenancy dependency (add "
        "`user: dict | None = Depends(get_current_user)` and scope with user_can_access, "
        "404-never-403):\n  " + "\n  ".join(sorted(unprotected)))


def test_projects_are_owner_scoped(client):
    """W364 — projects carry an owner and the by-id routes scope to it.

    Cross-user isolation itself is proven by the auth-on probe (this suite runs auth-off, where
    single-user mode is unguarded BY DESIGN — that back-compat is what this test pins down, plus
    the owner stamp that makes scoping possible at all)."""
    made = client.post("/api/v1/projects/", json={"title": "owner-stamp probe", "description": "d"})
    assert made.status_code == 201, made.text
    proj = made.json()
    pid = proj["id"]
    try:
        assert "owner_id" in proj, "projects must carry an owner_id for scoping to be possible"
        # auth-off: every operation still works unguarded (single-user back-compat)
        assert client.get(f"/api/v1/projects/{pid}").status_code == 200
        assert client.patch(f"/api/v1/projects/{pid}", json={"title": "renamed"}).status_code == 200
        assert client.get(f"/api/v1/projects/{pid}/outputs").status_code == 200
        assert any(p["id"] == pid for p in client.get("/api/v1/projects/").json())
    finally:
        client.delete(f"/api/v1/projects/{pid}")
    assert client.get(f"/api/v1/projects/{pid}").status_code == 404


def test_store_lock_serialises_across_processes(tmp_path):
    """W365 — `store_lock` is a CROSS-PROCESS lock; prove it across real processes.

    Round 10 built store_lock after the audit reproduced money-shaped losses on unserialised
    load-modify-write cycles (17 sales confirmed against one charge; 89% of recognised revenue
    destroyed; 196/200 constitutional UEG events lost). Its regression test used THREADS — but
    threads share one interpreter, so a thread-only test cannot distinguish a real file lock from
    an in-process one. A deployment runs multiple workers. This test spawns genuine OS processes.

    Each worker performs N lock-protected read-modify-write cycles on one shared JSON store. With
    correct serialisation the final total is exactly WORKERS*CYCLES; a lost update shows up as a
    smaller number, and a torn write as an unreadable file.
    """
    import json
    import pathlib as _pl
    import subprocess
    import sys

    store = tmp_path / "counter.json"
    store.write_text(json.dumps({"total": 0, "by_worker": {}}), encoding="utf-8")

    WORKERS, CYCLES = 4, 25
    repo_root = str(_pl.Path(__file__).resolve().parents[1])
    worker_src = (
        "import sys, json\n"
        f"sys.path.insert(0, {repo_root!r})\n"
        "from agentic_core.config import store_lock, atomic_write_json, load_json_tolerant\n"
        "from pathlib import Path\n"
        "store = Path(sys.argv[1]); wid = sys.argv[2]; cycles = int(sys.argv[3])\n"
        "for _ in range(cycles):\n"
        "    with store_lock(store):\n"
        "        doc = load_json_tolerant(store, {'total': 0, 'by_worker': {}})\n"
        "        doc['total'] = doc.get('total', 0) + 1\n"
        "        doc['by_worker'][wid] = doc['by_worker'].get(wid, 0) + 1\n"
        "        atomic_write_json(store, doc)\n"
    )

    procs = [
        subprocess.Popen([sys.executable, "-c", worker_src, str(store), f"w{i}", str(CYCLES)],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for i in range(WORKERS)
    ]
    for pr in procs:
        _out, err = pr.communicate(timeout=180)
        assert pr.returncode == 0, f"worker failed: {err.decode('utf-8', 'replace')[:400]}"

    # the store must still be readable (no torn write) and hold EVERY increment (no lost update)
    doc = json.loads(store.read_text(encoding="utf-8"))
    assert doc["total"] == WORKERS * CYCLES, (
        f"lost updates across processes: {doc['total']} of {WORKERS * CYCLES} survived "
        "— store_lock is not serialising real processes")
    assert sum(doc["by_worker"].values()) == WORKERS * CYCLES
    assert len(doc["by_worker"]) == WORKERS, "a whole worker's writes vanished"
    # no lockfile left behind to block the next writer
    assert not (tmp_path / "counter.json.lock").exists(), "lock leaked after the last release"


def test_cross_tenant_isolation_under_auth(tmp_path):
    """W366 — CI now exercises AUTH-ON isolation, not just auth-off behaviour.

    The whole suite runs in single-user (auth-off) mode, where every surface is unguarded BY
    DESIGN. That means the tenancy work (W252/W295/W320/W324/W343/W350/W363/W364) was proven only
    by hand-run probes — CI could never catch a regression that re-opened cross-user access, which
    is how the projects module stayed unowned long enough that one user could delete another's
    work. This runs the isolation checks with AUTH_ENABLED=true so a regression fails the build.

    It runs in a SUBPROCESS on purpose: flipping auth and rebinding the stores in-process would
    mean reloading modules mid-suite, and mutating shared interpreter state is exactly the class
    that has broken this suite before. A child process cannot pollute its parent.
    """
    import json
    import pathlib as _pl
    import subprocess
    import sys

    repo_root = str(_pl.Path(__file__).resolve().parents[1])
    child = r"""
import json, os, sys
sys.path.insert(0, %(root)r)
from fastapi.testclient import TestClient
from agentic_core.app_mvp import app
c = TestClient(app)
out = {}

admin = c.post("/api/v1/auth/token", data={"username": "admin", "password": os.environ["ADMIN_PASSWORD"]})
assert admin.status_code == 200, f"admin bootstrap failed: {admin.text}"
ah = {"Authorization": "Bearer " + admin.json()["access_token"]}
tok = {}
for u in ("alice", "bob"):
    c.post("/api/v1/auth/register", json={"username": u, "password": "pw-" + u + "-X1", "role": "user"}, headers=ah)
    r = c.post("/api/v1/auth/token", data={"username": u, "password": "pw-" + u + "-X1"})
    assert r.status_code == 200, u + " login failed: " + r.text
    tok[u] = {"Authorization": "Bearer " + r.json()["access_token"]}

# §9 user workspace — a client-supplied owner_id must be ignored, and no cross-user read
for u in ("alice", "bob"):
    r = c.put("/api/v1/user/workspace",
              json={"history": [{"id": u + "-1", "output": u + "-private"}],
                    "prefs": {"tone": u}, "owner_id": "SPOOF"}, headers=tok[u])
    assert r.status_code == 200, r.text
    out["stamp_" + u] = r.json()["owner_id"]
a_ws = c.get("/api/v1/user/workspace", headers=tok["alice"]).json()
out["alice_sees_own"] = a_ws["history"][0]["output"] == "alice-private"
out["alice_sees_bob"] = "bob-private" in json.dumps(a_ws)
probe = c.get("/api/v1/user/workspace?owner_id=bob", headers=tok["alice"]).json()
out["param_probe_owner"] = probe["owner_id"]
out["param_probe_leaks"] = "bob-private" in json.dumps(probe)

# projects — the surface where a cross-user DELETE was possible (W364)
made = c.post("/api/v1/projects/", json={"title": "alice project", "description": "d"}, headers=tok["alice"])
assert made.status_code == 201, made.text
pid = made.json()["id"]
out["owner_stamped"] = made.json().get("owner_id")
out["bob_lists_it"] = any(p["id"] == pid for p in c.get("/api/v1/projects/", headers=tok["bob"]).json())
out["bob_read_status"] = c.get("/api/v1/projects/" + pid, headers=tok["bob"]).status_code
out["bob_delete_status"] = c.delete("/api/v1/projects/" + pid, headers=tok["bob"]).status_code
out["alice_project_survives"] = c.get("/api/v1/projects/" + pid, headers=tok["alice"]).status_code == 200
# the owner keeps full access to their own work
out["owner_patch"] = c.patch("/api/v1/projects/" + pid, json={"title": "renamed"}, headers=tok["alice"]).status_code
out["owner_delete"] = c.delete("/api/v1/projects/" + pid, headers=tok["alice"]).status_code
print("RESULT" + json.dumps(out))
""" % {"root": repo_root}

    env = {
        **os.environ,
        "AUTH_ENABLED": "true",
        "ADMIN_PASSWORD": "ci-authon-probe-Pw9",
        "AI_DISABLE_LOCAL": "1",
        "PYTHONIOENCODING": "utf-8",
        "DATA_DIR": str(tmp_path / "data"),
        "WORKSTATION_DATA_DIR": str(tmp_path / "data"),
        "PROJECTS_DIR": str(tmp_path / "projects"),
        "WORKSTATION_UEG_PATH": str(tmp_path / "ueg.jsonl"),
    }
    proc = subprocess.run([sys.executable, "-c", child], capture_output=True, timeout=600, env=env)
    stdout = proc.stdout.decode("utf-8", "replace")
    assert proc.returncode == 0, (
        "auth-on child failed:\n" + proc.stderr.decode("utf-8", "replace")[-1500:])
    marker = [ln for ln in stdout.splitlines() if ln.startswith("RESULT")]
    assert marker, f"no result from the auth-on child:\n{stdout[-800:]}"
    res = json.loads(marker[0][len("RESULT"):])

    # the server stamps the authenticated user — a client cannot claim another owner
    assert res["stamp_alice"] == "alice" and res["stamp_bob"] == "bob", res
    # no cross-user read of the personal workspace, by body or by query parameter
    assert res["alice_sees_own"] and not res["alice_sees_bob"], res
    assert res["param_probe_owner"] == "alice" and not res["param_probe_leaks"], res
    # projects: owned, invisible to others, and NOT deletable by them
    assert res["owner_stamped"] == "alice", res
    assert not res["bob_lists_it"], "bob can list alice's project"
    assert res["bob_read_status"] == 404, "must be 404, never 403 — ids must not be probeable"
    assert res["bob_delete_status"] == 404, "bob can DELETE alice's project"
    assert res["alice_project_survives"], "alice's project did not survive bob's delete attempt"
    # and the owner still has full access to their own work
    assert res["owner_patch"] == 200 and res["owner_delete"] == 204, res


def test_ueg_first_touch_construction_is_race_free(tmp_path):
    """W367 — concurrent FIRST-TOUCH construction must never erase a logged event.

    CI caught this as 119 of 120 concurrent UEG events surviving. Root cause: the singleton's
    initialisation lived in __init__, which runs UNGUARDED — two threads constructing the logger
    for a not-yet-existing path could both run `_initialise()`, and `_initialise` writes an EMPTY
    graph. The second write could land after the first thread had already appended, destroying a
    constitutional event: silent loss from a tamper-evident ledger.

    Measured before the fix: 18 of 60 trials lost events. After: 0 of 60. This guards the window.
    """
    import json as _json
    import pathlib as _pl
    import threading as _th
    from agentic_core.gaas.v5 import UEGLogger

    THREADS, TRIALS = 6, 12
    for trial in range(TRIALS):
        path = str(tmp_path / f"ueg_{trial}.json")
        UEGLogger._instances.pop(path, None)          # force a genuine first touch
        barrier = _th.Barrier(THREADS)

        def worker(n: int, _p=path, _b=barrier):
            _b.wait()                                  # every thread hits construction together
            UEGLogger(_p).log({"type": "first_touch.probe", "n": n})

        threads = [_th.Thread(target=worker, args=(i,)) for i in range(THREADS)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        nodes = _json.loads(_pl.Path(path).read_text(encoding="utf-8"))["nodes"]
        assert len(nodes) == THREADS, (
            f"trial {trial}: {len(nodes)} of {THREADS} constitutional events survived concurrent "
            "first-touch construction — an initialisation race is erasing ledger events")
        assert UEGLogger(path).verify_chain().get("valid") is True, (
            f"trial {trial}: chain invalid after concurrent first touch")


def test_ai_memory_survives_concurrent_writes(tmp_path, monkeypatch):
    """W368 — concurrent AI-memory writes must not destroy each other.

    `add_memory` was an UNSERIALISED read-append-write, and `_write` was a bespoke temp+os.replace
    that bypassed the hardened shared writer. Measured before the fix with 8 concurrent writers x
    15 writes: **107 of 120 memories lost and 93 PermissionError raised** (os.replace fails on
    Windows when another writer holds the destination). The gateway writes here after every
    completion, so this ran on the live request path. After the fix: 0 lost, 0 raised.
    """
    import json as _json
    import threading as _th
    import importlib

    store = tmp_path / "memory.json"
    import agentic_core.ai.memory as _mem
    importlib.reload(_mem)
    m = _mem.VectorMemory()
    monkeypatch.setattr(m, "storage_path", str(store), raising=False)

    WRITERS, EACH = 8, 15
    errors: list = []

    def writer(w: int):
        for i in range(EACH):
            try:
                m.add_memory(f"probe w{w} i{i}", {"w": w})
            except Exception as exc:                     # noqa: BLE001 — recording, not swallowing
                errors.append(type(exc).__name__)

    threads = [_th.Thread(target=writer, args=(k,)) for k in range(WRITERS)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert not errors, f"concurrent memory writes raised: {sorted(set(errors))}"
    stored = _json.loads(store.read_text(encoding="utf-8"))
    assert len(stored) == WRITERS * EACH, (
        f"{WRITERS * EACH - len(stored)} of {WRITERS * EACH} memories were destroyed by "
        "concurrent writers — the read-append-write cycle is not serialised")


def test_user_store_survives_concurrent_writes(tmp_path, monkeypatch):
    """W369 — the ACCOUNT store must never be corrupted or emptied by concurrent writes.

    `_save_users` was a plain `write_text`, so two concurrent writers left the users file truncated
    mid-JSON. `_load_users()` tolerates a decode error by returning {} — so a torn write silently
    emptied EVERY account, and the admin bootstrap would then mint a brand-new admin. Reproduced
    before the fix: 20 concurrent registrations left the file unreadable (JSONDecodeError) with all
    accounts gone. After: 21 of 21 intact, file readable, no exceptions.
    """
    import json as _json
    import threading as _th
    import agentic_core.auth.core as ac

    store = tmp_path / "users.json"
    monkeypatch.setattr(ac, "_USER_STORE", store, raising=False)
    store.write_text("{}", encoding="utf-8")

    WRITERS = 20
    errors: list = []

    def register(i: int):
        try:
            with ac._users_mutation():
                users = ac._load_users()
                users[f"user{i}"] = {"username": f"user{i}", "role": "user",
                                     "hashed_password": "hashed"}
                ac._save_users(users)
        except Exception as exc:                     # noqa: BLE001 — recording, not swallowing
            errors.append(type(exc).__name__)

    threads = [_th.Thread(target=register, args=(i,)) for i in range(WRITERS)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert not errors, f"concurrent account writes raised: {sorted(set(errors))}"
    raw = store.read_text(encoding="utf-8")
    try:
        users = _json.loads(raw)
    except Exception as exc:                          # noqa: BLE001
        raise AssertionError(
            f"the account store was CORRUPTED by concurrent writes ({type(exc).__name__}); "
            "_load_users would return {} and every account would silently vanish") from exc
    assert len(users) == WRITERS, (
        f"{WRITERS - len(users)} of {WRITERS} accounts were destroyed by concurrent registration")


def test_svg_and_png_exports_are_real(client):
    """W372 — svg/png are produced for REAL, and mp4/mp3 stay honestly un-faked.

    All four were catalogue-only. Two can be produced honestly in-house (svg is a text format, png
    via Pillow) and now are; mp4/mp3 need a real media encoder that is not present, so they must
    remain catalogued — a "video" that is silently a slideshow of stills would be a fabrication.

    Asserts the bytes are genuinely valid (SVG parses as XML, PNG decodes as an image), that the
    render carries the deliverable's OWN title rather than filler, and that the card lines are
    de-duplicated and bounded — defects that only became visible by rendering the card and LOOKING
    at it (a repeated heading, and the last line colliding with the footer).
    """
    import xml.etree.ElementTree as _ET
    import agentic_core.api.deliverables as _D

    made = client.post("/api/v1/deliverables/produce", json={
        "type": "report", "title": "Media export contract probe",
        "brief": "a short probe deliverable for the svg/png export contract"})
    assert made.status_code == 200, made.text
    did = made.json()["id"]

    fmts = client.get("/api/v1/deliverables/output-formats").json()
    assert "svg" in fmts["live_ids"], "svg must be advertised as live"
    # mp4/mp3 must NOT be advertised as live while no encoder exists
    assert "mp4" not in fmts["live_ids"] and "mp3" not in fmts["live_ids"], \
        "mp4/mp3 advertised as live but no media encoder exists — that would be a fabrication"

    svg = client.get(f"/api/v1/deliverables/{did}/export?format=svg")
    assert svg.status_code == 200 and svg.headers["content-type"].startswith("image/svg+xml")
    _ET.fromstring(svg.content)                       # genuinely well-formed XML, not a stub
    assert b"Media export contract probe" in svg.content, "the render lost the deliverable's title"

    if "png" in fmts["live_ids"]:                     # Pillow-gated, exactly like pdf/docx/pptx
        png = client.get(f"/api/v1/deliverables/{did}/export?format=png")
        assert png.status_code == 200 and png.headers["content-type"] == "image/png"
        from PIL import Image
        import io as _io
        img = Image.open(_io.BytesIO(png.content))
        img.load()                                    # decodes: a real raster, not bytes labelled png
        assert img.size == (_D._CARD_W, _D._CARD_H)

    # the card's lines come from the deliverable and are de-duplicated + bounded so they fit
    doc = [x for x in _D._load() if x["id"] == did][0]
    lines = _D._card_lines(doc)
    assert len(lines) == len({ln.lower() for ln in lines}), f"duplicate card lines: {lines}"
    assert len(lines) <= _D._CARD_MAX_LINES, f"{len(lines)} lines will overlap the footer"


def test_frontend_fabrications_do_not_return():
    """W374 — the fabricated UI markers deleted in Round 11 must never come back.

    Round 11 removed handlers that invented results with no backend behind them: a "Run Manual
    Audit" that fabricated PASSED rows with random hashes, fake infrastructure provisioning, a
    scripted mission log that always ended "All systems nominal / Mission is LIVE", mock results on
    seven hub pages, thirteen fabricated flagship cards, and an invented reputation economy. That
    work was verified once by grepping the shipped bundle — but nothing STOPPED it returning.

    This is the cheap, automatable half of that protection: the exact fabricated strings must not
    reappear in the frontend source. The other half — that every control still WORKS in a real
    browser — is honestly NOT covered here; it needs a browser harness this repo does not have
    (recorded in docs/FRONTEND_DEFECT_LEDGER.md rather than left implied).
    """
    import pathlib as _pl
    import re
    import pytest as _pytest

    src = _pl.Path(__file__).resolve().parents[1] / "apps" / "workstation-superapp" / "src"
    if not src.exists():                       # backend-only checkouts
        _pytest.skip("frontend source not present")

    # Each marker is a string that only ever existed to make an unbuilt thing look real.
    FABRICATIONS = {
        "All systems nominal": "the scripted launch log that always succeeded",
        "Engine running at 100": "the QEP engine card's invented fidelity result",
        "CERT-87a1b2c3": "a fabricated issued-certificate id",
        "Historical_Makkah_360": "a fabricated AR/VR scene result",
        "2.42x": "the invented meta-voting weight",
        "142 cross-realm": "the invented contribution count",
        "Provisioning infrastructure": "fake infrastructure provisioning",
        "zero_placeholder_integrity": "the hardcoded audit inventory",
    }

    # Scan CODE only. Running this on a clean tree first showed every hit was a false positive:
    # the markers survive only inside the comments that document what was removed. A guard that
    # fires on its own documentation is noise — and the "fix" would be deleting useful history.
    def _strip_comments(text: str) -> str:
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)      # block comments
        text = re.sub(r"^\s*//.*$", " ", text, flags=re.M)       # whole-line comments
        text = re.sub(r"(?<![:'\"])//[^\n'\"]*$", " ", text, flags=re.M)   # trailing comments
        return text

    offenders = []
    for f in list(src.rglob("*.tsx")) + list(src.rglob("*.ts")):
        try:
            code = _strip_comments(f.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        for marker, why in FABRICATIONS.items():
            if marker in code:
                offenders.append(f"{f.relative_to(src)}: {marker!r} ({why})")

    assert not offenders, (
        "fabricated UI markers have returned to the frontend — these strings exist only to make an "
        "unbuilt capability look real:\n  " + "\n  ".join(sorted(offenders)))


def test_local_model_budget_cannot_throttle_the_owned_model():
    """W375 — the owned model's time budget must never be sized from failures.

    Found by walking a real user journey: a domain tool returned the deterministic floor's template
    while /native-ai/status reported a healthy real model. Cause: the budget was
    `2 x avg-of-ALL-recorded-runs` (floor 25s). That is self-reinforcing — too small a budget makes
    fast timeouts, timeouts are recorded as failures, the average falls, the next budget is smaller.
    Measured live: all-row avg 17.5s -> 35s budget, while a real generation needs ~98s isolated and
    >120s under load. Success rate fell to 15% and users got template text instead of AI output.

    After the fix a real generation completed: served_by ollama:llama3.2, 4759 chars in 145s.

    Guards the two properties that matter, without needing ollama present:
      1. a local model always gets the full allowed window, and
      2. the budget is computed from SUCCESSFUL latencies only.
    """
    # `agentic_core.ai.native.orchestrator` as a package ATTRIBUTE is a NativeOrchestrator
    # instance (a singleton shadowing the module name), so `import ... as` yields the object, not
    # the module. Import the names directly, and reach the module via sys.modules to patch it.
    import sys as _sys
    from agentic_core.ai.native.orchestrator import (LOCAL_BUDGET_FLOOR_S, LOCAL_BUDGET_CEILING_S,
                                                     local_model_budget_s)
    _mod = _sys.modules["agentic_core.ai.native.orchestrator"]

    # 1 — the floor is the full window; the adaptive term may only raise, never throttle
    assert LOCAL_BUDGET_FLOOR_S >= 180.0, (
        "a local model must get the full window — a smaller floor recreates the throttling spiral")
    assert LOCAL_BUDGET_CEILING_S >= LOCAL_BUDGET_FLOOR_S
    assert local_model_budget_s() >= 180.0

    # 2 — a model whose recent record is mostly fast FAILURES must STILL get the full window: this
    #     is exactly the poisoned-history case the old `2 x avg-of-all-rows` formula collapsed on.
    import agentic_core.api.operational_excellence as _oe
    real = _oe.model_health

    def poisoned(*a, **k):
        return {"ollama": {"window_runs": 26, "success_rate": 0.154, "avg_ms": 17501,
                           "success_runs": 4, "success_avg_ms": 18101, "success_p90_ms": 22937}}

    _oe.model_health = poisoned
    try:
        assert _mod.local_model_budget_s() >= 180.0, (
            "a poisoned failure history still throttles the owned model — the spiral is back")
    finally:
        _oe.model_health = real

    # 3 — model_health must expose SUCCESS-only latency, or an honest budget cannot be computed
    h = _oe.model_health()
    if h:
        sample = next(iter(h.values()))
        for key in ("success_runs", "success_p90_ms"):
            assert key in sample, f"model_health lost {key} — budgets would fall back to mean-of-all"


def test_client_apps_never_ship_engine_scaffolding():
    """W376 — the Web app and Phone app are PUBLIC surfaces and must not display engine internals.

    W355/W356 scrubbed the website's HTML, but the client apps render prose from `data.json`, which
    came straight from the stored blueprint — so a VSB's public web app showed end users the
    provenance marker, an "_Acting as: <role>._" line, and floor sentences ("Native structured
    content for 'X', grounded in: …"). Found by opening a generated app and LOOKING at it; every
    automated check passed because the files served 200 with real bytes.

    Note what this does and does not do: scrubbing makes floor-era content PRESENTABLE, not
    SUBSTANTIVE. Entities generated while the owned model was throttled (W375) still hold thin
    content; only regeneration with a real model serving fixes that.
    """
    from agentic_core.api.vsb import _public_prose, _entity_appdata

    raw = ("_[Workstation native structured engine — owned, no external dependency]_\n\n"
           "_Acting as: IDBO Conceptualisation engine._\n\n"
           "## INKASHAF Native structured content for 'INKASHAF', grounded in: Atmospheric water "
           "energy harvesting (domain: science).\n- atmospheric water\n\n"
           "## Problem Understanding Native structured synthesis grounded in the input's salient "
           "terms: - energy harvesting\n")

    cleaned = _public_prose(raw)
    for marker in ("Workstation native structured engine", "Acting as:", "Native structured",
                   "grounded in:"):
        assert marker.lower() not in cleaned.lower(), (
            f"{marker!r} would be shown to an end user of the VSB's public app")
    # the entity's OWN terms must survive — scrubbing must not gut real content
    assert "INKASHAF" in cleaned and "atmospheric water" in cleaned

    # and the app data actually served to the client is scrubbed at source (covers webapp + PWA,
    # which share _entity_appdata)
    appdata = _entity_appdata({
        "vsb_id": "vsb-scrub-probe", "name": "Probe VSB", "domain": "science",
        "challenge": "Atmospheric water energy harvesting",
        "genesis_blueprint": {"concept": raw},
    })
    blob = f"{appdata.get('concept','')} {appdata.get('challenge','')} " \
           f"{appdata.get('business_plan',{}).get('executive_summary','')}"
    for marker in ("Workstation native structured engine", "Acting as:", "Native structured"):
        assert marker.lower() not in blob.lower(), (
            f"{marker!r} reaches the client apps through _entity_appdata")


def test_model_health_rebaseline_preserves_history(client, tmp_path, monkeypatch):
    """W378 — re-baselining a model's health must EXCLUDE old rows from scoring, never delete them.

    W375 fixed a budget defect that had been recording the owned model's forced timeouts as its own
    failures. The fix did not clear the damage: a 14.8% success rate kept the model demoted below
    the deterministic floor, so users kept getting thin template output while probation healed it
    one attempt per ten minutes — hours of wall clock.

    Deleting those rows would erase evidence, so this records a baseline timestamp with a REQUIRED
    reason, keeps every row readable, and logs the action to the UEG.
    """
    import agentic_core.api.operational_excellence as _oe

    monkeypatch.setattr(_oe, "_STORE", tmp_path / "outcomes.json", raising=False)
    monkeypatch.setattr(_oe, "_BASELINE_STORE", tmp_path / "baselines.json", raising=False)

    import json as _json
    rows = [
        {"kind": "model_attempt", "served_by": "probe-model", "success": False,
         "duration_ms": 35000, "created_at": "2026-01-01T00:00:00Z"},
        {"kind": "model_attempt", "served_by": "probe-model", "success": False,
         "duration_ms": 35000, "created_at": "2026-01-01T00:01:00Z"},
        {"kind": "model_attempt", "served_by": "probe-model", "success": True,
         "duration_ms": 90000, "created_at": "2026-06-01T00:00:00Z"},
    ]
    (tmp_path / "outcomes.json").write_text(_json.dumps(rows), encoding="utf-8")

    before = _oe.model_health()["probe-model"]
    assert before["window_runs"] == 3 and before["success_rate"] < 0.5

    # a reason is REQUIRED — a silent reset would be exactly the evidence-erasing this avoids
    import pytest as _pytest
    with _pytest.raises(ValueError):
        _oe.set_health_baseline("probe-model", "   ")

    _oe.set_health_baseline("probe-model", "the failures measured a since-fixed budget defect",
                            at="2026-03-01T00:00:00Z")

    after = _oe.model_health()["probe-model"]
    assert after["window_runs"] == 1, "rows after the baseline should be the only ones scoring"
    assert after["success_rate"] == 1.0, "the post-fix success should now define the score"

    # HISTORY PRESERVED: the excluded rows are still on disk, readable and auditable
    kept = _json.loads((tmp_path / "outcomes.json").read_text(encoding="utf-8"))
    assert len(kept) == 3, "re-baselining must not delete recorded history"
    stored = _json.loads((tmp_path / "baselines.json").read_text(encoding="utf-8"))
    assert stored["probe-model"]["reason"], "the baseline must record WHY it was set"


def test_working_owned_model_is_not_demoted_below_the_floor():
    """W380 — a model that works most of the time must still be TRIED before the floor.

    The native floor is a FALLBACK, not a rival: ordering a model after it means the model is never
    attempted, because the floor always answers. The old rule demoted anything under a 0.6 success
    rate, and a local model measured at 58.8% (10 of 17) missed by 1.2 points — so it served nothing
    while /native-ai/status reported it healthy and §6 required it to serve. Every failure is caught
    by the floor anyway, so the true cost of trying is latency, not a broken response.

    Demotion now means "effectively dead" (< 0.25), not "imperfect".
    """
    import sys
    import agentic_core.ai.native.orchestrator  # noqa: F401 — load the module
    mod = sys.modules["agentic_core.ai.native.orchestrator"]
    import agentic_core.api.operational_excellence as _oe

    assert mod._DEMOTE_BELOW_FLOOR_RATE <= 0.35, (
        "demotion must mean effectively dead; a stricter bar silently stops the owned model serving")

    real = _oe.model_health
    try:
        # a model working ~59% of the time — the exact case that was being exiled
        _oe.model_health = lambda *a, **k: {
            "ollama": {"window_runs": 17, "success_rate": 0.588, "avg_ms": 90000,
                       "success_runs": 10, "success_p90_ms": 120000,
                       "last_at": "2099-01-01T00:00:00Z"}}
        order = mod._reorder_by_health(["ollama", "native"])
        assert order.index("ollama") < order.index("native"), (
            f"a 58.8%-success owned model was ordered behind the floor ({order}) — it would never "
            "be tried, so users get template output from a model that mostly works")

        # ...but a genuinely dead model IS demoted, so the guard still protects latency
        _oe.model_health = lambda *a, **k: {
            "ollama": {"window_runs": 20, "success_rate": 0.05, "avg_ms": 180000,
                       "success_runs": 1, "success_p90_ms": 180000,
                       "last_at": "2099-01-01T00:00:00Z"}}
        dead_order = mod._reorder_by_health(["ollama", "native"])
        assert dead_order.index("native") < dead_order.index("ollama"), (
            "an effectively-dead model must still be demoted below the floor")
    finally:
        _oe.model_health = real


def test_w392_marketplace_listing_survives_a_legacy_cp1252_file(tmp_path, monkeypatch):
    """A listing written in cp1252 must still be readable.

    Found in the real dev store: a listing file containing byte 0x97 (a cp1252 em-dash). The
    module read it with read_text() and no encoding, which uses the PLATFORM default - cp1252 on
    Windows, where it decodes, and UTF-8 on Linux, where it raises. _all_listings swallowed that
    with a bare 'except: pass', so the SAME store showed the listing in Windows development and
    silently DROPPED it in Linux CI and production. Fails on the pre-fix code under UTF-8.
    """
    import importlib
    monkeypatch.setenv('LISTINGS_DIR', str(tmp_path))
    import agentic_core.api.marketplace as mkt
    mkt = importlib.reload(mkt)

    name = 'Digital Reactor ' + chr(0x2014) + ' Legacy'
    doc = {'id': 'legacy1', 'name': name, 'description': 'd', 'price_wst': 10.0,
           'creator_id': 'someone', 'sales_count': 0, 'status': 'active'}
    legacy = tmp_path / 'legacy1.json'
    legacy.write_bytes(json.dumps(doc, ensure_ascii=False).encode('cp1252'))
    assert 0x97 in legacy.read_bytes(), 'fixture must really be cp1252-encoded'

    names = [l.name for l in mkt._all_listings()]
    assert name in names, 'a cp1252-encoded listing was dropped instead of read: %r' % (names,)
    assert mkt._load('legacy1').price_wst == 10.0

    # The cp1252 case above only FAILS pre-fix where the platform default is UTF-8 (Linux CI); on
    # Windows the old code happened to decode it. A test that cannot fail where it is written is
    # nearly worthless, so this second record uses U+0081 -> byte 0x81, which is undefined in cp1252
    # AND invalid in UTF-8. It is unreadable under either platform default and only a deliberate
    # fallback recovers it, so the test bites on every platform.
    doc2 = dict(doc, id='legacy2', name='Odd ' + chr(0x81) + ' Byte')
    (tmp_path / 'legacy2.json').write_bytes(json.dumps(doc2, ensure_ascii=False).encode('latin-1'))
    names2 = [l.name for l in mkt._all_listings()]
    assert doc2['name'] in names2, (
        'a listing readable only via an explicit fallback was dropped: %r' % (names2,))
