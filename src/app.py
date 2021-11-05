from api_handler import APIBMEHandler
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

markets = ['DAX','IBEX','EUROSTOXX']

apihandler = APIBMEHandler(market='IBEX')






app.layout = html.Div(children=[
    html.H1(
        children='MIAX Data Explorer',
    ),

    html.H5(
        children='mIAx API',
    ),
    html.Div([
            dcc.Dropdown(
                id='markets',
                options=[{'label': i, 'value': i} for i in markets],
                value='IBEX'
            ),
            dcc.Dropdown(
                id='tickers',
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(
        id='figura',
    )
])

@app.callback(    
    Output(component_id='tickers', component_property='options'),    
    Input(component_id='markets', component_property='value'))

def change_index(selected_index):
    apihandler.market=selected_index
    ticker_master=apihandler.get_ticker_master()
    ticks = list(ticker_master.ticker)
    dropdown_values=[{'label': i, 'value': i} for i in ticks]
    return dropdown_values

@app.callback(    
    Output('tickers', 'value'),    
    Input('tickers', 'options'))

def change_value(ticker):
    return ticker[0]['value']

@app.callback(    
    Output('figura', 'figure'),    
    Input('tickers', 'value'))

def change_figure(new_ticker):
    df=apihandler.get_data_ticker(ticker=new_ticker)
    fig = go.Figure(        
        go.Candlestick(        
            x=df.index,open=df['open'],        
            high=df['high'],        
            low=df['low'],        
            close=df['close']))
    return fig

if __name__ == "__main__":    
    app.run_server(host="0.0.0.0", debug=False, port=8080)