import pandas as pd
from dash import html, Input, Output, State, ctx, dash, dcc

# --- Load and prepare data ---
df = pd.read_csv("datasets/final_dataset_missions.csv")

# --- Planets and styles ---
textures = {
    "Earth": "/assets/images/earth_orbit.png",
    "Moon": "/assets/images/moon_image.png",
    "Solar System": "/assets/images/solar_system.png",
    "Outer Space": "/assets/images/outer_space.png"
}

planet_ids = {name: name.lower().replace(" ", "-") + "-id" for name in textures}

base_style = {
    "backgroundSize": "cover",
    "borderRadius": "50%",
    "width": "13vh",
    "height": "13vh",
    "margin": "0px",
    "transition": "transform 0.4s ease, box-shadow 0.4s ease",
    "position": "relative",
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    "color": "white",
    "fontWeight": "bold",
    "fontSize": "20px",
    "textShadow": "0 0 4px black"
}

def get_planet_layout():
    return html.Div([
        dcc.Store(id="previous-planet-values", data={name: "0" for name in textures}),
        dcc.Interval(id="planet-init-trigger", interval=100, n_intervals=0, max_intervals=1),
        html.Div([
            html.Div(
                id=planet_ids[name],
                style={
                    **base_style,
                    "backgroundImage": f"url('{path}')"
                },
                children="0"
            )
            for name, path in textures.items()
        ], style={
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "height": "100%",
            "width": "100%",
            "alignItems": "center",
            "padding": "0",
        })
    ], style={"margin": "0px", "height": "100%", "padding": "0px"})

def register_planet_callbacks(app):
    @app.callback(
        [Output(planet_ids[name], "children") for name in textures] +
        [Output(planet_ids[name], "style") for name in textures] +
        [Output("previous-planet-values", "data")],
        Input("selected-years", "data"),
        State("previous-planet-values", "data"),
        prevent_initial_call=False
    )
    def update_planets(year_range, previous_values):
        if not year_range:
            raise dash.exceptions.PreventUpdate

        start, end = year_range
        mask = (df['Year'] >= start) & (df['Year'] <= end)
        filtered = df[mask]

        planet_values = {
            "Earth": str(filtered[filtered['Mission Goal'] == 'Earth orbit'].shape[0]),
            "Moon": str(filtered[filtered['Mission Goal'] == 'Moon'].shape[0]),
            "Solar System": str(filtered[filtered['Mission Goal'] == 'Solar system'].shape[0]),
            "Outer Space": str(filtered[filtered['Mission Goal'] == 'Outer space'].shape[0]),
        }

        children_outputs = []
        style_outputs = []

        for name in textures:
            new_val = planet_values.get(name, "0")

            style = {
                **base_style,
                "backgroundImage": f"url('{textures[name]}')"
            }


            children_outputs.append(new_val)
            style_outputs.append(style)

        return children_outputs + style_outputs + [planet_values]
