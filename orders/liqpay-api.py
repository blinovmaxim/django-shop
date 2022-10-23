from shop.settings import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY
import base64
import hashlib
import json
import random


def generate_random_order_id():
    order_id = random.getrandbits(99)
    return order_id


def get_total_price(total):
    pass


params = {"public_key": LIQPAY_PUBLIC_KEY,
          "version": "3",
          "action": "pay",
          "amount": "1480",
          "currency": "UAH",
          "description": "buy in test shop",
          "order_id": f"{generate_random_order_id()}",
          "language": "ru",
          "result_url": "http://127.0.0.1:8000/"
          }

json_string = json.dumps(params)
data = base64.b64encode(json_string.encode())

print(data)

sigh_string = LIQPAY_PRIVATE_KEY + f"{data}"[2:-1] + LIQPAY_PRIVATE_KEY
# hash_str = hashlib.sha1(sigh_string.encode())
signature = base64.standard_b64encode(hashlib.sha1(sigh_string.encode()).digest())

print(signature)
generate_random_order_id()