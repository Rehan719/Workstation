from fastapi import FastAPI
app = FastAPI(title="MultiSigCouncil CLI")
@app.get("/council/pending")
def pending(): return {"count": 0}
