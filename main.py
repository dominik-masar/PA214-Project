# main.py
import dash
from dash import dcc, html, Input, Output
#from app import app
from home import get_home_layout
from profiles import get_profiles_layout
from info import get_info_layout
from seaborn import color_palette
import matplotlib.colors as mcolors
from callbacks.sidebar_callbacks import register_sidebar_callbacks
from callbacks.map_callbacks import register_map_callbacks
from visualisation.map_figure import map_fig
from visualisation.active_years_figure import get_active_years_fig, register_active_years_callbacks
from visualisation.timeline_figure import get_timeline_layout, register_timeline_callbacks
from visualisation.planets_figure import get_planet_layout, register_planet_callbacks
from preprocessing.color_palette_generator import generate_country_colors
from preprocessing.loadDatasets import load_datasets, get_country_list
from utils.min_max_setter import set_max_count_to_app

DATASET_MISSIONS_PATH = "datasets/final_dataset_missions.csv"
DATASET_ASTRONAUTS_PATH = "datasets/astronauts.csv"

# Load datasets
missions_df, astronauts_df = load_datasets(mission_path=DATASET_MISSIONS_PATH, astronauts_path=DATASET_ASTRONAUTS_PATH)
palette = color_palette("hls", 100)
hex_colors = [mcolors.to_hex(c) for c in palette]
color_map = generate_country_colors(missions_df, column='Country')
available_countries = get_country_list(missions_df, astronauts_df)

app = dash.Dash(__name__, suppress_callback_exceptions=True)
#app = dash.Dash(__name__)
app.title = "Space Missions"
app.missions_df = missions_df
app.astronauts_df = astronauts_df
app.color_map = color_map

set_max_count_to_app(app, missions_df)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    # Add all stores used in callbacks here, with default values
    dcc.Store(id="trigger-update"),
    dcc.Store(id="selected-years"),
    dcc.Store(id="window-size"),
    dcc.Store(id="start-position"),
    dcc.Store(id="initial-start-position"),
    dcc.Store(id="animation-index"),
    dcc.Store(id="is-playing"),
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return get_home_layout(app)
    elif pathname.startswith('/profiles'):
        return get_profiles_layout(app, available_countries)
    elif pathname.startswith('/info'):
        return get_info_layout(app, pathname)
    else:
        return html.Div("404 Page Not Found")


register_timeline_callbacks(app)
register_sidebar_callbacks(app)
register_map_callbacks(app)
register_planet_callbacks(app)
register_active_years_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
