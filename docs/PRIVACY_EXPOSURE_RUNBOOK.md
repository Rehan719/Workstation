# Privacy exposure runbook

This repository is **public**. Two exposures were found in it on 2026-10-14:
- credentials pasted into archived text (round W729)
- 1,276 files of the Owner's own legal and career papers (round W731)

This page explains how the platform keeps that from happening again. It also says what to do if it does.

## What keeps it out

| Where | What runs | What it does |
|---|---|---|
| Every commit on the Owner's machine | the pre-commit hook (`python scripts/install_privacy_hook.py` installs it) | refuses the commit when a staged file holds a finding |
| Every pull request (CI) and every local suite run | `test_w732_the_public_tree_holds_no_privacy_exposure` | fails on a finding anywhere in the tracked tree |
| Every push to the host | the host's secret scanning with push protection (on) | blocks a provider key at the push |
| Inside the platform | `GET /api/v1/compliance/privacy-exposure` | the same scan, read by the platform itself: findings by path and kind, and what was **not** checked |

All four use one screen, `agentic_core/privacy_exposure.py`. It looks for five kinds:

| Kind | Meaning |
|---|---|
| `credential` | a key-shaped value |
| `case_number` | a tribunal case number shape |
| `personal_document` | a document file whose name says it is a personal paper (CV, grievance, settlement, payslip, passport...) |
| `private_folder` | anything under a folder kept private |
| `private_marker` | a name or word from the Owner's private marker list |

The marker list lives **outside** the repository:
- `WORKSTATION_PRIVATE_MARKERS`, or by default `~/.workstation/private_markers.txt`
- one marker per line; `#` starts a comment

That way the screen never publishes what it protects. If the list is missing, the screen says that kind was
**not checked**. It never says the tree is clear of names it had no way to look for.

The screen reports the path, the line and the kind. It never reports the matched text.

## If a finding appears

1. **Stop.** Do not push. If the finding is already on the public host, treat it as already copied by others.
2. **See it.** Run `python scripts/privacy_check.py` (the whole tree) or open the platform route.
3. **A credential:**
   - Revoke or rotate it at its provider first. Only the Owner can, or someone acting on his yes for that one key.
   - Then replace the value with a marker.
   - Redacting the file alone does not make a published key safe.
4. **Private papers:**
   - Run `python scripts/move_to_private_store.py --dest <a private folder outside the repo> <paths>`. It does a dry run first.
   - Add `--apply` once the count is right. Every file is copied and proven byte-identical by hash before it leaves the repo, and a manifest is written beside the copies.
   - In the same commit, add the folders to `.gitignore` and to `PRIVATE_FOLDERS`.
5. **A false positive:**
   - Allow it by exact path and kind, with a reason, in `config/privacy_allow.json`.
   - Never widen a pattern to make a finding go away.
6. **History:**
   - The steps above remove the material from the tree. Git history still holds it.
   - Rewriting history, or making the repository private, is the **Owner's decision**, and it is never taken automatically.
   - Rewriting history changes every commit id and needs every clone re-made. Making the repository private changes the cost of CI.
7. **Record it.** Open a register row with `scripts/followups.py` naming the kind and the paths, never the matched text.
