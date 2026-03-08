from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Workstation API")

# Allow your frontend domains (add more as needed)
origins = [
    "http://localhost:3000",
    "https://workstation-pwa.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Workstation backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
