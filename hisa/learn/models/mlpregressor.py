from __future__ import absolute_import

from sklearn import neural_network
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import argparse
from sklearn.metrics import accuracy_score

class MLPModel():
    def __init__(self, filename, stock_filename, company, activation='logistic',
                    solver='lbfgs', alpha=0.01):
        self.df = pd.read_csv(filename)
        stock = pd.read_csv(stock_filename)
        dates = [int(pd.to_datetime(date).strftime("%s")) for date in self.df['date']]
        self.x = np.asarray([dates, self.df['neg'], self.df['pos'], self.df['neu']], dtype=float).T
        self.y = np.asarray(stock[company + '_open'])
        self.activation = activation
        self.solver = solver
        self.alpha = alpha
        self.model = neural_network.MLPRegressor(hidden_layer_sizes=(500,),
                                                 activation=self.activation,
                                                 solver=self.solver,
                                                 alpha=self.alpha)

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

    model = MLPModel(args.feat_vec, args.stock, args.company)
    print("MAPE SCORE: ", model.mape())

    return 0

if __name__ == "__main__":
    main()
