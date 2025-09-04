# config.py
import os
from pathlib import Path

class Config:
    """Configuration class for Road Surface Classifier project"""
    
    # Project root directory
    PROJECT_ROOT = Path(__file__).parent.absolute()
    
    # Data paths
    DATA_ROOT = Path("/ocean/projects/cis250156p/ppradhan/swank")
    DATASET_ROOT = DATA_ROOT / "dataset_multiclass"
    
    # Dataset files
    DATASET_TRAIN = DATASET_ROOT / "dataset_train.csv"
    DATASET_VAL = DATASET_ROOT / "dataset_val.csv"
    CLASS_WEIGHTS_FILE = DATASET_ROOT / "class_weights.csv"
    
    # Results and outputs
    RESULTS_DIR = DATA_ROOT / "results"
    MODELS_DIR = DATA_ROOT / "models"
    LOGS_DIR = DATA_ROOT / "logs"
    
    # AWS and MLFlow settings
    AWS_PROFILE = "truenas"
    MLFLOW_S3_ENDPOINT_URL = "http://truenas.local:9807"
    
    # Model parameters
    CHIP_SIZE = 224
    BATCH_SIZE = 64
    NUM_WORKERS = 16
    LEARNING_RATE = 0.00040984645874638675
    INCLUDE_NIR = True
    
    # Training parameters
    SEG_K = 0.7
    OB_K = 0.9
    
    # Environment-specific overrides
    @classmethod
    def load_from_env(cls):
        """Load configuration from environment variables"""
        if os.getenv("RSC_DATA_ROOT"):
            cls.DATA_ROOT = Path(os.getenv("RSC_DATA_ROOT"))
            cls.DATASET_ROOT = cls.DATA_ROOT / "dataset_multiclass"
            cls.DATASET_TRAIN = cls.DATASET_ROOT / "dataset_train.csv"
            cls.DATASET_VAL = cls.DATASET_ROOT / "dataset_val.csv"
            cls.CLASS_WEIGHTS_FILE = cls.DATASET_ROOT / "class_weights.csv"
            cls.RESULTS_DIR = cls.DATA_ROOT / "results"
            cls.MODELS_DIR = cls.DATA_ROOT / "models"
            cls.LOGS_DIR = cls.DATA_ROOT / "logs"
        
        if os.getenv("RSC_AWS_PROFILE"):
            cls.AWS_PROFILE = os.getenv("RSC_AWS_PROFILE")
        
        if os.getenv("RSC_MLFLOW_ENDPOINT"):
            cls.MLFLOW_S3_ENDPOINT_URL = os.getenv("RSC_MLFLOW_ENDPOINT")
    
    @classmethod
    def setup_environment(cls):
        """Set up environment variables"""
        os.environ["AWS_PROFILE"] = cls.AWS_PROFILE
        os.environ["MLFLOW_S3_ENDPOINT_URL"] = cls.MLFLOW_S3_ENDPOINT_URL
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        for dir_path in [cls.RESULTS_DIR, cls.MODELS_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# Load environment overrides
Config.load_from_env()