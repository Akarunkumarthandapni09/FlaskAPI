import os
import sys
import logging
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import traceback

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Use persistent directory for Azure
BASE_DIR = "/home/site/wwwroot"

# Load trained model and label map
try:
    model_path = os.path.join(BASE_DIR, "approval_model.pkl")
    label_map_path = os.path.join(BASE_DIR, "label_map.pkl")
    
    model = joblib.load(model_path)
    label_map = joblib.load(label_map_path)
    
    app.logger.info(f"Model loaded from {model_path}")
    app.logger.info(f"Label map loaded from {label_map_path}")
except Exception as e:
    app.logger.error("Error loading model files: %s", e)
    app.logger.error("Traceback:\n%s", traceback.format_exc())
    raise

@app.route("/")
def home():
    return "Service is running", 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON"}), 400

        req_type = data.get("request_type")
        desc = data.get("description")
        if not req_type or not desc:
            return jsonify({"error": "Both request_type and description are required"}), 400

        df = pd.DataFrame([{"request_type": req_type, "description": desc}])
        pred_label = int(model.predict(df)[0])
        pred_flow = label_map.get(pred_label, "Unknown")

        app.logger.info(f"Prediction: {pred_flow} for input {data}")
        return jsonify({"approval_flow": pred_flow})

    except Exception as e:
        app.logger.error("Prediction error: %s", e)
        app.logger.error("Traceback:\n%s", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
