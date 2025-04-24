import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Dash(__name__)

# Load astronaut data
astronauts_df = pd.read_csv('datasets/astronauts.csv')
astronauts_df = astronauts_df.dropna(subset=['Mission.Year'])
# Rename 'Profile.Name' to 'Name' in the astronauts dataframe
#astronauts_df.rename(columns={'Profile.Name': 'Name'}, inplace=True)

# Load company data (missions)
missions_df = pd.read_csv('datasets/space_with_geo_with_countries.csv')
# missions_df = missions_df.dropna(subset=['Datum'])
# Extract year from 'Datum' column and create 'Mission.Year' column
# missions_df['Mission.Year'] = pd.to_datetime(missions_df['Datum'], errors='coerce').dt.year.astype(str)
# Extract country from 'Location' column
#missions_df['Country'] = missions_df['Location'].str.split(',').str[-1].str.strip()
missions_df['Company ID'] = missions_df['Company Name'].factorize()[0]

# Get full x-axis range (earliest to latest launch) for astronauts
min_year = astronauts_df['Mission.Year'].min()
max_year = astronauts_df['Mission.Year'].max()

# Available countries from astronaut and mission data
available_countries = astronauts_df['Profile.Nationality'].dropna().unique()
available_countries = set(available_countries).union(set(missions_df['Country'].dropna().unique()))
available_countries = sorted(available_countries)

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
]  # TODO: Check correctness and add more milestones

app.layout = html.Div([
    dcc.RadioItems(
        id='data-toggle',
        options=[
            {'label': 'Astronauts', 'value': 'astronauts'},
            {'label': 'Companies', 'value': 'companies'}
        ],
        value='astronauts',  # Default value
        labelStyle={'display': 'inline-block'}
    ),
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
    [Input('data-toggle', 'value'),
     Input('country-dropdown', 'value')]
)
def update_figure(data_state, selected_country):
    if data_state == 'astronauts':
        # Use astronaut data
        filtered_df = astronauts_df[astronauts_df['Profile.Nationality'] == selected_country]
        #filtered_df.rename(columns={'Profile.Name': 'Name'}, inplace=True)
        x_column = 'Mission.Year'
        y_column = 'Profile.Astronaut Numbers.Overall'
        y_label = 'Astronaut'
        hover_data = ['Profile.Name', 'Profile.Nationality', 'Mission.Role', 'Mission.Year', 'Mission.Name']
        title = f'Launches Over Time by Astronaut from {selected_country}'
    else:
        # Use missions data
        filtered_df = missions_df[missions_df['Country'] == selected_country]
        x_column = 'Year'
        y_column = 'Company ID'
        y_label = 'Company'
        hover_data = ['Company Name', 'Location', 'Detail']
        title = f'Launches Over Time by Companies from {selected_country}'

    # Create figure
    fig = px.scatter(
        filtered_df,
        x=x_column,
        y=y_column,
        color='Profile.Name' if data_state == 'astronauts' else 'Company Name',
        hover_data=hover_data,
        title=title,
        labels={'Mission.Year': 'Launch Date', y_column: y_label},
        range_x=[min_year, max_year]
    )

    # Reverse the y-axis
    fig.update_layout(yaxis=dict(autorange="reversed"))

    # Hide y-axis tick labels
    fig.update_layout(
        yaxis=dict(
            showticklabels=False,
            title=None
        )
    )

    # Precompute marks for the milestones
    if(filtered_df[y_column].size > 0 ):
        n = filtered_df[y_column].max() # Get the maximum y value and add 1 for the vertical line
    else:
        n = 1
    step = 10 
    steps = n // step if n > step else 1 
    """
    n = max(filtered_df[y_column].max(), 1) if not filtered_df.empty else 1
    step = 10
    steps = max(n // step, 1)"""

    # Add milestones as invisible points with hover text
    for m in milestones:
        # Add invisible milestone markers to trigger hover
        fig.add_trace(go.Scatter(
            x=[m["year"]] * steps,
            y=[i for i in range(0, n, step)],  # Invisible, just for positioning
            mode="markers",
            marker=dict(color="purple", opacity=0),
            hovertext=m["label"],
            hoverinfo="text"
        ))

        # Add vertical lines for the milestones
        fig.add_trace(go.Scatter(
            x=[m["year"], m["year"]],
            y=[0, n],  # Extend the line across the y-axis
            mode="lines",
            line=dict(dash="dash", color="purple", width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

    return fig

if __name__ == '__main__':
    app.run(debug=True)



# TODO: size of the dots depending on the number of missions that year (mainly for companies)
# TODO: reverse the order of the y-axis (astronauts and companies) to have the first astronaut/companies at the top - or reverse the legends