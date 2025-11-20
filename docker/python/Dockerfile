FROM python:3.12

WORKDIR /app
ENV FLASK_APP=app
ENV MECABRC=/usr/local/etc/mecabrc


RUN apt-get update && apt-get install -y \
  mecab \
  mecab-ipadic-utf8 \
  libmecab-dev \
  curl \
  tar \
  && rm -rf /var/lib/apt/lists/*

RUN cp /etc/mecabrc /usr/local/etc/

COPY docker/python/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY docker/python/handic-mecab-20230109_src.tar.gz /usr/src/handic/handic-mecab-20230109_src.tar.gz
RUN cd /usr/src/handic && \
    tar zxvf handic-mecab-20230109_src.tar.gz

RUN cd /usr/src/handic/handic-mecab-20230109_src && \
     ./configure --with-dicdir="/usr/src/dict/handic" && \
    make && \
    make install

COPY sksk_app /app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]