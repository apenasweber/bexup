from fastapi import APIRouter

router = APIRouter()

from fastapi import HTTPException
import requests

get_cars_router = APIRouter(tags=["Get Cars"])


@get_cars_router.get("/car-brands", response_model=list[str])
def get_car_brands():
    try:
        response = requests.get("https://parallelum.com.br/fipe/api/v1/carros/marcas")
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        return [brand["nome"] for brand in data]
    except requests.exceptions.RequestException as error:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch car brands from FIPE service.",
        ) from error
