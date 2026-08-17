import joblib
import pandas as pd

# Load model and scaler
model = joblib.load("model/final_churn_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# Exact feature order used during training
MODEL_COLUMNS = model.get_booster().feature_names


def predict_customer(customer_data):
    """
    customer_data: dictionary from the form
    returns: prediction (0/1), probability
    """

    # One customer only
    df = pd.DataFrame([customer_data])

    # ---------- Numeric ----------
    # ---------- Convert numeric columns ----------
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(int)

    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    df[numeric_cols] = df[numeric_cols].astype(float)
        # ---------- Scale only numeric ----------
    numeric_cols = scaler.feature_names_in_
    df[numeric_cols] = scaler.transform(df[numeric_cols])

    # ---------- One-hot encoding ----------
    categorical = [
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod"
    ]

    df = pd.get_dummies(df, columns=categorical)

    # ---------- Match model columns ----------
    for col in MODEL_COLUMNS:
        if col not in df.columns:
            df[col] = 0

    df = df[MODEL_COLUMNS]

    # ---------- Predict ----------
    probability = model.predict_proba(df)[0][1]
    prediction = int(probability >= 0.5)

    return prediction, probability