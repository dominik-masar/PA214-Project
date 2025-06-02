import numpy as np
from dash.dependencies import Output, Input
import plotly.express as px

def map_fig(csv_data, max_missions, precision=2, max_size=40):
    csv_data = csv_data.copy()

    csv_data['lat_round'] = csv_data['Latitude'].round(precision)
    csv_data['lon_round'] = csv_data['Longitude'].round(precision)

    grouped = csv_data.groupby(['lat_round', 'lon_round']).size().reset_index(name='count')
    grouped['marker_size'] = max_size * np.sqrt(grouped['count'] / max_missions)

    fig = px.scatter_geo(
        grouped,
        lat='lat_round',
        lon='lon_round',
        size='marker_size',
        hover_name='count',
        projection='natural earth',
        size_max=grouped['marker_size'].max()
    )

    fig.update_geos(
        visible=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="black",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision=True
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
        return map_fig(filtered_df, app.max_missions)
