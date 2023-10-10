import streamlit as st
import matplotlib.pyplot as plt
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

plt.scatter(gwei_values, transaction_prices)
plt.xlabel("Gwei")
plt.ylabel("Transaction price")

st.pyplot(plt)
