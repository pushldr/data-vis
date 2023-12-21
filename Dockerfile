FROM python:3.9.13-slim-buster

COPY ./app.py /app.py
COPY ./requirements.txt /requirements.txt
COPY ./world.csv /world.csv
COPY ./owid-covid-data.csv /owid-covid-data.csv

EXPOSE 8050

RUN pip install -r /requirements.txt

CMD ["python", "/app.py"]