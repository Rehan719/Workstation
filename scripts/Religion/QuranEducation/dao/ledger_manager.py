import json
import os
from datetime import datetime
import uuid

class LedgerManager:
    def __init__(self, ledger_path="knowledge/Religion/QuranEducation/dao/ledger_state.json"):
        self.ledger_path = ledger_path
        self.ensure_ledger_exists()
        self.load_ledger()

    def ensure_ledger_exists(self):
        if not os.path.exists(self.ledger_path):
            os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
            initial_state = {
                "version": "8.5.0",
                "last_updated": str(datetime.now()),
                "balances": {},
                "reputation": {},
                "verifiable_credentials": []
            }
            with open(self.ledger_path, 'w') as f:
                json.dump(initial_state, f, indent=2)

    def load_ledger(self):
        with open(self.ledger_path, 'r') as f:
            self.data = json.load(f)

    def save_ledger(self):
        self.data["last_updated"] = str(datetime.now())
        with open(self.ledger_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def issue_token(self, user_id, token_type, amount):
        if user_id not in self.data["balances"]:
            self.data["balances"][user_id] = {}

        current_balance = self.data["balances"][user_id].get(token_type, 0)
        self.data["balances"][user_id][token_type] = current_balance + amount
        self.save_ledger()
        return self.data["balances"][user_id][token_type]

    def get_balance(self, user_id, token_type):
        return self.data["balances"].get(user_id, {}).get(token_type, 0)

    def issue_verifiable_credential(self, user_id, credential_type, claims):
        credential = {
            "id": f"urn:uuid:{uuid.uuid4()}",
            "type": ["VerifiableCredential", credential_type],
            "issuer": "did:vsn:qep-governance",
            "issuanceDate": str(datetime.now()),
            "credentialSubject": {
                "id": f"did:vsn:{user_id}",
                **claims
            },
            "proof": {
                "type": "Ed25519Signature2020",
                "proofPurpose": "assertionMethod",
                "verificationMethod": "did:vsn:qep-governance#key-1",
                "jws": "eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..MOCK_SIG"
            }
        }
        self.data["verifiable_credentials"].append(credential)
        self.save_ledger()
        return credential

    def update_reputation(self, user_id, delta):
        current_rep = self.data["reputation"].get(user_id, 0)
        self.data["reputation"][user_id] = current_rep + delta
        self.save_ledger()
        return self.data["reputation"][user_id]

    def get_reputation(self, user_id):
        return self.data["reputation"].get(user_id, 0)
