from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def menu():
    return render_template('index.html')


@app.route('/pieChart')
def pie_chart():
    return render_template('pieChart.html')


@app.route('/candleStick/ETHUSDT/')
def candle_stick():
    return render_template('ETHUSDTcs.html')


@app.route('/candleStick/BTCUSDT/')
def candle_stick1():
    return render_template('BTCUSDTcs.html')


if __name__ == '__main__':
    app.run(debug=True)
