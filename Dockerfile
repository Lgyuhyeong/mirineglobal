FROM python:3.10.2
USER root

WORKDIR /Pyexam2

COPY Stock2.py /Pyexam2
COPY StockException.py /Pyexam2
COPY loggingExam.py /Pyexam2

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt