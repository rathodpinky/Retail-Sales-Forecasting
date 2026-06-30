import joblib

model = joblib.load("models/Retail_Final_Model.pkl")

scaler = joblib.load("models/standard_scaler.pkl")


def predict(data):

    data_scaled = scaler.transform(data)

    prediction = model.predict(data_scaled)

    return prediction