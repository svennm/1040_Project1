"""Trading signal generation strategies.

The :mod:`signal_generator` module contains functions and classes for
constructing trading signals based on various strategies including
time‑range breakouts, correlation‑based momentum and trend following, and
a simple daily “peg” strategy.  All strategies return :class:`Signal`
instances which encapsulate the recommended action and metadata.

The strategies are designed to operate on data provided by
``DataCollector``.  They are intentionally written to be stateless; any
stateful memory or history should be maintained by the calling
application or by the :mod:`signal_processor` module.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from data_collector import DataCollector
from utils import compute_series_correlation


@dataclass
class Signal:
    """Representation of a trading signal.

    Attributes
    ----------
    symbol : str
        The instrument symbol.
    direction : str
        Either ``"long"`` or ``"short"``.
    entry_price : float
        Suggested entry price for the trade.
    stop_price : Optional[float]
        Optional stop‑loss price.  If ``None`` the caller must set a default.
    take_profit : Optional[float]
        Optional take‑profit price.  If ``None`` the caller must set a default.
    strategy : str
        Name of the strategy that generated the signal.
    metadata : Dict[str, object]
        Additional information (e.g. correlation values) that can be used by the
        signal processor.
    timestamp : datetime
        Time when the signal was generated.
    """

    symbol: str
    direction: str
    entry_price: float
    stop_price: Optional[float]
    take_profit: Optional[float]
    strategy: str
    metadata: Dict[str, object] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)


class SignalGenerator:
    """Collection of trading strategies.

    Parameters
    ----------
    collector : DataCollector
        Data collector used to fetch price data.
    logger : Optional[logging.Logger]
        Logger for diagnostics.  If omitted the module logger is used.
    """

    def __init__(self, collector: DataCollector, logger: Optional[logging.Logger] = None) -> None:
        self.collector = collector
        self.logger = logger or logging.getLogger(__name__)

    # ---------------------------------------------------------------------
    # Time‑range breakout strategy
    # ---------------------------------------------------------------------
    def time_range_breakout(
        self,
        symbol: str,
        start_time: datetime,
        end_time: datetime,
        buffer: float = 0.0001,
    ) -> Optional[Tuple[Signal, Signal]]:
        """Generate long/short breakout signals for a time window.

        This strategy observes price action between ``start_time`` and
        ``end_time`` (UTC).  After ``end_time`` has passed, it determines the
        highest high and lowest low within the window.  It then proposes two
        limit orders: a long entry slightly above the high (using ``buffer``)
        and a short entry slightly below the low.  The first order to trigger
        cancels the other.  If there is insufficient data to determine high
        and low, returns ``None``.

        Parameters
        ----------
        symbol : str
            Instrument symbol.
        start_time : datetime
            Start of the observation window (UTC).
        end_time : datetime
            End of the observation window (UTC).  Signals are only valid
            after this time.
        buffer : float, optional
            Additional price distance to add/subtract from the high/low when
            placing limit orders.  Defaults to ``0.0001``.

        Returns
        -------
        Optional[Tuple[Signal, Signal]]
            A tuple containing the long and short signals, or ``None`` if
            insufficient data.
        """
        now = datetime.utcnow()
        if now < end_time:
            # Not time to generate signals yet
            self.logger.debug("Breakout window for %s has not ended (now=%s, end=%s)", symbol, now, end_time)
            return None
        # Fetch bar data for the window; using M1 bars for granularity
        bars = self.collector.get_bar_data(symbol, timeframe="M1", start=start_time, end=end_time)
        if bars.empty:
            self.logger.warning("No bars found for %s between %s and %s", symbol, start_time, end_time)
            return None
        high = bars['high'].max()
        low = bars['low'].min()
        long_entry = high + buffer
        short_entry = low - buffer
        long_signal = Signal(
            symbol=symbol,
            direction="long",
            entry_price=float(long_entry),
            stop_price=None,
            take_profit=None,
            strategy="time_range_breakout",
            metadata={"window_start": start_time, "window_end": end_time, "high": float(high), "low": float(low)},
        )
        short_signal = Signal(
            symbol=symbol,
            direction="short",
            entry_price=float(short_entry),
            stop_price=None,
            take_profit=None,
            strategy="time_range_breakout",
            metadata={"window_start": start_time, "window_end": end_time, "high": float(high), "low": float(low)},
        )
        return long_signal, short_signal

    # ---------------------------------------------------------------------
    # Correlation‑based momentum/trend following
    # ---------------------------------------------------------------------
    def correlation_momentum(
        self,
        symbols: Sequence[str],
        timeframes: Sequence[str],
        correlation_threshold: float = 0.7,
        window_size: int = 100,
    ) -> List[Signal]:
        """Generate momentum signals based on correlation.

        For each instrument in ``symbols`` this function computes the
        correlation of its closing prices with those of the other instruments
        over the provided ``timeframes`` and a sliding window of length
        ``window_size``.  Instruments whose average correlation with the group
        exceeds ``correlation_threshold`` are considered aligned; for those
        instruments, a simple momentum signal is generated: go long if the
        latest closing price is above its moving average, or short if below.

        The caller must ensure that all instruments have enough historical
        data.  The function returns a list of :class:`Signal` objects.

        Parameters
        ----------
        symbols : sequence of str
            List of instruments to analyse.
        timeframes : sequence of str
            Timeframes for correlation calculation (e.g. ``["H1", "H4"]``).
        correlation_threshold : float, optional
            Minimum average correlation required to trigger a signal.  Default is
            0.7.
        window_size : int, optional
            Number of bars used in moving average calculations.  Default is 100.

        Returns
        -------
        list of Signal
            Generated signals for instruments with sufficiently high correlation.
        """
        corr_matrix = self.collector.compute_correlations(symbols, timeframes, window_size)
        signals: List[Signal] = []
        # For each symbol compute average correlation across timeframes
        for sym in symbols:
            # Extract rows for this symbol; index is (symbol, timeframe)
            rows = corr_matrix.loc[(sym, slice(None))]
            # Compute mean correlation excluding self (diagonal)
            # We'll drop the column equal to symbol then mean across rows and columns
            avg_corr = rows.drop(columns=sym).mean().mean()
            self.logger.debug("Average correlation for %s across %s: %.3f", sym, timeframes, avg_corr)
            if avg_corr < correlation_threshold:
                continue
            # Determine momentum direction using D1 bars
            now = datetime.utcnow()
            bars = self.collector.get_bar_data(sym, timeframe="D1", start=now - timedelta(days=window_size), end=now)
            if len(bars) < window_size:
                self.logger.warning("Not enough daily bars to compute momentum for %s", sym)
                continue
            closes = bars['close']
            ma = closes.rolling(window=window_size).mean().iloc[-1]
            latest_close = closes.iloc[-1]
            direction = "long" if latest_close > ma else "short"
            signals.append(
                Signal(
                    symbol=sym,
                    direction=direction,
                    entry_price=float(latest_close),
                    stop_price=None,
                    take_profit=None,
                    strategy="correlation_momentum",
                    metadata={"avg_correlation": float(avg_corr), "moving_average": float(ma)},
                )
            )
        return signals

    # ---------------------------------------------------------------------
    # Peg (daily buy and sell) strategy
    # ---------------------------------------------------------------------
    def daily_peg(
        self,
        symbol: str,
        settle_hour: int = 1,
        exit_hour: int = 22,
    ) -> Optional[Tuple[Signal, Signal]]:
        """Generate buy and sell signals for a daily “peg” strategy.

        This strategy aims to capture intraday mean‑reversion by buying at
        ``settle_hour`` (UTC) once spreads have typically narrowed after
        rollover, and selling at ``exit_hour`` (UTC) before spreads widen in
        anticipation of the close.  Two signals are produced: one at the
        entry and one at the exit.  The exit signal uses the ``entry_price``
        as metadata to allow the signal processor to compute P&L.

        Parameters
        ----------
        symbol : str
            Instrument symbol.
        settle_hour : int, optional
            Hour of day (0–23) to enter the market.  Default is 1 UTC.
        exit_hour : int, optional
            Hour of day (0–23) to exit the market.  Default is 22 UTC.

        Returns
        -------
        Optional[Tuple[Signal, Signal]]
            Entry and exit signals, or ``None`` if the current time is not
            within the entry or exit window.
        """
        now = datetime.utcnow()
        if now.hour == settle_hour and 0 <= now.minute < 5:
            # At settlement time; buy
            # Use the latest price as entry
            ticks = self.collector.get_tick_data(symbol, n_ticks=1)
            if ticks.empty:
                return None
            price = float(ticks.iloc[-1]['ask'])
            entry_signal = Signal(
                symbol=symbol,
                direction="long",
                entry_price=price,
                stop_price=None,
                take_profit=None,
                strategy="daily_peg",
                metadata={},
            )
            return entry_signal, None
        elif now.hour == exit_hour and 0 <= now.minute < 5:
            # At exit time; sell
            ticks = self.collector.get_tick_data(symbol, n_ticks=1)
            if ticks.empty:
                return None
            price = float(ticks.iloc[-1]['bid'])
            exit_signal = Signal(
                symbol=symbol,
                direction="short",
                entry_price=price,
                stop_price=None,
                take_profit=None,
                strategy="daily_peg",
                metadata={},
            )
            return None, exit_signal
        else:
            return None
