from dash import html, dcc

def get_navbar():
    return html.Div([
        dcc.Link("🚀 Space Missions", href="/home", style=link_style),
        dcc.Link("👩‍🚀 Profiles", href="/profiles", style=link_style),
        dcc.Link("📖 Mission Logs", href="/logs", style=link_style),
    ], style={
        'backgroundColor': '#111',
        'padding': '10px',
        'display': 'flex',
        'gap': '20px',
        'fontSize': '18px',
        'color': 'white'
    })

link_style = {
    'textDecoration': 'none',
    'color': 'white',
    'padding': '6px 12px',
    'borderRadius': '6px',
    'backgroundColor': '#333'
}
