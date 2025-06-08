import pandas as pd
from dash import html, dcc
from navbar import get_navbar
import re

# TODO nechci tohle posila z app?
missions_df = pd.read_csv("datasets/final_dataset_missions.csv")
wiki_df = pd.read_csv("datasets/wiki_summaries.csv")
merged_df = pd.merge(missions_df, wiki_df, on="Index", how="left")

# Ensure merged_df has the same number of records as missions_df
merged_df = merged_df.set_index(missions_df.index)


def get_info_layout(app, pathname):
    # Extract page number
    try:
        page = int(pathname.split("/logs/")[-1]) if "/logs/" in pathname else 1
    except ValueError:
        page = 1

    page_size = 15
    total = len(merged_df)
    total_pages = (total + page_size - 1) // page_size
    page = max(1, min(page, total_pages))

    start = (page - 1) * page_size
    end = start + page_size
    page_df = merged_df.iloc[start:end]

    # Generate mission cards
    mission_cards = []
    for _, row in page_df.iterrows():
        idx = row.name 
        mission_cards.append(
            html.Div([
            html.H3(row["Detail"]),
            html.P(f"📍 Location: {row['Location']}"),
            html.P(f"🚀 Rocket: {row['Rocket'] or 'N/A'}"),
            html.P(f"🛰️ Company: {row['Company Name']}"),
            html.P(f"📅 Date: {row['Datum']}"),
            html.P(f"🌌 Goal: {row['Mission Goal']}"),
            html.P(f"🟢 Mission Status: {row['Status Mission']}"),
            html.P(f"🛠️ Rocket Status: {row['Status Rocket']}"),
            html.Details([
                html.Summary("🔎 Wikipedia Summary"),
                html.P(row.get("Wikipedia_Summary", "No summary available."))
            ]),
            ], id=f"mission-{idx}", 
               style={
            'border': '1px solid #ccc',
            'padding': '15px',
            'borderRadius': '8px',
            'marginBottom': '20px',
            'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
            'backgroundColor': '#fff'
            })
        )

    # Pagination controls
    nav = html.Div([
        dcc.Link("← Previous", href=f"/logs/{page - 1}", style={'marginRight': '30px'}) if page > 1 else "",
        html.Span(f"Page {page} of {total_pages}", style={'fontWeight': 'bold'}),
        dcc.Link("Next →", href=f"/logs/{page + 1}", style={'marginLeft': '30px'}) if page < total_pages else "",
    ], style={'textAlign': 'center', 'marginTop': '40px'})

    return html.Div([
        get_navbar(),
        html.Div([
            html.H1("🚀 Mission Logs", style={'textAlign': 'center', 'marginBottom': '30px'}),
            html.Div(mission_cards),
            nav
        ], style={'maxWidth': '1000px', 'margin': 'auto'})
    ])


def get_mission_detail_layout(app, mission_id):
    # mission_id is the index of the mission in merged_df
    try:
        mission = merged_df.loc[mission_id]
    except Exception:
        return html.Div("Mission not found.")

    return html.Div([
        get_navbar(),
        html.Div([
            html.H2(mission["Detail"]),
            html.P(f"📍 Location: {mission['Location']}"),
            html.P(f"🚀 Rocket: {mission['Rocket'] or 'N/A'}"),
            html.P(f"🛰️ Company: {mission['Company Name']}"),
            html.P(f"📅 Date: {mission['Datum']}"),
            html.P(f"🌌 Goal: {mission['Mission Goal']}"),
            html.P(f"🟢 Mission Status: {mission['Status Mission']}"),
            html.P(f"🛠️ Rocket Status: {mission['Status Rocket']}"),
            html.Details([
                html.Summary("🔎 Wikipedia Summary"),
                html.P(mission.get("Wikipedia_Summary", "No summary available."))
            ]),
            dcc.Link("← Show All Mission Logs", href="/logs/1", style={'marginTop': '30px', 'display': 'block'})
        ], style={'maxWidth': '700px', 'margin': 'auto', 'marginTop': '40px'})
    ])