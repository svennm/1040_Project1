"""Top level package for the trading platform.

This package contains modules for collecting data from MetaTrader 5,
recording spreads, generating trading signals based on correlation and breakout
strategies, processing those signals using Bayesian logic, and publishing
signals via a simple messaging system.  See the individual modules for
detailed documentation.
"""

__all__ = [
    "data_collector",
    "spread_recorder",
    "signal_generator",
    "signal_processor",
    "messaging",
    "evaluation",
    "utils",
]
