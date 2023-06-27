FROM python:3.9.16

WORKDIR /sksk
ENV FLASK_APP=app

COPY ./requirements.txt ./docker/

RUN pip install --upgrade pip
RUN pip install -r ./docker/requirements.txt