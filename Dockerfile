##
# Dockerfile for the trading platform
#
# This Dockerfile sets up a minimal Ubuntu environment with Python and the
# MetaTrader5 Python package.  It assumes that the MetaTrader 5 terminal
# executable will be mounted into the container at runtime via a volume
# mount.  The terminal itself is **not** downloaded or installed by this
# Dockerfile because MetaQuotes does not provide a native Linux version.  If
# running on Linux you can install MT5 under Wine and mount that directory
# into the container; on Windows you can mount the terminal directly.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip \
    xvfb \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy source code
COPY src /app/src

# Add src to PYTHONPATH so that relative imports work when running as a script
ENV PYTHONPATH=/app/src

# Create logs directory
RUN mkdir -p /app/logs

# By default run the main module; pass environment variables for MT5
# configuration (MT5_PATH, MT5_LOGIN, MT5_PASSWORD, MT5_SERVER).
CMD ["python3", "-u", "/app/src/main.py"]
