# Founder's guide: Workstation on your own Windows machine

DRAFT until the Owner ratifies it. Written in round W920 for row FU-742 (plan item P5.6).

## How this guide was checked

- Every command in a box below is run on the tree this guide is committed with, by the guard named under it, both in the suite and on the Windows CI job. [observed]
- None of them has been run on your own machine, so your first run there is the first that counts. [observed]

## 1. What you need first

- Windows 10 or 11, with Python 3.12 and Node.js 20 on PATH. These are the versions the Windows and frontend CI jobs use (`.github/workflows/spine.yml`). [observed]
- A copy of this repository. Every command below is run from its folder. [observed]
- Nothing in this guide switches anything on. Sign-in, self-serve sign-up, external AI and real money stay as they are until you change them, in the order of section 7. [observed]

## 2. Set up, once

```
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

- It makes a Python environment in the venv folder and installs the backend's pinned dependencies into it from requirements.txt. Then it installs the frontend's with npm install. These are the same lists the Windows and frontend CI jobs install on every push. [observed]
- It copies .env.example to .env when there is no .env. Every switch in that file is off. [observed]
- It stops at the first step that fails and says which step it was. When it finishes, it has checked that the app imports. [observed]
- Run by test_w919, which holds `setup.ps1` to files that exist and to the install steps CI runs. The script itself has not been run on a fresh Windows machine. [observed]

## 3. Start it

```
.\start_backend.bat
.\start_frontend.bat
```

- The first starts the backend on http://127.0.0.1:8000, with the environment set-up made. It is the same app the Dockerfile and render.yaml start (`agentic_core/app_mvp.py`). [observed]
- The second starts the frontend from apps\workstation-superapp, on the address it prints: port 5173, unless that port is taken. It sends every /api request to the backend. [observed]
- Run by test_w919, which starts the app exactly as `start_backend.bat` names it and reads its health from it. The folder `start_frontend.bat` opens, and its dev script, are checked to exist, and the frontend CI job builds the same app on every push. [observed]

## 4. Check that it is running

```
curl.exe http://127.0.0.1:8000/health
```

- An answer with "status": "healthy" means the backend is serving (`GET /health`). No answer means it is not running, or something else holds the port. [observed]
- Run by test_w920, which starts the app and runs this command against it: curl.exe on Windows, and curl elsewhere. [observed]

## 5. Run the tests

```
.\venv\Scripts\python.exe -m pytest integration_tests -q -n 4
```

- This runs the whole suite in four processes. The Windows CI job runs the same command on every push. [observed]
- Run without DATA_DIR set, the suite keeps its stores in folders of its own under data: _test_store and the test_ folders beside it (`integration_tests/conftest.py`). [observed]
- Your stores are under the same data folder, so take a backup first (section 6). [inference]

## 6. Back up and restore your stores

```
.\venv\Scripts\python.exe scripts\backup_stores.py backup --to D:\workstation-backups
.\venv\Scripts\python.exe scripts\backup_stores.py verify D:\workstation-backups\workstation-stores-<time>.zip
.\venv\Scripts\python.exe scripts\backup_stores.py restore D:\workstation-backups\workstation-stores-<time>.zip --into D:\restored-data
```

- Stop the backend first. A store written during the copy is copied as it was at that moment. [observed]
- backup writes one archive of every file under the data root, with each file's SHA-256 in a manifest (`scripts/backup_stores.py`). It refuses, and writes no archive, when: [observed]
  - the folder is inside the repository;
  - the folder is inside the data root;
  - the data root holds no file;
  - a store is configured outside the data root, which it names.
- verify names every missing, extra or changed file. restore checks the archive first, writes only into an empty or new folder, and then checks every file it wrote. To use the restored stores, set DATA_DIR to that folder and start the backend again. [observed]
- Run by test_w918, here and on the Windows CI job. It uses stores with nested folders, binary bytes, CRLF text and non-ASCII names, and a restore must give them back byte for byte. [observed]
- Nothing takes a backup on a schedule or copies one off the machine. Where the copies go, and how often, is yours to choose. [deferred]

## 7. The launch gates, in order

Each gate is your switch, and this guide turns none of them. They come in the order the plan rules, and each waits on the work its plan item names.

1. Sign-in (AUTH_ENABLED), after the authentication-readiness round. [plan item P4.1]
2. Self-serve sign-up (SELF_SERVE_SIGNUP), after an invited stage. [plan item P4.2]
3. External AI (AI_ALLOW_EXTERNAL and a key), as accelerants only: the owned model and the native floor still serve first. [plan item P4.3]
4. A managed database, deferred and recorded as a boundary. The stores stay files until then. [plan item P4.4]
5. A production deploy on Google Cloud, in your own account, after a measured dry run (row FU-603). [plan item P4.5]
6. Real money (REAL_MONEY_ENABLED), last, after a compliance and KYC review. Every amount until then is virtual WST. [plan item P4.6]

## 8. Where it can run, and what that costs

- This machine: what the machine and its power already cost you. Nothing above sends anything to a paid service while the switches are off. [inference]
- Docker on this machine (`docker-compose.yml`). The production image serves no pages and carries no law corpus or plan yet (row FU-1156). [observed]
- Render, as `render.yaml` describes it. The price is on Render's own pricing page, which has not been read for this guide, so no figure is given. [deferred]
- Google Cloud, plan item P4.5 (row FU-603). The price is on Google's own pages, which have not been read for this guide either. [deferred]
- No channel here is promised to cost nothing. [observed]
- Reading each provider's own price page, with the date it was read, waits on your decision in row FU-1176: whether this guide may quote a provider's published price at all. [owner decision]
