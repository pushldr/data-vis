FROM python:3.9.13-slim-buster

COPY ./dashboard.py /dashboard.py
COPY ./requirements.txt /requirements.txt
COPY ./world.csv /world.csv
COPY ./owid-covid-data.csv /owid-covid-data.csv


RUN pip install -r /requirements.txt

CMD ["python", "/dashboard.py"]