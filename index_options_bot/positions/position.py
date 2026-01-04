# index_options_bot/positions/position.py

class Position:
    """
    Represents ONE live trade.
    No API calls.
    No loops.
    Just state.
    """

    def __init__(self, symbol, qty, entry_price, sl):
        self.symbol = symbol
        self.qty = qty
        self.entry_price = entry_price
        self.sl = sl

        self.is_open = True
        self.exit_price = None
        self.exit_reason = None

    def close(self, price, reason):
        self.is_open = False
        self.exit_price = price
        self.exit_reason = reason
