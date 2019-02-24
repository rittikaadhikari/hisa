import re
import json
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import argparse
import os

import csv

class ProcessTweets(object):
    def __init__(self, filename, outname):
        self.filename = filename
        self.outname = outname
        json_file = open(filename)
        json_str = json_file.read()
        self.json = json.loads(json_str)
        self.sid = SentimentIntensityAnalyzer()

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_sentiment(self, tweet):
        polarity_scores = self.sid.polarity_scores(tweet)
        return polarity_scores['neg'], polarity_scores['pos'], polarity_scores['neu']

    def get_tweets(self):
        df = pd.DataFrame.from_dict(self.json)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by=['timestamp'], inplace=True, ascending=True)
        df.reset_index(inplace=True)

        self.json = df.to_dict()

        timestamps = self.json['timestamp']

        start_date = pd.to_datetime(timestamps[0])
        end_date = start_date + timedelta(hours=1)

        sentiments = dict()
        temp = []

        tweets = self.json['text']

        for count, tweet in enumerate(tweets, start=0):
            tweet = tweets[tweet]
            curr_time = timestamps[count]
            if isinstance(tweet, int):
                print(tweet)
            if curr_time >= start_date and curr_time < end_date:
                neg, pos, neu = self.get_sentiment(self.clean_tweet(tweet))
                temp.append([neg, pos, neu])
            else:
                means = np.mean(np.asarray(temp), axis=0)
                obj = {'neg': means[0], 'pos': means[1], 'neu': means[2]}
                sentiments[start_date.strftime("%Y-%m-%d %H:%M:%S")] = obj
                temp = []
                start_date = end_date
                end_date = start_date + timedelta(hours=1)
                neg, pos, neu = self.get_sentiment(self.clean_tweet(tweet))
                temp.append([neg, pos, neu])

        tmp_df = pd.DataFrame.from_dict(sentiments)
        neg = tmp_df.loc['neg', :]
        pos = tmp_df.loc['pos', :]
        neu = tmp_df.loc['neu', :]
        df = pd.DataFrame()
        df['neg'] = neg
        df['pos'] = pos
        df['neu'] = neu
        df = df.set_index(pd.to_datetime(tmp_df.columns.values))
        df.index.name = 'date'
        df.to_csv(self.outname, sep=',')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input_dir', required=True, help='directory containing json files from twitterscraper')
    ap.add_argument('--output_dir', required=True, help='directory of resulting sentiment csv files')
    args = ap.parse_args()

    if(not os.path.exists(args.output_dir)):
        os.makedirs(args.output_dir)

    files = []
    for dirpath, dirnames, filenames in os.walk(args.input_dir):
        for f in filenames:
            if f.split('.')[-1] == 'json':
                 files.append((f.split('.')[0], os.path.join(dirpath, f)))

    for f in files:
        ProcessTweets(f[1], os.path.join(args.output_dir, f[0] + '.csv')).get_tweets()


if __name__ == "__main__":
    main()
