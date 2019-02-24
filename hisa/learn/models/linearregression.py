from __future__ import absolute_import

from sklearn import linear_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import argparse
from sklearn.metrics import accuracy_score

class LinearModel():
    def __init__(self, filename, stock_filename, company, alpha=0.3):
        self.df = pd.read_csv(filename)
        stock = pd.read_csv(stock_filename)
        dates = [int(pd.to_datetime(date).strftime("%s")) for date in self.df['date']]
        self.x = np.asarray([dates, self.df['neg'], self.df['pos'], self.df['neu']], dtype=float).T
        self.y = np.asarray(stock[company + '_open'])
        self.alpha = alpha
        self.model = linear_model.LinearRegression(fit_intercept=True, normalize=True)

    def train(self):
        self.model.fit(self.x, self.y)

    def predict(self):
        return self.model.predict(self.x)

    def mape(self):
        self.train()
        preds = self.predict()
        score = 0
        for count, pred in enumerate(preds, start=0):
            score += abs(pred - self.y[count])
        score /= len(self.y)
        return score

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--feat_vec', required=True, help='feature vectors created using preprocess')
    ap.add_argument('--stock', required=True, help='stock values')
    ap.add_argument('--company', required=True)
    args = ap.parse_args()

    model = LinearModel(args.feat_vec, args.stock, args.company)
    print("MAPE SCORE: ", model.mape())

    return 0

if __name__ == "__main__":
    main()
