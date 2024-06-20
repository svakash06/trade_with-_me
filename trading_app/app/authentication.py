import pyotp
from SmartApi import SmartConnect
import credentials

def authenticate():
    myotp = pyotp.TOTP(credentials.CD).now()
    obj = SmartConnect(api_key=credentials.API_KEY)
    data = obj.generateSession(credentials.USER_NAME, credentials.PWD, myotp)
    refreshToken = data['data']['refreshToken']
    feedToken = obj.getfeedToken()
    return obj, refreshToken, feedToken