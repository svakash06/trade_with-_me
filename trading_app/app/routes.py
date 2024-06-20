from flask import render_template, request, redirect, url_for, flash
from flask import current_app as app
from . import authentication, market, data, ema, order
import pandas as pd
from datetime import datetime, timedelta

def get_token_info(csv_file, ExchangeSegment, InstrumentType, Symbol, StrikePrice, OptionType):
    df = pd.read_csv(csv_file)
    filtered_df = df[(df['ExchangeSegment'] == ExchangeSegment) & 
                     (df['InstrumentType'] == InstrumentType) &
                     (df['Symbol'] == Symbol) & 
                     (df['StrikePrice'] == StrikePrice) & 
                     (df['OptionType'] == OptionType)]
    return filtered_df.to_dict('records')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trade', methods=['GET', 'POST'])
def trade():
    if request.method == 'POST':
        exchange_segment = request.form['exchange_segment']
        instrument_type = request.form['instrument_type']
        symbol = request.form['symbol']
        strike_price = int(request.form['strike_price'])
        option_type = request.form['option_type']
        
        try:
            token_info = get_token_info('OpenAPIScripMaster.csv', exchange_segment, instrument_type, symbol, strike_price, option_type)
            df = pd.DataFrame(token_info)
            return render_template('trade.html', df=df)
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('index'))
    return render_template('trade.html')

@app.route('/auto_trade', methods=['POST'])
def auto_trade():
    index = int(request.form['index'])
    exchange_segment = request.form['exchange_segment']
    instrument_type = request.form['instrument_type']
    symbol = request.form['symbol']
    strike_price = int(request.form['strike_price'])
    option_type = request.form['option_type']
    
    try:
        token_info = get_token_info('OpenAPIScripMaster.csv', exchange_segment, instrument_type, symbol, strike_price, option_type)
        token = token_info[index]['token']
        obj, refreshToken, feedToken = authentication.authenticate()
        holidays = market.load_holidays('holidays_list_bse_nse.csv')
        
        if not market.is_market_open(holidays):
            flash("Market is closed.", "warning")
            return redirect(url_for('trade'))
        
        quantity = 1  # Define your quantity
        position_held = False
        
        while True:
            if not market.is_market_open(holidays):
                flash("Market is closed.", "warning")
                break
            
            live_data = data.get_live_data(obj, exchange_segment, symbol, token)
            if not live_data:
                continue
            
            historical_data = data.get_historical_data(obj, {
                "exchange": exchange_segment,
                "tradingsymbol": symbol,
                "symboltoken": token,
                "interval": "5minute",
                "start_time": datetime.now() - timedelta(days=1),
                "end_time": datetime.now()
            })
            
            if not historical_data:
                continue
            
            df = pd.DataFrame(historical_data)
            signals = ema.generate_signals(df, short_period=12, long_period=26)
            signal = signals.iloc[-1]['signal']
            
            if not position_held:
                if signal == 'buy':
                    flash("EMA crossover indicates a buy signal. Placing buy order.", "success")
                    buy_order_id = order.place_order(obj, symbol, token, quantity, 'BUY', exchange_segment)
                    if buy_order_id:
                        flash(f"Buy order placed. Order id is: {buy_order_id}", "success")
                        position_held = True
            else:
                if signal == 'sell':
                    flash("EMA crossover indicates a sell signal. Placing sell order.", "success")
                    sell_order_id = order.place_order(obj, symbol, token, quantity, 'SELL', exchange_segment)
                    if sell_order_id:
                        flash(f"Sell order placed. Order id is: {sell_order_id}", "success")
                        position_held = False
                        break
            
            time.sleep(60*5)
        
        return redirect(url_for('trade'))
    
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('trade'))
