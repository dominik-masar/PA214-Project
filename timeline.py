
import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
import pandas as pd
import math

# Load and preprocess the CSV
df = pd.read_csv("Space_Corrected.csv")
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
df = df.dropna(subset=['Datum'])
df['Year'] = df['Datum'].dt.year

# Group by year
missions_by_year = df.groupby('Year').size().reset_index(name='MissionCount')
min_year = df['Year'].min()
max_year = df['Year'].max()

# Fill missing years
all_years = pd.DataFrame({'Year': list(range(min_year, max_year + 1))})
missions_by_year = all_years.merge(missions_by_year, on='Year', how='left').fillna(0)
missions_by_year['MissionCount'] = missions_by_year['MissionCount'].astype(int)

years = missions_by_year['Year'].tolist()
missions_per_year = missions_by_year['MissionCount'].tolist()
max_count = max(missions_per_year)




app = dash.Dash(__name__)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

# App layout
app.layout = html.Div([

    html.H2("Interactive Timeline: Drag to Select Year"),

    html.Div(id='year-display', style={
        'fontSize': '18px',
        'fontWeight': 'bold',
        'marginBottom': '10px',
        'color': 'darkblue'
    }),

    dcc.Store(id="selected-year", data=1957),

    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flexStart'}, children=[

        html.Div("Mission Count", style={
            'writingMode': 'vertical-rl',
            'transform': 'rotate(180deg)',
            'textAlign': 'center',
            'fontWeight': 'bold',
            'fontSize': '14px',
            'height': '300px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'marginRight': '5px'
        }),

        html.Div([

            html.Div(id='timeline-container', style={
                'position': 'relative',
                'width': '1000px',
                'height': '300px',
                'border': '1px solid #ddd',
                'backgroundColor': '#fdfdfd',
                'overflow': 'hidden',
                'marginBottom': '10px'
            }),

            # Updated slider position & labels every 5th year
            html.Div(
                dcc.Slider(
                    id='timeline-slider',
                    min=min(years),
                    max=max(years),
                    step=1,
                    marks={year: str(year) for year in years if year % 5 == 0},  # Label only every 5th year
                    value=1957,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                style={
                    'width': '1032px',
                    'position': 'relative',
                    'marginTop': '-19px',  # Perfect vertical alignment
                    'left': '-23px',
                    'zIndex': '999'
                }
            ),
            dcc.Interval(id="year-interval", interval=1000, n_intervals=0),
        ])
    ]),

    html.Div(id='missions-count-display', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'darkgreen'}),
])

@app.callback(
    Output('year-display', 'children'),
    Input('selected-year', 'data')
)
def display_selected_year(year):
    return f"Selected Year: {year}"

@app.callback(
    Output('timeline-container', 'children'),
    Input('selected-year', 'data')
)
def update_timeline(selected_year):
    container_width = 1000
    container_height = 300
    point_width_px = container_width / len(years)

    points_and_lines = []
    red_points_positions = []

    for i, year in enumerate(years):
        height_ratio = missions_per_year[i] / max_count
        height_px = height_ratio * container_height
        left_px = i * point_width_px
        top_px = container_height - height_px

        red_points_positions.append((left_px, top_px))

        points_and_lines.append(html.Div(
            id=f"point-{year}",
            style={
                'position': 'absolute',
                'top': f'{top_px - 3}px',
                'left': f'{left_px - 3}px',
                'width': '6px',
                'height': '6px',
                'backgroundColor': 'red',
                'borderRadius': '50%',
                'cursor': 'pointer',
                'zIndex': 10
            },
            title=f"Year: {year} - Missions: {missions_per_year[i]}",
        ))

        points_and_lines.append(html.Div(
            style={
                'position': 'absolute',
                'top': f'{top_px}px',
                'left': f'{left_px}px',
                'width': '2px',
                'height': f'{height_px}px',
                'backgroundColor': 'blue',
                'zIndex': 5
            }
        ))

    for i in range(len(red_points_positions) - 1):
        x1, y1 = red_points_positions[i]
        x2, y2 = red_points_positions[i + 1]

        distance = calculate_distance(x1, y1, x2, y2)
        angle = math.degrees(calculate_angle(x1, y1, x2, y2))

        points_and_lines.append(html.Div(
            style={
                'position': 'absolute',
                'top': f'{y1}px',
                'left': f'{x1}px',
                'width': f'{distance}px',
                'height': '2px',
                'backgroundColor': 'green',
                'transform': f'rotate({angle}deg)',
                'transformOrigin': '0 0',
                'zIndex': 5
            }
        ))

        min_x = min(x1, x2)
        width = abs(x2 - x1)
        top_fill = max(y1, y2)
        height_fill = container_height - top_fill

        points_and_lines.append(html.Div(
            style={
                'position': 'absolute',
                'top': f'{top_fill}px',
                'left': f'{min_x}px',
                'width': f'{width}px',
                'height': f'{height_fill}px',
                'background': 'linear-gradient(to top, rgba(0, 128, 0, 0.2), transparent)',
                'zIndex': 1
            }
        ))

    return points_and_lines

@app.callback(
    Output('selected-year', 'data'),
    Input('timeline-slider', 'value'),
)
def update_selected_year_from_slider(selected_year):
    return selected_year

@app.callback(
    Output('missions-count-display', 'children'),
    Input('selected-year', 'data')
)
def display_missions_count(year):
    index = years.index(year)
    missions = missions_per_year[index]
    return f"Missions in {year}: {missions}"

@app.callback(
    Output('timeline-slider', 'value'),
    Input("year-interval", 'n_intervals'),
    State('selected-year', 'data')
)
def increment_slider(n_intervals, current_year):
    return current_year + 1


if __name__ == "__main__":
    app.run(debug=True)