import re
import datetime
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import csv

class PreprocessData(object):
    def __init__(self, stock_filename, filenames):
        self.stock_file = stock_filename
        self.filenames = filenames

    def preprocess_all(self):
        for filename in self.filenames:
            company_name = filename.split('/')[2].split('.')[0]
            dates, company = self.preprocess(filename)
            company_dict = dict.fromkeys(dates, {})

            for count, date in enumerate(dates, start=0):
                company_dict[date]['neg'] = company[count][0]
                company_dict[date]['pos'] = company[count][1]
                company_dict[date]['neu'] = company[count][2]

            tmp_df = pd.DataFrame.from_dict(company_dict)
            neg = tmp_df.loc['neg', :]
            pos = tmp_df.loc['pos', :]
            neu = tmp_df.loc['neu', :]
            df = pd.DataFrame()
            df['neg'] = neg
            df['pos'] = pos
            df['neu'] = neu
            df = df.set_index(pd.to_datetime(tmp_df.columns.values))
            df.index.name = 'date'
            df.to_csv('../data/' + company_name + '_feat_vec.csv', sep=',')

    def preprocess(self, filename):
        stocks = pd.read_csv(self.stock_file)
        tweets = pd.read_csv(filename)
        j = 0
        total = np.zeros(3)
        vals = 0
        avg_sent = []
        i = 0

        while True:
            tweet_dt = tweets['date'][i]
            if tweet_dt >= stocks['date'][len(stocks['date']) - 1]:
                if vals != 0:
                    avg_sent.append(total / vals)
                    total = np.zeros(3)
                    vals = 0
                else:
                    avg_sent.append(np.zeros(3))
                break
            stocks_dt = stocks['date'][j]
            if tweet_dt >= stocks_dt:
                j += 1
                if vals != 0:
                    avg_sent.append(total / vals)
                    total = np.zeros(3)
                    vals = 0
                else:
                    avg_sent.append(np.zeros(3))
            else:
                total += np.array([tweets['neg'][i],tweets['pos'][i],tweets['neu'][i]])
                vals += 1
                i += 1

        return stocks['date'], avg_sent

def main():
    PreprocessData('../data/hourly_stocks.csv', ['../data/google.csv', '../data/apple.csv',
                    '../data/amazon.csv', '../data/capital_one.csv',
                    '../data/nvidia.csv']).preprocess_all()

if __name__ == "__main__":
    main()
