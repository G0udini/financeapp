# Finance Application

### At start you have fake 10.000$. Use an application that take real prices information from stock market and see if you can make money on it

___

## Build & Run

### requirements

* docker
* .env file in root directory with following rules:

```shell
SECRET_KEY=
DEBUG=True

API_KEY= #you need to get it from Finnhub to connect to their api

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

Use **docker-compose up --build** command to run app in docker

## Description

This app was made to:

1. Learn how to trade(buy/sell stocks, observer price change) because api provides real time prices
2. Try it without threat to your real money

**stocklist** - to find interesting meta stock info
**stocklist/APPL** - to get info about company and current price or price dynamics for the year / or to buy and sell companies stocks
**profile** - to get information about your current portfolio and operation history
