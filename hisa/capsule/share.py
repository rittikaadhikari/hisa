from __future__ import absolute_import

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
import os
from hisa.capsule import Capsule
from hisa.config.app import AppConfig

from hisa._util import (
    _check_value_error
)

class Share(Capsule):
    def __init__(self, equity_symbol, interval='daily', minute_interval='1min', start=None, end=None, size='compact'):
        self.name = equity_symbol
        self.key = os.environ['ALPHA_VANTAGE_API_KEY']
        self.ts = TimeSeries(key=self.key, output_format = 'pandas')
        self.data = None
        self.metata = None
        self.interval = interval
        self.minute_interval = minute_interval
        _check_value_error(self.interval, ['intraday','daily','daily_adjusted','weekly'])
        _check_value_error(self.minute_interval, ['1min', '5min', '15min', '30min'])
        if self.interval == 'intraday':
            self.data, self.meta_data = self.ts.get_daily(symbol=self.name, interval=self.minute_interval, outputsize=size)
        elif self.interval == 'daily':
            self.data, self.meta_data = self.ts.get_daily(symbol=self.name, outputsize=size)
        elif self.interval == 'daily_adjusted':
            self.data, self.meta_data = self.ts.get_daily_adjusted(symbol=self.name, outputsize=size)
        elif self.interval == 'weekly':
            self.data, self.meta_data = self.ts.get_weekly(symbol=self.name, outputsize=size)

        if start == None:
            start = self.data.index[0]
        if end == None:
            end = self.data.index[-1]
        self.data.index = pd.to_datetime(self.data.index)
        self.data = self.data.loc[start:end]
        self.data = self.data.rename(columns=lambda x: x.split(' ')[-1])


    def plot(self, column, title=None, start=None, end=None):
        if start == None:
            start = self.data.index[0]
        if end == None:
            end = self.data.index[-1]
        if title == None:
            title = self.name + ': ' + column + ' [' + str(start.date()) + ', ' + str(end.date()) + ']'
        sample = self.data.loc[start:end]
        _check_value_error(column, self.data.columns)
        p = sample[column].plot()
        plt.title(title)
        plt.show()
        return p


    def save(self, filename):
        self.data.to_csv(filename)
