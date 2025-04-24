import pandas as pd
import plotly.express as px

def barchart_fig(csv_data):
    company_counts = csv_data['Company Name'].value_counts().reset_index()
    company_counts.columns = ['Company Name', 'Count']

    fig = px.bar(
        company_counts, 
        x='Count',
        y='Company Name', 
        title='Number of Missions per Company',
        labels={'Count': 'Number of Missions', 'Company Name': 'Company'}
    )

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig