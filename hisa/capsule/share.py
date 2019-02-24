from __future__ import absolute_import

import matplotlib.pyplot as plt
import pandas as pd
import os
from hisa.capsule import Capsule
from hisa.config.app import AppConfig
from hisa.learn.sentiment.sentiment import ProcessTweets
import urllib.request
import json

from hisa._util import (
    _check_value_error
)

class Share(Capsule):
    def __init__(self, equity_symbol, company_name, interval='daily', minute_interval='1min', start=None, end=None, size='compact'):
        self.symbol = equity_symbol
        self.name = company_name.lower()
        self.key = os.environ['ALPHA_VANTAGE_API_KEY']
        self.data = None
        self.metata = None
        self.interval = interval
        self.minute_interval = minute_interval
        _check_value_error(self.interval, ['intraday','daily','daily_adjusted','weekly'])
        _check_value_error(self.minute_interval, ['1min', '5min', '15min', '30min', '60min'])

        av_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_'+self.interval+'&symbol='+self.symbol+'&interval='+minute_interval+'&apikey='+self.key
        with urllib.request.urlopen(av_url) as url:
            json_file = json.loads(url.read().decode())

        key = 'Time Series ('
        if self.interval == 'intraday':
            key += self.minute_interval+')'
        elif self.interval == 'daily' or self.interval == 'daily_adjusted':
            key += 'Daily)'
        elif self.interval == 'weekly':
            key = 'Weekly Time Series'
        j = json_file[key]
        self.data = pd.DataFrame.from_dict(j, orient='index')
        self.data.index.name = 'date'

        if start == None:
            start = self.data.index[0]
        if end == None:
            end = self.data.index[-1]
        self.data.index = pd.to_datetime(self.data.index)
        self.data = self.data.loc[start:end]
        self.data = self.data.rename(columns=lambda x: x.split(' ')[-1])
        self.data = self.data.astype(float)


    def plot(self, column, title=None, start=None, end=None, save=False, filename='plot.png'):
        if start == None:
            start = self.data.index[0]
        if end == None:
            end = self.data.index[-1]
        if title == None:
            title = self.name + ': ' + column + ' [' + str(start.date()) + ', ' + str(end.date()) + ']'
        sample = self.data.loc[start:end]
        columns = column.split(',')
        data_cols = self.data.columns.tolist()
        for c in columns:
            _check_value_error(c, data_cols)
        for i in range(len(data_cols)):
            if data_cols[i] not in columns:
                sample = sample.drop(data_cols[i], 1)

        p = sample.plot()
        plt.title(title)
        if save:
            plt.savefig(filename)
        plt.show()
        return p


    def get_sample(self, start, end):
        return self.data[start:end]


    def get_dataframe(self):
        return self.data


    def to_csv(self, filename):
        self.data.to_csv(filename)


    def generate_twitter_sentiment(self, output_path='tweets.json', num=1000, start=None, end=None):
        command = "twitterscraper " + self.name
        if start == None:
            start = self.data.index[0]
        if end == None:
            end = self.data.index[-1]

        command += ' -l ' + str(num)
        command += ' -o ' + output_path
        command += ' --lang en'
        command += ' -bd ' + str(start)
        command += ' -ed ' + str(end)

        print(command)
        os.system(command)
        sentiment_out = os.path.join(os.path.split(output_path)[0], os.path.split(output_path)[-1].split('.')[0] + '.csv')
        print("Getting sentiment...")
        ProcessTweets(output_path, sentiment_out).get_tweets()
