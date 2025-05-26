import dash
from dash import dcc, html, callback_context
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px

def barchart_fig(data):

    country_counts = data['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']

    fig = px.bar(
        country_counts, 
        x='Count',
        y='Country',
        labels={'Count': 'Number of Missions'},
        text='Country'  # <-- Add this to show country names inside the bars
    )

    fig.update_layout(
        yaxis=dict(
            categoryorder='total ascending',
            showticklabels=False,
            title='',
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=0),  # Reduce left margin (l=left)
    )
    return fig

def register_barchart_callbacks(app):
    @app.callback(
        Output('bar-fig', 'figure'),  # or whatever your bar chart graph id is
        Input('selected-years', 'data')
    )
    def update_bar_chart(year_range):
        start, end = year_range
        df = app.missions_df
        filtered_df = df[(df['Year'] >= start) & (df['Year'] <= end)]
        return barchart_fig(filtered_df)