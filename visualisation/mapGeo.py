import pandas as pd
import plotly.express as px

def map_fig():
    # Create DataFrame with given coordinates
    data = {
        "Latitude": [
            28.52427955, 40.964989, 32.21785207, 45.9178932, 27.7567667, 35.0000663, 
            45.9178932, 35.0000663, 27.7567667, 30.39434145, 37.93523815, 40.964989, 
            28.24576155, 30.8124247, 40.964989, -41.5000831, 35.0000663, 27.7567667
        ],
        "Longitude": [
            -80.6818558, 100.2838215, -96.0370219, 63.40837214, -81.4639835, 104.999955, 
            63.40837214, 104.999955, -81.4639835, 130.9577895, -75.46969557, 100.2838215, 
            102.027938, 34.8594762, 100.2838215, 172.8344077, 104.999955, -81.4639835
        ]
    }

    df = pd.DataFrame(data)

    # Create scatter plot on a world map
    fig = px.scatter_geo(
        df,
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
