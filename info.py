# pages/info.py
from dash import html
from navbar import get_navbar


def get_info_layout(app, pathname):
    # You can later parse the pathname to load specific astronaut/company
    return html.Div([
        get_navbar(),
        html.H2("Detail Information"),
        html.P(f"Info page for: {pathname}")
    ])
