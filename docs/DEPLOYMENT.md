# Deployment Runbook — Workstation IDBO

The architecture as configured: **FastAPI backend on Render** ([`render.yaml`](../render.yaml)). The Vite/React
frontend's Vercel deployment is **retired** (Owner, 2026-10-07; config archived), and **Google Cloud Platform**
with development / beta / release channels is the planned target (see "Frontend" below). CI ([`.github/workflows/spine.yml`](../.github/workflows/spine.yml))
boots the backend + runs the integration suite and builds the frontend on every push.

> Older guides under `_archive/docs/deployment/`, `_archive/docs/deployment_guide.md`, and `_archive/docs/DEPLOY_QEP.md` are kept
> for reference but this file is the current source of truth.

## AI posture — in-house-first (no external key required)

The platform runs on its **own native AI fabric** (`agentic_core/ai/native/`): an always-available
native structured-reasoning engine (the floor), plus a self-hosted local model (Ollama) when
present. **The backend boots and fully serves with no AI key at all.** External providers
(Anthropic/OpenAI) are *optional accelerants*, used only when `AI_ALLOW_EXTERNAL=true` **and** a key
is configured. Provenance (`served_by`, `is_external`) is reported throughout, and the Operational
Excellence page (`/operations`) surfaces the in-house rate.

## Backend (Render)

1. Connect the repo; Render reads `render.yaml` (Blueprint) — Python web service,
   `pip install -r requirements.txt`, `uvicorn agentic_core.app_mvp:app`, health check `/health`.
2. Set env vars (most have safe defaults in `render.yaml`):

   | Var | Default | Notes |
   |-----|---------|-------|
   | `AI_ALLOW_EXTERNAL` | `false` | Keep `false` for pure in-house. Set `true` only to allow external accelerants. |
   | `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | unset | Optional. Only used when `AI_ALLOW_EXTERNAL=true`. OpenAI also enables avatar voice/vision. |
   | `OLLAMA_URL` | unset | Optional self-hosted model; absent → native floor. |
   | `AI_DISABLE_LOCAL` | unset | Set `1` to skip the local model and always use the native floor (fast/deterministic). |
   | `CORS_ORIGINS` | — | Your frontend origin(s), e.g. `https://<app>.vercel.app`. |
   | `AUTH_ENABLED` / `JWT_SECRET` / `ADMIN_PASSWORD` | `false` / auto / — | Set before a public launch. |
   | `DATA_DIR` | `data` | **All** persistent stores resolve through `config.data_path()` and honour `DATA_DIR` (locked by `test_data_dir_configurable`). Point it at a Render disk / mounted volume so data survives redeploys. Default (`data/`) is unchanged. |

3. **Payments are virtual/simulated by default and safe.** See the safety section below — do **not**
   set a live Stripe key.

## Docker / self-host (any container host) — COST-FREE by default

A production [`Dockerfile`](../Dockerfile) (+ [`.dockerignore`](../.dockerignore)) and
[`docker-compose.yml`](../docker-compose.yml) ship the **live backend, the pages it serves, and what its routes read**
(the pages are built inside the image; `_archive/`, the tests and every private folder are excluded; W1128).
In-house-first, file persistence on a local volume, no paid services:

```bash
docker compose up --build        # backend on :8000, persistent local volume — $0
```

The image runs `uvicorn agentic_core.app_mvp:app` as a non-root user with a `/health` healthcheck and
`DATA_DIR=/app/data` (mount a volume there for durable data). The app keeps its records in files and reads no
database: the Owner deferred managed Postgres (plan item P4.4) on 2026-10-12 until a measured need exists, so
the Postgres service kept commented in `docker-compose.yml` would hold nothing if started (W1147).

## Single-service option (backend serves the SPA)

If the frontend is **built** into `apps/workstation-superapp/dist`, the backend automatically serves it
from `/` (and falls back to the SPA shell for client routes), so the API + UI share one origin — handy
for the local dev preview and for a single-container deploy. **Fully optional**: when no `dist` exists
(CI, or the split deploy with the frontend on Vercel) the backend stays API-only and this is skipped.
`/api/*`, `/health`, and `/docs` always take precedence over the SPA fallback.

```
npm --prefix apps/workstation-superapp run build   # produce dist/
uvicorn agentic_core.app_mvp:app --port 8000       # GET / now serves the app
```

## Cost summary (what is / isn't chargeable)

**$0 by default:** local/Docker run, in-house native AI + self-hosted Ollama, file persistence, Stripe
**test** mode. **Costs money only when YOU enable it on your own account:** hosting the backend
(Render/any host; on Google Cloud about $3.65 a month for the release machine's address, costed below), a
managed Postgres, an external AI key (per-token), Stripe **live** mode (real money +
fees). Nothing chargeable is triggered autonomously.

## Frontend — Vercel RETIRED; Google Cloud planned (Owner, 2026-10-07)

- **Vercel is retired.** The Vercel project still attached to the GitHub repo points at `src/qep_frontend`, a
  folder that no longer exists, which is why its check has failed on every commit since 2026-08-30. The repo's
  `vercel.json` is archived at `_archive/deployment/vercel/workstation-superapp.vercel.json`. **The Owner deleted the
  Vercel project on 2026-10-07**, so no further Vercel checks run. Optionally, remove the Vercel GitHub app from the
  repository as well (GitHub → Settings → Integrations).
- **Planned target: Google Cloud Platform (free tier)**, with three channels:
  - **development**: every push to the working branch;
  - **beta**: a tag or a `beta` branch;
  - **release**: `main` after a reviewed merge.

  The shape chosen and costed, with its steps, is "The Google Cloud deploy, step by step" below (W1134). The
  release channel runs on one free-tier machine with its records on a disk of their own, because the platform
  keeps its records as files and Cloud Run's storage volumes do not lock them; Cloud Run stays a candidate for
  development and beta. Deploys from GitHub sign in by Workload Identity Federation (no stored keys). The
  project and the deploy are the Owner's.
- Build: root `apps/workstation-superapp` (npm workspace), `npm run build` → `dist` (Vite).

## The dry run (P4.5), measured on 2026-11-20 (W1128)

OWNER RULING 2026-11-19: the dry run is taken now; nothing is deployed and no account is touched. The image was
built from this tree and booted on a round's machine, with the memory a free-tier machine has (a 1 GiB cap).

- What it carries: the pages, built in a stage of its own the way CI builds them; the plan and the register
  (`docs/`), the law corpus (`knowledge/`) and the product catalogue (`products/`), which routes read; and every
  private folder left out of the build context.
- What it installs: the pinned set without the GPU learning stack (torch, torchsde, triton and 18 CUDA libraries),
  because the first deploy runs the floor only; the three modules that use torch guard its import. No system
  package: every pin has a prebuilt wheel but docopt, which is pure Python.
- Built in 206 seconds; the image is 2.28 GB.
- Booted: healthy 8.3 seconds after it started, with 225 MiB of memory at idle and 253 MiB after the probes, under
  the 1 GiB cap. The tree's own boot, with torch loaded, measured 711 MB.
- Asked: `/` served the pages; `/health`, `/api/v1/plan`, `/api/v1/plan/followups`, `/api/v1/catalog/products`
  and `/api/v1/law/bundle` answered 200 from the files the image carries.

How it was built here: this environment reaches the internet only through an egress proxy that re-signs TLS and
refuses the Debian package mirror. The image installs no system package, so the mirror is not needed; the two base
images were local copies that trust the proxy's certificate, and the build ran on the host network with the proxy
passed in. The Dockerfile is the one committed here, unchanged.

Found by the dry run: the legal matter's folder is set in `agentic_core/legal/matter.json` as a path on the
Owner's own Windows machine, so the image carries the path and `/api/v1/law/bundle` answers with it (FU-1282).

Closed by W1129: the folder is named on the machine that holds it, by `LEGAL_MATTER_FOLDER` in that machine's own
`.env`, which the image leaves out. The committed file names none, and the route answers with the folder's state
and the setting that named it, never its path.

Done since (FU-603): W1134 wrote the next section, with the secrets pattern with no stored keys, the records' disk
kept apart from the machine, the cost labels and the costs; W1137 made the backup a daily snapshot and drilled the
restore and the rollback on this machine. The project, the billing and the deploy itself stay the Owner's.

## The Google Cloud deploy, step by step (P4.5), read at Google's pages on 2026-11-20 (W1134)

OWNER RULING 2026-11-20: the exact Google Cloud deploy steps are written here. The project, its billing and the
deploy itself stay the Owner's. Nothing here has been run against a Google account: each command is copied from the
Google page its step names, in the form that page gives it. A value in capitals (PROJECT_ID, PROJECT_NUMBER,
BILLING_ACCOUNT, BUCKET_NAME, TAG and the like) is the Owner's to fill in. Where no page read here settles a point,
the step says so.

THE PAGES, each read on 2026-11-20 (in brackets, the date the page gives as last updated, or that it shows
none):
- [free] https://docs.cloud.google.com/free/docs/free-cloud-features (2026-11-13)
- [vm] https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/create (2026-11-10)
- [cos] https://docs.cloud.google.com/container-optimized-os/docs/how-to/create-configure-instance (2026-11-10)
- [cos-run] https://docs.cloud.google.com/container-optimized-os/docs/how-to/run-container-instance (2026-11-10)
- [containers] https://docs.cloud.google.com/compute/docs/containers (2026-11-10)
- [migrate] https://docs.cloud.google.com/compute/docs/containers/migrate-containers (2026-11-10)
- [startup] https://docs.cloud.google.com/compute/docs/instances/startup-scripts/linux (2026-11-10)
- [metadata] https://docs.cloud.google.com/compute/docs/metadata/querying-metadata (2026-11-10)
- [mount] https://docs.cloud.google.com/compute/docs/disks/format-mount-disk-linux (2026-11-10)
- [firewall] https://docs.cloud.google.com/firewall/docs/using-firewalls (2026-11-10)
- [registry] https://docs.cloud.google.com/artifact-registry/docs/docker/store-docker-container-images (2026-11-10)
- [registry-pricing] https://cloud.google.com/artifact-registry/pricing (no date shown)
- [network-pricing] https://cloud.google.com/vpc/network-pricing (no date shown)
- [run-volumes] https://docs.cloud.google.com/run/docs/configuring/services/cloud-storage-volume-mounts (2026-11-19)
- [snapshots] https://docs.cloud.google.com/compute/docs/disks/scheduled-snapshots (2026-11-10)
- [disk-pricing] https://cloud.google.com/compute/disks-image-pricing (no date shown)
- [disks-create] https://docs.cloud.google.com/sdk/gcloud/reference/compute/disks/create (2026-09-29)
- [detach-disk] https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/detach-disk (2026-05-27)
- [attach-disk] https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/attach-disk (2026-07-21)
- [vm-stop] https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/stop (2026-08-11)
- [vm-start] https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/start (2026-07-21)
- [budget-cli] https://docs.cloud.google.com/sdk/gcloud/reference/billing/budgets/create (2026-05-27)
- [budgets] https://docs.cloud.google.com/billing/docs/how-to/budgets (2026-11-10)
- [uptime] https://docs.cloud.google.com/monitoring/uptime-checks (2026-11-20)
- [wif] https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines (2026-11-17)
- [static-promote] https://docs.cloud.google.com/vpc/docs/reserve-static-external-ip-address (2026-11-12)
- [managed-certs] https://docs.cloud.google.com/load-balancing/docs/ssl-certificates/google-managed-certs (2026-11-10)
- [cos-fs] https://docs.cloud.google.com/container-optimized-os/docs/concepts/disks-and-filesystem (2026-11-10)
- [caddy-image] https://hub.docker.com/_/caddy (2026-11-16)
- [caddy-https] https://raw.githubusercontent.com/caddyserver/website/master/src/docs/markdown/automatic-https.md (no date shown)
- [caddy-proxy] https://raw.githubusercontent.com/caddyserver/website/master/src/docs/markdown/quick-starts/reverse-proxy.md (no date shown)
- [caddy-headers] https://raw.githubusercontent.com/caddyserver/website/master/src/docs/markdown/caddyfile/directives/reverse_proxy.md (no date shown)
- [le-challenges] https://raw.githubusercontent.com/letsencrypt/website/main/content/en/docs/challenge-types.md (2026-02-12)

The last four, for step 12 (W1140), are the sources caddyserver.com and letsencrypt.org are built from, read there
because this environment's network refuses both sites; the image's page is Docker Hub's.

THE SHAPE, AND WHY
- One e2-micro machine in us-central1 runs the release channel. The free tier gives one non-preemptible e2-micro a
  month in us-west1, us-central1 or us-east1, and 30 GB-months of standard persistent disk [free].
- The platform keeps its records as files under DATA_DIR, so they live on a 20 GB disk of their own beside a 10 GB
  boot disk: 30 GB together, the free tier's whole allowance. The data disk is created with auto-delete=no, because
  a disk created with a machine is deleted with it by default [vm]; deleting or replacing the machine leaves the
  records where they are.
- Not Cloud Run for the release channel. A Cloud Storage volume there "does not provide concurrency control for
  multiple writes (file locking) to the same file": the last write wins and all previous writes are lost, and it is
  "not a fully POSIX-compliant file system" [run-volumes]. Cloud Run stays a candidate for a development or beta
  channel whose records may be lost.
- The machine runs Container-Optimized OS, from the image project cos-cloud [cos]. It starts the image with docker
  run from a startup script, because the container startup agent that once did that is deprecated [containers]; the
  script follows the migration page's own example [migrate].

WHAT IT COSTS, read at the pricing pages (the arithmetic is this round's, over a 730-hour month)
- The machine and its two disks: inside the free tier [free].
- The machine's public IPv4 address: $0.005 an hour on a standard machine, and the free tier covers one hour a
  month [network-pricing], so about $3.65 a month. It is this shape's one recurring charge.
- The registry: free up to 0.5 GiB a month, then $0.000136986 per GiB-hour, about $0.10 per GiB-month
  [registry-pricing]. The image is 2.28 GB as built (W1128) and the registry stores it compressed, so one image costs
  at most about $0.16 a month; the stored size is read from the repository after the first push.
- The daily snapshots of the data disk: standard snapshot storage is $0.05 per GB a month in us-central1, and a
  snapshot after the first holds only what changed [disk-pricing]. The records are small, so this is cents a month;
  the figure is read from the bill after the first week. While a restored disk and the old one both exist, the
  standard disk space past the free 30 GB-months is $0.000054795 per GiB-hour [disk-pricing].
- Data sent out: 1 GB a month is free from North America [free]. The rate after that was not read here, nor was the
  uptime check's own price.
- In all, about $3.65 to $3.85 a month before data sent out and the snapshots' cents. The budget alert in step 1
  watches the bill.

THE STEPS, run from the Workstation folder with gcloud signed in as the Owner

**Step 1. A budget alert, before anything else** [budget-cli] [budgets]

```bash
gcloud billing budgets create --billing-account=BILLING_ACCOUNT --display-name="workstation" \
    --budget-amount=10USD --filter-projects=projects/PROJECT_ID \
    --threshold-rule=percent=0.50 --threshold-rule=percent=0.90 --threshold-rule=percent=1.00
```

The amount is the Owner's; 10 USD is about three times the bill above. An alert warns and stops nothing: "Setting an
alerts-only budget doesn't automatically cap Google Cloud or Google Maps Platform usage or spending" [budgets]. That
page points to a spend cap budget where a service supports one; the spend cap page was not read here.

**Step 2. Each service's API, once** [registry]

The registry page's first step is to enable its service's API in the project, if it is not already enabled; the
project's creator holds the permission to do so through the Owner role [registry]. Each service the steps use is
enabled the same way, once: Compute Engine, Artifact Registry, Cloud Storage, Cloud Monitoring and Cloud Billing's
budgets.

**Step 3. The registry, in the machine's region** [registry] [registry-pricing]

```bash
gcloud artifacts repositories create workstation --repository-format=docker \
    --location=us-central1 --description="Workstation images" --project=PROJECT_ID
gcloud auth configure-docker us-central1-docker.pkg.dev
```

The pricing page's own advice is to keep a repository in the region its machines run in, "so that there are no
cross-region data transfer costs" [registry-pricing].

**Step 4. Build the release and push it** [registry]

```bash
docker build -t workstation:TAG .
docker tag workstation:TAG us-central1-docker.pkg.dev/PROJECT_ID/workstation/workstation:TAG
docker push us-central1-docker.pkg.dev/PROJECT_ID/workstation/workstation:TAG
```

The image is built from this tree's Dockerfile, as the dry run built it; the tag and the push are the page's. TAG is
the commit's short hash (`git rev-parse --short HEAD`), so a release names the code it carries, and every earlier
release stays in the repository to roll back to.

**Step 5. The backup: a daily snapshot of the data disk, kept 14 days** [snapshots] [disk-pricing]

```bash
gcloud compute resource-policies create snapshot-schedule workstation-daily --region=us-central1 \
    --description="Workstation records, daily" --max-retention-days=14 --start-time=03:00 --daily-schedule \
    --on-source-disk-delete=keep-auto-snapshots --storage-location=us-central1
```

Google takes the snapshots; nothing runs on the machine and nothing holds a key. The page's daily example takes
its flags this way, starting at a UTC time, and keep-auto-snapshots keeps the snapshots if the disk itself is
deleted [snapshots]; its example stores them in the US multi-region, and us-central1 keeps them beside the disk at
the rate the pricing page gives for it [disk-pricing]. The schedule is attached to the data disk once step 7 has
made it. Each snapshot is taken while the platform runs; an application-consistent snapshot is on a page not read
here.

**Step 6. The firewall rule: ports 80 and 443, to the machine tagged workstation** [firewall] [migrate]

```bash
gcloud compute firewall-rules create workstation-http --network=default --direction=ingress --action=allow \
    --target-tags=workstation --source-ranges=0.0.0.0/0 --rules=tcp:80,tcp:443
```

Container-Optimized OS denies incoming traffic by default, so the startup script opens the machine's own firewall
with the migration page's two rules [migrate]; this rule is what lets ports 80 and 443 in from outside, and the
network's other rules are unchanged. Port 443 is answered once step 12 has given the machine its domain.

**Step 7. The machine, its kept data disk and its startup script** [vm] [cos] [startup] [mount] [metadata] [cos-run]

```bash
gcloud compute instances create workstation --zone=us-central1-a --machine-type=e2-micro \
    --image-family=cos-stable --image-project=cos-cloud \
    --boot-disk-size=10GB --boot-disk-type=pd-standard \
    --create-disk=name=workstation-data,device-name=workstation-data,size=20GB,type=pd-standard,auto-delete=no \
    --metadata=image-tag=TAG --metadata-from-file=startup-script=deploy/gcp/startup.sh \
    --tags=workstation --labels=app=workstation,channel=release --deletion-protection
```

The flags are the reference's [vm]; an image family starts the machine from the family's latest image, and
cos-stable is the Container-Optimized OS family the OS's own page lists [cos]. `deploy/gcp/startup.sh` is committed
beside this file and keeps Unix line endings on every checkout (`.gitattributes`), since the machine runs it with
bash. Compute Engine runs it as root at every boot [startup]. It formats the data disk only if the disk is blank,
mounts it at /mnt/disks/data with the mount page's commands [mount], opens the host firewall, reads the project and
the image's tag from the machine's metadata server [metadata], signs the registry in with `docker-credential-gcr`,
which the OS carries [cos-run], and starts the platform with its records on the data disk. Its disk step was driven
in this round on disk images: a blank disk is formatted once, a formatted one is kept byte for byte, and a disk
holding anything else, a short one or a missing one is refused, untouched, and the platform is not started
(test_w1134). The labels are the cost labels: a budget can be narrowed to them with --filter-labels [budget-cli].
NOT READ HERE: the roles the machine's service account needs to pull from the repository; if the pull is refused,
that grant is what is missing. The script's output is read on the machine with
`sudo journalctl -u google-startup-scripts.service` [startup]. Then the data disk takes step 5's schedule
[snapshots]:

```bash
gcloud compute disks add-resource-policies workstation-data --resource-policies=workstation-daily \
    --zone=us-central1-a
```

**Step 8. A release, and a rollback, are the same two commands** [startup] [vm]

```bash
gcloud compute instances add-metadata workstation --zone=us-central1-a --metadata=image-tag=TAG
sudo google_metadata_script_runner startup
```

The first runs where gcloud is and sets the tag the platform starts from. The second runs on the machine (SSH from
the console) and re-runs the startup script, the page's way to re-run one [startup]; the script pulls the image
first, and leaves the running platform as it was if the pull fails. A rollback is the same with the previous tag.
The page shows add-metadata with --metadata-from-file; the --metadata form is the one create takes [vm]. Drilled on
this machine (below).

**Step 9. A restore, from the latest snapshot** [vm-stop] [disks-create] [detach-disk] [attach-disk] [vm-start]

```bash
gcloud compute instances stop workstation --zone=us-central1-a
gcloud compute disks create workstation-data-restored --source-snapshot=SNAPSHOT --type=pd-standard \
    --zone=us-central1-a
gcloud compute instances detach-disk workstation --device-name=workstation-data --zone=us-central1-a
gcloud compute instances attach-disk workstation --disk=workstation-data-restored --device-name=workstation-data \
    --zone=us-central1-a
gcloud compute instances start workstation --zone=us-central1-a
```

The machine is stopped first: the detach reference warns that "detaching a disk without first unmounting it may
result in incomplete I/O operations and data corruption" [detach-disk]. SNAPSHOT is the latest of the schedule's,
and the disk made from it keeps the device name the startup script looks for, so at the next boot the script finds
its file system and keeps it. The old disk is deleted once the restored one has been read; until then the two
together are past the free 30 GB-months [disk-pricing]. Drilled on this machine (below).

**Step 10. The uptime check and its alert, from outside the machine (FU-1095)** [uptime]

In the console: Monitoring, Uptime checks, Create uptime check; protocol HTTP, resource type URL, the machine's
address as the host and /health as the path; once step 12 has given the machine its domain, protocol HTTPS and the
domain as the host, since Caddy answers plain HTTP with a redirect. Then, in the page's words: "To be notified when an uptime check fails,
create an alerting policy and configure notification channels for that policy"; the channel is the Owner's e-mail.
By default a notification is sent when at least two regions report the check failing for at least a minute [uptime].
Then the drill FU-1095 asks for, with the Owner watching: on the machine, `docker stop workstation`; see the e-mail
arrive; `docker start workstation`; see the alert clear.

**Step 11. Later: deploys from GitHub, with no stored key** [wif]

The first deploys are run by the Owner by hand, signed in as the Owner. When a workflow deploys, it signs in through
a workload identity pool and holds no key:

```bash
gcloud iam workload-identity-pools create github --location="global" \
    --description="GitHub Actions" --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc workstation --location="global" \
    --workload-identity-pool="github" --issuer-uri="https://token.actions.githubusercontent.com/" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository_id=assertion.repository_id,attribute.ref=assertion.ref" \
    --attribute-condition="assertion.repository_id=='REPOSITORY_ID' && assertion.ref=='refs/heads/main'"
gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_EMAIL --role=roles/iam.workloadIdentityUser \
    --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository_id/REPOSITORY_ID"
```

The condition names the repository by its number, not its name: the page warns that the name fields "increase the
chances of cybersquatting and typosquatting attacks" and says to use the numeric `*_id` fields, "which are unique and
can't be reused" [wif]. Only main, the release channel, may deploy. The workflow's job asks for `id-token: write` and
`contents: read`, and signs in with the step `uses: 'google-github-actions/auth@v1'`, given
`workload_identity_provider` and `service_account` [wif]. NOT READ HERE: the roles the deploying service account
needs, and whether a later version of that action is current.

**Step 12. HTTPS, before anyone signs in: a fixed address, the Owner's domain, and Caddy in front (FU-1284)**
[static-promote] [network-pricing] [caddy-https] [caddy-proxy] [caddy-headers] [caddy-image] [le-challenges]
[cos-fs] [managed-certs]

As steps 1 to 11 leave it, the machine serves plain HTTP at its address, so what a person types would cross the
internet unencrypted: no person signs in (P4.1) until this step is done and the domain answers over HTTPS. A
publicly trusted certificate is for a domain: a host name qualifies only if it is "not an IP address"
[caddy-https]. The domain is the Owner's to buy (FU-1289).

First the machine's address is made its own. The address step 7 gave the machine is ephemeral, and the domain must
keep pointing at it. Promoting it keeps it, and "does not cause Google Cloud to drop packets sent to the VM"
[static-promote]:

```bash
gcloud compute addresses create workstation-ip --addresses=EXTERNAL_IP --region=us-central1
```

EXTERNAL_IP is the machine's address, as the console's IP addresses page lists it, where the same promotion is a
menu item [static-promote]. The price does not change: a static or ephemeral address in use on a standard machine
is $0.005 an hour, and a static one is in use "whether the instance is running or stopped"; one reserved and
attached to nothing is $0.01 an hour [network-pricing].

Then, at the domain's DNS provider, an A record for the domain naming EXTERNAL_IP. Caddy obtains a certificate when
"your domain's A/AAAA records point to your server", "ports `80` and `443` are open externally" and its data
directory "is writeable and persistent" [caddy-https]. Then the machine is told its domain, and its startup script
is run again as in step 8:

```bash
gcloud compute instances add-metadata workstation --zone=us-central1-a --metadata=domain=DOMAIN
sudo google_metadata_script_runner startup
```

The script refuses a domain that is not a host name, an IP address included, and leaves the running platform as it
was. Otherwise it starts the platform on a private Docker network with no port of its own, believing a forwarded
client address only from Caddy's fixed address, and starts Caddy, the official image pinned by its digest
[caddy-image], on ports 80 and 443 in front of it with Caddy's own one-command reverse proxy, `caddy reverse-proxy
--from DOMAIN --to workstation:8000` [caddy-proxy]. Caddy obtains the domain's certificate from a public
certificate authority, keeps it renewed and redirects HTTP to HTTPS itself [caddy-https]. Let's Encrypt's HTTP-01
challenge "can only be done on port 80" [le-challenges], which is why step 6 admits port 80 as well as 443. The
reverse proxy "sets or augments the `X-Forwarded-For` header field" and by default ignores the values a request
brings for it, "to prevent spoofing" [caddy-headers]. Caddy keeps its certificates in a Docker volume on the boot
disk: its data directory "must not be treated as a cache" [caddy-image], and on this OS /var/lib/docker is
stateful, for the lifetime of the boot disk [cos-fs]. A new machine obtains a new certificate.

THE OTHER WAY, NOT TAKEN: a global external Application Load Balancer with a Google-managed certificate
[managed-certs] needs a domain too, and its forwarding rule alone is $0.025 an hour, about $18.25 a month
[network-pricing], against nothing more on the machine.

DRILLED ON THIS MACHINE, 2026-11-20 (W1137): run again in W1138 on an image with FU-1287's change. The image
built from the current tree (workstation:w1138) and the one built from W1128's tree (workstation:9dfc0f37), each
started with the flags `deploy/gcp/startup.sh` gives the release machine and the free tier's 1 GiB of memory, on
Docker volumes standing in for the data disk.
- The current release came up healthy in 7.4 seconds and wrote a made-up project. After
  the writes, `docker diff` showed the container had changed nothing outside the volume and `/tmp`: the records, and
  everything else the platform wrote in the drill, are on the volume. The first drill found `/app/logs/autonomy`, where the
  autonomy pipelines keep what they write, beside the code, and matplotlib's font cache under `/home/app`
  (FU-1287); W1138 put the logs folder on the data root and the cache under `/tmp`.
- RESTORE: the volume was copied whole (3669 bytes compressed) and restored onto a fresh volume in
  0.6 seconds; the 13 files on the copy are byte-identical to the
  original, owned by the image's user. The current release on the copy came up in
  7.3 seconds and read the project back (HTTP 200).
- ROLLBACK: the previous release, started on the same records, came up in 7.3 seconds,
  read the project (HTTP 200) and listed it; the current release, started again, came up in
  7.3 seconds and read it (HTTP 200).
- On Google Cloud the copy is the snapshot of step 5 and the fresh volume is step 9's restored disk; the first
  restore from a real snapshot is driven at the deploy, with the Owner watching (FU-1288).

HTTPS, DRILLED ON THIS MACHINE, 2026-11-20 (W1140): the startup script's own front (`start_front`, sourced from
`deploy/gcp/startup.sh` by `deploy/https_drill.sh`), started for workstation.localhost, a name Caddy certifies from
its own local authority: a public authority certifies only a domain, which is the Owner's. Ports 80 and 443 of this
machine were used, as the release machine uses them, with the image built in W1138 (workstation:w1138).
- The front came up healthy in 8.0 seconds. HTTPS answered 200, with a
  certificate issued by Caddy Local Authority - ECC Intermediate; plain HTTP was answered 308 https://workstation.localhost/health; and
  the platform had no port of its own.
- Caddy held its fixed address, 172.30.0.2, and Docker gave the platform 172.30.0.128, from the
  network's top half. The platform's log gave the request's address as 172.30.0.1, the address Caddy saw
  it come from, and gave 172.30.0.1 again for a request that wrote its own
  X-Forwarded-For of 203.0.113.7.
- Started on the same network without the setting, the platform gave Caddy's own address,
  172.30.0.2, for the same request: without it, the sign-in limits, which count failed
  attempts by the address they come from, would count every person as one address.
- On Google Cloud the name is the Owner's domain and the authority a public one; the first certificate is obtained
  at the deploy, with the Owner watching (FU-1289).

## Payments & money safety (READ BEFORE LAUNCH)

The payments rails (`agentic_core/api/v310/payments.py`) operate in modes
`simulation → test → live_gated → live`. **Live charges require ALL THREE: `REAL_MONEY_ENABLED = True` in code (`agentic_core/economy/owner_payments.py` — a reviewed code change, currently `False`), a `sk_live_` key, AND
`STRIPE_LIVE_ENABLED=true`** — otherwise the code refuses to move real money. While the constant is `False`, a live key reports `live_gated` whatever the env switches say.

- Keep money **virtual/simulated**: leave `STRIPE_SECRET_KEY` unset (or a `sk_test_` test key) and
  **do not** set `STRIPE_LIVE_ENABLED`.
- ⚠️ **Security finding:** a real `sk_live_` key currently lives in the local (gitignored, untracked)
  `.env` and is auto-loaded at boot. The payments code correctly *gates* it (refuses to charge), but
  the recommendation stands: **swap the local `.env` to a `sk_test_` key.** Never commit `.env` (it
  is gitignored), never set `STRIPE_LIVE_ENABLED`, and never deploy the live key to Render.

## Watching the first deploy: failures are recorded, not alerted

Every route failure is recorded in the outcome ledger (`agentic_core/api/operational_excellence.py`) and in the
event chain, and shown on the Operations page (`/operations`). Nothing sends a failure to anyone, so an outage on
the first deploy would reach no person (FU-1095). The smallest addition, for that deploy:

1. An uptime check on `/health` from OUTSIDE the machine, in your own cloud account beside the billing alert,
   e-mailing you when it fails. A boot failure cannot report itself, so the check must not run on the machine it
   watches.
2. Name it in the deploy dry run. Drive it once at the deploy, with you watching: stop the service, see the alert
   arrive, start the service, see it clear.
3. `/health` returns a fixed body, so the check sees only a process that is dead or unreachable. A process that is
   up and failing its routes still answers it; those failures are read on the Operations page.

The check, its address and its e-mail are yours to set up: this platform sends nothing.

## Verify before deploy

```bash
python -c "import agentic_core.app_mvp"                       # backend imports/boots
python -m pytest integration_tests -q                         # integration suite (its conftest isolates the stores; AI_DISABLE_LOCAL=1 → fast)
npm --prefix apps/workstation-superapp run build              # frontend tsc + vite build
```

CI (`spine.yml`) runs the backend boot+suite and the frontend build on every push; require it green
before promoting a deploy.
