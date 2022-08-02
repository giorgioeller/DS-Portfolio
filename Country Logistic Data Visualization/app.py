# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# continent data obtained from https://www.geonames.org/countries/
# logistic data for countries obtained from https://databank.worldbank.org/source/logistics-performance-index-(lpi)/Type/TABLE/preview/on#
# more information about the Logistics Performance Index (LPI) available on: https://lpi.worldbank.org/about

from cmath import nan
from pydoc import visiblename
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__, title='Logistic Data Visualization')   

# Load logistic and continent data
continents = pd.read_csv('continents.csv', delimiter=';', na_filter=False)
continents = continents.replace({'Continent':{'AS':'Asia', 'EU':'Europe', 'AF':'Africa', 'OC':'Oceania',
                                              'NA':'North America', 'SA':'South America'}})
df = pd.read_csv('logistics_data.csv')

# Create a dataframe with the raw data
df = df.merge(continents, on='Country Code', how='left')
df = df.dropna(subset=['Country Code'])

# Variables with data for dataframe about logistic data
countries = df['Country Name']
logistic_values = df.iloc[:, 4:10].transpose()
logistic_values = logistic_values.replace(to_replace='..', value=None)
logistic_values = logistic_values.astype(float)
dates = []
for i in logistic_values.index.values.tolist():
    dates.append(int(i[0:4]))

# Create dataframe for logistic data 
logistic_data = pd.DataFrame(logistic_values.values, columns=countries)

# Dash app
app.layout = html.Div(children=[
    html.Div(children=
        '''Country Logistic Data Viewer''',
        style={'padding-top': '1vh',
               'padding-bottom': '2vh',
               'font-size': '6vh',
               'font-weight': 'bold',
               'text-align': 'center'}
        ),

    # Interactive plot and filters
    html.Div(children=[
        dcc.Dropdown(
            id='country-dropdown',
            multi=True,
            value=['Canada', 'United States'],
            style={'padding': '1vh'}
        ),

        dcc.Graph(
            id='logistics-graph',
            config={'showTips':True},
            style={'width': '85%', 
                   'vertical-align': 'middle', 
                   'height': '75vh', 
                   'display': 'inline-block'}
        ),

        dcc.Checklist(
            id='continent-checklist',
            options=['Africa', 'North America', 'South America', 'Asia', 'Europe', 'Oceania'],
            value=['North America'],
            labelStyle = {'display': 'block'},
            style={'width': '14%', 
                   'vertical-align': 'top', 
                   'display': 'inline-block'}
        )
    ],
        style={'backgroundColor':'white',
               'border': '2px solid black', 
               'borderRadius': '15px', 
               'overflow': 'hidden'}
    )
])

# Callback for updating available countries
@app.callback(
    Output('country-dropdown', 'options'),
    Input('continent-checklist', 'value'))
def update_dropdown(available_countries):
    selected_countries = df.loc[df['Continent'].isin(available_countries), 'Country Name'].values.tolist()
    return selected_countries

@app.callback(
    Output('logistics-graph', 'figure'),
    Input('country-dropdown', 'value'))
def update_graph(countries):
    if countries is not None:
        shown_countries = countries
    else:
        shown_countries = []
    fig = px.line(
                  logistic_data[shown_countries], 
                  x=dates,
                  y=logistic_data[shown_countries].columns[:],
                  labels={'x':'Year', 
                          'value':'Logistics Performance Index (LPI)',
                          'variable':'Country'},
                  markers=True,
                  template='plotly_white'
                  )
    fig.update_layout({'plot_bgcolor':'white', 'paper_bgcolor':'white'})
    return fig

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=False) #Switch to True for more details about the app