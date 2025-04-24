import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load astronaut data
astronauts_df = pd.read_csv('datasets/astronauts.csv').dropna(subset=['Mission.Year'])

# Load mission data
missions_df = pd.read_csv('datasets/space_with_geo_with_countries.csv')
missions_df['Company ID'] = missions_df['Company Name'].factorize()[0]

milestones = [
    {"year": 1961, "label": "First Man in Space: Yuri Gagarin"},
    {"year": 1969, "label": "First Moon Landing: Neil Armstrong"},
    {"year": 1971, "label": "First Space Station (Salyut 1)"},
    {"year": 1981, "label": "First Space Shuttle Launch (Columbia)"},
    {"year": 1998, "label": "First Module of ISS (Zarya) Launched"},
    {"year": 2000, "label": "First Crew to ISS (Expedition 1)"},
    {"year": 2004, "label": "First Private Spacecraft Launch (SpaceShipOne)"},
    {"year": 2012, "label": "First Private Company to Dock with ISS (SpaceX Dragon)"},
    {"year": 2019, "label": "First Image of a Black Hole (Event Horizon Telescope)"},
    {"year": 2020, "label": "First Crew Launch from U.S. Soil in 9 Years (SpaceX Crew Dragon)"},
]

def get_bottom_fig(data_state='astronauts', selected_country='U.S.'):
    if data_state == 'astronauts':
        filtered_df = astronauts_df[astronauts_df['Profile.Nationality'] == selected_country]
        x_column = 'Mission.Year'
        y_column = 'Profile.Astronaut Numbers.Overall'
        color_column = 'Profile.Name'
        hover_data = ['Profile.Name', 'Profile.Nationality', 'Mission.Role', 'Mission.Year', 'Mission.Name']
        y_label = 'Astronaut'
    else:
        filtered_df = missions_df[missions_df['Country'] == selected_country]
        x_column = 'Year'
        y_column = 'Company ID'
        color_column = 'Company Name'
        hover_data = ['Company Name', 'Location', 'Detail']
        y_label = 'Company'

    fig = px.scatter(
        filtered_df,
        x=x_column,
        y=y_column,
        color=color_column,
        hover_data=hover_data,
        title=f'Launches Over Time by {y_label}s from {selected_country}',
        labels={x_column: 'Launch Date', y_column: y_label},
        range_x=[astronauts_df['Mission.Year'].min(), astronauts_df['Mission.Year'].max()]
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed", showticklabels=False, title=None)
    )

    if filtered_df[y_column].size > 0:
        n = filtered_df[y_column].max()
    else:
        n = 1
    step = 10
    steps = max(n // step, 1)

    for m in milestones:
        fig.add_trace(go.Scatter(
            x=[m["year"]] * steps,
            y=[i for i in range(0, n, step)],
            mode="markers",
            marker=dict(color="purple", opacity=0),
            hovertext=m["label"],
            hoverinfo="text"
        ))
        fig.add_trace(go.Scatter(
            x=[m["year"], m["year"]],
            y=[0, n],
            mode="lines",
            line=dict(dash="dash", color="purple", width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

    return fig
