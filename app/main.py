import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints import login
from core import settings

app = FastAPI(
    title="Api for FIPE vehicle prices",
    description="API to fetch vehicle prices from FIPE (Fundação Instituto de Pesquisas Econômicas)",
    version="v1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login, prefix="/login", tags=["login"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
