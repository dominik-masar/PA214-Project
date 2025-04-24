import pandas as pd
import plotly.express as px

def barchart_fig(csv_data, year):
    filtered_data = csv_data[csv_data['Year'] == year]

    country_counts = filtered_data['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']

    fig = px.bar(
        country_counts, 
        x='Count',
        y='Country', 
        title='Number of Missions per Country',
        labels={'Count': 'Number of Missions', 'Country': 'Country'}
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig