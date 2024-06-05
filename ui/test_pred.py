import streamlit as st

import pandas as pd
import seaborn as sns
import requests
import numpy as np
import matplotlib.pyplot as plt

def get_pred_goog():
    url_pred = 'https://lw-project-image-g4ikxb6kuq-ew.a.run.app/predict'
    json_obj =  requests.get(url_pred).json()['predict']
    forecast_recovered = pd.Series(json_obj['forecast'])
    forecast_recovered.index = pd.to_datetime(forecast_recovered.index, utc=True)
    forecast_recovered.index = forecast_recovered.index.tz_localize(None)

    confidence_int_upper = np.array(json_obj['confidence_int_upper'])
    confidence_int_lower = np.array(json_obj['confidence_int_lower'])

    train = pd.DataFrame(json_obj['train'])
    train.index = pd.to_datetime(train.index, utc=True)
    train.index = train.index.tz_localize(None)
    train.iloc[0, 0] = train.iloc[1, 0]

    test = pd.DataFrame(json_obj['test'])
    test.index = pd.to_datetime(test.index, utc=True)
    test.index = test.index.tz_localize(None)


    return forecast_recovered ,train, test, confidence_int_upper, confidence_int_lower

a, b, c, d, e = get_pred_goog()
# b.iloc[0,0] = b.iloc[1,0]

# a = pd.DataFrame(a).set_index(c.index)

# a = a[0]


def plot_forecast(fc, train, test, upper=None, lower=None):


    is_confidence_int = isinstance(upper, np.ndarray) and isinstance(lower, np.ndarray)

    # Prepare plot series
    fc_series = pd.Series(fc, index=test.index)
    lower_series = pd.Series(upper, index=test.index) if is_confidence_int else None
    upper_series = pd.Series(lower, index=test.index) if is_confidence_int else None

    # Plot
    fig, ax = plt.subplots(figsize=(10, 4), dpi=100)
    ax.plot(train, label='training', color='black')
    ax.plot(test, label='actual', color='black', ls='--')
    ax.plot(fc_series, label='forecast', color='orange')
    if is_confidence_int:
        ax.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.15)
    #ax.title('Forecast vs Actuals')
    ax.legend(loc='upper left', fontsize=8)
    return fig #st.pyplot()


plot_forecast(a,b,c,d,e)
