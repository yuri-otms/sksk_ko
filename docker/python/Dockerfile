FROM python:3.9.16

WORKDIR /sksk
ENV FLASK_APP=app

RUN apt-get update && apt-get install -y \
  mecab \
  mecab-ipadic-utf8 \
  openjdk-11-jdk


RUN cp /etc/mecabrc /usr/local/etc/

COPY ./requirements.txt ./docker/

RUN pip install --upgrade pip
RUN pip install -r ./docker/requirements.txt

