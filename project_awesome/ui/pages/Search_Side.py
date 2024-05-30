import streamlit as st
import pandas as pd

st.title('Company Finder')

# search bar
search_query = st.text_input('Enter search query:')

# sample data for demonstration
data = {
    'Name': ['Apple', 'Netflix', 'Starbucks', 'Nvidia', 'Meta', 'Amazon', 'Google', 'Microsoft', 'Tesla', 'IBM'],
    'Classification': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
    'Ticker': ['AAPL', 'NFLX', 'SBUX', 'NVDA', 'META', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'IBM'],
    'Industry': ['Tech', 'Tech', 'Non-tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Non-tech', 'Tech'],
    '2020 Stock Price': [120, 500, 80, 300, 250, 3200, 1500, 200, 700, 130],
    '2021 Stock Price': [140, 550, 85, 350, 270, 3400, 1600, 250, 800, 150],
    '2022 Stock Price': [130, 530, 90, 340, 280, 3300, 1550, 260, 820, 140],
    '2023 Stock Price': [150, 600, 100, 360, 290, 3500, 1650, 270, 840, 160],
    '2024 Stock Price': [160, 620, 110, 370, 300, 3600, 1700, 280, 860, 170]
}

# data = pd.read_csv('data.csv')

df = pd.DataFrame(data)

# set ticker as index
df = df.set_index('Ticker')

# filter data based on search query
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    filtered_df = df

# assign colors to values (classifications)
def highlight_age(value):
    if value == 1:
        return 'color: green'
    elif value == 2:
        return 'color: orange'
    else:
        return 'color: red'

def apply_styles(filtered_df):
    return filtered_df.style.applymap(highlight_age, subset=['Classification'])

# apply styles to df
styled_df = apply_styles(filtered_df)

# show the styled df
st.dataframe(styled_df)

# drop all unnecessay columns
df_drop = filtered_df.drop(columns=['Classification', 'Industry', 'Name'])

# transpose the df to switch rows and columns for plotting
df_drop_transposed = df_drop.T

# plot line chart
st.title('Stock Prices Over Years')
st.line_chart(df_drop_transposed)
