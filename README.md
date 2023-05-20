# Model server boilerplate (using flask)

This project is a Flask-based server for serving machine learning models. It currently supports models from TensorFlow and scikit-learn.

## Requirements

* Docker (version 20.10.5 or later)

## Setup

To set up and run this server, follow these steps:

1. Clone this repository to your local machine:

```sh
git clone https://github.com/cabjr/model-server-boilerplate.git
```

2. Build the Docker image:
```sh
docker build -t model-server .
```
Run the Docker container:
```sh
docker run -p 5000:5000 model-server
```
The Flask server should now be running on localhost:5000.

## Endpoints
The server exposes the following endpoints:

**POST** /predict: Make a prediction using a machine learning model.

- Input: A JSON object with two properties: model_type (a string that is either "tensorflow" or "scikit") and features (an array of feature values).
- Output: A JSON object with a prediction property containing the model's prediction.

**GET** /livenessprobe: Check that the server is running and that the models are loaded and working correctly. Returns a JSON object with a status property that is either "healthy" or "error".

## Adding Models
To add a new model, follow these steps:

- Save your model to a file.
- Add the model file path, input shape, and output shape to the model_metadata.json file.
- If your model is not a TensorFlow or scikit-learn model, you will need to modify main.py to handle your type of model.

## License
This project is licensed under the terms of the MIT license.
