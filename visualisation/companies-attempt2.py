import csv
import pandas as pd
import plotly.express as px

filename = 'datasets/space_with_geo-firstAttempt.csv'

# Load CSV into a DataFrame
df = pd.read_csv(filename)

# Convert 'Datum' to datetime
df['Datum'] = pd.to_datetime(df['Datum'], utc=True, errors='coerce')

# Drop rows with invalid dates (if any)
df = df.dropna(subset=['Datum'])

# Create scatter plot with Plotly Express
fig = px.scatter(
    df,
    x='Datum',
    y='Company Name',
    color='Company Name',
    hover_data=['Detail', 'Profile.Gender', ''],
    title='Launches Over Time by Company',
    labels={'Datum': 'Launch Date', 'Company Name': 'Company'}
)

# Show the plot
fig.show()
