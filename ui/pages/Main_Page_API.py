import streamlit as st

import numpy as np
import pandas as pd
import requests

st.markdown("""# Project Awesome: Overview
List your companies by applying the necessary filters.""")


# Define the API endpoint
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'

# Make the API call
response = requests.get(url)

# Display the response in the app
df = pd.DataFrame(response.json())

#df = df.set_index('Ticker')

# Create a multiselect filter for the 'Classification' column
selected_classifications = st.multiselect('Select Classifications', df['Meta Data'].unique())

# Filter the DataFrame based on the selected classifications
if selected_classifications:
    filtered_df = df[df['Meta Data'].isin(selected_classifications)]
else:
    filtered_df = df

# Create a multiselect filter for the 'Classification' column
selected_industries = st.multiselect('Select Industries', df['Meta Data'].unique())

# Filter the DataFrame based on the selected classifications
if selected_industries:
    filtered_df = df[df['Meta Data'].isin(selected_industries)]
else:
    filtered_df = df


def highlight_age(value):
    if value == 'IBM':
        return 'color: green'
    elif value == 'Compact':
        return 'color: yellow'
    else:
        return 'color: red'


# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 100, 3)

head_df = filtered_df.head(line_count)

def apply_styles(head_df):
    return head_df.style.applymap(highlight_age, subset=['Meta Data'])

# Apply styles to the DataFrame
styled_df = apply_styles(head_df)

# Display the styled DataFrame
st.dataframe(styled_df)
