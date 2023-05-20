# Model server boilerplate (using flask)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=flat-square&logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/-TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/-Scikit%20Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![k6](https://img.shields.io/badge/-k6-0899D3?style=flat-square&logo=k6&logoColor=white)
![Gunicorn](https://img.shields.io/badge/-Gunicorn-6D0202?style=flat-square&logo=gunicorn&logoColor=white)

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

## Load Testing

We use [k6](https://k6.io/) for load testing our service. Follow the steps below to run a load test.

### Step 1: Install k6

If you haven't installed k6 on your machine, please follow the instructions on the [official k6 installation guide](https://k6.io/docs/getting-started/installation) for your specific platform.

### Step 2: Configure the load test

We have prepared a script for load testing named `loadTest.js` at the root directory of the project.

This script sends a `POST` request to the `/predict` route on your Flask server every second for 30 seconds with 10 simultaneous virtual users. It checks whether the response has a status 200 and whether the transaction time is less than 200 milliseconds.

In `loadTest.js`, the `options` object defines the parameters for the load test:

```javascript
export let options = {
    vus: 10,  // number of virtual users
    duration: '30s',  // duration of the test
};
``` 
You can adjust these parameters to fit your load testing needs.

### Step 3: Run the load test

First, make sure your Flask server is running. Then, you can start the load test by running the following command in your terminal:

```bash
k6 run loadTest.js
```

If your server is running on a different host or port, you'll need to update the URL in the load test script.

The load test will simulate the traffic to your server based on the parameters you set in the options object in loadTest.js.

Remember to monitor the resources of the server during the test to see how it behaves under load and adjust your configuration or infrastructure accordingly based on the results.

## License
This project is licensed under the terms of the MIT license.
