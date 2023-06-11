# Crypto Market Cap Visualization with Flask

This repository contains the codebase for a simple Flask application that fetches cryptocurrency data from the Binance and CoinGecko API and visualizes it.

## Features

* Fetch real-time cryptocurrency data from Binance and CoinGecko API.
* Calculate market cap for a list of cryptocurrencies.
* Visualize the market cap data with a pie chart using Plotly.
* Serve the visualization in a Flask web application.

## Getting Started

### Follow these steps to get the application running locally:

1. Clone the repository.
2. Install the necessary packages:
	`pip install -r requirements.txt`
3. Run the data collecting application:
	`python methods.py`
4. Run the Flask application:
	`python app.py`
5. Navigate to http://localhost:5000 in your browser to view the application.

## Default settings
By default, data will be collected for 1 hour every 5 minutes. However, you can change this in the methods.py file within the main function.

The default code example is as follows:
	`start_collecting(minutes_interval=5, hours=1)`

The minutes_interval variable is responsible for chart renewal, where a value of 5 means the charts will be renewed every 5 minutes.
The hours variable is a timer that determines how long data will be collected. You can change it to days or minutes.

For example:
	`start_collecting(minutes_interval=10, days=7)`
In this case, data collection will be continuous for 7 days, and the charts will be renewed every 10 minutes.

### app.py: 
The main application file. It sets up the Flask application and the routes for the different pages.
### methods.py: 
Contains the functions that are used to collect and process data from the CoinGecko and Binance API.
### HTML files: 
These are the templates rendered by the Flask application. They include index.html for the main page, pie_chart.html for the market cap pie chart, and ETHUSDTcs.html and BTCUSDTcs.html for the candlestick charts.

## How It Works

The application uses the CoinGecko API to collect real-time data about the market capitalizations of selected cryptocurrencies, and then uses this data to create a pie chart visualization. It also uses the Binance API to get real-time candlestick data for Bitcoin and Ethereum and uses Plotly to create the visualizations.

On startup, the application begins collecting data from the CoinGecko API. The data is refreshed every minute to ensure that the visualizations stay up-to-date.

### The application provides three main routes:

* `'/'`: This route displays the main page of the application with menu and list with market capitalizations of selected cryptocurrencies.
* `'/MCpieChart'`: This route displays a pie chart visualization of the market capitalizations of selected cryptocurrencies.
* `'/candleStick/ETHUSDT/'` and '/candleStick/BTCUSDT/': These routes display candlestick chart visualizations for Ethereum and Bitcoin, respectively.
