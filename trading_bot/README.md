# Simplified Trading Bot – Binance Futures Testnet

A small Python CLI application that places Market and Limit orders on
Binance Futures Testnet (USDT-M), with structured code, input validation,
and logging of all requests, responses, and errors.

## Project Structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # Binance client wrapper (testnet connection)
    orders.py           # Order placement logic (MARKET / LIMIT)
    validators.py        # Input validation
    logging_config.py    # Logging setup
  cli.py                 # CLI entry point (argparse)
  logs/
    bot.log             # Sample log output (MARKET + LIMIT orders)
  requirements.txt
  .env.example
  README.md
```

## Setup

1. Register for a Binance Futures Testnet account at
   https://testnet.binancefuture.com and generate an API Key + Secret.

2. Clone this repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your API credentials as environment variables.

   On Windows (Command Prompt):
   ```bash
   set BINANCE_API_KEY=your_key_here
   set BINANCE_API_SECRET=your_secret_here
   ```

   On Mac/Linux:
   ```bash
   export BINANCE_API_KEY=your_key_here
   export BINANCE_API_SECRET=your_secret_here
   ```

   (See `.env.example` for the expected variable names. Real keys should
   never be committed to the repository.)

## How to Run

Place a MARKET order:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Place a LIMIT order:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 66000
```

### Sample Output
```
--- Order Request Summary ---
Symbol   : BTCUSDT
Side     : BUY
Type     : MARKET
Quantity : 0.01
Price    : N/A (market order)
------------------------------

✅ Order placed successfully.
Order ID     : 20890523162
Status       : NEW
Executed Qty : 0.0000
Avg Price    : N/A
```

All requests, responses, and errors are also written to `logs/bot.log`.

## Assumptions

- Only Binance Futures Testnet (USDT-M) is supported; base URL is hardcoded
  in `bot/client.py` (`https://testnet.binancefuture.com/fapi`).
- API credentials are read from environment variables only — never
  hardcoded or committed to version control.
- Quantity and price precision follow Binance's exchange rules for the
  chosen symbol (e.g. BTCUSDT); invalid precision will return an API error,
  which is caught and logged.
- The CLI only supports single order placement per run (no batch/queue).

## Error Handling

- **Invalid input** (bad side/type, missing price for LIMIT, non-positive
  quantity) is caught by `bot/validators.py` and reported before any API
  call is made.
- **API errors** (e.g. insufficient balance, invalid symbol) and
  **network errors** are caught in `bot/orders.py` and logged with full
  detail to `logs/bot.log`, with a clean failure message printed to console.

## Bonus / Future Improvements

- Additional order types (Stop-Limit, OCO) could be added by extending
  `bot/orders.py` with new branches following the same pattern as
  MARKET/LIMIT.
- An interactive CLI menu (via `Typer` or `Click` prompts) could replace
  the current flag-based interface for a friendlier UX.
