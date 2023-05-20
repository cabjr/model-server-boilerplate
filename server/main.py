from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import joblib
import json
import os

app = Flask(__name__)

# Load model metadata
with open("/models/model_metadata.json", "r") as file:
    model_metadata = json.load(file)

# Load the models at app startup
models = {}
for library, library_models in model_metadata.items():
    for model_name, metadata in library_models.items():
        if library == 'tensorflow':
            models[model_name] = load_model(metadata['model_path'])
        else:
            # Assume it's a scikit-learn model
            models[model_name] = joblib.load(metadata['model_path'])

@app.route('/livenessprobe', methods=['GET'])
def livenessprobe():
    # Attempt to use each model to make sure it's loaded and working
    for model_name, model in models.items():
        library = 'tensorflow' if 'tensorflow' in model_name else 'scikit'
        dummy_input = np.zeros(model_metadata[library][model_name]['input_shape']).tolist()
        try:
            model.predict(dummy_input)
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Error on model {model_name}: {str(e)}'}), 500

    return jsonify({'status': 'healthy'}), 200

@app.route('/predict', methods=['POST'])
def predict():
    # Get the model type and name from the POST data
    model_library = request.json['model_library']
    model_name = request.json['model_name']

    # Get the model for this type
    model = models.get(model_name)

    if model is None:
        return jsonify({'error': 'Invalid model name'}), 400

    # Get the features from the POST data
    features = np.array(request.json['features'])

    # Check if the input shape matches the expected shape for this model
    expected_input_shape = model_metadata[model_library][model_name]['input_shape']
    if features.shape != tuple(expected_input_shape):
        return jsonify({'error': 'Invalid input shape'}), 400

    # Make a prediction using the model
    if model_library == 'tensorflow':
        prediction = model.predict(features).tolist()
    else:
        # Assume it's a scikit-learn model
        prediction = model.predict(features).tolist()

    # Check if the output shape matches the
    # Check if the output shape matches the expected shape for this model
    expected_output_shape = model_metadata[model_library][model_name]['output_shape']
    if len(prediction) != expected_output_shape[0]:
        return jsonify({'error': 'Unexpected prediction shape'}), 500

    # Return the prediction
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
