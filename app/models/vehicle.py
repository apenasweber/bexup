from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    models = relationship("Model", back_populates="brand")


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="models")
    years = relationship("Year", back_populates="model")


class Year(Base):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    vehicle_model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model", back_populates="years")
    vehicle_value = relationship("VehicleValue", uselist=False, back_populates="year")


class VehicleValue(Base):
    __tablename__ = "vehicle_values"

    id = Column(Integer, primary_key=True, index=True)
    type_vehicle = Column(Integer)
    value = Column(String)
    brand = Column(String)
    model = Column(String)
    year_model = Column(Integer)
    fuel = Column(String)
    code_fipe = Column(String)
    month_reference = Column(String)
    sigla_fuel = Column(String)
    year_id = Column(Integer, ForeignKey("years.id"))
    year = relationship("Year", back_populates="vehicle_value")
