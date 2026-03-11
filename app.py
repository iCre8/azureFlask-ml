from flask import Flask, request, jsonify
import logging
from flask.logging import create_logger

import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def scale(payload):
    """Scales Payload"""

    LOG.info("Scaling Payload")
    scaler = StandardScaler().fit(payload)
    scaled_adhoc_predict = scaler.transform(payload)
    return scaled_adhoc_predict

@app.route("/")
def home():
    html = "<h3> Prediction Home</h3>"
    return html.format(format)

@app.route("/predict", methods=['POST'])
def predict():
    """Performs an sklearn prediction

    input looks like:
            {
    "CHAS":{
      "0":0
    },
    "RM":{
      "0":6.575
    },
    "TAX":{
      "0":296.0
    },
    "PTRATIO":{
       "0":15.3
    },
    "B":{
       "0":396.9
    },
    "LSTAT":{
       "0":4.98
    }

    result looks like:
    { "prediction": [ 20.35373177134412 ] }

    """

    try:
        clf = joblib.load("boston_housing_prediction.joblib")
    except OSError as e:
        LOG.error("Failed to load model: %s", str(e))
        return jsonify({'error': 'Model not loaded'}), 500

    json_payload = request.json
    if not json_payload:
        return jsonify({'error': 'Empty payload'}), 400
    
    inference_payload = pd.DataFrame(json_payload)
    if inference_payload.empty:
        return jsonify({'error': 'Invalid payload'}), 400
    
    LOG.info("JSON payload received")
    inference_payload = pd.DataFrame(json_payload)
    LOG.info("Inference payload DataFrame created: %s", inference_payload.shape)
    scaled_payload = scale(inference_payload)
    prediction = list(clf.predict(scaled_payload))
    LOG.info("Prediction: %s", prediction)
    return jsonify({'prediction': prediction})

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
