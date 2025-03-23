import plotly.express as px

df = px.data.gapminder().query("year == 2024")

fig = px.scatter_geo(
    df, 
    locations="iso_alpha", 
    hover_name="country", 
)

fig.update_geos(
    visible=True,
    landcolor="lightgray",
    showcountries=True,
    countrycolor="black",
)

fig.show()
