import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from test_pred import get_pred_goog, plot_forecast
import os

# Styling function
def apply_styles(df):
    return df.style.applymap(highlight_age, subset=['2024 Ratio Stock/S&P500'])

# # header + description

# Highlighting function
def highlight_age(value):
    if value > 1.1:
        return 'color: green'
    elif 0.9 <= value <= 1.1:
        return 'color: yellow'
    else:
        return 'color: red'
# st.markdown("""# Project Awesome: Overview
# List your companies by applying the necessary filters.""")
# Function to clear search query

# pull the csv file
file_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(file_path,'..','process_data')
data = pd.read_csv(os.path.join(data_path,'raw_data_ui.csv'))

# converting data into a df
df = pd.DataFrame(data)

# set ticker as index
df = df.set_index('Ticker')
# Set CSS styling

css_path = os.path.join('style.css')
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set page title and description
st.markdown(
    """
    <h1 class="title">Stock Market Advisor</h1>
    <p class="subtitle">Companies List</p>
    """,
    unsafe_allow_html=True
)
# Apply filters
filtered_df = df#.rename(columns={
    # '2024 Ratio Stock/S&P500': '2024 Ratio',
    # '2023 Ratio Stock/S&P500': '2023 Ratio',
    # '2022 Ratio Stock/S&P500': '2022 Ratio',
    # '2021 Ratio Stock/S&P500': '2021 Ratio',
    # '2020 Ratio Stock/S&P500': '2020 Ratio'})
# Sidebar filters
with st.sidebar:
    st.title('Filters')
    selected_classifications = st.multiselect('Select 2024 Ratio Stock/S&P500', df['Recommendation'].unique())
    selected_industries = st.multiselect('Select Sectors', df['Sector'].unique())
    # search bar
    search_query = st.text_input('Enter search query:')
    line_count = st.number_input("Number of rows to display", 1, 1000, 3)
    # Select sort column
    sort_by = st.selectbox('Sort by', options=['None'] + list(filtered_df.columns), index=0)
    sort_descending = st.checkbox('Sort descending', value=False)




if selected_classifications:
    filtered_df = filtered_df[filtered_df['Recommendation'].isin(selected_classifications)]
    search_query=''

if selected_industries:
    filtered_df = filtered_df[filtered_df['Sector'].isin(selected_industries)]
    search_query = ''

if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_string(), axis=1)]



if sort_by != 'None':
    if pd.api.types.is_numeric_dtype(filtered_df[sort_by]):
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=not sort_descending)
    else:
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=not sort_descending)


# Display filtered dataframe
head_df = filtered_df.head(line_count)
styled_df = apply_styles(head_df)
st.write(styled_df)

# Display line chart
st.subheader('Stock Ratio Over Years')

df_drop = head_df.drop(columns=['Name', 'Last Sale', 'Market Cap', 'Sector', 'Industry', 'Recommendation'])


#
df_drop.rename(columns={
    '2024 Ratio Stock/S&P500': '2024 Ratio',
    '2023 Ratio Stock/S&P500': '2023 Ratio',
    '2022 Ratio Stock/S&P500': '2022 Ratio',
    '2021 Ratio Stock/S&P500': '2021 Ratio',
    '2020 Ratio Stock/S&P500': '2020 Ratio'}, inplace=True)

df_drop_transposed = df_drop.T
st.line_chart(df_drop_transposed)


# Display Google stock price prediction button
if st.button('Display Google stock price prediction'):
    a, b, c, d, e = get_pred_goog()
    st.pyplot(plot_forecast(a, b, c, d, e))
