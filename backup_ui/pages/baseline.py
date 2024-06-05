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
  'Classification': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
    'Ticker': ['AAPL', 'NFLX', 'SBUX', 'NVDA', 'META', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'IBM'],
    'Industry': ['Tech', 'Tech', 'Non-tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Non-tech', 'Tech'],
    '2020 Ratio': [1.5, 0.8, 0.9, 1.5, 1.1, 1.5, 0.8, 0.9, 1.5, 1.1],
    '2021 Ratio': [1.8, 1.1, 0.3, 1.3, 1.7, 1.8, 1.1, 0.3, 1.3, 1.7],
    '2022 Ratio': [1.2, 1.3, 0.7, 1.1, 1.3, 1.2, 1.3, 0.7, 1.1, 1.3],
    '2023 Ratio': [1.3, 0.9, 1.4, 1.8, 1.2, 1.3, 0.9, 1.4, 1.8, 1.2],
    '2024 Ratio': [1.1, 1, 0.5, 1.5, 1, 1.1, 1, 0.5, 1.5, 1],
    '2020 Stock Price': [120, 500, 80, 300, 250, 3200, 1500, 200, 700, 130],
    '2021 Stock Price': [140, 550, 85, 350, 270, 3400, 1600, 250, 800, 150],
    '2022 Stock Price': [130, 530, 90, 340, 280, 3300, 1550, 260, 820, 140],
    '2023 Stock Price': [150, 600, 100, 360, 290, 3500, 1650, 270, 840, 160],
    '2024 Stock Price': [160, 620, 110, 370, 300, 3600, 1700, 280, 860, 170]
}

# converting data into a df
df = pd.DataFrame(data)

# set ticker as index
df = df.set_index('Ticker')

# create a multiselect filter for the 'Classification' column
selected_classifications = st.multiselect('Select Classification', df['Classification'].unique())

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
df_drop = head_df.drop(columns=['Classification', 'Industry', '2020 Stock Price', '2021 Stock Price', '2022 Stock Price', '2023 Stock Price', '2024 Stock Price'])

# transpose the df to switch rows and columns
df_drop_transposed = df_drop.T

# show line chart
st.title('Stock Ratio Over Years')
st.line_chart(df_drop_transposed)





import streamlit as st
import pandas as pd
import altair as alt

# Sample DataFrame with only one column
data = {
    'name': ['A', 'B', 'C', 'D', 'E']
}
df = pd.DataFrame(data)

# Define the baseline value
baseline_value = 1

# Create a line chart with Altair
line_chart = alt.Chart(df).mark_point().encode(
    x='name:N',
    y=alt.value(baseline_value),
).properties(
    width=600,
    height=400
)

# Create a baseline rule
baseline = alt.Chart(pd.DataFrame({'baseline': [baseline_value]})).mark_rule(color='red').encode(
    y='baseline:Q'
)

# Combine the line chart and the baseline
combined_chart = line_chart + baseline

# Display the chart in Streamlit
st.altair_chart(combined_chart, use_container_width=True)
