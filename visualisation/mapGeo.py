from dash.dependencies import Output, Input, State
import plotly.express as px

def map_fig(csv_data, precision=2, min_size=1.5, max_size=8):
    csv_data = csv_data.copy()

    # Round lat/lon to cluster points
    csv_data['lat_round'] = csv_data['Latitude'].round(precision)
    csv_data['lon_round'] = csv_data['Longitude'].round(precision)

    # Aggregate by rounded lat/lon
    grouped = csv_data.groupby(['lat_round', 'lon_round']).size().reset_index(name='count')

    # Normalize counts to marker sizes between min_size and max_size
    counts = grouped['count']
    if counts.max() == counts.min():
        # Avoid division by zero if all counts equal
        grouped['marker_size'] = min_size
    else:
        grouped['marker_size'] = min_size + (counts - counts.min()) / (counts.max() - counts.min()) * (
                    max_size - min_size)

    fig = px.scatter_geo(
        grouped,
        lat='lat_round',
        lon='lon_round',
        size='marker_size',  # size now scaled
        hover_name='count',
        projection='natural earth',
        size_max=max_size,
    )

    fig.update_geos(
        visible=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="black",
    )

    # Optional: if you want to control marker sizing better, disable default sizemode
    fig.update_traces(marker=dict(sizemode='diameter'))

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
