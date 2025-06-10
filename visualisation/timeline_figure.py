import dash
from dash import dcc, html, callback_context
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_daq as daq
from design.color_palettes import PALETTE

min_year = 1957
max_year = 2020
len_years = max_year - min_year + 1

play_button_style = {
    'padding': '0.5em 1.2em',
    'borderRadius': '0.5em',
    'border': f"1px solid {PALETTE['button']}",
    'backgroundColor': PALETTE['button'],
    'color': PALETTE['text'],
    'fontSize': '1em',
    'cursor': 'pointer',
    'fontWeight': 600,
    'marginRight': '1em',
    'transition': 'background 0.2s'
}
toggle_style = {
    'backgroundColor': 'white',
    'borderRadius': '0.5em',
    'padding': '0.5em 1.2em',
    'fontWeight': 600,
    'color': PALETTE['secondary'],
    'display': 'flex',
    'alignItems': 'center',
    'marginLeft': 'auto',
    'justifyContent': 'flex-end'
}

def get_timeline_layout():
    df = dash.get_app().missions_df
    years = list(range(min_year, max_year + 1))

    return html.Div([
        html.Div(id='year-display', style={
            'fontSize': '1.1em',
            'fontWeight': 'bold',
            #'marginBottom': '0.5em',
            'color': 'darkblue'
        }),
        dcc.Store(id="selected-years", data=[min_year, max_year]),
        dcc.Store(id="window-size", data=max_year - min_year + 1),
        dcc.Store(id="start-position", data=min_year),
        dcc.Store(id="initial-start-position", data=min_year),
        dcc.Store(id="animation-index", data=0),
        dcc.Store(id="is-playing", data=False),

        html.Div([
            html.Button('Play', id='play-button', n_clicks=0, style=play_button_style),
            html.Div([
                html.Span(id='timeline-mode-label', style={
                    'marginRight': '0.8em',
                    'fontWeight': 600,
                    'color': PALETTE['secondary'],
                    'fontSize': '1em'
                }),
                daq.ToggleSwitch(
                    id='timeline-mode-toggle',
                    value=False,
                    style=toggle_style
                )
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'flex-end',
            })
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'gap': '1.5em',
            'width': '100%',
            'justifyContent': 'space-between'
        }),

        html.Div(style={
            'display': 'flex',
            'flexDirection': 'row',
            'alignItems': 'flexStart',
            'width': '100%',
            'boxSizing': 'border-box',
            'height': '70%'  # Let parent control overall height, this is for inner split
        }, children=[
            html.Div("Mission Count", style={
                'writingMode': 'vertical-rl',
                'transform': 'rotate(180deg)',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'height': '100%',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'marginRight': '0.5em',
                'fontSize': '0.9em'
            }),
            html.Div([
                html.Div(id='timeline-container', style={
                    'position': 'absolute',
                    'top': 0,
                    'left': 0,
                    'width': '100%',
                    'height': 'calc(100% - 2.0em)',  # Reserve space for slider
                    'overflow': 'hidden',
                    'margin': '0',
                    'padding': '0',
                    'boxSizing': 'border-box'
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
                        'width': '100%',
                        'position': 'absolute',
                        'bottom': 0,
                        'left': 0,
                        'zIndex': 999,
                        'margin': 0,
                        'padding': 0
                    }
                )
            ], style={
                'flex': '1 1 0%',
                'minWidth': 0,
                'height': '100%',
                'position': 'relative'
            })
        ]),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0, disabled=True),
    ], style={'width': '100%', 'height': '100%', 'boxSizing': 'border-box', 'display': 'flex', 'flexDirection': 'column'})

def _hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    rgb = tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'

def register_timeline_callbacks(app):
    @app.callback(
        Output('timeline-container', 'children'),
        [Input('selected-years', 'data'),
         Input('trigger-update', 'data'),
         Input('timeline-mode-toggle', 'value')]
    )
    def update_timeline(selected_range, trigger_data, mode_toggle):
        if trigger_data and trigger_data['search_triggered']:
            df = app.filtered_df
        else:
            df = app.missions_df

        color_map = app.color_map
        years = list(range(min_year, max_year + 1))
        missions_by_year = df.groupby('Year').size().reindex(years, fill_value=0)
        max_count = missions_by_year.max()

        mode = 'window' if mode_toggle else 'cumulative'
        start_year, end_year = selected_range

        # Responsive: use 100% for width/height, parent controls actual size
        points_and_lines = []

        for i, year in enumerate(years):
            year_df = df[df['Year'] == year]
            total_missions = len(year_df)
            height_ratio = total_missions / max_count if max_count > 0 else 0
            height_pct = height_ratio * 100
            bar_width_pct = 100 / (len_years + 1)
            left_pct = (i / (len_years + 1)) * 100 + bar_width_pct / 2
            top_pct = 100 - height_pct

            is_selected = start_year <= year <= end_year
            alpha = 1.0 if is_selected else 0.2

            if total_missions > 0:
                counts = year_df['Country'].value_counts().to_dict()
                sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
                top_countries = sorted_counts[:2]
                others_count = sum(ct for _, ct in sorted_counts[2:])
                segs = {c: ct for c, ct in top_countries}
                if others_count > 0:
                    segs['Others'] = others_count

                y_offset_pct = 100
                for c, ct in segs.items():
                    seg_height_pct = (ct / max_count) * 100
                    y_offset_pct -= seg_height_pct
                    base_color = color_map.get(c, '#888888')
                    color = _hex_to_rgba(base_color, alpha)
                    points_and_lines.append(html.Div(
                        style={
                            'position': 'absolute',
                            'top': f'{y_offset_pct}%',
                            'left': f'{left_pct}%',
                            'width': f'{bar_width_pct}%',
                            'height': f'{seg_height_pct}%',
                            'backgroundColor': color,
                            'borderLeft': '1px solid white',
                            'boxSizing': 'border-box',
                            'zIndex': 5
                        },
                        title=f"{c}: {ct} missions in {year}"
                    ))
            else:
                points_and_lines.append(html.Div(
                    style={
                        'position': 'absolute',
                        'top': f'{top_pct}%',
                        'left': f'{left_pct}%',
                        'width': f'{bar_width_pct}%',
                        'height': f'{height_pct}%',
                        'backgroundColor': f'rgba(128,128,128,{alpha})',
                        'borderLeft': '1px solid transparent',
                        'boxSizing': 'border-box',
                        'zIndex': 5
                    },
                    title=f"Year: {year} - Missions: 0",
                ))
        return points_and_lines

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
        Output('timeline-slider', 'value'),
        Input('timeline-slider', 'value'),
        Input('interval-component', 'n_intervals'),
        Input('timeline-mode-toggle', 'value'),
        State('window-size', 'data'),
        State('start-position', 'data'),
        State('animation-index', 'data'),
        State('is-playing', 'data'),
        State('initial-start-position', 'data'),
        State('selected-years', 'data'),
        State('timeline-mode-toggle', 'value'),
    )
    def update_selected_years(slider_range, n_intervals, mode_toggle_changed, window_size, start_pos, animation_index, is_playing, initial_start_pos, current_selected_years, mode_toggle):
        ctx = callback_context

        if not ctx.triggered:
            raise PreventUpdate

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        mode = 'window' if mode_toggle else 'cumulative'
        if trigger_id == 'timeline-slider' or trigger_id == 'timeline-mode-toggle':
            start, end = slider_range
            window_size = end - start + 1
            return [start, end], window_size, start, 0, slider_range

        elif trigger_id == 'interval-component' and is_playing:
            if mode == 'cumulative':
                start, end = slider_range
                new_end = end + 1
                if new_end > max_year:
                    new_end = start
                return [start, new_end], window_size, start_pos, animation_index + 1, [start, new_end]
            else:
                new_start = start_pos + 1
                new_end = new_start + window_size - 1
                if new_end > max_year:
                    new_start = initial_start_pos
                    new_end = new_start + window_size - 1
                return [new_start, new_end], window_size, new_start, animation_index + 1, [new_start, new_end]

        else:
            raise PreventUpdate
        
    @app.callback(
        Output('timeline-mode-label', 'children'),
        Input('timeline-mode-toggle', 'value')
    )
    def update_mode_label(toggle_value):
        return "Floating Window Mode" if toggle_value else "Cumulative Mode"