import streamlit as st
import requests

import pandas as pd

st.title('Company Finder')

# Search bar
search_query = st.text_input('Enter search query:')


# Define the API endpoint
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'

# Make the API call
response = requests.get(url)

# Display the response in the app
df = pd.DataFrame(response.json())

# Setting the Ticker as Index
#df = df.set_index('Ticker')

# Filter data based on search query
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

# Apply styles to the DataFrame
styled_df = apply_styles(filtered_df)

# Display the styled DataFrame
st.dataframe(styled_df)
