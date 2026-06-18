# Contributing to Workstation

Workstation is an open-source AI-mediated workspace (Apache 2.0). Contributions welcome.

## How to contribute

1. **Domain hubs** — improve AI prompts and output quality for Religion, Science, Law, Employment, Education, Care
2. **Products** — extend Factory, Reactor, Incubator, or Synthesis Studio with new product types
3. **Persistence** — migrate file-based JSON store to SQLite/PostgreSQL
4. **Frontend** — improve UI, add export formats, improve the domain hub pages
5. **Security** — report vulnerabilities via `SECURITY.md`

## Standards

**No fabricated metrics.** No commit message, PR description, or document in this repository may use the words "certified", "converged", or "passed" without a test or measurement that would catch a false positive. Percentage claims (uptime, resolution rate, viral coefficient) require a real data source — not a calculation applied to invented inputs.

**No silent simulation.** Any endpoint on the MVP path (`app_mvp.py`) must make a real LLM call or return a clearly labelled error. Do not add `# Simulation` blocks, hardcoded responses, or `random.uniform()` calls to endpoints mounted in `app_mvp.py`.

**Working code over documentation.** A PR that adds a working feature with no comment is better than a PR that adds documentation for a feature that doesn't exist.

## RFC process

For major architectural changes: open a PR with a proposal in `docs/rfcs/`. Keep it to one page: what changes, why, what breaks, how to test it.

## Code of Conduct

See `CODE_OF_CONDUCT.md`.
