# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# continent data obtained from https://www.geonames.org/countries/
# logistic data for countries obtained from https://databank.worldbank.org/source/logistics-performance-index-(lpi)/Type/TABLE/preview/on#

from cmath import nan
from pydoc import visiblename
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Load logistic and continent data
continents = pd.read_csv("continents.csv", delimiter=";", na_filter=False)
continents = continents.replace({"Continent":{"AS":"Asia", "EU":"Europe", "AF":"Africa", "OC":"Oceania",
                                              "NA":"North America", "SA":"South America"}})
df = pd.read_csv("logistics_data.csv")

# Create a dataframe with the raw data
df = df.merge(continents, on="Country Code", how="left")
df = df.dropna(subset=['Country Code'])

# Variables with data for dataframe about logistic data
countries = df["Country Name"]
dates = [2007, 2010, 2012, 2014, 2016, 2018]
logistic_values = df.iloc[:, 4:10].transpose()
logistic_values = logistic_values.replace(to_replace="..", value=None)
logistic_values = logistic_values.astype(float)

# Create dataframe for logistic data 
logistic_data = pd.DataFrame(logistic_values.values, columns=countries)

# Dash app
app.layout = html.Div(children=[
    html.H1(children='Logistic Data Visualization'),

    html.Div(children='''
        Sorted by country and/or continent.
    '''),

    # Graph and checklist
    html.Div(children=[
        dcc.Graph(
            id='logistics-graph',
            style={'width': '170vh', 'height': '100vh'}
            ),

        dcc.Checklist(
            id="continent-checklist",
            options=["Africa", "North America", "South America", "Asia", "Europe", "Oceania"],
            value=["North America"],
            inline=False
            )
    ]),
    
])

# Callback for updating graph
@app.callback(
    Output("logistics-graph", "figure"),
    Input("continent-checklist", "value"))
def update_graph(continent_selected):
    selected_countries = df.loc[df["Continent"].isin(continent_selected), 'Country Name'].values.tolist()
    fig = px.line(logistic_data[selected_countries], 
                  x=dates, 
                  y=logistic_data[selected_countries].columns[:], 
                  markers=True)
    return fig

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)