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
