import streamlit as st
import yfinance as yf
import requests
import json
import pandas as pd

# Setup Google Generative AI
GOOGLE_API_KEY = "AIzaSyCffMQoYpKJzdk46zTONhlQm6VI21ihWLQ"
GENERATIVE_MODEL = "gemini-1.5-flash"

def get_generative_ai_response(prompt):
    try:
        url = f"https://generativeai.googleapis.com/v1/models/{GENERATIVE_MODEL}:generateText?key={GOOGLE_API_KEY}"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get('candidates', [{}])[0].get('output', 'No response text available')
    except Exception as e:
        st.error(f"Error fetching response from Generative AI: {e}")
        return None

# Title
st.title("Investment Advice App")

# User inputs
monthly_savings = st.number_input("Enter your monthly savings (in Rs):", min_value=0, value=5000, step=100)
investment_duration = st.number_input("Enter the investment duration (in months):", min_value=1, value=24, step=1)

# Calculate total savings
total_savings = monthly_savings * investment_duration
st.write(f"Total savings after {investment_duration} months: Rs {total_savings}")

# Generate investment advice
st.header("Investment Advice")

# Risk Tolerance
risk_tolerance = st.selectbox("Select your risk tolerance level:", ["Low", "Moderate", "High"])

# User input for custom prompt
user_input_prompt = st.text_area("Enter your custom prompt for investment advice:", value=f"""
I am currently in class 11th and have 2 years before joining an engineering college. The total fees for 4 years of college is Rs. 10 lakh. I can save Rs. {monthly_savings} every month, accumulating a total amount of Rs. {total_savings} after {investment_duration} months. 
I want to invest this money on a monthly basis to maximize profit or return with minimal risk, so that I can pay as much of my fees from the investment as possible. 
Please provide specific companies, stocks, or mutual funds suitable for a {risk_tolerance} risk tolerance.
""")

if st.button("Get Investment Advice"):
    response = get_generative_ai_response(user_input_prompt)
    if response:
        st.write(response)

# Fetch stock data using yfinance
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    return hist

# Example stock tickers (you can replace these with your choices)
stock_tickers = {
    "HDFC Bank": "HDFCBANK.NS",
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS"
}

# Display stock data
st.header("Stock Data")
for company, ticker in stock_tickers.items():
    st.subheader(company)
    data = fetch_stock_data(ticker)
    st.line_chart(data["Close"])

# Monthly Savings Plan Table
st.header("Monthly Savings Plan")

# Table data
table_data = {
    "Expense": ["Hostel Fees", "Mess Fees", "Personal Expenses", "Academic Supplies", "Miscellaneous"],
    "Original Amount (Rs)": [5000, 3000, 2000, 1000, 1000],
    "Savings Strategy": [
        "Shared room or annual payment discount (10%)",
        "Cooking 5 meals a month (saves Rs 50 per meal)",
        "Reducing non-essential expenses by 20%",
        "Buying second-hand or digital books (saves 30%)",
        "Limiting miscellaneous spending by 20%"
    ],
    "New Amount (Rs)": [4500, 2750, 1600, 700, 800],
    "Monthly Savings (Rs)": [500, 250, 400, 300, 200]
}

# Create DataFrame
df = pd.DataFrame(table_data)

# Display table
st.table(df)

# Footer
st.write("This app provides general investment advice based on your inputs. Please consult with a financial advisor before making any investment decisions.")

