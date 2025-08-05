"""Simple in‑process messaging system for trading signals.

This module defines a :class:`MessageBus` class that can be used to publish
and consume trading signals within a single process.  It is intentionally
minimal and synchronous; for a production system you might integrate
RabbitMQ, Kafka or another message broker instead.
"""

from __future__ import annotations

import logging
import threading
from collections import deque
from typing import Deque, Iterator, Optional

from signal_generator import Signal


class MessageBus:
    """Thread‑safe message queue for signals."""

    def __init__(self, maxsize: int = 1000, logger: Optional[logging.Logger] = None) -> None:
        self.queue: Deque[Signal] = deque(maxlen=maxsize)
        self.lock = threading.Lock()
        self.logger = logger or logging.getLogger(__name__)

    def publish(self, signal: Signal) -> None:
        """Publish a signal to the queue."""
        with self.lock:
            self.queue.append(signal)
        self.logger.debug("Published signal: %s", signal)

    def consume(self) -> Iterator[Signal]:
        """Consume signals from the queue.

        Returns an iterator over available signals.  The iterator will
        immediately exhaust if no signals are present.  Consumption is not
        blocking; if you need blocking behaviour use a condition variable
        or a proper queue implementation.
        """
        while True:
            with self.lock:
                if not self.queue:
                    break
                signal = self.queue.popleft()
            yield signal
