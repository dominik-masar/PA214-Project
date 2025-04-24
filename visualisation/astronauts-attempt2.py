import csv
import pandas as pd
import plotly.express as px

filename = 'datasets/astronauts.csv'

# Load CSV into a DataFrame
df = pd.read_csv(filename)

# Convert 'Datum' to datetime
#df['Mission.Year'] = pd.to_datetime(df['Mission.Year'], utc=True, errors='coerce')

# Drop rows with invalid dates (if any)
df = df.dropna(subset=['Mission.Year'])

# Create scatter plot with Plotly Express
fig = px.scatter(
    df,
    x='Mission.Year',
    y='Profile.Name',
    color='Profile.Name',
    hover_data=['Profile.Nationality', 'Mission.Role', 'Mission.Year','Mission.Name'],
    title='Launches Over Time by Astronaut',
    labels={'Mission.Year': 'Launch Date', 'Profile.Name': 'Name'}
)

# Show the plot
fig.show()
