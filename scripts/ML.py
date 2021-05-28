#!/usr/bin/env python

import sys
import logging
import time
import string
import datetime
import getopt
import random
import subprocess
import os

# Import Machine Leaning Libraries
import scipy
import numpy
import matplotlib
import pandas
import sklearn
import pickle

from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import Birch
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_blobs
from sklearn.svm import SVR

class ML:
    def __init__(self, i_raw_data, i_stock):
        self.stock = i_stock
        self.raw_data = i_raw_data

        # Define all models here
        self.models = []
        self.add_Models()

        self.train_Models()
        self.predict_Results()

    def predict_Results(self):
        x=1

    def train_Models(self):

        # Create different classifiers.
        C = 10
        classifiers = {
            'L1 logistic': LogisticRegression(C=C, penalty='l1',
                                              solver='saga',
                                              multi_class='multinomial',
                                              max_iter=10000),
            'L2 logistic (Multinomial)': LogisticRegression(C=C, penalty='l2',
                                                            solver='saga',
                                                            multi_class='multinomial',
                                                            max_iter=10000),
            'L2 logistic (OvR)': LogisticRegression(C=C, penalty='l2',
                                                    solver='saga',
                                                    multi_class='ovr',
                                                    max_iter=10000),
            'Linear SVC': SVC(kernel='linear', C=C, probability=True,
                              random_state=0),
        }

        df = pandas.read_csv(self.stock.file)
        days = list()
        adj_close_prices = list()

        # Get only the dates and adjusted close prices
        df_days = df.loc[:, 'Date']
        df_adj_close = df.loc[:, 'Adj Close']

        # Create the independent data set (dates)
        starting_date = df_days[0]
        starting_date = int(starting_date.split('-')[0] + starting_date.split('-')[1] + starting_date.split('-')[2])
        for day in df_days:
            days.append([int(day.split('-')[0] + day.split('-')[1] + day.split('-')[2]) - starting_date])
        # Create the dependent data set (adj close prices)
        for adj_close_price in df_adj_close:
            adj_close_prices.append(float(adj_close_price))

        X = numpy.array(days)
        y = adj_close_prices
        X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.05, random_state=1)
        classifiers[0].fit(X_train, Y_train)
        predictions = self.models[0][1].predict(X_validation)

        l_accuracy_scores = accuracy_score(Y_validation, predictions)
        l_confusion_matrix = confusion_matrix(Y_validation, predictions)
        l_classification_report = classification_report(Y_validation, predictions)


        print("Finished")

    def add_Models(self):
        self.models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
        self.models.append(('LDA', LinearDiscriminantAnalysis()))
        self.models.append(('KNN', KNeighborsClassifier()))
        self.models.append(('CART', DecisionTreeClassifier()))
        self.models.append(('NB', GaussianNB()))
        self.models.append(('SVM', SVC(gamma='auto')))
        self.models.append(('NBC', MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)))
        self.models.append(('RFC', RandomForestClassifier()))

