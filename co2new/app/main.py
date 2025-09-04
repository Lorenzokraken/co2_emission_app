from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.routers import co2
from app.database.database import get_db
from app.models.models import Country, Year
from app.schemas.schemas import CountryBase, YearBase
from typing import List

app = FastAPI(
    title="CO2 Emissions API",
    description="API for CO2 emissions data visualization and prediction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(co2.router, prefix="/api")
app.include_router(co2.router)

# Serve static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Add missing routes for /countries and /years (needed for frontend compatibility)
@app.get("/countries", response_model=List[CountryBase])
def get_countries_root(db: Session = Depends(get_db)):
    countries = db.query(Country).order_by(Country.name).all()
    return countries

@app.get("/years", response_model=List[YearBase])
def get_years_root(db: Session = Depends(get_db)):
    years = db.query(Year).order_by(Year.year).all()
    return years

@app.get("/")
async def root():
    return {"message": "CO2 Emissions API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}