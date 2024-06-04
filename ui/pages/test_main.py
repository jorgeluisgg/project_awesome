import streamlit as st

import pandas as pd
import seaborn as sns
import requests

st.title('Company Finder')

# search bar
search_query = st.text_input('Enter search query:')

# pull the csv file
data = pd.read_csv('../raw_data/raw_data_ui.csv')

# converting data into a df
df = pd.DataFrame(data)

# set ticker as index
df = df.set_index('Ticker')

# filter data based on search query
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    filtered_df = df

def highlight_age(value):
    if value > 1.1:
        return 'color: green'
    elif value > 0.9 and value < 1.1:
        return 'color: yellow'
    else:
        return 'color: red'



def apply_styles(filtered_df):
    return filtered_df.style.applymap(highlight_age, subset=['2024 Ratio Stock/S&P500'])

# apply styles to df
styled_df = apply_styles(filtered_df)

# show the styled df
st.dataframe(styled_df)

# drop all unnecessay columns
df_drop = filtered_df.drop(columns=['Name', 'Last Sale', 'Market Cap', 'Sector', 'Industry', 'Recommendation'])

# transpose the df to switch rows and columns
df_drop_transposed = df_drop.T

# show line chart
st.title('Stock Ratio Over Years')
st.line_chart(df_drop_transposed)


import streamlit as st
import requests

# define base URL
url = 'https://lw-project-image-g4ikxb6kuq-ew.a.run.app/classify?'

# Allow the user to input ticker symbols
tickers = st.text_input('Enter ticker symbols separated by commas:', 'AAPL, GOOG')

# Convert the input string to a list
ticker_list = [ticker.strip() for ticker in tickers.split(',')]

# Set up parameters for the API request
params = {'ticker': ticker_list}

# Make the API request
response = requests.get(url, params=params)

# Display the response
st.write(response.json())
