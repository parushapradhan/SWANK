#!/usr/bin/env python3
""" Check features.sqlite3 dataset structure and contents """

import sqlite3
import pandas as pd
import pathlib

# Database path
database_path = '/ocean/projects/cis250156p/ppradhan/road_surface_classifier-master/data/road_surface_classifier/features.sqlite3'

print("=== Features.sqlite3 Dataset Analysis ===")
print(f"Database path: {database_path}")

# Check if file exists
db_file = pathlib.Path(database_path)
if not db_file.exists():
    print(f"❌ Database file not found: {database_path}")
    exit()

print(f"✅ Database file exists")
print(f"File size: {db_file.stat().st_size / (1024*1024):.1f} MB")

# Connect to database
try:
    with sqlite3.connect(database_path) as con:
        print("\n=== Database Structure ===")
        
        # Check tables
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con)
        print("Tables in database:")
        print(tables)
        
        # Check features table structure
        print("\n=== Features Table Structure ===")
        features_info = pd.read_sql("PRAGMA table_info(features);", con)
        print("Columns in features table:")
        for _, row in features_info.iterrows():
            print(f"  {row['cid']}: {row['name']} ({row['type']})")
        
        # Get sample data
        print("\n=== Sample Data ===")
        sample_data = pd.read_sql("SELECT * FROM features LIMIT 3;", con)
        print("First 3 rows:")
        print(sample_data)
        
        # Count total rows
        print("\n=== Dataset Size ===")
        count_result = pd.read_sql("SELECT COUNT(*) as total FROM features;", con)
        total_rows = count_result.iloc[0]['total']
        print(f"Total roads in dataset: {total_rows:,}")
        
        # Check for key columns and their distributions
        print("\n=== Column Analysis ===")
        
        # Check if surface column exists (ground truth)
        if 'surface' in sample_data.columns:
            surface_dist = pd.read_sql("SELECT surface, COUNT(*) as count FROM features GROUP BY surface ORDER BY count DESC;", con)
            print("Surface distribution (ground truth):")
            print(surface_dist)
        
        # Check if highway column exists
        if 'highway' in sample_data.columns:
            highway_dist = pd.read_sql("SELECT highway, COUNT(*) as count FROM features GROUP BY highway ORDER BY count DESC LIMIT 10;", con)
            print("\nHighway types (top 10):")
            print(highway_dist)
        
        # Check if class_num exists
        if 'class_num' in sample_data.columns:
            class_dist = pd.read_sql("SELECT class_num, COUNT(*) as count FROM features GROUP BY class_num ORDER BY class_num;", con)
            print("\nClass distribution:")
            print(class_dist)
        
        # Check for image-related columns
        image_columns = [col for col in sample_data.columns if 'path' in col.lower() or 'img' in col.lower()]
        if image_columns:
            print(f"\nImage-related columns: {image_columns}")
            
            # Check if image files exist
            if 'chip_path' in sample_data.columns:
                sample_paths = pd.read_sql("SELECT chip_path FROM features LIMIT 5;", con)
                print("\nSample image paths:")
                for path in sample_paths['chip_path']:
                    path_obj = pathlib.Path(path)
                    exists = path_obj.exists()
                    print(f"  {path}: {'✅' if exists else '❌'}")
        
        # Check for geometry column
        if 'wkt' in sample_data.columns:
            print("\n✅ WKT geometry column found")
            # Check sample WKT
            sample_wkt = pd.read_sql("SELECT wkt FROM features LIMIT 1;", con)
            wkt_sample = sample_wkt.iloc[0]['wkt']
            print(f"Sample WKT: {wkt_sample[:100]}...")
        
        print("\n=== Summary ===")
        print(f"✅ Database contains {total_rows:,} road features")
        print(f"✅ Table has {len(features_info)} columns")
        print(f"✅ Ready for inference with MassInferenceDataset")

except Exception as e:
    print(f"❌ Error accessing database: {e}")
    import traceback
    traceback.print_exc()