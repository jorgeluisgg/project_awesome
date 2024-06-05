import streamlit as st

import numpy as np
import pandas as pd
import requests


# header + description
st.markdown("""# Project Awesome: Overview
List your companies by applying the necessary filters.""")


# define the API endpoint
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'

# API call
response = requests.get(url)

# turn API into df
df = pd.DataFrame(response.json())

# setting ticker as index
#df = df.set_index('Ticker')

# create a multiselect filter for the 'Classification' column
selected_classifications = st.multiselect('Select Classifications', df['Meta Data'].unique())

# filter the df based on the selected classifications
if selected_classifications:
    filtered_df = df[df['Meta Data'].isin(selected_classifications)]
else:
    filtered_df = df

# create a multiselect filter for the 'Industry' column
selected_industries = st.multiselect('Select Industries', df['Meta Data'].unique())

# filter the df based on the selected classifications
if selected_industries:
    filtered_df = df[df['Meta Data'].isin(selected_industries)]
else:
    filtered_df = df

# assign colors to values
def highlight_age(value):
    if value == 'IBM':
        return 'color: green'
    elif value == 'Compact':
        return 'color: yellow'
    else:
        return 'color: red'


# this slider allows the user to select a number of lines to display in the df
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 100, 3)

# create df  based on filter
head_df = filtered_df.head(line_count)

# define style function
def apply_styles(head_df):
    return head_df.style.applymap(highlight_age, subset=['Meta Data'])

# apply style function to df
styled_df = apply_styles(head_df)

# show styled df
st.dataframe(styled_df)


