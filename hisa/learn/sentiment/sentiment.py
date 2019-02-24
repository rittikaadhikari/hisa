import re
import json
import datetime
from datetime import datetime
from datetime import timedelta
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
        start_date = datetime.strptime(self.json[0]['timestamp'], '%Y-%m-%dT%H:%M:%S')
        end_date = start_date + timedelta(hours=1)

        sentiments = dict()
        temp = []

        for tweet in self.json:
            curr_time = datetime.strptime(tweet['timestamp'], '%Y-%m-%dT%H:%M:%S')
            if curr_time >= start_date and curr_time < end_date or curr_time < start_date:
                neg, pos, neu = self.get_sentiment(self.clean_tweet(tweet['text']))
                temp.append([neg, pos, neu])
            else:
                sentiments[start_date.strftime("%Y-%m-%dT%H:%M:%S")] = np.mean(np.asarray(temp), axis=0)
                temp = []
                start_date = end_date
                end_date = start_date + timedelta(hours=1)
                neg, pos, neu = self.get_sentiment(self.clean_tweet(tweet['text']))
                temp.append([neg, pos, neu])

        data = open(self.outname, 'w')
        csvwriter = csv.writer(data)
        count = 0
        for sentiment in [sentiments]:
            if count == 0:
                header = sentiment.keys()
                csvwriter.writerow(header)
                count += 1
            csvwriter.writerow(sentiment.values())
        data.close()

def main():
    ProcessTweets('../data/apple_tweets.json', '../data/apple.csv').get_tweets()
    ProcessTweets('../data/capital_one_tweets.json', '../data/capital_one.csv').get_tweets()
    ProcessTweets('../data/google_tweets.json', '../data/google.csv').get_tweets()
    ProcessTweets('../data/amazon_tweets.json', '../data/amazon.csv').get_tweets()
    ProcessTweets('../data/nvidia_tweets.json', '../data/nvidia.csv').get_tweets()

if __name__ == "__main__":
    main()
