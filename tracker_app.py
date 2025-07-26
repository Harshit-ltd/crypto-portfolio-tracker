import streamlit as st
import json
import requests
import pandas as pd
from datetime import datetime

# Load portfolio from JSON
def load_portfolio():
    with open("portfolio.json", "r") as file:
        return json.load(file)

# Save portfolio back to JSON (optional: for future editing features)
def save_portfolio(portfolio):
    with open("portfolio.json", "w") as file:
        json.dump(portfolio, file, indent=4)

# Get real-time prices from CoinGecko
def get_prices(symbols):
    ids = ",".join(symbols)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd,inr"
    response = requests.get(url)
    return response.json()

# Streamlit app layout
st.set_page_config(page_title="💰 Crypto Portfolio Tracker", layout="wide")
st.title("💼 Real-Time Crypto Portfolio Tracker")
st.caption("Built with ❤️ using Python + Streamlit + CoinGecko API")

portfolio = load_portfolio()
symbols = list(portfolio.keys())

price_data = get_prices(symbols)

# Dataframe for display
rows = []

total_usd = 0
total_inr = 0
alerts = []

for symbol in symbols:
    info = portfolio[symbol]
    amount = info["amount"]
    buy_price = info["buy_price"]
    alert_above = info.get("alert_above")

    current_usd = price_data[symbol]["usd"]
    current_inr = price_data[symbol]["inr"]

    value_usd = current_usd * amount
    value_inr = current_inr * amount
    gain_usd = value_usd - (buy_price * amount)

    total_usd += value_usd
    total_inr += value_inr

    if alert_above and current_usd > alert_above:
        alerts.append(f"🚨 {symbol.upper()} crossed ${alert_above}! Current: ${current_usd}")

    rows.append({
        "Token": symbol.capitalize(),
        "Amount": amount,
        "Buy Price (USD)": f"${buy_price}",
        "Current Price (USD)": f"${current_usd}",
        "Value (USD)": f"${value_usd:,.2f}",
        "Gain/Loss (USD)": f"${gain_usd:,.2f}",
        "Value (INR)": f"₹{value_inr:,.2f}"
    })

df = pd.DataFrame(rows)

st.dataframe(df, use_container_width=True)

# Show portfolio summary
col1, col2 = st.columns(2)
col1.metric("📊 Total Portfolio Value (USD)", f"${total_usd:,.2f}")
col2.metric("💹 Total Portfolio Value (INR)", f"₹{total_inr:,.2f}")

# Alerts
if alerts:
    st.warning("⚠️ Alerts Triggered:")
    for alert in alerts:
        st.write(alert)

# Footer
st.caption(f"⏱ Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")