from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

path = os.path.dirname(os.path.abspath(__file__))

# from project_awesome.interface.main import classification
companies = pd.read_csv(path + '/../../process_data/data_FINAL_ALL.csv')

companies.set_index('Ticker',inplace = True)
search_text = 'sp500'
stockinfo = companies.loc[:, companies.columns.str.contains(search_text)]

app = FastAPI()
# app.state = loadmodel_model()

@app.get("/")
def root():
    """
    Root endpoint that provides a welcome message and basic information.
    """
    return {
    'greeting': 'Hello friends!'
    }

@app.get("/classify")
def classify(ticker: str = 'GOOG'):
    # stock = yf.Ticker(ticker)
    prediction = stockinfo.loc[ticker].mean()
    return {"classify":float(prediction)
        }

@app.get("/predict")
def prediction(ticker: str = 'GOOG'):
    tmp_df = pd.read_csv(path + "/../../process_data/Google_data_time_series.csv", index_col="Date")

    train_size = 0.8
    index = round(train_size*tmp_df.shape[0])

    df_train = tmp_df.iloc[:index]
    df_test = tmp_df.iloc[index:]

    arima = ARIMA(df_train, order=(0, 1, 0), trend='t')
    arima = arima.fit()

    forecast = arima.forecast(len(df_test), alpha=0.05)  # 95% confidence

    # Forecast values and confidence intervals
    forecast_results = arima.get_forecast(len(df_test), alpha=0.05)
    forecast = forecast_results.predicted_mean
    confidence_int = forecast_results.conf_int().values

    forecast_df = pd.DataFrame(forecast).set_index(df_test.index)
    forecast_df = forecast_df["predicted_mean"]

    new_df = df_train.fillna('')
    json_obj = {
    'forecast': forecast_df.to_dict(),
    'confidence_int_upper': confidence_int[:,0].tolist(),
    'confidence_int_lower': confidence_int[:,1].tolist(),
    'train': new_df.to_dict(),
    'test': df_test.to_dict()
    }

    return {"predict": json_obj}
