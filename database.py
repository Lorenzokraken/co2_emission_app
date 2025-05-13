from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Percorso corretto: stesso livello di app.py
engine = create_engine("sqlite:///co2_emissions.db", echo=False)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
