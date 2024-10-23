import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load your preprocessed data
@st.cache_data
def load_data():
    df = pd.read_parquet("./preprocessed_NSE_Data_2024.parquet")
    return df

data = load_data()


# Authentication
def authenticate(username, password):
    # Replace with actual authentication logic
    return username == "root" and password == "admin"

# Login page
def login_page():
    st.title("NSE Stock Data Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.experimental_set_query_params(logged_in="true")
            st.experimental_rerun()  # Alternatively, use this if you need to trigger a rerun
        else:
            st.error("Invalid credentials")

# Main dashboard
def main_dashboard(df):
    st.title("NSE Stock Performance 2024")
    
    # Latest 7 days stock bar graph
    end_date = df['TradDt'].max()
    start_date = end_date - timedelta(days=6)
    last_7_days = df[(df['TradDt'] >= start_date) & (df['TradDt'] <= end_date)]
    
    fig = go.Figure(data=[go.Bar(x=last_7_days['TradDt'], y=last_7_days['ClsPric'])])
    st.plotly_chart(fig)
    
    # Top gainers and losers
    # Implement logic to calculate top gainers and losers
    # Display in a table

# Favorite stock page
def favorite_stock_page(df, stock):
    st.title(f"{stock} Details")
    
    # Stock definition
    # Add logic to fetch and display stock definition
    
    # Weekly trend
    # Implement logic to show weekly trend for the selected stock

# Main app logic
def main():
    df = load_data()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_dashboard(df)
        
        # Sidebar for favorite stock
        with st.sidebar:
            st.header("Enter Your Favorite Stock")
            stock = st.text_input("Stock Symbol")
            if st.button("View Stock Details"):
                if stock in df['TckrSymb'].unique():
                    favorite_stock_page(df, stock)
                else:
                    st.error("Stock not found")

if __name__ == "__main__":
    main()
# st.write(data.head())

# # Sidebar for user input
# st.sidebar.header('User Input Features')

# # Select ticker symbol
# ticker = st.sidebar.selectbox(
#     'Select Ticker Symbol:',
#     sorted(data['TckrSymb'].unique())
# )

# # Filter data by selected ticker
# filtered_data = data[data['TckrSymb'] == ticker]

# # Display basic information
# st.write(f"## Stock Data for {ticker}")
# st.write(f"Data Range: {filtered_data['TradDt'].min()} to {filtered_data['TradDt'].max()}")

# # Plot closing price and moving averages
# st.write("### Closing Price and Moving Averages")
# fig, ax = plt.subplots()
# ax.plot(filtered_data['TradDt'], filtered_data['ClsPric'], label='Closing Price')
# ax.plot(filtered_data['TradDt'], filtered_data['MA5'], label='MA5', linestyle='--')
# ax.plot(filtered_data['TradDt'], filtered_data['MA20'], label='MA20', linestyle='--')
# ax.set_xlabel('Date')
# ax.set_ylabel('Price')
# ax.legend()
# st.pyplot(fig)

# # Plot trading volume and volume moving average
# st.write("### Trading Volume and Volume Moving Average")
# fig, ax = plt.subplots()
# ax.bar(filtered_data['TradDt'], filtered_data['TtlTradgVol'], label='Trading Volume')
# ax.plot(filtered_data['TradDt'], filtered_data['VolMA10'], label='VolMA10', color='orange', linestyle='--')
# ax.set_xlabel('Date')
# ax.set_ylabel('Volume')
# ax.legend()
# st.pyplot(fig)

# # Plot volatility
# st.write("### Volatility")
# fig, ax = plt.subplots()
# ax.plot(filtered_data['TradDt'], filtered_data['Volatility'], label='Volatility', color='red')
# ax.set_xlabel('Date')
# ax.set_ylabel('Volatility')
# ax.legend()
# st.pyplot(fig)

# # Display table of data
# st.write("### Data Table")
# st.write(filtered_data)

# # Additional features
# st.sidebar.write("Additional Features")
# if st.sidebar.checkbox("Show Raw Data"):
#     st.write(filtered_data)

