import streamlit as st
import requests

import pandas as pd

# header
st.title('Company Finder')

# search bar
search_query = st.text_input('Enter search query:')


# define the API endpoint
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'

# API call
response = requests.get(url)

# turn API into df
df = pd.DataFrame(response.json())

# setting ticker as index
#df = df.set_index('Ticker')

# filter data based on search query
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    filtered_df = df

def highlight_age(value):
    if value == 'IBM':
        return 'color: green'
    elif value == 'Compact':
        return 'color: yellow'
    else:
        return 'color: red'

def apply_styles(filtered_df):
    return filtered_df.style.applymap(highlight_age, subset=['Meta Data'])

# apply styles to df
styled_df = apply_styles(filtered_df)

# show the styled df
st.dataframe(styled_df)
