import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from test_pred import get_pred_goog, plot_forecast

# Styling function
def apply_styles(df):
    return df.style.applymap(highlight_age, subset=['2024 Ratio Stock/S&P500'])

# Highlighting function
def highlight_age(value):
    if value > 1.1:
        return 'color: green'
    elif 0.9 <= value <= 1.1:
        return 'color: yellow'
    else:
        return 'color: red'

# Set CSS styling
css_path = os.path.join('style.css')
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set page title and description
st.markdown(
    """
    <h1 class="title">Stock Market Investor</h1>
    <p class="subtitle">List your companies by applying the necessary filters.</p>
    """,
    unsafe_allow_html=True
)

# Load data
data = pd.read_csv('../raw_data/raw_data_ui.csv')
df = pd.DataFrame(data)

# Set ticker as index
df = df.set_index('Ticker')

# Sidebar filters
with st.sidebar:
    st.title('Filters')
    selected_classifications = st.multiselect('Select 2024 Ratio Stock/S&P500', df['Recommendation'].unique())
    selected_industries = st.multiselect('Select Sectors', df['Sector'].unique())

# Apply filters
filtered_df = df
if selected_classifications:
    filtered_df = filtered_df[filtered_df['Recommendation'].isin(selected_classifications)]
if selected_industries:
    filtered_df = filtered_df[filtered_df['Sector'].isin(selected_industries)]

# Display filtered dataframe
line_count = st.number_input("Number of rows to display", 1, 1000, 10)
head_df = filtered_df.head(line_count)
styled_df = apply_styles(head_df)
st.write(styled_df)

# Display line chart
st.title('Stock Ratio Over Years')
with st.echo():
    df_drop = head_df.drop(columns=['Name', 'Last Sale', 'Market Cap', 'Sector', 'Industry', 'Recommendation'])
    df_drop_transposed = df_drop.T
    st.line_chart(df_drop_transposed)

# Display Google stock price prediction button
if st.button('Display Google stock price prediction'):
    a, b, c, d, e = get_pred_goog()
    st.pyplot(plot_forecast(a, b, c, d, e))
