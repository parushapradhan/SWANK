#!/usr/bin/env python3
""" Test the CustomSQLiteDataset """

import sys
import os
sys.path.append(os.getcwd())

from rsc.inference.custom import CustomSQLiteDataset

# Test the dataset
sqlite_path = "/ocean/projects/cis250156p/ppradhan/road_surface_classifier-master/data/road_surface_classifier/features.sqlite3"

try:
    dataset = CustomSQLiteDataset(sqlite_path)
    print(f"Dataset length: {len(dataset)}")
    
    # Test first item
    osm_id, image = dataset[0]
    print(f"First item - osm_id: {osm_id}, image shape: {image.shape}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
