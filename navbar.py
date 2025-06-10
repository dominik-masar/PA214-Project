from dash import html, dcc
from design.color_palettes import PALETTE


link_style = {
    'textDecoration': 'none',
    'color': PALETTE['text'],
    'padding': '8px 18px',
    'borderRadius': '8px',
    'backgroundColor': PALETTE['secondary'],
    'fontWeight': 600,
    'transition': 'background 0.2s'
}

def get_navbar():
    search_input_style = {
        'padding': '8px 12px',
        'borderRadius': '8px 0 0 8px',
        'border': f"1px solid {PALETTE['input_border']}",
        'outline': 'none',
        'fontSize': '16px',
        'width': '160px',
        'marginRight': '-1px',
        'backgroundColor': PALETTE['input_bg'],
        'color': PALETTE['text'],
    }
    search_button_style = {
        'padding': '8px 16px',
        'borderRadius': '0 8px 8px 0',
        'border': f"1px solid {PALETTE['button']}",
        'backgroundColor': PALETTE['button'],
        'color': PALETTE['text'],
        'fontSize': '16px',
        'cursor': 'pointer',
        'marginRight': '4px',
        'fontWeight': 600
    }
    reset_button_style = {
        'padding': '8px 16px',
        'borderRadius': '8px',
        'border': f"1px solid {PALETTE['accent']}",
        'backgroundColor': PALETTE['accent'],
        'color': PALETTE['secondary'],
        'fontSize': '16px',
        'cursor': 'pointer',
        'fontWeight': 600
    }
    return html.Div([
        dcc.Link("🚀 Space Missions", href="/home", style=link_style),
        dcc.Link("👩‍🚀 Astronauts", href="/astronauts", style=link_style),
        dcc.Link("🏢 Companies", href="/companies", style=link_style),
        dcc.Link("📖 Mission Logs", href="/logs", style=link_style),
        html.Div([
            dcc.Input(id='search-input', type='text', placeholder='Search...', style=search_input_style),
            html.Button('Search', id='search-button', n_clicks=0, style=search_button_style),
            html.Button('Reset', id='reset-button', n_clicks=0, style=reset_button_style),
            dcc.Store(id='trigger-update')
        ], style={
            'width': 'auto',
            'display': 'inline-flex',
            'alignItems': 'center',
            'marginLeft': '10px',
            'marginRight': '10px',
            'marginLeft': 'auto'
        }),
    ], style={
        'backgroundColor': PALETTE['background'],
        'padding': '14px',
        'display': 'flex',
        'gap': '24px',
        'fontSize': '18px',
        'color': PALETTE['text'],
        'alignItems': 'center'
    })
