# Quick script to check your model's classes
# import torch
import pathlib
from tqdm import tqdm

import torch
from rsc.train.plmcnn import PLMaskCNN



def check_model_classes(model_path):
    """Check what classes your model predicts"""
    
    # Load model
    model = PLMaskCNN.load_from_checkpoint(model_path, map_location=torch.device('cpu'))
    
    # Get labels
    labels = model.__dict__.get('labels')
    
    print("Model predicts these classes:")
    for i, label in enumerate(labels):
        print(f"  {i}: {label}")
    
    print(f"\nTotal classes: {len(labels)}")
    
    # Check if it's detailed classification
    if 'asphalt' in labels and 'concrete' in labels:
        print("✅ Model can distinguish asphalt vs concrete!")
    elif 'paved' in labels:
        print("ℹ️ Model uses simplified paved/unpaved classification")
    else:
        print("❓ Unknown classification scheme")
    
    return labels

# Run the check
model_path = '/ocean/projects/cis250156p/ppradhan/road_surface_classifier-master/data/road_surface_classifier/results/20250902_154834Z/model-epoch=14-val_loss=0.75055.ckpt'  # Update this
labels = check_model_classes(model_path)