#페이스 이미지 명시
FROM python:3.10.2
USER root

WORKDIR /Pyexam2

COPY Stock2.py /Pyexam2
COPY StockException.py /Pyexam2
COPY loggingExam.py /Pyexam2
COPY requirements.txt /Pyexam2

#버전에 대한 정보 업데이트 / 최신 버전으로 패키지 수정
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y
#글자깨짐 방지
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8


RUN pip install kaleido
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip install lxml