import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import preprocessing as pp

df = pp.load_data(start=1960, end=2015)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Filter out countries from the dropdown menu for which GDP or CO2 graph does not exist
countries = df[(df['year']==1960) & 
               (df['co2_emissions_kt'].notna()) & 
               (df['gdp_2010'].notna())]['country'].unique() 

app.layout = html.Div([
    dcc.Dropdown(
                id='country',
                options=[{'label': country, 'value': country} for country in countries],
                value='Finland',
                style={'position': 'relative', 'width': '50%', 'display': 'inline-block'}
    ),
    dcc.Graph(id='graph-with-country')
    ],
    style={'position': 'relative', 'width': '80%', 'display': 'inline-block'}
    )

@app.callback(
    dash.dependencies.Output('graph-with-country', 'figure'),
    [dash.dependencies.Input('country', 'value')])

def update_figure(selected_country):
    filtered_df = df[df['country'] == selected_country]
    data = [
        dict(
            type='scatter',
            x=filtered_df['year'],
            y=filtered_df['co2_vs_year1_percent'],
            name='Hiilidioksipäästöt (1960: 100%)',
            mode='lines'
        ),
        dict(
            type='scatter',
            x=filtered_df['year'],
            y=filtered_df['gdp_vs_year1_percent'],
            name='BKT v. 2010 dollareina (1960: 100%)',
            mode='lines'
        )    
    ]

    layout=go.Layout(xaxis={#'type': 'log', 
                    'title': 'Vuosi',
                   #'range': [1950, 2000]
                   },
                    yaxis={#'type': 'log', 
                   # 'title': 'CO2 emissions compared to 1991 (100 percent)',
                   #'range': [0, 200]
                   },
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            title='Hiilidioksidipäästöjen ja BKT:n kehitys alueittain vuosina 1960-2014',
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )  
    return dict(data=data, layout=layout)
        



if __name__ == '__main__':
    app.run_server(debug=True)