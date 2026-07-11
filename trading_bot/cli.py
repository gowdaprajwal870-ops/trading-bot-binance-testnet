"""
cli.py
Command-line entry point for the Simplified Trading Bot.

Example usage:
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
    python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 66000
"""

import argparse
import sys

from bot.client import get_client
from bot.orders import place_order
from bot.logging_config import log_and_print


def parse_args():
    parser = argparse.ArgumentParser(
        description="Place Market or Limit orders on Binance Futures Testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading pair symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], dest="order_type", help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", required=False, type=float, default=None, help="Price (required for LIMIT orders)")

    return parser.parse_args()


def main():
    args = parse_args()

    print("\n--- Order Request Summary ---")
    print(f"Symbol   : {args.symbol}")
    print(f"Side     : {args.side}")
    print(f"Type     : {args.order_type}")
    print(f"Quantity : {args.quantity}")
    print(f"Price    : {args.price if args.price else 'N/A (market order)'}")
    print("------------------------------\n")

    try:
        client = get_client()
    except EnvironmentError as e:
        log_and_print(f"STARTUP ERROR: {e}", level="error")
        sys.exit(1)

    response = place_order(
        client=client,
        symbol=args.symbol.upper(),
        side=args.side,
        order_type=args.order_type,
        quantity=args.quantity,
        price=args.price,
    )

    if response:
        print("\n✅ Order placed successfully.")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")
    else:
        print("\n❌ Order failed. Check bot.log for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
