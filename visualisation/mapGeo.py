import dash
from dash import dcc, html, callback_context
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px

def map_fig(csv_data):

    # Create scatter plot on a world map
    fig = px.scatter_geo(
        csv_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Latitude",
        projection="natural earth",  # World map projection
    )

    # Customize map appearance
    fig.update_geos(
        visible=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="black",
    )

    return fig

def register_map_callbacks(app):
    @app.callback(
        Output('map-fig', 'figure'),  # or whatever your bar chart graph id is
        Input('selected-years', 'data')
    )
    def update_map(year_range):
        start, end = year_range
        df = app.missions_df
        filtered_df = df[(df['Year'] >= start) & (df['Year'] <= end)]
        return map_fig(filtered_df)
