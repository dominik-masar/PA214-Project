from dash.dependencies import Output, Input, State
from visualisation.map_figure import map_fig

def register_map_callbacks(app):
    @app.callback(
        Output('map-fig', 'figure'),  # or whatever your bar chart graph id is
        Input('trigger-update', 'data'),
        Input("selected-years", "data")
    )
    def update_map(trigger_data, year_range):
        start, end = year_range
        df = app.missions_df
        if trigger_data and trigger_data['search_triggered']:
            df = app.filtered_df

        filtered_df = df[(df['Year'] >= start) & (df['Year'] <= end)]
        return map_fig(filtered_df, app.max_missions)
    