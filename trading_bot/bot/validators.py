"""
validators.py
Validates user-supplied order parameters before they are sent to Binance.
"""

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT"]


def validate_order(symbol, side, order_type, quantity, price=None):
    errors = []

    if not symbol or not symbol.strip():
        errors.append("Symbol is required (e.g. BTCUSDT)")
    elif not symbol.isalnum():
        errors.append("Symbol must be alphanumeric (e.g. BTCUSDT)")

    if side not in VALID_SIDES:
        errors.append(f"Side must be one of {VALID_SIDES}")

    if order_type not in VALID_ORDER_TYPES:
        errors.append(f"Order type must be one of {VALID_ORDER_TYPES}")

    if quantity is None or quantity <= 0:
        errors.append("Quantity must be greater than 0")

    if order_type == "LIMIT":
        if price is None or price <= 0:
            errors.append("Price is required and must be greater than 0 for LIMIT orders")

    if errors:
        raise ValueError("; ".join(errors))

    return True
