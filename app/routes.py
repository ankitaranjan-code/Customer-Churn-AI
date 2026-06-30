from flask import Blueprint, render_template, request
from app.utils import predict_churn

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")


@main.route("/predict", methods=["POST"])
def predict():

    try:

        prediction_text, prediction_prob, churn_result = predict_churn(request.form)

        return render_template(
            "index.html",
            prediction_text=prediction_text,
            prediction_prob=prediction_prob,
            churn_result=churn_result
        )

    except Exception as e:

        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}",
            prediction_prob=0,
            churn_result=False
        )