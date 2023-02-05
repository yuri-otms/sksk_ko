FROM python:alpine

# WORKDIR /app

# COPY ./app /app/

# RUN pip install Flask

# CMD ["python", "index.py"]

WORKDIR /sksk_ko

COPY ./sksk_ko /sksk_ko/

RUN pip install Flask

CMD ["python", "server.py"]