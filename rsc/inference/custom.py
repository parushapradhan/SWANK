#!/usr/bin/env python3
""" Custom dataset for features.csv that works with evaluate.py """

import pandas as pd
import pathlib
import torch
from torch.utils.data import Dataset
from rsc.common.utils import imread
import sqlite3
class CustomFeaturesDataset(Dataset):
    def __init__(self, csv_path, transform=None):
        """
        Custom dataset for features.csv structure
        
        Args:
            csv_path: Path to features.csv
            transform: Preprocessing transform
        """
        self.df = pd.read_csv(csv_path)
        self.transform = transform
        print(f"Loaded {len(self.df)} features from {csv_path}")
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        
        # Load image from chip_path
        image = imread(row['chip_path'])
        
        # Apply transform if provided
        if self.transform:
            image = self.transform(image)
        
        # Return in format expected by evaluate.py: (osm_id, x)
        return row['osm_id'], image
        
class CustomSQLiteDataset(Dataset):
    def __init__(self, sqlite_path, transform=None):
        with sqlite3.connect(sqlite_path) as con:
            self.df = pd.read_sql('SELECT * FROM features', con)
        self.transform = transform
        print(f"Loaded {len(self.df)} features from SQLite")
        print(f"Columns: {list(self.df.columns)}")
    
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        
        # Debug: print what we're trying to access
        print(f"Row {idx}: osm_id={row['osm_id']}, chip_path={row['chip_path']}")
        
        # Load image from chip_path
        image = imread(row['chip_path'])
        
        # Apply transform if provided
        if self.transform:
            image = self.transform(image)
        
        # Return in format expected by evaluate.py: (osm_id, x)
        return row['osm_id'], image