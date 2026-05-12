# REST API Specification: vΩ∞-CAPITAL-FUND

## 1. Capital Vault
- `POST /api/capital/deposit`: Initiates a PQC-signed deposit.
- `POST /api/capital/withdraw`: Owner-initiated withdrawal with liquidity guard.

## 2. Mesh Federation
- `GET /api/mesh/peers`: Discovers Workstation peer nodes.
- `POST /api/mesh/treaty/negotiate`: Initiates a bilateral treaty.

## 3. Governance & Judiciary
- `GET /api/council/judge/rulings`: Lists AI judge rulings.
- `POST /api/council/judge/override`: Owner emergency veto of a ruling.

## 4. Compliance
- `GET /api/regulatory/report/form-adv`: Generates SEC Form ADV bundle.
- `GET /api/regulatory/report/rep015`: Generates FCA REP015 return.
