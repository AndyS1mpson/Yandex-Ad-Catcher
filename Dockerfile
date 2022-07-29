#############
## BUILDER ##
#############
FROM mcr.microsoft.com/playwright/python:latest as builder

RUN apt update -y && \
    apt install python3-gdbm

COPY requirements.txt .
RUN pip install --user -r requirements.txt


################
## PRODUCTION ##
################
FROM mcr.microsoft.com/playwright/python:latest as prod

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH


COPY --from=builder /root/.local /root/.local

RUN  apt-get update -y && \
    apt-get -y install xvfb xserver-xephyr tigervnc-standalone-server x11-utils gnumeric

# install playwright for web scraping
RUN playwright install

WORKDIR /app
COPY ad_catcher/ .
