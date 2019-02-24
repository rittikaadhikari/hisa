import re
import json
import datetime
from datetime import datetime
from datetime import timedelta
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
        start_date = pd.to_datetime(self.json[0]['timestamp'])
        end_date = start_date + timedelta(hours=1)

        sentiments = dict()
        temp = []

        for tweet in self.json:
            curr_time = datetime.strptime(tweet['timestamp'], '%Y-%m-%dT%H:%M:%S')
            if curr_time >= start_date and curr_time < end_date or curr_time < start_date:
                neg, pos, neu = self.get_sentiment(self.clean_tweet(tweet['text']))
                temp.append([neg, pos, neu])
            else:
                means = np.mean(np.asarray(temp), axis=0)
                obj = {'neg': means[0], 'pos': means[1], 'neu': means[2]}
                sentiments[start_date.strftime("%Y-%m-%d %H:%M:%S")] = obj
                temp = []
                start_date = end_date
                end_date = start_date + timedelta(hours=1)
                neg, pos, neu = self.get_sentiment(self.clean_tweet(tweet['text']))
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
    ProcessTweets('../data/apple_tweets.json', '../data/apple.csv').get_tweets()
    ProcessTweets('../data/capital_one_tweets.json', '../data/capital_one.csv').get_tweets()
    ProcessTweets('../data/google_tweets.json', '../data/google.csv').get_tweets()
    ProcessTweets('../data/amazon_tweets.json', '../data/amazon.csv').get_tweets()
    ProcessTweets('../data/nvidia_tweets.json', '../data/nvidia.csv').get_tweets()

if __name__ == "__main__":
    main()
