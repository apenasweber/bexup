from typing import List
import requests
from fastapi import APIRouter, Depends, HTTPException
from app.api_1.v1.auth.auth_bearer import JWTBearer
from app.queues.queue_utils import enqueue_message
import logging
from app.models.vehicle import Brand
from app.core.database import get_db
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO)

router = APIRouter(dependencies=[Depends(JWTBearer())], tags=["Get Cars"])


def fetch_car_brands_from_fipe():
    try:
        response = requests.get(
            "https://parallelum.com.br/fipe/api/v1/carros/marcas", timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        logging.error(f"Error fetching data from FIPE: {error}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch car brands from FIPE service.",
        ) from error


@router.get("/car-brands", response_model=List[str])
def get_car_brands():
    data = fetch_car_brands_from_fipe()
    return [brand["nome"] for brand in data]


@router.post("/enqueue-brand/")
def enqueue_brand(brand_name: str):
    enqueue_message(brand_name)
    logging.info(f"Brand {brand_name} enqueued successfully!")
    return {"message": "Brand enqueued successfully!"}


@router.get("/stored-car-brands", response_model=List[str])
def get_stored_car_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    return [brand.name for brand in brands]
