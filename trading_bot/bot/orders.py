"""
orders.py
Handles the actual order placement logic (MARKET and LIMIT),
using the validated inputs and the shared Binance client.
"""

from binance.enums import (
    ORDER_TYPE_MARKET,
    ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC,
)
from bot.validators import validate_order
from bot.logging_config import log_and_print


def place_order(client, symbol, side, order_type, quantity, price=None):
    """
    Places a MARKET or LIMIT order on Binance Futures Testnet.

    Returns the raw API response dict on success, or None on failure
    (failures are logged, not raised, so the CLI can print a clean message).
    """
    try:
        validate_order(symbol, side, order_type, quantity, price)

        log_and_print(
            f"Placing order -> Symbol: {symbol}, Side: {side}, "
            f"Type: {order_type}, Qty: {quantity}, Price: {price}"
        )

        if order_type == "MARKET":
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity,
            )
        else:  # LIMIT
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price,
            )

        log_and_print(f"Order Response: {response}")
        log_and_print(
            f"SUCCESS - Order ID: {response.get('orderId')}, "
            f"Status: {response.get('status')}, "
            f"ExecutedQty: {response.get('executedQty')}, "
            f"AvgPrice: {response.get('avgPrice', 'N/A')}"
        )
        return response

    except ValueError as ve:
        log_and_print(f"VALIDATION ERROR: {ve}", level="error")
        return None
    except Exception as e:
        log_and_print(f"API/NETWORK ERROR: {e}", level="error")
        return None
