from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Handle audio file prediction here
    # You can use request.files to get the audio file
    # Process the file using your deep learning model
    # Return the prediction result
    return "Prediction: [Human/AI]"


if __name__ == "__main__":
    app.run(debug=True)
