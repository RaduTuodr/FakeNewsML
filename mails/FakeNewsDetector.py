import os

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

if os.path.exists(DF_PATH):
    print("File exists!")
else:
    print("File has to be downloaded!")
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('saurabhshahane/fake-news-classification', path=REL_PATH, unzip=True)

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

train_prediction = model.predict(X_train_features)
accuracy_train = accuracy_score(y_train, train_prediction)

print('Accuracy score on train data: ', int(accuracy_train * 1000) / 10)

model.fit(X_test_features, y_test)

test_prediction = model.predict(X_test_features)
accuracy_test = accuracy_score(y_test, test_prediction)

print('Accuracy score on test data: ', int(accuracy_test * 1000) / 10)

message = ["Obama - I did a little blow when I was in high school. Nevertheless, I will continue to attack civilians in"
           " the Middle East and destabilize it as much as I possibly can throughout my mandate."]
message_features = feature_extraction.transform(message)
prediction = model.predict(message_features)

if prediction[0] == 0:
    print("SPAM")
else:
    print("AUTHENTIC")
