# Bitcoin Dashboard – Real-Time Scraping & Visualization

This project is a real-time dashboard that displays the current price of Bitcoin using data scraped from CoinDesk: https://www.coindesk.com/price/bitcoin

Built with:
- Python
- Dash (Plotly)
- Web scraping (via curl in a Bash script)
- Pandas + Plotly for data processing and visualization

---

## Features

- Real-time Bitcoin price graph (1H / 24H / 7D)
- Summary of key indicators: Open, High, Low, Close
- Daily report (generated at 8 PM): volatility, evolution, and key prices
- Clean and responsive user interface
- Cross-platform (Windows, macOS, Linux)

---

## 🛠️ How It Works

1. Scraping: The `scraping.sh` script fetches the current BTC price from CoinDesk and appends it to `prices.csv`.
2. Dashboard: The `dashboard.py` file loads this CSV and displays the data through interactive graphs and components using Dash.
3. Automatic updates: The scraping script can be scheduled to run every 5 minutes using cron (Linux/Mac) or Task Scheduler (Windows).

---

## Authors

Project created by:
- Lyne Naccache
- Dylan Masson

---

## Project Structure

Python-Git-Linux-Project-MASSON-Dylan-Lyne-NACCACHE/
├── dashboard.py         → Dash app (frontend + logic)  
├── scraping.sh          → Shell script for scraping BTC price  
├── prices.csv           → Collected price data  
├── debug_coindesk.html  → Raw HTML from scraping (for debug)  
├── logfile.log          → Log file (optional)  
└── README.md            → This file
