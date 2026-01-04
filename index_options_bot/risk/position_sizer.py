# index_option_bot/risk/position_sizer.py

def calculate_quantity(capital, entry_price, sl_price):
    risk_amount = capital * 0.01  # 1% risk
    risk_per_lot = abs(entry_price - sl_price)
    
    if risk_per_lot == 0:
        return 0

    qty = int(risk_amount / risk_per_lot)
    return max(qty, 0)

