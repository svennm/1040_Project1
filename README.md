# Trading System Platform

This repository implements a modular trading platform built around **MetaTrader 5** (MT5) on a headless Linux server.  It is designed to run a complete trading workflow from data collection and signal generation through to evaluation and logging.  The system emphasises correlation‑based breakout and trend following strategies across multiple asset classes.

## Overview

The platform comprises several components:

* **Data Collection** – Uses the official `MetaTrader5` Python API to connect to an MT5 terminal and download tick and bar data for foreign exchange pairs (majors), equity indices (S&P 500 and NAS100) and commodities (gold).  It can compute correlations across different time frames (1 hour, 4 hours, 1 day, 10 days and 30 days) and exports time series for further analysis and charting.

* **Spread Recorder** – Continuously records the spread (difference between ask and bid) for each instrument, storing averages and monitoring when spreads widen.  Logs are rotated daily so they can be inspected later.

* **Signal Generation** – Implements a suite of trading strategies:
  * **Time‑Range Breakout** – For a specified time window [t₀, t₁], it measures the high and low and places limit orders above and below once t₁ has elapsed.  If one order triggers the other is cancelled.  The module can evaluate the correlation of the resulting P&L across multiple instruments (e.g. GBPUSD buy vs USDJPY buy).
  * **Correlation‑Based Trend Following** – Calculates correlations between instruments over multiple look‑back horizons and biases signals toward assets with aligned momentum.  It can scale from two up to five correlated instruments.
  * **Daily “Peg” Strategy** – A simple daily strategy that buys an asset at the start of the day (after spreads settle) and sells at the end of the day (before spreads widen).  This is useful for instruments that tend to exhibit mean‑reversion over the trading day.

* **Signal Processor and Evaluation** – Maintains a history of past trades and signals, then uses Bayesian logic to estimate the expected reward‑to‑risk (RR) ratio for long and short positions.  Rather than making hard directional predictions, it produces two evaluation bars: one showing expected RR for an eight‑hour horizon and another for a seven‑day horizon.  Strategies can then “bet” only when the asymmetry of expected outcomes is favourable.

* **Messaging System** – A simple in‑process message bus that stores generated signals and makes them available to downstream components.  It can easily be extended to integrate with messaging platforms such as Slack or email.

The code is structured as a collection of Python modules in the `src` directory.  Each module has docstrings describing its purpose and how it should be used.

## Installation

The recommended way to run this project is inside a Docker container.  The provided `Dockerfile` builds a headless Ubuntu environment, installs Python and the required packages, and sets up the MT5 API.  You will need to supply your MT5 terminal path and account credentials via environment variables or a configuration file (see `src/main.py`).

### Prerequisites

* **MetaTrader 5 Terminal** – Download the MT5 terminal for Linux (via Wine) or Windows.  On Linux the terminal should be installed in a directory accessible to the container.  On Windows you can mount the installation into the container.
* **Broker Credentials** – An MT5 login, password and server name from your broker.  These credentials are needed to initialise the MT5 API.

### Build and Run

1. **Build the Docker image**

   ```bash
   docker build -t trading-system .
   ```

2. **Run the container**

   When running the container you must mount the directory containing your MT5 terminal and pass configuration via environment variables or a configuration file.  For example:

   ```bash
   docker run \
     -e MT5_PATH=/terminal/mt5/terminal64.exe \
     -e MT5_LOGIN=12345678 \
     -e MT5_PASSWORD=YourPassword \
     -e MT5_SERVER=Broker-Server \
     -v /path/to/mt5:/terminal/mt5:ro \
     trading-system
   ```

   The container will start the trading platform and begin collecting data, generating signals and logging spreads.  Logs are written to standard output and saved under `/app/logs` within the container.

## Directory Structure

```
repo/
├── Dockerfile          # Build definition for the trading environment
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── src/                # Source code for the trading platform
│   ├── __init__.py
│   ├── main.py         # Entry point – wires together all modules
│   ├── data_collector.py  # Data download and correlation utilities
│   ├── spread_recorder.py  # Spread logger
│   ├── signal_generator.py # Strategy implementations
│   ├── signal_processor.py # Bayesian evaluation and memory
│   ├── messaging.py        # In‑memory messaging / signalling
│   ├── evaluation.py       # Evaluation bar plotting
│   └── utils.py           # Helper functions
└── logs/                # Runtime logs (created at runtime)
```

## Disclaimer

This code is provided for educational purposes only.  It does **not** constitute financial advice or a recommendation to trade.  Trading involves risk and you should consult a qualified professional before placing trades.  Use this software at your own risk; the authors assume no liability for any losses incurred.
