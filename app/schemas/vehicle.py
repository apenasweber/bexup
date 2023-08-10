# app/schemas/vehicle.py

from pydantic import BaseModel
from typing import List, Optional


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int

    class Config:
        orm_mode = True


class ModelBase(BaseModel):
    name: str
    brand_id: int


class ModelCreate(ModelBase):
    pass


class Model(ModelBase):
    id: int

    class Config:
        orm_mode = True


class YearBase(BaseModel):
    name: str
    model_id: int


class YearCreate(YearBase):
    pass


class Year(YearBase):
    id: int

    class Config:
        orm_mode = True


class VehicleValueBase(BaseModel):
    type_vehicle: int
    value: str
    brand: str
    model: str
    year_model: int
    fuel: str
    code_fipe: str
    month_reference: str
    sigla_fuel: str
    year_id: int


class VehicleValueCreate(VehicleValueBase):
    pass


class VehicleValue(VehicleValueBase):
    id: int

    class Config:
        orm_mode = True
