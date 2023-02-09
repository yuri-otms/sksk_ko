FROM python:alpine

# WORKDIR /app

# COPY ./app /app/

# RUN pip install Flask

# CMD ["python", "index.py"]

WORKDIR /sksk

COPY ./sksk /sksk/

RUN pip install Flask

CMD ["python", "server.py"]