from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('owid-covid-data.csv')
df2 = pd.read_csv('world.csv')

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Covid-19 Dashboard'),
    html.P("Total Deaths: " + '{:,.0f}'.format(df2['total_deaths'].max())),
    html.P("Total Cases: " + '{:,.0f}'.format(df2['total_cases'].max())),
    html.P("Total Vaccinations: " + '{:,.0f}'.format(df2['total_vaccinations'].max())),
    html.P("Select type:"),
    dcc.RadioItems(
        id='type', 
        options=["Deaths", "Cases", "Vaccinations"],
        value="Deaths",
        inline=True
    ),
    html.P("Global View Timeline:"),
    dcc.Graph(id="graph"),
    html.P("Select Group:"),
    dcc.Dropdown(df["location"].drop_duplicates(), 'Ireland', id='country_dropdown', multi=True),
    dcc.Graph(id="graph2")
])


@app.callback(
    Output("graph", "figure"), 
    Input("type", "value"))
def display_choropleth(type):
    global df
    type2 = type
    color_range = [0, 1250000]
    if type == "Deaths":
        type2 = "total_deaths"
        color_range = [0, 1250000]
    elif type == "Cases":
        type2 = "total_cases"
        color_range = [0, 100000000]
    else:
        type2 = "total_vaccinations"
        color_range = [0, 3500000000]
    
    fig = px.choropleth(df, locations='iso_code', color=type2, animation_frame='date', range_color=color_range)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output("graph2", "figure"), 
    Input("type", "value"), 
    Input("country_dropdown", "value"))
def display_line(type, country_dropdown):
    global df
    type2 = type
    if type == "Deaths":
        type2 = "total_deaths"
    elif type == "Cases":
        type2 = "total_cases"
    else:
        type2 = "total_vaccinations"
    
    if isinstance(country_dropdown, str):
        country_dropdown = [country_dropdown]
    
    data = df[df["location"].isin(country_dropdown)]
    
    fig = px.line(data, x="date", y=type2, color="location")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_yaxes(title_text=type)
    fig.update_xaxes(title_text="Date")
    return fig



app.run_server(debug=False)