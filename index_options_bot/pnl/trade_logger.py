# index_options_bot/pnl/trade_logger.py

import csv
import os
from datetime import datetime


class TradeLogger:
    """
    Logs each completed trade into a CSV file.
    """

    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

        self.file_path = os.path.join(self.log_dir, "trades.csv")
        self._ensure_header()

    def _ensure_header(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "date",
                    "time",
                    "symbol",
                    "qty",
                    "entry_price",
                    "exit_price",
                    "pnl",
                    "exit_reason"
                ])

    def log_trade(self, symbol, qty, entry_price, exit_price, pnl, exit_reason):
        now = datetime.now()

        with open(self.file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                now.date(),
                now.strftime("%H:%M:%S"),
                symbol,
                qty,
                entry_price,
                exit_price,
                pnl,
                exit_reason
            ])

        print("[PNL] Trade logged to CSV")
