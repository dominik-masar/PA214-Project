import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from visualisation.barchartFigure import barchart_fig
from visualisation.mapGeo import map_fig
from visualisation.bottomView import get_bottom_fig #TODO rename
from preprocessing.loadDatasets import load_datasets, get_country_list

DATASET_MISSIONS_PATH = "datasets/space_with_geo_with_countries.csv"
DATASET_ASTRONAUTS_PATH = "datasets/astronauts.csv"

# Load data
missions_df, astronauts_df = load_datasets(mission_path=DATASET_MISSIONS_PATH , astronauts_path=DATASET_ASTRONAUTS_PATH)
available_countries = get_country_list(missions_df, astronauts_df) # TODO: maybe we'll actually want to have 2 separate lists

# Create figures
main_fig = map_fig(missions_df)
bar_fig = barchart_fig(missions_df, 2000) # TODO: insert variable year

main_fig.update_layout(height=700)
bar_fig.update_layout(height=700)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with 80:20 ratio
app.layout = html.Div([
    html.Div([dcc.Graph(figure=main_fig)], style={'width': '70%', 'display': 'inline-block'}),
    html.Div([dcc.Graph(figure=bar_fig)], style={'width': '30%', 'display': 'inline-block'}),
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
    ], style={'width': '80%', 'display': 'inline-block'})
])

@app.callback(
    Output('active-years-fig', 'figure'),
    [Input('bottom-view-toggle', 'value'),
     Input('country-dropdown', 'value')]
)
def update_active_years_fig(selected_view, selected_country):
    # You can add more logic here to select country if needed
    return get_bottom_fig(missions_df, astronauts_df, view_type=selected_view, selected_country=selected_country)


if __name__ == '__main__':
    app.run(debug=True)