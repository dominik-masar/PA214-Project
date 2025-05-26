import dash
from dash import dcc, html, callback_context
from dash.dependencies import Output, Input, State
import pandas as pd
import math
from dash.exceptions import PreventUpdate

# Load and preprocess the CSV
df = pd.read_csv("Space_Corrected.csv")
df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')
df = df.dropna(subset=['Datum'])
df['Year'] = df['Datum'].dt.year

# Normalize locations to country level
def normalize_country(loc):
    if isinstance(loc, str):
        if 'USA' in loc or 'Texas' in loc or 'Florida' in loc:
            return 'USA'
        return loc.split(',')[-1].strip()
    return loc

df['Country'] = df['Location'].apply(normalize_country)

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

# Define some colors for countries
COUNTRY_COLORS = {
    'USA': 'rgba(31, 119, 180, 0.6)',
    'Russia': 'rgba(255, 127, 14, 0.6)',
    'China': 'rgba(44, 160, 44, 0.6)',
    'India': 'rgba(214, 39, 40, 0.6)',
    'Japan': 'rgba(148, 103, 189, 0.6)',
    'Europe': 'rgba(140, 86, 75, 0.6)',
    'Others': 'rgba(128, 128, 128, 0.4)',
}

app = dash.Dash(__name__)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

app.layout = html.Div([

    html.H2("Interactive Timeline: Select Year Range"),

    html.Div(id='year-display', style={
        'fontSize': '18px',
        'fontWeight': 'bold',
        'marginBottom': '10px',
        'color': 'darkblue'
    }),

    dcc.Store(id="selected-years", data=[min_year, max_year]),
    dcc.Store(id="window-size", data=max_year - min_year + 1),
    dcc.Store(id="start-position", data=min_year),
    dcc.Store(id="animation-index", data=0),
    dcc.Store(id="is-playing", data=False),

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

            html.Div(
                dcc.RangeSlider(
                    id='timeline-slider',
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=[min_year, max_year],
                    marks={year: str(year) for year in years if year % 5 == 0},
                    tooltip={"placement": "bottom", "always_visible": True},
                    allowCross=False,
                ),
                style={
                    'width': '1032px',
                    'position': 'relative',
                    'marginTop': '-19px',
                    'left': '-23px',
                    'zIndex': '999'
                }
            )
        ])
    ]),

    html.Button('Play', id='play-button', n_clicks=0, style={'marginBottom': '10px'}),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),

    html.Div(id='missions-count-display', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'darkgreen'}),

    html.Div([
        html.Span([
            html.Span(style={
                'display': 'inline-block',
                'width': '12px',
                'height': '12px',
                'backgroundColor': col,
                'marginRight': '6px',
                'opacity': '0.6',
                'border': '1px solid #444'
            }),
            html.Span(country, style={'marginRight': '12px'})
        ]) for country, col in COUNTRY_COLORS.items()
    ], style={'marginTop': '10px', 'display': 'flex', 'flexWrap': 'wrap'}),

])

@app.callback(
    Output('year-display', 'children'),
    Input('selected-years', 'data')
)
def display_selected_range(year_range):
    return f"Selected Years: {year_range[0]} – {year_range[1]}"

@app.callback(
    Output('timeline-container', 'children'),
    Input('selected-years', 'data')
)
def update_timeline(selected_range):
    start_year, end_year = selected_range
    container_width = 1000
    container_height = 300
    point_width_px = container_width / len(years)

    points_and_lines = []
    red_points_positions = []

    for i, year in enumerate(years):
        height_ratio = missions_per_year[i] / max_count if max_count > 0 else 0
        height_px = height_ratio * container_height
        left_px = i * point_width_px
        top_px = container_height - height_px

        red_points_positions.append((left_px, top_px))

        in_range = start_year <= year <= end_year

        if missions_per_year[i] > 0:
            year_df = df[df['Year'] == year]
            counts = year_df['Country'].value_counts().to_dict()

            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            top_countries = sorted_counts[:2]
            others_count = sum(ct for _, ct in sorted_counts[2:])

            segs = {}
            for c, ct in top_countries:
                segs[c] = ct
            if others_count > 0:
                segs['Others'] = others_count

            opacity = 0.9 if in_range else 0.3
            border_color = 'blue' if in_range else 'transparent'

            y_offset = container_height
            for c, ct in segs.items():
                seg_height = (ct / max_count) * container_height
                y_offset -= seg_height

                points_and_lines.append(html.Div(
                    style={
                        'position': 'absolute',
                        'top': f'{y_offset}px',
                        'left': f'{left_px}px',
                        'width': f'{point_width_px}px',
                        'height': f'{seg_height}px',
                        'backgroundColor': COUNTRY_COLORS.get(c, COUNTRY_COLORS['Others']).replace('0.6', str(opacity)),
                        'borderLeft': f'1px solid {border_color}',
                        'boxSizing': 'border-box',
                        'zIndex': 5
                    },
                    title=f"{c}: {ct} missions in {year}"
                ))
        else:
            points_and_lines.append(html.Div(
                style={
                    'position': 'absolute',
                    'top': f'{top_px}px',
                    'left': f'{left_px}px',
                    'width': f'{point_width_px}px',
                    'height': f'{height_px}px',
                    'backgroundColor': 'rgba(128,128,128,0.3)',
                    'borderLeft': '1px solid transparent',
                    'boxSizing': 'border-box',
                    'zIndex': 5
                },
                title=f"Year: {year} - Missions: {missions_per_year[i]}",
            ))

        point_color = 'red' if in_range else '#aaa'
        points_and_lines.append(html.Div(
            id=f"point-{year}",
            style={
                'position': 'absolute',
                'top': f'{top_px - 3}px',
                'left': f'{left_px + point_width_px / 2 - 3}px',
                'width': '6px',
                'height': '6px',
                'backgroundColor': point_color,
                'borderRadius': '50%',
                'cursor': 'pointer',
                'zIndex': 10
            },
            title=f"Year: {year} - Missions: {missions_per_year[i]}",
        ))

    selected_points = [(x, y) for (x, y), year in zip(red_points_positions, years) if start_year <= year <= end_year]
    for i in range(len(selected_points) - 1):
        x1, y1 = selected_points[i]
        x2, y2 = selected_points[i + 1]

        distance = calculate_distance(x1, y1, x2, y2)
        angle = math.degrees(calculate_angle(x1, y1, x2, y2))

        points_and_lines.append(html.Div(
            style={
                'position': 'absolute',
                'top': f'{y1}px',
                'left': f'{x1 + point_width_px / 2}px',
                'width': f'{distance}px',
                'height': '2px',
                'backgroundColor': 'green',
                'transform': f'rotate({angle}deg)',
                'transformOrigin': '0 0',
                'zIndex': 5
            }
        ))

    return points_and_lines

@app.callback(
    Output('missions-count-display', 'children'),
    Input('selected-years', 'data')
)
def display_missions_count(year_range):
    start_year, end_year = year_range
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    total_missions = filtered_df.shape[0]
    return f"Missions from {start_year} to {end_year}: {total_missions}"

@app.callback(
    Output('interval-component', 'disabled'),
    Output('play-button', 'children'),
    Output('is-playing', 'data'),
    Input('play-button', 'n_clicks'),
    State('is-playing', 'data')
)
def play_pause(n_clicks, is_playing):
    if n_clicks == 0:
        return True, "Play", False
    else:
        new_state = not is_playing
        return not new_state, "Pause" if new_state else "Play", new_state

@app.callback(
    Output('selected-years', 'data'),
    Output('window-size', 'data'),
    Output('start-position', 'data'),
    Output('animation-index', 'data'),
    Input('timeline-slider', 'value'),
    Input('interval-component', 'n_intervals'),
    State('window-size', 'data'),
    State('start-position', 'data'),
    State('animation-index', 'data'),
    State('is-playing', 'data'),
    prevent_initial_call=True
)
def update_selected_years(slider_range, n_intervals, window_size, start_pos, animation_index, is_playing):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'timeline-slider':
        start, end = slider_range
        new_window_size = end - start + 1
        new_start_pos = start
        return [start, end], new_window_size, new_start_pos, 0

    elif trigger_id == 'interval-component' and is_playing:
        new_start_pos = start_pos + 1
        if new_start_pos + window_size - 1 > max_year:
            new_start_pos = slider_range[0]

        new_end_pos = new_start_pos + window_size - 1
        new_animation_index = animation_index + 1

        return [new_start_pos, new_end_pos], window_size, new_start_pos, new_animation_index

    else:
        raise PreventUpdate

if __name__ == '__main__':
    app.run(debug=True)