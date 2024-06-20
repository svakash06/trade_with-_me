def get_live_data(obj, exchange, tradingsymbol, symboltoken):
    try:
        ltp_data = obj.ltpData(exchange, tradingsymbol, symboltoken)
        return ltp_data['data']
    except Exception as e:
        print(f"Error fetching live data: {e}")
        return None

def get_historical_data(obj, params):
    try:
        formatted_params = {
            "exchange": params["exchange"],
            "tradingsymbol": params["tradingsymbol"],
            "symboltoken": params["symboltoken"],
            "interval": params["interval"],
            "fromdate": params["start_time"].strftime("%Y-%m-%d %H:%M"),
            "todate": params["end_time"].strftime("%Y-%m-%d %H:%M")
        }
        historical_data = obj.candlestickData(formatted_params)
        return historical_data['data']
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None