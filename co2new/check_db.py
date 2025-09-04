#!/usr/bin/env python3
"""
Script to check the database tables and data.
"""

import sys
import os
import sqlite3

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'co2_emissions.db')
print(f"Database path: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(f"  - {table[0]}")
        
    # Check data in tables
    for table in tables:
        table_name = table[0]
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} rows")
            
            # Show first few rows for verification
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                print(f"    Sample data:")
                for row in rows:
                    print(f"      {row}")
        except Exception as e:
            print(f"  - {table_name}: Error querying data - {e}")
            
    conn.close()
    
except Exception as e:
    print(f"Error connecting to database: {e}")