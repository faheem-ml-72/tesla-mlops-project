from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import joblib
import numpy as np
import datetime

# Load trained model
model = joblib.load("model/tesla_gp_model.pkl")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Tesla Stock Prediction API is Running"}


@app.get("/predict/{days_ahead}")
def predict(days_ahead: int):

    today = datetime.date.today()
    future_date = today + datetime.timedelta(days=days_ahead)

    future_ordinal = np.array([[future_date.toordinal()]])

    prediction, sigma = model.predict(future_ordinal, return_std=True)

    return {
        "predicted_price": float(prediction[0]),
        "lower_bound": float(prediction[0] - 2 * sigma[0]),
        "upper_bound": float(prediction[0] + 2 * sigma[0])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/app", response_class=HTMLResponse)
def web_app():
    return """
    <html>
        <head>
            <title>Tesla Stock Predictor</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>🚀 Tesla Stock Prediction</h1>
            <form action="/predict">
                <label>Enter number of days ahead:</label><br><br>
                <input type="number" name="days_ahead" required>
                <br><br>
                <button type="submit">Predict</button>
            </form>
        </body>
    </html>
    """
