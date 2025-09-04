#!/usr/bin/env python3
"""
Script to initialize the database tables for the CO2 Emissions app.
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.database import Base, engine
from app.models.models import Country, Year, Emission

def create_tables():
    """Create all tables in the database."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    success = create_tables()
    if success:
        print("Database initialization completed.")
        sys.exit(0)
    else:
        print("Database initialization failed.")
        sys.exit(1)