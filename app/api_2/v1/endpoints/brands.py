from fastapi import APIRouter, Depends, HTTPException
from app.api_2.db import collection_brands
from app.services.fipe_service import get_vehicle_details_by_brand_with_retry
import logging
from app.api_1.v1.auth.auth_bearer import JWTBearer

router = APIRouter(dependencies=[Depends(JWTBearer())], tags=["Load Vehicles"])

logger = logging.getLogger(__name__)


@router.post("/process-brand/")
async def process_brand(brand: str):
    try:
        details = await get_vehicle_details_by_brand_with_retry(brand)
        if not details:
            raise HTTPException(status_code=404, detail="Details not found")

        # Save to MongoDB
        await collection_brands.insert_one(details)

        return {"status": "success", "message": "Data saved successfully"}
    except Exception as e:
        logger.error(f"Failed to process brand {brand}. Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
