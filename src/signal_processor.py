"""Signal processing and Bayesian evaluation.

The :mod:`signal_processor` module provides classes for consuming trading
signals, tracking trade outcomes, and estimating expected reward‑to‑risk
ratios for long and short positions.  The intent is not to make crisp
predictions about price direction but to quantify the asymmetry of
outcomes.  A positive expected RR indicates favourable odds for going
long, whereas a negative expected RR suggests better odds for going
short.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np

from signal_generator import Signal


@dataclass
class TradeRecord:
    """Simple record of a completed trade for performance tracking."""

    symbol: str
    direction: str  # 'long' or 'short'
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    pnl: float  # profit or loss per unit


class SignalProcessor:
    """Process signals and evaluate expected reward‑to‑risk.

    The processor maintains a history of completed trades and uses it to
    estimate the expected RR for future signals.  A Bayesian update
    mechanism (using a normal–inverse‑gamma prior) could be implemented
    here, but for simplicity we use an exponential moving average of past
    PnL values per symbol and direction.
    """

    def __init__(self, decay: float = 0.9, logger: Optional[logging.Logger] = None) -> None:
        """Initialise the processor.

        Parameters
        ----------
        decay : float, optional
            Exponential decay factor used when updating the moving average of
            PnL.  A value closer to 1 gives more weight to recent trades.
        logger : Optional[logging.Logger]
            Logger for diagnostics.
        """
        self.decay = decay
        self.logger = logger or logging.getLogger(__name__)
        # history by (symbol, direction) -> (ema, count)
        self._ema: Dict[tuple[str, str], float] = {}
        self._count: Dict[tuple[str, str], int] = {}

    def register_trade(self, trade: TradeRecord) -> None:
        """Register a completed trade for PnL tracking.

        Parameters
        ----------
        trade : TradeRecord
            The completed trade record including entry/exit and PnL.
        """
        key = (trade.symbol, trade.direction)
        prev_ema = self._ema.get(key, 0.0)
        prev_count = self._count.get(key, 0)
        # Update exponentially weighted moving average
        new_ema = self.decay * prev_ema + (1 - self.decay) * trade.pnl
        self._ema[key] = new_ema
        self._count[key] = prev_count + 1
        self.logger.debug(
            "Updated EMA for %s %s: old=%.4f new=%.4f count=%d", trade.symbol, trade.direction, prev_ema, new_ema, prev_count + 1
        )

    def expected_rr(self, symbol: str) -> Dict[str, float]:
        """Compute expected reward‑to‑risk for long and short directions.

        The expected RR for a direction is computed as the exponential moving
        average PnL divided by an assumed unit risk.  Because no stop‑loss
        information is stored in trade records, this method assumes a risk of
        1.0 per trade.  You can override this logic by modifying the PnL
        normalisation in this method.

        Returns
        -------
        dict
            Dictionary with keys ``"long"`` and ``"short"`` mapping to expected
            RR values.  Missing values (no history) default to 0.
        """
        rr: Dict[str, float] = {}
        for direction in ["long", "short"]:
            key = (symbol, direction)
            ema = self._ema.get(key)
            if ema is None:
                rr[direction] = 0.0
            else:
                rr[direction] = ema  # risk assumed to be 1
        return rr

    def evaluation_bar(self, symbol: str) -> Dict[str, Dict[str, float]]:
        """Return expected RR at multiple horizons.

        This method produces a two‑level dictionary mapping horizon labels
        (``"8h"``, ``"7d"``) to expected RR for long and short directions.  In
        this simplified implementation horizons are not currently used to
        weight PnL differently; the same EMA is returned for all horizons.

        Returns
        -------
        dict
            Mapping from horizon to a sub‑dictionary ``{"long": value, "short": value}``.
        """
        base_rr = self.expected_rr(symbol)
        return {"8h": base_rr, "7d": base_rr}
