"""
utils.py
Handles data preprocessing, model loading, and churn prediction logic.
"""

import os
import joblib
import pandas as pd


def predict_churn(form_data):
    print("✅ predict_churn() is running")
    try:

        # --------------------------------------------------
        # Locate Model Folder
        # --------------------------------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        models_dir = os.path.join(project_root, "models")

        print("\n" + "=" * 70)
        print("DEBUG: Loading model artifacts from:")
        print(models_dir)
        print("=" * 70)

        # --------------------------------------------------
        # Load Files
        # --------------------------------------------------

        model = joblib.load(
            os.path.join(models_dir, "customer_churn_model.pkl")
        )

        scaler = joblib.load(
            os.path.join(models_dir, "scaler.pkl")
        )

        features = joblib.load(
            os.path.join(models_dir, "features.pkl")
        )

        print("✅ All model files loaded successfully.")

        # --------------------------------------------------
        # Read Form Data
        # --------------------------------------------------

        customer = {
            "SeniorCitizen": int(form_data.get("SeniorCitizen", 0)),
            "Partner": form_data.get("Partner", "No"),
            "Dependents": form_data.get("Dependents", "No"),
            "tenure": int(form_data.get("tenure", 0)),
            "PhoneService": form_data.get("PhoneService", "No"),
            "MultipleLines": form_data.get("MultipleLines", "No"),
            "InternetService": form_data.get("InternetService", "No"),
            "OnlineSecurity": form_data.get("OnlineSecurity", "No"),
            "OnlineBackup": form_data.get("OnlineBackup", "No"),
            "DeviceProtection": form_data.get("DeviceProtection", "No"),
            "TechSupport": form_data.get("TechSupport", "No"),
            "StreamingTV": form_data.get("StreamingTV", "No"),
            "StreamingMovies": form_data.get("StreamingMovies", "No"),
            "Contract": form_data.get("Contract", "Month-to-month"),
            "PaperlessBilling": form_data.get("PaperlessBilling", "Yes"),
            "PaymentMethod": form_data.get(
                "PaymentMethod",
                "Electronic check",
            ),
            "MonthlyCharges": float(
                form_data.get("MonthlyCharges", 0)
            ),
            "TotalCharges": float(
                form_data.get("TotalCharges", 0)
            ),
        }

        # --------------------------------------------------
        # Convert to DataFrame
        # --------------------------------------------------

        df = pd.DataFrame([customer])

        df = pd.get_dummies(df, drop_first=True)

        df = df.reindex(columns=features, fill_value=0)

        cols_to_scale = [
            "tenure",
            "MonthlyCharges",
            "TotalCharges",
        ]

        df[cols_to_scale] = scaler.transform(df[cols_to_scale])

        # --------------------------------------------------
        # Prediction
        # --------------------------------------------------

        prediction = model.predict(df)[0]

        probability = model.predict_proba(df)[0][1]

        probability = round(probability * 100, 2)

        churn = prediction == 1

        if churn:
            text = "Customer is likely to churn."
        else:
            text = "Customer is likely to stay."

        return text, probability, churn

    except Exception as e:
        raise Exception(f"Prediction pipeline failed:\n\n{str(e)}")