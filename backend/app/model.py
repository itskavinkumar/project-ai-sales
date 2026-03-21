import joblib
import os

# Get absolute path to model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "lead_scoring_model.pkl")

# Load model
model = joblib.load(MODEL_PATH)
