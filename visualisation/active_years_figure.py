import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.express.colors import qualitative
from matplotlib.colors import to_rgba
from dash import dcc, html, Input, Output

milestones = [
    {"year": 1961, "label": "First Man in Space: Yuri Gagarin"},
    {"year": 1969, "label": "First Moon Landing: Neil Armstrong"},
    {"year": 1971, "label": "First Space Station (Salyut 1)"},
    {"year": 1981, "label": "First Space Shuttle Launch (Columbia)"},
    {"year": 1998, "label": "First Module of ISS (Zarya) Launched"},
    {"year": 2000, "label": "First Crew to ISS (Expedition 1)"},
    {"year": 2004, "label": "First Private Spacecraft Launch (SpaceShipOne)"},
    {"year": 2012, "label": "First Private Company to Dock with ISS (SpaceX Dragon)"},
    {"year": 2019, "label": "First Image of a Black Hole (Event Horizon Telescope)"},
    {"year": 2020, "label": "First Crew Launch from USA Soil in 9 Years (SpaceX Crew Dragon)"},
]

# Color palette
palette = qualitative.Plotly

# Alternative palettes:
# palette = qualitative.D3
# palette = qualitative.Set1
# palette = qualitative.Pastel1
# palette = qualitative.Dark2
# palette = qualitative.Prism


def get_settings(view_type, selected_country, missions_df, astronauts_df):
    # TODO allow selected_country == 'all'
    settings = type('Settings', (), {})()
    if view_type == 'astronauts':
        if selected_country == 'all':
            settings.filtered_df = astronauts_df
        else:
           settings.filtered_df = astronauts_df[astronauts_df['Profile.Nationality'] == selected_country]

        settings.group_column = 'Profile.Name'
        settings.x_column = 'Mission.Year'
        settings.y_column = 'Profile.Astronaut Numbers.Overall'
        settings.hover_cols = ["Profile.Gender","Profile.Birth Year","Profile.Nationality","Profile.Military",
                               "Mission.Name", "Mission.Role","Mission.Year",
                               "Profile.Selection.Year", "Profile.Selection.Group","Profile.Lifetime Statistics.Mission count"]
        # Optional: map column names to custom labels for hover info
        settings.hover_labels = {
            "Profile.Gender": "Gender",
            "Profile.Birth Year": "Birth Year",
            "Profile.Nationality": "Nationality",
            "Profile.Military": "Military",
            "Mission.Name": "Mission",
            "Mission.Role": "Role",
            "Mission.Year": "Mission Year",
            "Profile.Selection.Year": "Selection Year",
            "Profile.Selection.Group": "Selection Group",
            "Profile.Lifetime Statistics.Mission count": "Total Missions"
        }
        settings.y_label = 'Astronaut'
        settings.point_size = 12
        settings.unique_names = settings.filtered_df[settings.group_column].unique()
        settings.height = max(250, 20 * len(settings.unique_names))
    else:
        if selected_country == 'all':
            settings.filtered_df = missions_df
        else:
            settings.filtered_df = missions_df[missions_df['Country'] == selected_country]

        settings.group_column = 'Company Name'
        settings.x_column = 'Year'
        settings.y_column = 'Company ID'
        #settings.hover_cols = ['Company Name', 'Location', 'Detail']
        settings.hover_cols = ['Detail']
        settings.hover_labels = {"Detail": ""}
        settings.y_label = 'Company'
        settings.point_size = 12
        settings.unique_names = settings.filtered_df[settings.group_column].unique()
        settings.height = max(250, 40 * len(settings.unique_names))
    return settings

def assign_colors(names, palette):
    return {name: palette[i % len(palette)] for i, name in enumerate(names)}

def add_milestone_traces(fig, milestones, max_y, step=1):
    # TODO pridat info o roku do milestonu
    steps = max(max_y // step, 1)
    for m in milestones:
        fig.add_trace(go.Scatter(
            x=[m["year"]] * steps,
            y=list(range(0, max_y, step)),
            mode="markers",
            marker=dict(color="purple", opacity=0),
            hovertext=m["label"],
            hoverinfo="text"
        ))

        fig.add_trace(go.Scatter(
            x=[m["year"], m["year"]],
            y=[0, max_y],
            mode="lines",
            line=dict(dash="dash", color="rgba(128,0,128,0.2)", width=2),
            showlegend=False,
            hoverinfo="skip"
        ))

def add_group_scatter_traces(fig, settings, name_y_map, color_map):   
    for name, group in settings.filtered_df.groupby(settings.group_column):
        # Group by x_column (year), aggregate rows that overlap
        grouped_by_year = group.groupby(settings.x_column)
        x_vals = []
        y_vals = []
        texts = []
        customdatas = []
        opacities = []
        for year, year_group in grouped_by_year:
            x_vals.append(year)
            y_vals.append(name_y_map[name])
            # Aggregate hover info for all missions in this year
            hover_lines = []
            for _, row in year_group.iterrows():
                hover_line = "<br>".join([
                    f"{settings.hover_labels.get(col, col)}: {row[col]}"
                    for col in settings.hover_cols
                ])
                hover_lines.append(hover_line)
            # Add company name and year as first line
            header = f"{name} ({int(year)})"
            text = header + "<br><b></b><br>" + ("<br>".join(hover_lines) if len(hover_lines) > 1 else hover_lines[0])
            texts.append(text)
            if 'Detail' in year_group.columns:
                customdatas.append(", ".join(str(d) for d in year_group['Detail']))
            else:
                customdatas.append(None)

            if settings.group_column == 'Company Name':
                # For companies, change opacity based on number of missions in the year
                count = len(year_group)
                if count <= 2:
                    opacities.append(0.3)
                elif 3 <= count <= 6:
                    opacities.append(0.6)
                else:
                    opacities.append(1.0)

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers',
            name=name,
            marker=dict(color=color_map[name], opacity=opacities, size=settings.point_size),
            text=texts,
            hoverinfo="text",
            customdata=customdatas,
        ))

def add_trajectory_lines(fig, settings, name_y_map, color_map, ):
    for name, group in settings.filtered_df.groupby(settings.group_column):
        sorted_group = group.sort_values(by=settings.x_column)
        if len(sorted_group) < 2:
            continue

        x_vals = [sorted_group.iloc[0][settings.x_column], sorted_group.iloc[-1][settings.x_column]]

        rgba = to_rgba(color_map[name], alpha=0.1)
        line_color = f'rgba({int(rgba[0]*255)},{int(rgba[1]*255)},{int(rgba[2]*255)},{rgba[3]})'

        fig.add_trace(go.Scatter(
            x=x_vals,
            y=[name_y_map[name], name_y_map[name]],
            mode='lines',
            name=f"{name} (trajectory)",
            line=dict(width=18, color=line_color),
            showlegend=False,
            hoverinfo='skip'
        ))

def get_active_years_fig(missions_df, astronauts_df, view_type='companies', selected_country='USA'):
    settings = get_settings(view_type, selected_country, missions_df, astronauts_df)
    color_map = assign_colors(settings.unique_names, palette)
    name_y_map = {name: i for i, name in enumerate(settings.unique_names)}

    fig = go.Figure()
    max_y = max(name_y_map.values()) + 1 if name_y_map else 1

    add_milestone_traces(fig, milestones, max_y)
    add_group_scatter_traces(fig, settings, name_y_map, color_map)
    add_trajectory_lines(fig, settings, name_y_map, color_map)

    fig.update_yaxes(side='right')
    fig.update_layout(
        #title=f'{selected_country}: {settings.y_label} Active Years',
        xaxis_title='Launch Date',
        yaxis_title=settings.y_label,
        xaxis=dict(fixedrange=True),
        yaxis=dict(
            range=[-0.5, max_y - 0.5],
            tickvals=list(name_y_map.values()),
            ticktext=list(name_y_map.keys()),
            autorange=False
        ),
        dragmode='pan',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=settings.height,
        margin=dict(t=20) 
    )

    return fig


def register_active_years_callbacks(app):
    @app.callback(
        Output('active-years-fig', 'figure'),
        [Input('view-type', 'data'),
         Input('country-dropdown', 'value')]
    )
    def update_active_years_fig(selected_view, selected_country):
        return get_active_years_fig(app.missions_df, app.astronauts_df, view_type=selected_view, selected_country=selected_country)
