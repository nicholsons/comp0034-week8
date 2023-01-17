import pickle
from pathlib import Path
import numpy as np
from flask import (
    render_template,
    current_app as app,
    request,
    redirect,
    url_for,
)


pickle_file = Path(__file__).parent.joinpath("data", "model_lr.pkl")
IRIS_MODEL = pickle.load(open(pickle_file, "rb"))


@app.route("/")
def index():
    """Create the homepage"""
    return render_template("index.html")


''' Version after activity 1
@app.get("/predict")
def predict():
    """Predict iris species

    Takes the arguments sepal_length,sepal_width,petal_length,petal_width  from an HTTP request; passes them as arguments to a function to get a prection of the iris variety and returns the result.

    Returns:
        species(str): A string of the iris species.
    """

    sepal_length = request.args.get("sep-len")
    sepal_width = request.args.get("sep-wid")
    petal_length = request.args.get("pet-len")
    petal_width = request.args.get("pet-wid")

    prediction = make_prediction(
        [sepal_length, sepal_width, petal_length, petal_width]
    )

    return prediction
'''

# Version after activity 2
@app.get("/predict")
def predict():
    """Predict iris species

    Takes the arguments sepal_length,sepal_width,petal_length,petal_width  from an HTTP request; passes them as arguments to a function to get a prection of the iris variety and returns the result.

    Returns:
        species(str): A string of the iris species.
    """

    sepal_length = request.args.get("sep-len")
    sepal_width = request.args.get("sep-wid")
    petal_length = request.args.get("pet-len")
    petal_width = request.args.get("pet-wid")

    prediction = make_prediction(
        [sepal_length, sepal_width, petal_length, petal_width]
    )

    prediction_text = f"Predicted Class: {prediction}"

    return redirect(url_for("index", prediction_text=prediction_text))


def make_prediction(flower_values):
    """Takes the flower values, makes a model using the prediction and returns a string of the predicted flower variety

    Parameters:
    flower_values (List): List of sepal length, sepal width, petal length, petal width

    Returns:
    variety (str): Name of the predicted iris variety
    """

    # Convert to a 2D numpy array with float values, needed as input to the model
    input_values = np.asarray([flower_values], dtype=float)

    # Get a prediction from the model
    prediction = IRIS_MODEL.predict(input_values)

    # convert the prediction to the variety name
    varieties = {0: "iris-setosa", 1: "iris-versicolor", 2: "iris-virginica"}
    variety = np.vectorize(varieties.__getitem__)(prediction[0])

    return variety
