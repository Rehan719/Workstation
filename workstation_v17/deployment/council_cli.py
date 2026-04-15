from fastapi import FastAPI
app = FastAPI(title="MultiSigCouncil CLI Interface")
@app.get("/council/status")
def get_status():
    return {"pending_approvals": 0, "quarum_met": True, "status": "ONLINE"}
