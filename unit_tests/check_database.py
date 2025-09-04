# First, let's see what's in your features.sqlite
import sqlite3
import pandas as pd

database_path = '/ocean/projects/cis250156p/ppradhan/road_surface_classifier-master/data/road_surface_classifier/features.sqlite3'

# Check the database
with sqlite3.connect(database_path) as con:
    # See what tables exist
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", con)
    print("Tables in database:")
    print(tables)
    
    # Check the features table
    features = pd.read_sql("SELECT * FROM features LIMIT 5;", con)
    print("\nFirst 5 features:")
    print(features.columns.tolist())
    print(features.head())
    
    # Count total features
    count = pd.read_sql("SELECT COUNT(*) as total FROM features;", con)
    print(f"\nTotal roads in database: {count.iloc[0]['total']}")
    
    # Check surface distribution (if you have ground truth)
    if 'surface' in features.columns:
        surface_dist = pd.read_sql("SELECT surface, COUNT(*) as count FROM features GROUP BY surface;", con)
        print("\nSurface distribution:")
        print(surface_dist)