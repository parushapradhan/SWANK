#!/usr/bin/env python3
""" Check what columns are in features.sqlite3 """

import sqlite3
import pandas as pd

# Connect to your SQLite database
sqlite_path = "/ocean/projects/cis250156p/ppradhan/road_surface_classifier-master/data/road_surface_classifier/features.sqlite3"

try:
    with sqlite3.connect(sqlite_path) as con:
        # Get table info
        cursor = con.cursor()
        cursor.execute("PRAGMA table_info(features)")
        columns_info = cursor.fetchall()
        
        print("Columns in features.sqlite3:")
        for col in columns_info:
            print(f"  - {col[1]} ({col[2]})")
        
        # Also check first few rows
        df = pd.read_sql('SELECT * FROM features LIMIT 3', con)
        print(f"\nFirst 3 rows:")
        print(df)
        
        # Check if any image-related columns exist
        image_cols = [col for col in df.columns if 'path' in col.lower() or 'img' in col.lower()]
        print(f"\nImage-related columns: {image_cols}")
        
except Exception as e:
    print(f"Error: {e}")
