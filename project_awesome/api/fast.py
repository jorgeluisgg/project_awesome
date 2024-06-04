from fastapi import FastAPI
import yfinance as yf
import pandas as pd
import os

path = os.path.dirname(os.path.abspath(__file__))

# from project_awesome.interface.main import classification
companies = pd.read_csv(path + '/../../process_data/raw_data_FINAL_ALL.csv')
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
def classify(ticker: str = 'NVDA'):
    # stock = yf.Ticker(ticker)
    prediction = stockinfo.loc[ticker].mean()
    return {"classify":float(prediction)
        }
