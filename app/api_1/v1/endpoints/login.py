from typing import List

from fastapi import APIRouter, HTTPException

from app.api_1.v1.auth.auth_handler import signJWT
from app.core.settings import settings

login_router = APIRouter(tags=["Login"])

DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD


@login_router.post("/login", response_model=dict)
def login(username: str, password: str):
    if username != DB_USER or password != DB_PASSWORD:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return signJWT(username)
