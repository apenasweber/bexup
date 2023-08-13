from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api_1.v1.endpoints.car_brands import router as get_cars_router
from app.api_1.v1.endpoints.login import login_router
from app.api_1.v1.endpoints.vehicles import router as vehicles_router

app = FastAPI(
    title="Api for FIPE vehicle prices",
    description="API to fetch vehicle prices from FIPE (Fundação Instituto de Pesquisas Econômicas)",
    version="v1",
)

app.include_router(login_router, prefix="/api/v1")
app.include_router(get_cars_router, prefix="/api/v1")
app.include_router(vehicles_router, prefix="/api/v1")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
