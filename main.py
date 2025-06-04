import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from seaborn import color_palette
import matplotlib.colors as mcolors
from callbacks.sidebar_callbacks import register_sidebar_callbacks
from callbacks.map_callbacks import register_map_callbacks
from visualisation.map_figure import map_fig
from visualisation.active_years_figure import get_bottom_fig
from visualisation.timeline_figure import get_timeline_layout, register_timeline_callbacks
from visualisation.planets_figure import get_planet_layout, register_planet_callbacks
from preprocessing.color_palette_generator import generate_country_colors
from preprocessing.loadDatasets import load_datasets, get_country_list
from utils.min_max_setter import set_max_count_to_app

DATASET_MISSIONS_PATH = "datasets/final_dataset_missions.csv"
DATASET_ASTRONAUTS_PATH = "datasets/astronauts.csv"

# Load your datasets
missions_df, astronauts_df = load_datasets(mission_path=DATASET_MISSIONS_PATH, astronauts_path=DATASET_ASTRONAUTS_PATH)
available_countries = get_country_list(missions_df, astronauts_df)

# color palette for countries
palette = color_palette("hls", 100)
hex_colors = [mcolors.to_hex(c) for c in palette]
color_map = generate_country_colors(missions_df, column='Country')

app = dash.Dash(__name__)
app.missions_df = missions_df
app.color_map = color_map

set_max_count_to_app(app, missions_df)
map_fig = map_fig(missions_df, app.max_missions)

app.layout = html.Div([
    html.Div(get_planet_layout(), style={'width': '70%', 'height': '120px', 'display': 'inline-block'}),
    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search...'
        ),
        html.Button('Search', id='search-button', n_clicks=0),
        html.Button('Reset', id='reset-button', n_clicks=0),
        dcc.Store(id='trigger-update')
    ], style={'width': '20%', 'display': 'inline-block', 'margin-left': '10px'}),
    html.Div([
        html.Div([dcc.Graph(id='map-fig', figure=map_fig)], style={'width': '65%', 'height': '100%', 'display': 'inline-block'}),
        html.Div(id='sidebar-fig', style={'width': '30%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'gap': '5%', 'height': '700px'}),

    html.Div(get_timeline_layout(), style={'width': '100%', 'display': 'inline-block'}),

    html.Div([
        dcc.RadioItems(
            id='bottom-view-toggle',
            options=[
                {'label': 'Astronauts', 'value': 'astronauts'},
                {'label': 'Companies', 'value': 'companies'}
            ],
            value='astronauts',
            labelStyle={'display': 'inline-block', 'margin-right': '20px'}
        ),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in sorted(available_countries)],
            value='USA',
            clearable=False
        ),
        dcc.Graph(id='active-years-fig', config={'scrollZoom': True}, style={'height': '600px'})
    ], style={'width': '80%', 'display': 'inline-block'}),
])

@app.callback(
    Output('active-years-fig', 'figure'),
    [Input('bottom-view-toggle', 'value'),
     Input('country-dropdown', 'value')]
)
def update_active_years_fig(selected_view, selected_country):
    return get_bottom_fig(missions_df, astronauts_df, view_type=selected_view, selected_country=selected_country)


register_timeline_callbacks(app)
register_sidebar_callbacks(app)
register_map_callbacks(app)
register_planet_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)