import streamlit as st

import pandas as pd
import seaborn as sns
import requests
import numpy as np
import matplotlib.pyplot as plt

def get_pred_goog():
    url_pred = 'https://lw-project-image-g4ikxb6kuq-ew.a.run.app/predict'
    response_pred = requests.get(url_pred, params='GOOG').json()
    json_obj = response_pred['predict']
    df_forecast = pd.DataFrame.from_dict(response_pred['predict']['forecast'], orient='index')

    confidence_int_upper = np.array(json_obj['confidence_int_upper'])
    confidence_int_lower = np.array(json_obj['confidence_int_lower'])

    train = pd.DataFrame(json_obj['train'])
    df_train = pd.to_datetime(train.index)

    test = pd.DataFrame(json_obj['test'])
    df_test = pd.to_datetime(test.index)

    return df_forecast,df_train, df_test, confidence_int_upper, confidence_int_lower


a, b, c, d, e = get_pred_goog()

def plot_forecast(fc, train, test, upper=None, lower=None):
    is_confidence_int = isinstance(upper, np.ndarray) and isinstance(lower, np.ndarray)
    # Prepare plot series
    fc_series = pd.Series(fc, index=test.index)
    lower_series = pd.Series(upper, index=test.index) if is_confidence_int else None
    upper_series = pd.Series(lower, index=test.index) if is_confidence_int else None

    # Plot
    plt.figure(figsize=(10,4), dpi=100)
    plt.plot(train, label='training', color='black')
    plt.plot(test, label='actual', color='black', ls='--')
    plt.plot(fc_series, label='forecast', color='orange')
    if is_confidence_int:
        plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.15)
    plt.title('Forecast vs Actuals')
    plt.legend(loc='upper left', fontsize=8)

breakpoint()
