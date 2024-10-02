import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load dataset
data = pd.read_csv('https://raw.githubusercontent.com/woodyuser/air-quality-data/ebdea5a5d26b40aa114cdfba0942af4259623262/data/PRSA_Data_Nongzhanguan_20130301-20170228.csv')

# Drop duplicate rows
data.drop_duplicates(inplace=True)

# Handle missing values
# Fill missing values with the mean for numerical columns
numeric_columns = data.select_dtypes(include=[np.number]).columns
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Handle missing values in 'wd' column
# Fill missing values with the most frequent value (mode)
most_frequent_wd = data['wd'].mode()[0]
data['wd'].fillna(most_frequent_wd, inplace=True)

# Convert 'wd' to numerical format using one-hot encoding
data = pd.get_dummies(data, columns=['wd'])

# Check if 'year', 'month', 'day', 'hour' columns exist before converting
if all(col in data.columns for col in ['year', 'month', 'day', 'hour']):
    # Convert 'year', 'month', 'day', 'hour' to a single datetime column
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    # Drop the original 'year', 'month', 'day', 'hour' columns
    data.drop(columns=['year', 'month', 'day', 'hour'], inplace=True)
else:
    st.write("Columns 'year', 'month', 'day', 'hour' are not present in the DataFrame.")

# Streamlit app
st.title('Air Quality Nongzhanguan Dashboard')

# Display data
st.write(data.head())

# Plot
fig = px.line(data, x='datetime', y='PM2.5', title='PM2.5 Levels Over Time')
st.plotly_chart(fig)