import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__)
filename = 'datasets/astronauts.csv'

# Load CSV into a DataFrame
df = pd.read_csv(filename)
df = df.dropna(subset=['Mission.Year'])

# Get full x-axis range (earliest to latest launch)
min_year = df['Mission.Year'].min()
max_year = df['Mission.Year'].max()

available_countries = df['Profile.Nationality'].dropna().unique()

# Important milestones for the timeline
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
] # TODO: Check correctness and add more milestones

app.layout = html.Div([
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in sorted(available_countries)],
        value='U.S.',
        clearable=False
    ),
    dcc.Graph(id='scatter-plot')
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('country-dropdown', 'value')
)
def update_figure(selected_country):
    filtered_df = df[df['Profile.Nationality'] == selected_country]
    fig = px.scatter(
        filtered_df,
        x='Mission.Year',
        #y='Profile.Name',
        y='Profile.Astronaut Numbers.Overall',
        color='Profile.Name',
        hover_data=['Profile.Nationality', 'Mission.Role', 'Mission.Year', 'Mission.Name'],
        title=f'Launches Over Time by Astronaut from {selected_country}',
        labels={'Mission.Year': 'Launch Date', 'Profile.Name': ''},
        range_x=[min_year, max_year] 
    )

    fig.update_layout(
        yaxis=dict(
            showticklabels=False,  # hides the names on y-axis ticks
            title=None
        )
    )

    # List of astronaut names (used for y position of vertical lines)
    astronaut_names = df['Profile.Name'].unique()
    
    # Add milestones as invisible points with hover text
    for m in milestones:
        # Add invisible milestone markers to trigger hover
        fig.add_trace(go.Scatter(
            x=[m["year"]] * 10,
            y=list(range(0, len(astronaut_names), len(astronaut_names) // 10)),  # Invisible, just for positioning
            mode="markers",
            marker=dict(color="purple", opacity=0),
            hovertext=m["label"],
            hoverinfo="text"
        ))

        # Optionally, add vertical lines for the milestones
        fig.add_trace(go.Scatter(
            x=[m["year"], m["year"]],
            y=[0, len(astronaut_names)],  # Extend the line across the y-axis
            mode="lines",
            line=dict(dash="dash", color="purple", width=2),
            showlegend=False,
            hoverinfo="skip" 
        ))

    return fig

if __name__ == '__main__':
    app.run(debug=True)
