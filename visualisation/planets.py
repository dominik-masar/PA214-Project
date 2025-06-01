import pandas as pd
from dash import html, Input, Output, State, ctx, dash,dcc

# --- Načtení a příprava dat (stejně jako v timeline) ---
df = pd.read_csv("datasets/final_dataset_missions.csv")

# --- Planety a styly ---
textures = {
    "Earth": "/assets/images/earth.PNG",
    "Mars": "/assets/images/mars.PNG",
    "Moon": "/assets/images/moon.PNG",
    "Milky Way": "/assets/images/milkyway.png"
}

planet_ids = {name: name.lower().replace(" ", "-") + "-id" for name in textures}

base_style = {
    "backgroundSize": "cover",
    "borderRadius": "50%",
    "width": "70px",
    "height": "70px",
    "margin": "30px",
    "transition": "transform 0.4s ease, box-shadow 0.4s ease"
}

pop_style = {
    "transform": "scale(1.5)",
}

def get_planet_layout():
    return html.Div([
        # Store pro předchozí hodnoty
        dcc.Store(id="previous-planet-values", data={name: "0" for name in textures}),
        dcc.Interval(id="planet-init-trigger", interval=100, n_intervals=0, max_intervals=1),

        html.Div([
            html.Div(id=planet_ids[name], style={
                **base_style,
                "margin": "5px",
                "backgroundImage": f"url('{path}')",
                "position": "relative",
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "color": "white",
                "fontWeight": "bold",
                "fontSize": "16px",
                "textShadow": "0 0 4px black"
            }, children="0")
            for name, path in textures.items()
        ], style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "gap": "10px",
            "padding": "0",
        })
    ], style={"margin": "10px", "padding": "10px"})

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

        # Počty misí podle zemí (příklad, můžeš upravit podle potřeby)
        planet_values = {
            "Earth": str(filtered[filtered['Mission Goal'] == 'Earth orbit'].shape[0]),
            "Mars": str(filtered[filtered['Mission Goal'] == 'Solar system'].shape[0]),
            "Moon": str(filtered[filtered['Mission Goal'] == 'Moon'].shape[0]),
            "Milky Way": str(filtered[filtered['Mission Goal'] == 'Outer space'].shape[0]),
        }

        children_outputs = []
        style_outputs = []

        for name in textures:
            new_val = planet_values.get(name, "0")
            prev_val = previous_values.get(name, "0")

            # Pokud se hodnota změnila, "popni" planetu
            if new_val != prev_val:
                style = {
                    **base_style,
                    "backgroundImage": f"url('{textures[name]}')",
                    "position": "relative",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "color": "white",
                    "fontWeight": "bold",
                    "fontSize": "18px",
                    "textShadow": "0 0 4px black",
                    **pop_style
                }
            else:
                style = {
                    **base_style,
                    "backgroundImage": f"url('{textures[name]}')",
                    "position": "relative",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "color": "white",
                    "fontWeight": "bold",
                    "fontSize": "18px",
                    "textShadow": "0 0 4px black",
                }

            children_outputs.append(new_val)
            style_outputs.append(style)

        return children_outputs + style_outputs + [planet_values]