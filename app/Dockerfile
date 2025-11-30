FROM python:3.12

WORKDIR /workspace
ENV FLASK_APP=app
ENV MECABRC=/usr/local/etc/mecabrc
ENV PYTHONPATH=/workspace/app


RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    mecab \
    mecab-ipadic-utf8 \
    libmecab-dev \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

RUN cp /etc/mecabrc /usr/local/etc/ || true

COPY ./app/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./app/handic-mecab-20230109_src.tar.gz /usr/src/handic/handic-mecab.tar.gz
RUN mkdir -p /usr/src/handic && \
    cd /usr/src/handic && \
    tar zxvf handic-mecab.tar.gz

RUN cd /usr/src/handic/handic-mecab-20230109_src && \
    ./configure --with-dicdir="/usr/src/dict/handic" && \
    make && make install || true


WORKDIR /workspace