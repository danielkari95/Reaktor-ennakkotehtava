import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import preprocessing

df = preprocessing.df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df[df['year'].mod(3).eq(0)]['year'].unique()} # only select every 3rd year
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df['year'] == selected_year]
    traces = []
    for country in filtered_df['country'].unique():
        df_by_country = filtered_df[filtered_df['country'] == country]
        traces.append(go.Scatter(
            x=df_by_country['gdp_vs_1991'],
            y=df_by_country['co2_vs_1991'],
            text=df_by_country['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=country
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={#'type': 'log',
                   'title': 'GDP compared to 1991 (100 percent)',
                   'range': [0, 300]},
            yaxis={#'type': 'log', 
                   'title': 'CO2 emissions compared to 1991 (100 percent)',
                   'range': [0, 200]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)