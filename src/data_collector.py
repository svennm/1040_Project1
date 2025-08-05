"""Data collection utilities for MetaTrader 5.

The :mod:`data_collector` module provides functions and classes for connecting to
the MetaTrader 5 (MT5) terminal, downloading tick and bar data, and computing
correlations across multiple instruments and timeframes.  It uses the
`MetaTrader5` Python package (provided by MetaQuotes) under the hood.  A
running MT5 terminal is required; when running inside Docker the terminal
should be mounted into the container and configured via environment variables.

Example usage::

    from datetime import datetime, timedelta
    from data_collector import DataCollector

    collector = DataCollector(
        mt5_path="/terminal/mt5/terminal64.exe",
        login=12345678,
        password="password",
        server="Broker-Server"
    )
    collector.connect()

    # Fetch the last 1000 ticks for EURUSD
    df_ticks = collector.get_tick_data("EURUSD", n_ticks=1000)

    # Fetch 100 H1 bars for EURUSD
    now = datetime.utcnow()
    df_bars = collector.get_bar_data("EURUSD", timeframe="H1", start=now - timedelta(days=5), end=now)

    # Compute correlations across symbols and time windows
    symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
    timeframes = ["H1", "H4", "D1"]
    corr = collector.compute_correlations(symbols, timeframes, window_size=100)
    print(corr)

"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

try:
    import MetaTrader5 as mt5
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "MetaTrader5 package is required. Install via pip install MetaTrader5 and "
        "ensure that a MetaTrader 5 terminal is available."
    ) from exc


class DataCollector:
    """High‑level interface for collecting and analysing market data from MT5.

    Parameters
    ----------
    mt5_path : str
        Path to the MT5 terminal executable.  This is required on first
        connection and must match the installed terminal location.
    login : int
        Trading account login ID.
    password : str
        Trading account password.
    server : str
        Name of the broker server (e.g. ``"MetaQuotes-Demo"``).
    logger : Optional[logging.Logger]
        Optional logger instance.  If not provided, a module‑level logger is used.

    Notes
    -----
    The connection will not be established until :meth:`connect` is called.  The
    MT5 terminal must be running; on Linux this typically means running the
    terminal under Wine or using the official `.terminal64.exe` binary.  For
    headless environments, you may need to run the terminal under an `xvfb`
    virtual display.
    """

    def __init__(
        self,
        mt5_path: str,
        login: int,
        password: str,
        server: str,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.mt5_path = mt5_path
        self.login = login
        self.password = password
        self.server = server
        self.logger = logger or logging.getLogger(__name__)
        self._connected = False

    def connect(self) -> None:
        """Initialise the MT5 terminal and log in.

        Raises
        ------
        RuntimeError
            If the connection fails (e.g., invalid credentials or terminal
            cannot be initialised).
        """
        self.logger.debug(
            "Initialising MT5 terminal at %s with login %s on server %s", self.mt5_path, self.login, self.server
        )
        if not mt5.initialize(path=self.mt5_path, login=self.login, password=self.password, server=self.server):
            error_code = mt5.last_error()
            raise RuntimeError(f"Failed to initialise MT5: {error_code}")
        self._connected = True
        self.logger.info("Connected to MT5 server %s as %s", self.server, self.login)

    def shutdown(self) -> None:
        """Shutdown the MT5 terminal connection."""
        if self._connected:
            mt5.shutdown()
            self._connected = False
            self.logger.info("MT5 connection closed")

    def get_tick_data(self, symbol: str, n_ticks: int = 1000) -> pd.DataFrame:
        """Retrieve the most recent tick data for a symbol.

        Parameters
        ----------
        symbol : str
            Instrument symbol (e.g. ``"EURUSD"``).
        n_ticks : int, optional
            Number of ticks to retrieve.  The default is 1000.

        Returns
        -------
        pandas.DataFrame
            DataFrame with columns ``['time', 'bid', 'ask', 'last', 'volume']``.
        """
        if not self._connected:
            raise RuntimeError("MT5 not connected; call connect() first")
        self.logger.debug("Requesting last %s ticks for %s", n_ticks, symbol)
        ticks = mt5.copy_ticks_from(symbol, datetime.utcnow() - timedelta(days=1), n_ticks)
        df = pd.DataFrame(ticks)
        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def get_bar_data(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> pd.DataFrame:
        """Retrieve bar (OHLC) data for a symbol over a date range.

        Parameters
        ----------
        symbol : str
            Instrument symbol.
        timeframe : str
            Timeframe name (``"M1"``, ``"H1"``, ``"H4"``, ``"D1"`` etc.).  See
            :class:`MetaTrader5.TIMEFRAME_M1` for available constants.
        start : datetime
            Start of the period (UTC).
        end : datetime
            End of the period (UTC).

        Returns
        -------
        pandas.DataFrame
            DataFrame with columns ``['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']``.
        """
        if not self._connected:
            raise RuntimeError("MT5 not connected; call connect() first")
        timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1,
        }
        if timeframe not in timeframe_map:
            raise ValueError(f"Unknown timeframe: {timeframe}")
        tf = timeframe_map[timeframe]
        self.logger.debug("Requesting bars for %s: %s to %s, timeframe %s", symbol, start, end, timeframe)
        rates = mt5.copy_rates_range(symbol, tf, start, end)
        df = pd.DataFrame(rates)
        if not df.empty:
            df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def compute_correlations(
        self,
        symbols: Sequence[str],
        timeframes: Sequence[str],
        window_size: int = 100,
    ) -> pd.DataFrame:
        """Compute pairwise correlations across symbols and timeframes.

        For each timeframe in ``timeframes`` this method downloads the last
        ``window_size`` bars for each symbol in ``symbols`` and computes the
        correlation matrix of closing prices.  The result is a multi‑index
        DataFrame indexed by timeframe and symbol.

        Parameters
        ----------
        symbols : sequence of str
            List of instrument symbols.
        timeframes : sequence of str
            List of timeframe names (e.g. ``["H1", "H4", "D1"]``).
        window_size : int, optional
            Number of bars to include when computing correlations.  Defaults
            to 100.

        Returns
        -------
        pandas.DataFrame
            A DataFrame whose rows are a MultiIndex ``(timeframe, symbol)`` and
            columns are the other symbols.  Each row contains correlation
            coefficients between the closing price of ``symbol`` and all
            other symbols on the given timeframe.
        """
        records: List[pd.DataFrame] = []
        now = datetime.utcnow()
        lookback = now - timedelta(days=30)  # a default range to fetch bars
        for tf in timeframes:
            closes: Dict[str, pd.Series] = {}
            for sym in symbols:
                bars = self.get_bar_data(sym, timeframe=tf, start=lookback, end=now)
                if len(bars) < window_size:
                    self.logger.warning(
                        "Not enough bars (%s) for %s on timeframe %s; correlations may be unreliable",
                        len(bars), sym, tf,
                    )
                closes[sym] = bars['close'].tail(window_size).reset_index(drop=True)
            # Build DataFrame and compute correlations
            df_closes = pd.DataFrame(closes)
            corr = df_closes.corr()
            # Flatten into long format
            corr['timeframe'] = tf
            corr = corr.set_index('timeframe', append=True).stack().unstack(level=0)
            # corr now has multiindex (symbol, timeframe) and columns other symbols
            records.append(corr)
        result = pd.concat(records)
        result.index.names = ['symbol', 'timeframe']
        return result
