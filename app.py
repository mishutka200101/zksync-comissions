import streamlit as st
import plotly.express as px
import pandas as pd
from pymongo import MongoClient


def fetch_data():
    client = MongoClient(st.secrets["db_url"])
    db = client["zksync"]
    collection = db["txs-prices"]

    return list(collection.find({}))


data = fetch_data()


gwei_values = [item["gwei"] for item in data]
transaction_prices = [(item["syncswap_fee"] + item["spacefi_fee"] +
                       item["woofi_fee"] + item["mavprot_fee"]) / 4 for item in data]

df = pd.DataFrame({
    "gwei": gwei_values,
    "avg_fee": transaction_prices
})

fig = px.scatter(df, x="gwei", y="avg_fee",
                 title="Зависимость средней цены транзакции от gwei")

st.plotly_chart(fig)
