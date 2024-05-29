FROM python:3.10.6-buster

COPY requirements_api.txt /requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY project_awesome/api /project_awesome/api
# COPY model.joblib / model.joblib

CMD uvicorn project_awesome.api.fast:app --host 0.0.0.0
