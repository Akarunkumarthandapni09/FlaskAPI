# app.py
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model and label map
model = joblib.load("approval_model.pkl")
label_map = joblib.load("label_map.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    req_type = data.get("request_type")
    desc = data.get("description")

    if not req_type or not desc:
        return jsonify({"error": "Both request_type and description are required"}), 400

    df = pd.DataFrame([{"request_type": req_type, "description": desc}])
    pred_label = int(model.predict(df)[0])
    pred_flow = label_map.get(pred_label, "Unknown")

    return jsonify({"approval_flow": pred_flow})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)