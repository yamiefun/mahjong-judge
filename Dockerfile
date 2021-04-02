FROM python:3.9-buster

RUN mkdir mahjong
COPY . /mahjong
RUN pip install -r /mahjong/requirements.txt

WORKDIR /mahjong
