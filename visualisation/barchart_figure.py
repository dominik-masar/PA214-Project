import pandas as pd
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

    # Add rounded edges to bars
    for trace in fig.data:
        trace.marker.line.width = 0
        trace.marker.line.color = 'rgba(0,0,0,0)'
        trace.marker.opacity = 1
        trace.marker.pattern = None
        trace.marker.cornerradius = 8  # <-- This works in Plotly 5.16+ (if installed)


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

    # TODO mission count: either hover info or number in brackets

    return fig
