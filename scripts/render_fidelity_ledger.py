"""Render docs/VISION_FIDELITY_LEDGER.md v3 from the W446 audit workflow's final result.

Input: a JSON file holding the workflow's return value — a list of
  {region, findings:[...], verdicts:[...], summary}
Output: markdown written to the path given as argv[2] — the destination's existing line endings
are preserved (the committed ledger is CRLF); a new file is written LF. argv[5] (optional) is the
port the audited backend ran on (default 8024).

Nothing load-bearing is clipped: observed/evidence/reason/summary are rendered whole (W446 refuter
catch — the first render cut file:line citations and the refuters' own verdict sentences).

The verdict that STANDS for each finding is the refuter's corrected_verdict when a verdict
exists for that index, else the assessor's verdict (marked 'not individually refuted').
"""
import json
import sys
from collections import Counter

REGION_TITLES = {
    "R1": "§10 + §11 — the solution-quality bar, continuous compliance, and the faith-content constitution",
    "R2": "§4 + §13 — the end-to-end lifecycle (Describe → … → Run forever) and what the output IS",
    "R3": "§5 + §17.3 + §17.4 — the living organisation, the living business system layers, the three integration modes",
    "R4": "§6 + §7 + §17.2 — the native AI mandate, the reconfigurable resource fabric, the seven biomimetic layers",
    "R5": "§1–§3, §3A, §9, §14, §15, §17.1 — the offerings, the avatar/UX, democratisation, the founding principles, the 4×6×4 grid",
    "R6": "§8 + §12 + §17.5 — the biomimetic living organism, the economic organism, the ten architecture invariants",
}
ORDER = ["R1", "R2", "R3", "R4", "R5", "R6"]
# Corrections to the audit text itself, found by later refutation and verified against the code. The JSON is
# never edited (it is the record of what the assessors and refuters said); the erratum renders beside the entry.
# What a LATER round did about an entry — assigned by executing the fix against the entry's own claim, never
# by reading a diff (v2's rule). Verdicts above are as the refuters left them; this is the delta since.
STATUS = {
    "R1.2": "FIXED W449 (P1.1) — assure_delivery takes served_by; floor-served content returns qms_gate_passed=None "
            "with basis 'not assessable', nothing counted as a gate run, the record still sealed (now per delivery: "
            "content hash + server inside the seal); every chip renders slate '—' with the basis. Guard: "
            "test_w449_floor_served_gate_is_not_assessable_both_ways.",
    "R5.2": "FIXED W449 (P1.1) — ai_text() measures coverage against the PROMPT's declared sections (the floor's own "
            "extractor) and threads served_by, so a floor-served NEWS2/tafsir/CV is 'QMS —', never 'pass'.",
    "R1.4": "attestation half FIXED W449 (ledger 3.11) — Genesis withholds modelled/simulated/ranked/optimised on a tie "
            "or identical candidates with the reason (test_w449_bar_attestations_withheld_on_tie_both_ways); the "
            "§10 wording half is an OWNER RULING (P3.0).",
    "R2.5": "FIXED W449 — the tie / identical-candidates facts travel with the selected candidate and the shipped "
            "EVIDENCE.md prints them beside it; the QMS record no longer counts ranked/simulated as met on a tie.",
    "R3.6": "gate half FIXED W449 — the board pack's verdict is 'not assessable' on the floor, never 'pass' "
            "(its own generation provenance reaches the gate); the empty-concept refusal and the identical-hash "
            "disclosure remain P1.14.",
    "R3.7": "gate half FIXED W449 — the cascade's QMS chip is 'QMS gate —' on the floor and no learning-loop row "
            "records a not-assessable run as a model outcome; the green in-house chip remains P1.5.",
    "R2.0": "gate half FIXED W449 — the §10 gate no longer seals a floor-served body as verified: website and "
            "board pack by their own generation provenance; repo / webapp / mobile by the provenance the "
            "journey now STORES on the entity (the refuter caught that the entity never carried it, so those "
            "three had still fallen to the old gate). A standalone /establish declares no origin and still "
            "gets the measured gate. Body half FIXED W450 (P1.2) — a floor-served field is an honest pending "
            "state at establishment, never the floor's text; the founder's words always ship; the README and "
            "footers no longer claim 'quality-gated, compliance-screened'. The body's SUBSTANCE still needs the "
            "owned model to compose it.",
    "R2.1": "narrative half FIXED W450 (P1.2) — on the floor the board pack's narrative is 'narrative pending the "
            "owned model' (its live layers stand), never the engine's marker/role/headings frame; a model-served "
            "narrative is scrubbed of markers. The empty-concept refusal and identical-hash disclosure remain P1.14.",
    "R2.6": "FIXED W450 (P1.2) — /repo drops its web/webapp/mobile scaffold placeholders when a generated surface "
            "is on disk (measured: it had overwritten the shipped three-page site with 471 bytes while ship.json said "
            "stale=false) and labels integrated_surfaces by what is on disk; a rename marks a shipped body stale. The "
            "file/zip endpoint and clickable tree remain P3.7.",
    "R2.9": "FIXED W450 (P1.2) — the floor's fallback name `VSB — {problem[:40]}` is gone: a neutral whole-word slug "
            "from the founder's words, marked name_pending, ships NOTHING; the newborn card asks the founder and "
            "POST /vsb/{id}/name ships the deferred body (living register, swarm CEO label and plan opening follow). "
            "An optional name field precedes the journey.",
    "R3.0": "FIXED W451 (P1.3) — /api/v138/ceo/chat runs through gateway.stream_meta (in-house first, honours "
            "AI_DISABLE_LOCAL, breaker, learning loop, tenant memory, profile, guardrail), grounded in the Board's "
            "directives + living plan + business plan + the real meeting log; the terminal frame names served_by; "
            "persona, lambda tool registration, Redis mock and canned advisory deleted. The floor's answer is the "
            "floor's structured frame, labelled amber — substance needs the owned model.",
    "R4.0": "FIXED W451 (P1.3) — CEOChat renders a provenanceBadge on every answer and the pill reads from the "
            "last answer's provenance ('no answer yet' before one); no 'Planetary Strategy Active', no 'Guardian' "
            "greeting, no dead fallback detector; the SSE parser buffers split lines.",
}
ERRATA = {
    "R1.0": "the refuter's 'the tafsir route is the only Religion tool without a disclaimer key' is wrong — "
            "interfaith (agentic_core/api/religion.py:302-347) returns none either; two of the five Religion POST "
            "tools lack one. The verdict is unaffected.",
}
VERDICTS = ["STUB", "MISSING", "DOC_OVERCLAIM", "API_ONLY", "PARTIAL", "DELIVERED"]


def clip(s, n=None):
    """Flatten to one line. `n` is accepted for call-site compatibility and IGNORED — no truncation."""
    s = (s or "").replace("\r", " ").replace("\n", " ").strip()
    return s


def standing(f, v):
    if v is None:
        return f.get("verdict", "?").upper(), "unrefuted"
    cv = (v.get("corrected_verdict") or f.get("verdict") or "?").upper()
    if v.get("refuted"):
        return cv, "refuted"
    if cv != f.get("verdict", "").upper():
        return cv, "corrected"
    return cv, "survived"


def main(src, dst, head, date, port="8024"):
    regions = json.load(open(src, encoding="utf-8"))
    by_key = {r["region"]: r for r in regions}
    rows = []  # (region, idx, finding, verdict, standing_verdict, how)
    for k in ORDER:
        r = by_key.get(k)
        if not r:
            continue
        vmap = {int(v["index"]): v for v in r.get("verdicts", []) if "index" in v}
        for i, f in enumerate(r["findings"]):
            sv, how = standing(f, vmap.get(i))
            rows.append((k, i, f, vmap.get(i), sv, how))

    total = len(rows)
    assessed = Counter(f.get("verdict", "?").upper() for _, _, f, _, _, _ in rows)
    stands = Counter(sv for *_, sv, _ in rows)
    hows = Counter(how for *_, how in rows)
    refuted_up = sum(1 for _, _, f, v, sv, how in rows if how in ("refuted", "corrected")
                     and VERDICTS.index(sv) > VERDICTS.index(f.get("verdict", "PARTIAL").upper()))
    refuted_down = sum(1 for _, _, f, v, sv, how in rows if how in ("refuted", "corrected")
                       and VERDICTS.index(sv) < VERDICTS.index(f.get("verdict", "PARTIAL").upper()))

    out = []
    w = out.append
    w(f"# Vision Fidelity Ledger — v3 ({date})")
    w("")
    w(f"**Supersedes v2 (2026-09-02, baseline `d937dd37`) in full.** v2 predated W435–W445 — eleven")
    w("workstreams including the whole W437–W444 reach campaign — and prompt v11 said to weigh it")
    w(f"accordingly. This edition is regenerated from a fresh six-region assessment against a backend")
    w(f"booted from HEAD `{head}` (port :{port}, single-user mode, `AI_DISABLE_LOCAL=1`). Under that flag the")
    w("gateway routes every model call to the deterministic native floor — the configuration CI runs and")
    w("the one any machine without a local model gets (it is NOT the shipped default: with the flag unset")
    w("and Ollama discoverable, the gateway serves from the local model). What IS assessable on the floor")
    w("is whether every floor-served surface discloses it. One caveat the audit itself found (R3.0/R4.0):")
    w("a surface that bypasses the gateway — the v138 AI-CEO chat — reached the host's Ollama directly and")
    w("returned real llama3.2 prose during this audit, so 'the floor served every call' is true of the")
    w("gateway path, not of every route.")
    w("")
    w("## How this document was generated — and what that means for reading it")
    w("")
    w("Six assessors ran one vision region each against the booted HEAD, explicitly barred from three")
    w("sources: the vision's own §16, the previous edition of this ledger, and `AUTONOMOUS_PROGRESS.md`")
    w("(a record of intent, not proof). They executed routes, read handlers and components, and counted")
    w("stores. The ASSESSMENT was capped at ten findings per region, most consequential first — and every")
    w("region returned exactly ten, so **60 is the size of the cap, not the size of the gap**; a region's")
    w("eleventh-worst thing is not in this ledger. **Every finding was then attacked by an independent")
    w("refuter instructed to default to refuted** (v2 refuted six per region), who had to reproduce the gap (execute the")
    w("route, read the code, count the store) before letting it stand, and who was told to correct the")
    w("verdict UP or DOWN when the assessor had it wrong.")
    w("")
    w("Reading rules that follow from the method:")
    w("")
    w("1. **DELIVERED is understated by construction.** Assessors were told their job was the gap that")
    w("   remains, but to report DELIVERED where they verified it. Read the DELIVERED entries as the")
    w("   floor of what works, not the ceiling.")
    w(f"2. **Every one of the {total} findings was individually refuted.** The refuters reproduced")
    w(f"   {hows['survived']} as stated and overturned {hows['refuted'] + hows['corrected']} — {refuted_down} moved to a")
    w(f"   HARSHER verdict (a DELIVERED claim that was not), {refuted_up} to a MILDER one (a STUB that was real")
    w("   machinery with an undisclosed shortfall). The verdict in each heading is the one the REFUTER")
    w("   stands behind; the assessor's original is shown where it differs.")
    w("3. **The floor is the environment.** A finding that says 'floor scaffold reached the user' is")
    w("   not a complaint that no model ran — it is a finding that the surface did not SAY so, or")
    w("   certified what it could not assess. That is the §15 principle-6 line, and it binds.")
    w("4. **Refuters reproduced with their OWN inputs.** Several verdicts below carry evidence from a")
    w("   second journey, VSB, change-record or transfer the refuter created on the live backend —")
    w("   a finding that reproduces under a second, independently chosen input is stronger evidence")
    w("   than one observation.")
    w("")
    w("## Summary")
    w("")
    w("| standing verdict (after refutation) | count | as assessed |")
    w("|---|---|---|")
    for vname in VERDICTS:
        w(f"| {vname} | {stands.get(vname, 0)} | {assessed.get(vname, 0)} |")
    w(f"| **total** | **{total}** | **{total}** |")
    w("")
    w("Per region:")
    w("")
    w("| region | sections | findings | STUB | MISSING | DOC_OVERCLAIM | API_ONLY | PARTIAL | DELIVERED |")
    w("|---|---|---|---|---|---|---|---|---|")
    for k in ORDER:
        rr = [x for x in rows if x[0] == k]
        if not rr:
            continue
        c = Counter(x[4] for x in rr)
        w(f"| {k} | {REGION_TITLES[k].split(' — ')[0]} | {len(rr)} | " + " | ".join(str(c.get(v, 0)) for v in VERDICTS) + " |")
    w("")
    w("The distilled, actionable form of the surviving gaps is **prompt v11 rev 2's `<ledger>` and")
    w("`<delivery_plan>`** (`docs/FABLE_DELIVERY_PROMPT.md`). This document is the evidence base behind")
    w("them: every `<ledger>` item cites the entries here it rests on by region.index, and every plan")
    w("workstream carries the region.index entries it closes (or says it rests on another instrument —")
    w("the reach audit for the scatter, the Owner's hand for P4).")
    w("")
    w("---")
    for k in ORDER:
        r = by_key.get(k)
        if not r:
            continue
        w("")
        w(f"## {k} — {REGION_TITLES[k]}")
        w("")
        if r.get("summary"):
            w(f"**Assessor's region summary:** {clip(r['summary'], 2400)}")
            w("")
        for (kk, i, f, v, sv, how) in [x for x in rows if x[0] == k]:
            key = f"{k}.{i}"
            av = f.get("verdict", "?").upper()
            tag = f" *(assessed {av})*" if sv != av else ""
            w(f"### {k}.{i} · {f.get('section', '').strip()} — **{sv}**{tag}")
            w("")
            if f.get("severity"):
                w(f"- **severity (assessor):** {clip(f['severity'], 200)}")
            w(f"- **claim:** {clip(f.get('vision_claim'), 600)}")
            w(f"- **observed:** {clip(f.get('observed'), 1400)}")
            w(f"- **evidence:** {clip(f.get('evidence'), 900)}")
            if f.get("disclosed_to_user"):
                w(f"- **disclosed to the user:** {clip(f['disclosed_to_user'], 400)}")
            if v is None:
                w("- **refutation:** NOT individually refuted — treat as a lead, not settled")
            elif how == "refuted":
                w(f"- **refutation: REFUTED — corrected to {sv}.** {clip(v.get('reason'), 1400)}")
            elif how == "corrected":
                w(f"- **refutation: STOOD, verdict CORRECTED {av} → {sv}.** {clip(v.get('reason'), 1400)}")
            else:
                w(f"- **refutation: SURVIVED** (reproduced by the refuter). {clip(v.get('reason'), 1200)}")
            if v is not None and v.get("evidence"):
                w(f"- **refuter's evidence:** {clip(v['evidence'], 900)}")
            if f.get("smallest_honest_fix"):
                label = ("residual lead (assessor's note on a DELIVERED entry — a lead, not a defect)" if sv == "DELIVERED"
                         else "smallest honest fix (assessor's proposal — a lead, not a decision)")
                w(f"- **{label}:** {clip(f['smallest_honest_fix'], 700)}")
            if key in STATUS:
                w(f"- **status now:** {STATUS[key]}")
            if key in ERRATA:
                w(f"- **erratum (W448, verified against the code):** {ERRATA[key]}")
            w("")
        w("---")
    w("")
    w("*Regenerated by W446 from the audit workflow's journal (status lines added from W449 onward). Every entry above is an observation against")
    w("the booted HEAD named in the header — routes executed, handlers and components read, stores counted —")
    w("not a claim read from another document. No browser was driven: statements about what a user SEES")
    w("(a chip's colour, a tab's default, a rendered badge) are reasoned from the component source, and the")
    w("assessors and refuters say so where it matters.*")
    import os
    eol = (chr(13) + chr(10)) if (os.path.exists(dst) and (chr(13) + chr(10)).encode() in open(dst, 'rb').read(4096)) else chr(10)
    open(dst, 'wb').write((eol.join(out) + eol).encode('utf-8'))
    print(f"wrote {dst} ({'CRLF' if len(eol) == 2 else 'LF'}): {total} findings; standing={dict(stands)}; hows={dict(hows)}; up={refuted_up} down={refuted_down}")


if __name__ == "__main__":
    main(*sys.argv[1:6])
