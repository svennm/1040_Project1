"""Spread recording and logging.

The :mod:`spread_recorder` module provides a :class:`SpreadRecorder` class that
continuously records the bid–ask spread of configured instruments.  It
subscribes to tick data via the MT5 API and writes spread information to a
time‑stamped CSV file.  Spreads can widen significantly during illiquid
periods; monitoring them helps identify when it may be unsafe to place
orders.

Example::

    from spread_recorder import SpreadRecorder

    recorder = SpreadRecorder(collector, symbols=["EURUSD", "GBPUSD"])
    recorder.start()
    # ... run your strategy ...
    recorder.stop()

The recorder runs in a background thread and stops gracefully when
:meth:`stop` is called.
"""

from __future__ import annotations

import csv
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

from data_collector import DataCollector


class SpreadRecorder:
    """Record bid–ask spreads for a set of instruments.

    Parameters
    ----------
    collector : DataCollector
        An initialised and connected :class:`~data_collector.DataCollector`.
    symbols : iterable of str
        Symbols whose spreads should be recorded.
    log_dir : str or Path, optional
        Directory in which to write CSV files.  Defaults to `logs/spreads` under
        the project root.
    interval : float, optional
        Polling interval in seconds.  Lower values record more granular
        spreads but may consume more CPU.  Default is 1.0 second.
    logger : Optional[logging.Logger]
        Logger for diagnostics; if omitted the module logger is used.
    """

    def __init__(
        self,
        collector: DataCollector,
        symbols: Iterable[str],
        log_dir: Optional[Path | str] = None,
        interval: float = 1.0,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.collector = collector
        self.symbols = list(symbols)
        self.interval = interval
        self.logger = logger or logging.getLogger(__name__)
        self.log_dir = Path(log_dir or Path(__file__).resolve().parent.parent / "logs" / "spreads")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start recording spreads in a background thread."""
        if self._thread and self._thread.is_alive():
            self.logger.warning("SpreadRecorder is already running")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.logger.info("Spread recorder started for symbols: %s", ", ".join(self.symbols))

    def stop(self) -> None:
        """Signal the recorder to stop and wait for the thread to finish."""
        if not self._thread:
            return
        self._stop_event.set()
        self._thread.join()
        self.logger.info("Spread recorder stopped")

    def _run(self) -> None:
        """Internal thread loop that polls spreads and writes to log files."""
        # Open one CSV file per symbol with today's date
        files: Dict[str, csv.writer] = {}
        handles: Dict[str, object] = {}
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        for sym in self.symbols:
            path = self.log_dir / f"{sym}_{date_str}.csv"
            handle = open(path, mode="a", newline="")
            writer = csv.writer(handle)
            # Write header if file is empty
            if handle.tell() == 0:
                writer.writerow(["timestamp", "bid", "ask", "spread"])
            files[sym] = writer
            handles[sym] = handle
        try:
            while not self._stop_event.is_set():
                now = datetime.utcnow()
                for sym in self.symbols:
                    # Request the most recent tick; we reuse get_tick_data
                    tick_df = self.collector.get_tick_data(sym, n_ticks=1)
                    if tick_df.empty:
                        continue
                    row = tick_df.iloc[-1]
                    bid = float(row['bid'])
                    ask = float(row['ask'])
                    spread = ask - bid
                    files[sym].writerow([now.isoformat(), bid, ask, spread])
                time.sleep(self.interval)
        finally:
            for handle in handles.values():
                handle.close()
