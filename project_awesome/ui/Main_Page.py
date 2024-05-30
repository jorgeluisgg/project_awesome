import streamlit as st

import numpy as np
import pandas as pd
import seaborn as sns
import requests

# header + description
st.markdown("""# Project Awesome: Overview
List your companies by applying the necessary filters.""")


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

# create a multiselect filter for the 'Classification' column
selected_classifications = st.multiselect('Select Classifications', df['Classification'].unique())

# filter the df based on the selected classifications
if selected_classifications:
    filtered_df = df[df['Classification'].isin(selected_classifications)]
else:
    filtered_df = df

# create a multiselect filter for the 'Industry' column
selected_industries = st.multiselect('Select Industries', filtered_df['Industry'].unique())

# filter the df based on the selected classifications
if selected_industries:
    filtered_df_1 = filtered_df[filtered_df['Industry'].isin(selected_industries)]
else:
    filtered_df_1 = filtered_df


def highlight_age(value):
    if value == 1:
        return 'color: green'
    elif value == 2:
        return 'color: yellow'
    else:
        return 'color: red'


# this slider allows the user to select a number of lines to display in the df
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 100, 3)

head_df = filtered_df_1.head(line_count)

def apply_styles(head_df):
    return head_df.style.applymap(highlight_age, subset=['Classification'])

# apply styles to df
styled_df = apply_styles(head_df)

# show the styled df
st.dataframe(styled_df)

# drop all unnecessay columns
df_drop = head_df.drop(columns=['Classification', 'Industry', 'Name'])

# transpose the df to switch rows and columns
df_drop_transposed = df_drop.T

# show line chart
st.title('Stock Prices Over Years')
st.line_chart(df_drop_transposed)
