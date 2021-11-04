import requests
import json
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def allocs_to_frame(json_allocations):
    alloc_list = []
    for json_alloc in json_allocations:
        #print(json_alloc)
        allocs = pd.DataFrame(json_alloc['allocations'])
        allocs.set_index('ticker', inplace=True)
        alloc_serie = allocs['alloc']
        alloc_serie.name = json_alloc['date'] 
        alloc_list.append(alloc_serie)
    all_alloc_df = pd.concat(alloc_list, axis=1).T
    return all_alloc_df


class APIBMEHandler:
    
    def __init__(self, market):
        self.url_base = 'https://miax-gateway-jog4ew3z3q-ew.a.run.app'
        self.competi = 'mia_7'
        self.user_key = 'AIzaSyBfNJ1ZIVQrnngOX_csBmi-xTq0_u0uihM'
        self.market = market
    
    def get_ticker_master(self):
        url = f'{self.url_base}/data/ticker_master'
        params = {'competi': self.competi,
                  'market': self.market,
                  'key': self.user_key}
        response = requests.get(url, params)
        tk_master = response.json()
        maestro_df = pd.DataFrame(tk_master['master'])
        return maestro_df
    
    def get_close_data_ticker(self, ticker):
        url = f'{self.url_base}/data/time_series'
        params = {'market': self.market,
                  'key': self.user_key,
                  'ticker': ticker}
        response = requests.get(url, params)
        tk_data = response.json()
        series_data = pd.read_json(tk_data, typ='series')
        return series_data
    
