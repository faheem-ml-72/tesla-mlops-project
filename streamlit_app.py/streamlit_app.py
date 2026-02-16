import streamlit as st
import requests

st.title("Tesla Stock Prediction")

days = st.number_input("Enter number of days ahead:", min_value=1, step=1)

if st.button("Predict"):

    url = f"https://tesla-stock-api-faheem.onrender.com/predict/{days}"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Price: {result['predicted_price']}")
        st.write(f"Lower Bound: {result['lower_bound']}")
        st.write(f"Upper Bound: {result['upper_bound']}")
    else:
        st.error("Error fetching prediction")

