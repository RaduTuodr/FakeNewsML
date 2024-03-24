import os
from typing import List

import numpy as np
import pandas as pd

from kaggle.api.kaggle_api_extended import KaggleApi

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


RAND_SEED = 1502
REL_PATH = 'D:\\'
DF_PATH = REL_PATH + 'WELFake_Dataset.csv'


def init_process():
    if os.path.exists(DF_PATH):
        print("File exists!")
    else:
        print("File has to be downloaded!")
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files('saurabhshahane/fake-news-classification', path=REL_PATH, unzip=True)


def train_model():
    df = pd.read_csv(DF_PATH)
    data = df.loc[df.notnull().all(axis=1)]

    data.loc[:, 'text'] = data['title'] + ' ' + data['text']

    data = data.dropna(subset=['text', 'title'], inplace=False)

    X = data['text']
    y = data['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.2,
                                                        random_state=RAND_SEED)

    feature_extraction = TfidfVectorizer(min_df=1, stop_words='english')

    X_train_features = feature_extraction.fit_transform(X_train)
    X_test_features = feature_extraction.fit_transform(X_test)

    y_train = y_train.astype('int')
    y_test = y_test.astype('int')

    model = LogisticRegression()
    model.fit(X_train_features, y_train)
    model.fit(X_test_features, y_test)

    model_info = {
        'model': model,
        'feature_extraction': feature_extraction,
        # 'X_train': X_train_features,
        # 'X_test': X_test_features,
        # 'y_train': y_train,
        # 'y_test': y_test
    }

    return model_info


def test_accuracy(model: LogisticRegression,
                  X_train_features,
                  y_train,
                  X_test_features,
                  y_test):

    model.fit(X_train_features, y_train)

    train_prediction = model.predict(X_train_features)
    accuracy_train = accuracy_score(y_train, train_prediction)

    print('Accuracy score on train data: ', int(accuracy_train * 1000) / 10)

    model.fit(X_test_features, y_test)

    test_prediction = model.predict(X_test_features)
    accuracy_test = accuracy_score(y_test, test_prediction)

    print('Accuracy score on test data: ', int(accuracy_test * 1000) / 10)


def message_predict(model: LogisticRegression, feature_extraction, message: str):

    message = [message]  # transforming string into something iterable

    message_features = feature_extraction.transform(message)
    prediction = model.predict(message_features)

    return prediction[0]


def getMessages(messages: List[str]):

    init_process()
    model_info = train_model()

    # test_accuracy(model_info['model'],
    #               model_info['X_train'],
    #               model_info['X_test'],
    #               model_info['y_train'],
    #               model_info['y_test'])

    predictions = []
    for message in messages:

        prediction = message_predict(model_info['model'],
                                     model_info['feature_extraction'],
                                     message)

        predictions.append(prediction)

    results = {
        'messages': messages,
        'predictions': predictions
    }

    return results
