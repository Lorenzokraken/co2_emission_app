from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Country(Base):
    __tablename__ = "countries"
    country_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    iso_code = Column(String)
    surface_km2 = Column(Integer)
    emissions = relationship("Emission", back_populates="country")

class Year(Base):
    __tablename__ = "years"
    year_id = Column(Integer, primary_key=True)
    year = Column(Integer, unique=True)
    emissions = relationship("Emission", back_populates="year")

class Emission(Base):
    __tablename__ = "emissions"
    emission_id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"))
    year_id = Column(Integer, ForeignKey("years.year_id"))
    co2 = Column(Float)
    co2_per_km2 = Column(Float)
    population = Column(Integer)
    
    country = relationship("Country", back_populates="emissions")
    year = relationship("Year", back_populates="emissions")