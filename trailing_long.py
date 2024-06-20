
import requests
import hmac
import hashlib
import base64
import json
import time

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = "4d6b52994f748665489b87bc663066333668feb644eb7995"
secret = "74ad9431700f3d9db39ad4fd3873da9d9ccc679016ff02"

# python3
secret_bytes = bytes(secret, encoding='utf-8')
# python2
secret_bytes = bytes(secret)

# Generating a timestamp
timeStamp = int(round(time.time() * 1000))


def create_futures_order(pair, price, quantity):

    # Enter your API Key and Secret here. If you don't have one, you can generate it from the websit
    body = {
        "timestamp": timeStamp,  # EPOCH timestamp in seconds
        "order": {
            "side": "sell",  # buy OR sell
            "pair": pair,  # instrument.string
            "order_type": "market_order",  # market_order OR limit_order
            "price": price,  # numeric value
            "total_quantity": quantity,  # numeric value
            "leverage": 10,  # numeric value
            # no_notification OR email_notification OR push_notification
            "notification": "email_notification",
            # good_till_cancel OR fill_or_kill OR immediate_or_cancel
            "time_in_force": "good_till_cancel",
            "hidden": False,  # True or False
            "post_only": False  # True or False
        }
    }

    json_body = json.dumps(body, separators=(',', ':'))

    signature = hmac.new(secret_bytes, json_body.encode(),
                         hashlib.sha256).hexdigest()

    url = "https://api.coindcx.com/exchange/v1/derivatives/futures/orders/create"

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }


