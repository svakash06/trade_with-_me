from datetime import datetime
import pandas as pd

def load_holidays(holidays_csv):
    holidays_df = pd.read_csv(holidays_csv)
    holidays = set(holidays_df['Date'].tolist())
    return holidays

def is_holiday(holidays):
    today = datetime.now().strftime('%Y-%m-%d')
    return today in holidays

def is_market_open(holidays):
    now = datetime.now()
    if is_holiday(holidays):
        return False
    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return market_open <= now <= market_close