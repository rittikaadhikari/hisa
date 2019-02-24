from __future__ import absolute_import

from sklearn import linear_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class RidgeModel():
    def __init__(self, filename, alpha=0.3, cv=3):
        self.data = data
        self.df = pd.read_csv(filename)
        self.x = [self.df['neg'], self.df['pos'], self.df['neu']]
        self.y = self.df['date']
        self.alpha = alpha
        self.cv = cv
        self.model = Ridge(alpha=alpha, cv=cv, normalize=True)

    def train(self):
        self.model.fit(self.x, self.y)

    def predict(self):
        self.model.predict(self.x, self.y)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feat_vec', required=True, help='feature vectors created using preprocess')
    args = ap.parse_args()

    files = []
    for dirpath, dirnames, filenames in os.walk(args.input_dir):
        for f in filenames:
            if f.split('.')[-1] == 'json':
                 files.append((f.split('.')[0], os.path.join(dirpath, f)))

    for f in files:
        ProcessTweets(f[1], os.path.join(args.output_dir, f[0] + '.csv')).get_tweets()


if __name__ == "__main__":
    main()
