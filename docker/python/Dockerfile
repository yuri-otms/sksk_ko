FROM python:3.9.16

WORKDIR /sksk
ENV FLASK_APP=app

RUN apt-get update && apt-get install -y \
  mecab \
  mecab-ipadic-utf8 \
  libmecab-dev
RUN cp /etc/mecabrc /usr/local/etc/

COPY ./requirements.txt ./docker/

RUN pip install --upgrade pip
RUN pip install -r ./docker/requirements.txt

COPY handic-mecab-20230109_src.tar.gz /usr/src/handic/handic-mecab-20230109_src.tar.gz
RUN cd /usr/src/handic && \
    tar zxvf handic-mecab-20230109_src.tar.gz

RUN cd /usr/src/handic/handic-mecab-20230109_src && \
     ./configure --with-dicdir="/usr/src/dict/handic" && \
    make && \
    make install

