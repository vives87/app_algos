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
    
    def __init__(self, market, algo_tag):
        self.url_base = 'https://miax-gateway-jog4ew3z3q-ew.a.run.app'
        self.competi = 'mia_7'
        self.user_key = 'AIzaSyBfNJ1ZIVQrnngOX_csBmi-xTq0_u0uihM'
        self.market = market
        self.algo_tag = algo_tag
    
    def get_ticker_master(self):
        url = f'{self.url_base}/data/ticker_master'
        params = {'competi': self.competi,
                  'market': self.market,
                  'key': self.user_key}
        response = requests.get(url, params)
        tk_master = response.json()
        maestro_df = pd.DataFrame(tk_master['master'])
        return maestro_df
    
    def get_close_data(self):
        maestro_df = self.get_ticker_master()
        data_close = {}
        for i, data in maestro_df.iterrows():
            ticker = data.ticker
            #logger.info(ticker)
            data_close[ticker] = self.get_close_data_ticker(ticker)
        data_close = pd.DataFrame(data_close)
        return data_close
    
    def get_close_data_ticker(self, ticker):
        url = f'{self.url_base}/data/time_series'
        params = {'market': self.market,
                  'key': self.user_key,
                  'ticker': ticker}
        response = requests.get(url, params)
        tk_data = response.json()
        series_data = pd.read_json(tk_data, typ='series')
        return series_data
    
    def get_open_data_ticker(self,ticker):
        url = f'{self.url_base}/data/time_series'
        params = {'market': self.market,
                  'key': self.user_key,
                  'ticker': ticker,
                  'close': False}
        response = requests.get(url, params)
        tk_data = response.json()
        open_data = pd.read_json(tk_data, typ='frame')['open']
        return open_data
    
    def get_close_data(self):
        maestro_df = self.get_ticker_master()
        data_close = {}
        for i, data in maestro_df.iterrows():
            ticker = data.ticker
            #logger.info(ticker)
            data_close[ticker] = self.get_close_data_ticker(ticker)
        data_close = pd.DataFrame(data_close)
        return data_close
    
    def get_open_data(self):
        maestro_df = self.get_ticker_master()
        data_open = {}
        for i, data in maestro_df.iterrows():
            ticker = data.ticker
            #logger.info(ticker)
            data_open[ticker] = self.get_open_data_ticker(ticker)
        data_open = pd.DataFrame(data_open)
        return data_open
    
    def get_user_algos(self):
        url = f'{self.url_base}/participants/algorithms'
        params = {'competi': self.competi,
                  'key': self.user_key}
        response = requests.get(url, params)
        algos = response.json()
        if algos:
            algos_df = pd.DataFrame(algos)
            print(algos_df.to_string())
            return algos_df

