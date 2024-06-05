import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Header and description
st.markdown("""# Project Awesome: Overview
List your companies by applying the necessary filters.""")

# Sample data for demonstration
data = {
    'Classification': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1],
    'Ticker': ['AAPL', 'NFLX', 'SBUX', 'NVDA', 'META', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'IBM'],
    'Industry': ['Tech', 'Tech', 'Non-tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Tech', 'Non-tech', 'Tech'],
    '2020 Ratio': [1.5, 0.8, 0.9, 1.5, 1.1, 1.5, 0.8, 0.9, 1.5, 1.1],
    '2021 Ratio': [1.8, 1.1, 0.3, 1.3, 1.7, 1.8, 1.1, 0.3, 1.3, 1.7],
    '2022 Ratio': [1.2, 1.3, 0.7, 1.1, 1.3, 1.2, 1.3, 0.7, 1.1, 1.3],
    '2023 Ratio': [1.3, 0.9, 1.4, 1.8, 1.2, 1.3, 0.9, 1.4, 1.8, 1.2],
    '2024 Ratio': [1.1, 1, 0.5, 1.5, 1, 1.1, 1, 0.5, 1.5, 1]
}

# Converting data into a DataFrame
df = pd.DataFrame(data)

# Set Ticker as index
df = df.set_index('Ticker')

# Create a multiselect filter for the 'Classification' column
selected_classifications = st.multiselect('Select Classification', df['Classification'].unique())

# Filter the DataFrame based on the selected classifications
if selected_classifications:
    filtered_df = df[df['Classification'].isin(selected_classifications)]
else:
    filtered_df = df

# Create a multiselect filter for the 'Industry' column
selected_industries = st.multiselect('Select Industries', filtered_df['Industry'].unique())

# Filter the DataFrame based on the selected industries
if selected_industries:
    filtered_df_1 = filtered_df[filtered_df['Industry'].isin(selected_industries)]
else:
    filtered_df_1 = filtered_df

# Define the highlight function
def highlight_age(value):
    if value == 1:
        return 'color: green'
    elif value == 2:
        return 'color: yellow'
    else:
        return 'color: red'

# Slider to select a number of lines to display in the DataFrame
line_count = st.number_input("Pick a number", 0,5060)

head_df = filtered_df_1.head(line_count)

def apply_styles(head_df):
    return head_df.style.applymap(highlight_age, subset=['Classification'])

# Apply styles to DataFrame
styled_df = apply_styles(head_df)

# Show the styled DataFrame
st.dataframe(styled_df)

# Drop all unnecessary columns
df_drop = head_df.drop(columns=['Classification', 'Industry'])

# Transpose the DataFrame to switch rows and columns
df_drop_transposed = df_drop.T

# Show line chart with baseline using Seaborn and Matplotlib
st.title('Stock Ratio Over Years')

# Create a Seaborn line plot with a baseline
plt.figure(figsize=(10, 6))
for column in df_drop_transposed.columns:
    sns.lineplot(data=df_drop_transposed[column], label=column, marker='o')

# Add the baseline
baseline_value = 1
plt.axhline(y=baseline_value, color='red', linestyle='--', label='S&P 500')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Ratio between chosen company and S&P 500')
plt.title('Stock Ratio Over Years with Baseline')
plt.legend()

# Display the plot in Streamlit
st.pyplot(plt)
