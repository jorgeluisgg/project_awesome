from fastapi import FastAPI
# from project_awesome.interface.main import classification

app = FastAPI()
# app.state = loadmodel_model()

@app.get("/")
def root():
    """
    Root endpoint that provides a welcome message and basic information.
    """
    return {
    'greeting': 'Hello suckers!'
    }


@app.get("/classify")
def classify(ticker: str = 'NPI'):
    return {"classify":
        f"Everything is shit! Just sell {ticker} already, take the money under your mattress and start buying farm animals and seeds"
        }
