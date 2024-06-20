import numpy as np

def calculate_ema(data, period, column='close'):
    return data[column].ewm(span=period, adjust=False).mean()

def generate_signals(data, short_period, long_period):
    data['short_ema'] = calculate_ema(data, short_period)
    data['long_ema'] = calculate_ema(data, long_period)
    data['signal'] = np.where(data['short_ema'] > data['long_ema'], 'buy', 'sell')
    return data