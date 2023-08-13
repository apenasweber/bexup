from app.models.vehicle import VehicleValue
from fastapi import APIRouter, Depends, HTTPException
from app.api_1.v1.auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.queues.queue_manager import send_brand_to_queue
from app.services.fipe_service import (
    get_brands_with_retry,
    get_models_with_retry,
    get_years_with_retry,
    get_vehicle_value_with_retry,
)
from app.models.vehicle import Brand, Model, Year, VehicleValue
import logging
import asyncio
from app.schemas.vehicle import VehicleUpdate

logging.basicConfig(level=logging.INFO)

router = APIRouter(dependencies=[Depends(JWTBearer())], tags=["Load Vehicles"])


@router.post("/trigger-load-vehicles")
async def trigger_load_vehicles(db: Session = Depends(get_db)):
    brands = await get_brands_with_retry()
    for brand_data in brands:
        send_brand_to_queue(brand_data)
        logging.info(f"Brand {brand_data['nome']} added to queue")
    return {"status": "Data loading has started!"}


@router.post("/load-vehicles")
async def load_vehicles(db: Session = Depends(get_db)):
    logging.info("Start loading vehicles...")
    try:
        await load_all_data(db)

        # Execute the commit in a separate thread
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, db.commit)

        logging.info("Data loaded successfully!")
        return {"status": "Data loaded successfully!"}
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")

        # Execute the rollback in a separate thread
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, db.rollback)

        return {"status": f"Failed to load data: {str(e)}"}


async def load_all_data(db: Session):
    brands = await get_brands_with_retry()
    for brand_data in brands:
        await load_brand_data(db, brand_data)


async def load_brand_data(db: Session, brand_data):
    brand = Brand(name=brand_data["nome"])
    db.add(brand)
    db.flush()
    await load_models_data(db, brand, brand_data["codigo"])


async def load_models_data(db: Session, brand: Brand, brand_code):
    models = await get_models_with_retry(brand_code)
    for model_data in models["modelos"]:
        model = Model(name=model_data["nome"], brand_id=brand.id)
        db.add(model)
        db.flush()
        await load_years_data(db, model, brand_code, model_data["codigo"])


async def load_years_data(db: Session, model: Model, brand_code, model_code):
    years = await get_years_with_retry(brand_code, model_code)
    for year_data in years:
        year = Year(name=year_data["nome"], vehicle_model_id=model.id)
        db.add(year)
        db.flush()
        load_vehicle_value_data(db, year, brand_code, model_code, year_data["codigo"])


async def load_vehicle_value_data(
    db: Session, year: Year, brand_code, model_code, year_code
):
    vehicle_value_data = await get_vehicle_value_with_retry(
        brand_code, model_code, year_code
    )
    vehicle_value = VehicleValue(
        type_vehicle=vehicle_value_data["TipoVeiculo"],
        value=vehicle_value_data["Valor"],
        brand=vehicle_value_data["Marca"],
        model=vehicle_value_data["Modelo"],
        year_model=vehicle_value_data["AnoModelo"],
        fuel=vehicle_value_data["Combustivel"],
        code_fipe=vehicle_value_data["CodigoFipe"],
        month_reference=vehicle_value_data["MesReferencia"],
        sigla_fuel=vehicle_value_data["SiglaCombustivel"],
        year_id=year.id,
    )
    db.add(vehicle_value)
    db.flush()


@router.put("/update-vehicle")
def update_vehicle(data: VehicleUpdate, db: Session = Depends(get_db)):
    vehicle = db.query(VehicleValue).filter(VehicleValue.id == data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    if data.model:
        vehicle.model = data.model
    if data.observations:
        vehicle.observations = data.observations

    db.commit()
    return {"status": "success", "message": "Vehicle updated successfully"}
