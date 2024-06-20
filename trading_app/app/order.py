def place_order(obj, tradingsymbol, symboltoken, quantity, transaction_type, exchange):
    try:
        order_params = {
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "quantity": quantity,
            "transactiontype": transaction_type,
            "exchange": exchange,
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY"
        }
        order_id = obj.placeOrder(order_params)
        return order_id
    except Exception as e:
        print(f"Error placing order: {e}")
        return None