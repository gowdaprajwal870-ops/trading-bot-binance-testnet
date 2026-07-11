"""
client.py
Wraps the Binance Futures Testnet client so the rest of the app
doesn't need to know connection details.
"""

import os
from binance.client import Client
from bot.logging_config import log_and_print

TESTNET_FUTURES_URL = "https://testnet.binancefuture.com/fapi"


def get_client():
    """
    Creates and returns a Binance Client configured for Futures Testnet.
    Reads API key/secret from environment variables:
        BINANCE_API_KEY
        BINANCE_API_SECRET
    """
    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise EnvironmentError(
            "Missing API credentials. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET environment variables before running."
        )

    client = Client(api_key, api_secret)
    client.FUTURES_URL = TESTNET_FUTURES_URL

    log_and_print("Connected to Binance Futures Testnet")
    return client
