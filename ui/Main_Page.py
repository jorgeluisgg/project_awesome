import streamlit as st

import numpy as np
import pandas as pd
import seaborn as sns
import requests

# header + description
st.markdown("""# Project Awesome: Overview
List your companies by applying the necessary filters.""")

# pull the csv file
data = pd.read_csv('../raw_data/raw_data_ui.csv')

# converting data into a df
df = pd.DataFrame(data)

# set ticker as index
df = df.set_index('Ticker')

# create a multiselect filter for the 'Classification' column
selected_classifications = st.multiselect('Select 2024 Ratio Stock/S&P500', df['Recommendation'].unique())

# filter the df based on the selected classifications
if selected_classifications:
    filtered_df = df[df['Recommendation'].isin(selected_classifications)]
else:
    filtered_df = df

# create a multiselect filter for the 'Industry' column
selected_industries = st.multiselect('Select Sectors', filtered_df['Sector'].unique())

# filter the df based on the selected classifications
if selected_industries:
    filtered_df_1 = filtered_df[filtered_df['Sector'].isin(selected_industries)]
else:
    filtered_df_1 = filtered_df


def highlight_age(value):
    if value > 1.1:
        return 'color: green'
    elif value > 0.9 and value < 1.1:
        return 'color: yellow'
    else:
        return 'color: red'


# this slider allows the user to select a number of lines to display in the df
# the selected value is returned by st.slider
#line_count = st.slider('Select a line count', 1, 1000, 3)
line_count = st.number_input("Pick a number", 0,5060)

head_df = filtered_df_1.head(line_count)

def apply_styles(head_df):
    return head_df.style.applymap(highlight_age, subset=['2024 Ratio Stock/S&P500'])

# apply styles to df
styled_df = apply_styles(head_df)

# show the styled df
st.dataframe(styled_df)

# drop all unnecessay columns
df_drop = head_df.drop(columns=['Name', 'Last Sale', 'Market Cap', 'Sector', 'Industry', 'Recommendation'])

# transpose the df to switch rows and columns
df_drop_transposed = df_drop.T

# show line chart
st.title('Stock Ratio Over Years')
st.line_chart(df_drop_transposed)
