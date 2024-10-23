import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta, datetime

@st.cache_data
def load_data():
    df = pd.read_parquet("./data/preprocessed_NSE_Data_2024.parquet")
    return df

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first!")
    st.stop()

data = load_data()

st.title("NSE Stock Performance 2024")

# Date filter
min_date = data['TradDt'].min().date()
max_date = data['TradDt'].max().date()

start_date = st.date_input("Start Date", value=max_date - timedelta(days=6), min_value=min_date, max_value=max_date)
end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

# Convert start_date and end_date to datetime
start_date = datetime.combine(start_date, datetime.min.time())
end_date = datetime.combine(end_date, datetime.min.time())

# Filter data based on selected dates
filtered_data = data[(data['TradDt'] >= start_date) & (data['TradDt'] <= end_date)]

# Calculate the average closing price for each day
average_closing_prices = filtered_data.groupby('TradDt').agg({'ClsPric': 'mean'}).reset_index()

# Line chart for the average closing price each day
st.subheader("Average Closing Price Over Selected Dates")

fig = go.Figure()

# Adding line trace
fig.add_trace(go.Scatter(
    x=average_closing_prices['TradDt'],
    y=average_closing_prices['ClsPric'],
    mode='lines+markers',
    text=average_closing_prices['ClsPric'].round(2).astype(str),
    hoverinfo='text',
    name='Average Closing Price'
))

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Average Closing Price',
    title='Average Closing Price Over Selected Dates'
)

st.plotly_chart(fig)

# Top gainers and losers over the previous 5 days
# last_5_days = data[(data['TradDt'] >= (end_date - timedelta(days=4))) & (data['TradDt'] <= end_date)]
# last_5_days['PriceChange'] = last_5_days['ClsPric'] - last_5_days['PrvsClsgPric']

# # Identify top 5 gainers and losers
# gainers = last_5_days.sort_values(by='PriceChange', ascending=False).head(5)
# losers = last_5_days.sort_values(by='PriceChange').head(5)

# # Line graph for Top Gainers and Losers
# st.subheader("Top Gainers and Losers (Last 5 Days)")
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=gainers['TradDt'], y=gainers['ClsPric'], mode='lines+markers', name='Gainers'))
# fig.add_trace(go.Scatter(x=losers['TradDt'], y=losers['ClsPric'], mode='lines+markers', name='Losers'))
# fig.update_layout(xaxis_title='Date', yaxis_title='Closing Price')
# st.plotly_chart(fig)

# Top 5 Gainers and Losers Section
st.subheader("Top 5 Gainers and Losers")

# Date input for top gainers and losers
selected_date = st.date_input("Select Date for Gainers and Losers", value=max_date, min_value=min_date, max_value=max_date)

# Convert selected_date to datetime
selected_datetime = datetime.combine(selected_date, datetime.min.time())

# Filter data for the selected date
selected_data = data[data['TradDt'] == selected_datetime]

# Calculate daily return percentage
selected_data['DailyReturn'] = (selected_data['ClsPric'] - selected_data['PrvsClsgPric']) / selected_data['PrvsClsgPric'] * 100

# Sort to get top 5 gainers and losers
top_gainers = selected_data.sort_values(by='DailyReturn', ascending=False).head(5)
top_losers = selected_data.sort_values(by='DailyReturn', ascending=True).head(5)

# Display top gainers
st.write("Top 5 Gainers")
st.table(top_gainers[['TckrSymb', 'ClsPric', 'DailyReturn']])

# Display top losers
st.write("Top 5 Losers")
st.table(top_losers[['TckrSymb', 'ClsPric', 'DailyReturn']])





# Stock Search Section
st.subheader("Search for a Stock")

# Initialize state for selected stock
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None

# Search input
search_input = st.text_input("Search Stock by Name or Symbol", "")

# Filter suggestions based on input
if search_input:
    suggestions = data[(data['TckrSymb'].str.contains(search_input.upper())) | 
                       (data['FinInstrmNm'].str.contains(search_input.upper()))]

    if not suggestions.empty:
        suggestion_list = suggestions[['TckrSymb', 'FinInstrmNm']].drop_duplicates().head(10).values.tolist()
        
        for i, (symb, name) in enumerate(suggestion_list):
            if st.button(f"{symb}: {name}", key=f"suggestion_{i}"):
                st.session_state.selected_stock = symb
                break

# Show static details for the selected stock
if st.session_state.selected_stock:
    st.write(f"Details for {st.session_state.selected_stock}:")
    stock_details = data[data['TckrSymb'] == st.session_state.selected_stock].iloc[0]
    static_columns = ['TckrSymb', 'FinInstrmNm', 'ISIN', 'FinInstrmId', 'Sgmt', 'Src']
    st.table(stock_details[static_columns].to_frame().T.reset_index(drop=True))

    selected_stock_data = data[data['TckrSymb'] == st.session_state.selected_stock]
    # Create and display the line chart
    fig = px.line(selected_stock_data, x='TradDt', y='HghPric', title=f"Closing Prices for {st.session_state.selected_stock}")
    st.plotly_chart(fig)

else:
    st.write("Type to search for a stock.")