import pandas as pd
import numpy as np
import matplotlib
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import pickle


def closed_groups(price):
    closed_groups=price.groupby('symbol')['close']
    closed_groups=closed_groups.transform(lambda x:x.shift(1) < x)
    price['prediction']=closed_groups *1
    removing_nan(price)


def removing_nan(price):
    price_data=price.dropna()
    predict_1(price_data)

def predict_1(price_data):
    X_col=price_data[['RSI', 'k_percent', 'will_r', 'MACD','price_rate_of_change']]
    Y_col=price_data[['prediction']]
    X_train, X_test, y_train, y_test = train_test_split(X_col, Y_col, random_state=0)
    print(X_test)
    rand_frst_clf = RandomForestClassifier(n_estimators=100, oob_score=True, criterion="gini", random_state=0)
    rand_frst_clf.fit(X_train, y_train)
    # y_pred = rand_frst_clf.predict(X_test)
    # target_names = ['Down Day', 'Up Day']
    #
    # # Build a classifcation report
    # report = classification_report(y_true=y_test, y_pred=y_pred, target_names=target_names, output_dict=True)
    #
    # # Add it to a data frame, transpose it for readability.
    # report_df = pd.DataFrame(report).transpose()
    pickle.dump(rand_frst_clf, open('rand_frst_clf.pkl', 'wb'))
    model = pickle.load(open('rand_frst_clf.pkl', 'rb'))

