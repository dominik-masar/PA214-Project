import pandas as pd
from dash.dependencies import Output, Input, State
import plotly.express as px

def barchart_fig(data, color_palette, top_n=9):

    country_counts = data['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']

    if len(country_counts) > top_n:
        top_countries = country_counts.head(top_n)
        others_count = country_counts['Count'][top_n:].sum()
        others_row = pd.DataFrame({'Country': ['Others'], 'Count': [others_count]})
        plot_data = pd.concat([top_countries, others_row], ignore_index=True)
    else:
        plot_data = country_counts

    fig = px.bar(
        plot_data,
        x='Count',
        y='Country',
        color='Country',
        color_discrete_map=color_palette,
        labels={'Count': 'Number of Missions'},
        text='Country'
    )

    fig.update_layout(
        yaxis=dict(
            categoryorder='total ascending',
            showticklabels=False,
            title='',
            showgrid=False,
            zeroline=False
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    return fig


def register_barchart_callbacks(app):
    @app.callback(
        Output('bar-fig', 'figure'),  # or whatever your bar chart graph id is
        Input('selected-years', 'data')
    )
    def update_bar_chart(year_range):
        start, end = year_range
        df = app.missions_df
        filtered_df = df[(df['Year'] >= start) & (df['Year'] <= end)]
        return barchart_fig(filtered_df, app.color_map)