#!/usr/bin/env python3
"""
Test script to verify database connection and data access for FastAPI app.
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.database import get_db
from app.models.models import Country, Year, Emission

def test_database_connection():
    """Test the database connection and query capabilities."""
    print("Testing database connection...")
    
    try:
        # Get a database session
        db_generator = get_db()
        db = next(db_generator)
        
        # Test querying countries
        print("Querying countries...")
        countries = db.query(Country).order_by(Country.name).limit(3).all()
        print(f"Found {len(countries)} countries:")
        for country in countries:
            print(f"  - {country.country_id}: {country.name}")
            
        # Test querying years
        print("Querying years...")
        years = db.query(Year).order_by(Year.year).limit(3).all()
        print(f"Found {len(years)} years:")
        for year in years:
            print(f"  - {year.year_id}: {year.year}")
            
        # Test querying emissions
        print("Querying emissions...")
        emissions = db.query(Emission).limit(3).all()
        print(f"Found {len(emissions)} emissions:")
        for emission in emissions:
            print(f"  - {emission.emission_id}: country_id={emission.country_id}, year_id={emission.year_id}, co2={emission.co2}")
            
        # Close the database session
        try:
            next(db_generator)
        except StopIteration:
            pass
            
        print("Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"Error testing database connection: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("All tests passed.")
        sys.exit(0)
    else:
        print("Tests failed.")
        sys.exit(1)