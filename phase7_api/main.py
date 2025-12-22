from fastapi import FastAPI
from phase7_api.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="St. Aloysius University AI Assistant",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}
