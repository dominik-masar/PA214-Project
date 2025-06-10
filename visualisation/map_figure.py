import numpy as np
import plotly.express as px

def map_fig(csv_data, max_missions, precision=2, max_size=40):
    csv_data = csv_data.copy()

    csv_data['lat_round'] = csv_data['Latitude'].round(precision)
    csv_data['lon_round'] = csv_data['Longitude'].round(precision)

    # Group by rounded lat/lon and aggregate count and location names
    grouped = csv_data.groupby(['lat_round', 'lon_round']).agg(
        count=('Latitude', 'size'),
        locations=('Location', lambda x: ', '.join(sorted(set(x))))
    ).reset_index()
    grouped['marker_size'] = max_size * np.sqrt(grouped['count'] / max_missions)

    # Format locations for hover: separate by <br> if more than one location
    def format_locations(loc_str):
        locs = sorted(set(loc_str.split(', ')))
        return '<br>'.join(locs)

    grouped['locations_hover'] = grouped['locations'].apply(format_locations)

    fig = px.scatter_geo(
        grouped,
        lat='lat_round',
        lon='lon_round',
        size='marker_size',
        hover_data={
            'count': True,
            'locations_hover': True,
            'lat_round': False,
            'lon_round': False,
            'marker_size': False,
            'locations': False
        },
        projection='natural earth',
        size_max=grouped['marker_size'].max(),
        #color_discrete_sequence=[PALETTE['primary']] # TODO 
    )

    fig.update_traces(
        hovertemplate="<b>Mission count:</b> %{customdata[0]}<extra></extra><br>" +
        "<b>Locations:</b><br>%{customdata[1]}<br>"
                      
    )

    fig.update_geos(
        visible=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="black",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        uirevision=True,
    )

    return fig
