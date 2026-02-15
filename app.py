from fastapi import FastAPI
import joblib
import numpy as np
import datetime

# Load trained model
model = joblib.load("model/tesla_gp_model.pkl")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tesla Stock Prediction API is Running"}git config --global user.name "Muhammed Faheem"


@app.get("/predict")
def predict(days_ahead: int):

    # Get today's date
    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=days_ahead)

    # Convert date to ordinal
    future_ordinal = np.array([[future_date.toordinal()]])

    # Predict
    prediction, sigma = model.predict(future_ordinal, return_std=True)

    return {
        "predicted_price": float(prediction[0]),
        "lower_bound": float(prediction[0] - 2*sigma[0]),
        "upper_bound": float(prediction[0] + 2*sigma[0])
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
