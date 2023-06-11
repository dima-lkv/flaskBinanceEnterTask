import logging
import threading
import time
from datetime import datetime, timedelta
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import csv
import plotly.graph_objs as go
import plotly

scheduler = BlockingScheduler()


def get_market_cap_by_ticker(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}"
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning(f'Rate limit exceeded continue in 1 minute')
        time.sleep(60)
        get_market_cap_by_ticker(symbol)
        return
    data = response.json()
    try:
        circulating_supply = data['market_data']['circulating_supply']
        current_price = data['market_data']['current_price']['usd']
        return round((current_price * circulating_supply) / 1000000000, 5)
    except KeyError as e:
        logging.warning(f'{symbol} not found. {e}')
        raise e


def createPieChart():
    symbols = ['bitcoin', 'ethereum', 'solana', 'tether', 'tron', 'dogecoin', 'cardano', 'litecoin', 'polkadot',
               'uniswap']
    marker_cap_values = []
    for symbol in symbols:
        marker_cap_values.append(get_market_cap_by_ticker(symbol))

    fig = go.Figure(data=[go.Pie(labels=symbols, values=marker_cap_values)])
    plotly.offline.plot(fig, filename=f'templates/pieChart.html', auto_open=False)
    print(f'New pie chart successfully created | {datetime.now()}')


def createCandleStick(symbol, crypto_data):
    fig = go.Figure(data=[go.Candlestick(
        x=[data['Kline open time'] for data in crypto_data.values()],
        open=[data['Open price'] for data in crypto_data.values()],
        high=[data['High price'] for data in crypto_data.values()],
        low=[data['Low price'] for data in crypto_data.values()],
        close=[data['Close price'] for data in crypto_data.values()],
    )])
    plotly.offline.plot(fig, filename=f'templates/{symbol}cs.html', auto_open=False)
    print(f'New candle stick for {symbol} successfully created | {datetime.now()}')


def write_to_csv(symbol, data):
    try:
        with open(f'data/{symbol}.csv', 'a') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)
        print(f'{symbol} successfully wrote to csv. | {datetime.now()}')
    except Exception as e:
        raise e


def get_crypto_data(startTime, endTime, symbol, interval):
    response = requests.get(
        f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={startTime}&endTime={endTime}')
    if response.status_code != 200:
        print(response.json())
        return response.json()
    data = response.json()
    write_to_csv(symbol, data)

    crypto_data = {}
    for i in range(len(data)):
        crypto_data[i] = {
            'Kline open time': datetime.fromtimestamp(data[i][0] / 1000),
            'Open price': float(data[i][1]),
            'High price': float(data[i][2]),
            'Low price': float(data[i][3]),
            'Close price': float(data[i][4]),
            'Volume': float(data[i][5]),
            'Kline Close time': datetime.fromtimestamp(data[i][6] / 1000),
            'Quote asset volume': float(data[i][7]),
            'Number of trades': data[i][8],
            'Taker buy base asset volume': float(data[i][9]),
            'Taker buy quote asset volume': float(data[i][10]),
        }

    createCandleStick(symbol, crypto_data)


def add_task(interval_minutes, startTime, endTime, symbols_list, interval):
    try:
        for symbol in symbols_list:
            scheduler.add_job(get_crypto_data, args=[startTime, endTime, symbol, interval], trigger='interval',
                              minutes=interval_minutes)
            time.sleep(1)
        scheduler.start()
        return True
    except Exception as e:
        raise e


def start_collecting(minutes_interval, days=None, hours=None, minutes=None):
    symbols_list = ['BTCUSDT', 'ETHUSDT']
    startTime = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
    endTime = int((datetime.now()).timestamp() * 1000)
    crypto_interval = '4h'

    def time_up():
        print("Finished.")
        scheduler.shutdown()
        raise SystemExit

    if days or hours:
        time_limit = days * 24 * 60 * 60 if days else hours * 60 * 60
    else:
        time_limit = minutes * 60 if minutes else 60
    logging.warning(
        f'Process started for {time_limit / 60 / 60} hour with interval every {minutes_interval} minute:\n{datetime.now()}\n...')

    t = threading.Timer(time_limit, time_up)
    t.start()
    for symbol in symbols_list:
        get_crypto_data(startTime=startTime, endTime=endTime, symbol=symbol, interval=crypto_interval)
    # add_task(minutes_interval, startTime, endTime, symbols_list, crypto_interval)
    process1 = threading.Thread(target=add_task, args=[minutes_interval, startTime, endTime, symbols_list, crypto_interval])
    process2 = threading.Thread(target=createPieChart)

    process1.start()
    process2.start()

    process1.join()
    process2.join()


def main():
    start_collecting(minutes_interval=5, minutes=1)


if __name__ == '__main__':
    main()
