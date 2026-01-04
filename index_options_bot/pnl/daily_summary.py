# index_options_bot/pnl/daily_summary.py

import csv
import os
from datetime import date


class DailyPnLSummary:
    """
    Maintains daily PnL summary.
    """

    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

        self.file_path = os.path.join(self.log_dir, "daily_pnl.csv")
        self._ensure_header()

    def _ensure_header(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "realized_pnl"])

    def update(self, pnl):
        today = date.today().isoformat()
        rows = []

        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                rows = list(csv.reader(f))

        header, data = rows[0], rows[1:]
        updated = False

        for row in data:
            if row[0] == today:
                row[1] = str(float(row[1]) + pnl)
                updated = True
                break

        if not updated:
            data.append([today, pnl])

        with open(self.file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

        print("[PNL] Daily PnL updated")
