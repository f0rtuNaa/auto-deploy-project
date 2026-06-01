import random
import string
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')


SHOPS = eval(config['Shops']['SHOPS'])
PRODUCTS = eval(config['Products']['PRODUCTS'])
MIN_RECEIPTS = int(config['Settings']['MIN_RECEIPTS'])
MAX_RECEIPTS = int(config['Settings']['MAX_RECEIPTS'])
MIN_ITEMS = int(config['Settings']['MIN_ITEMS'])
MAX_ITEMS = int(config['Settings']['MAX_ITEMS'])
MIN_AMOUNT = int(config['Settings']['MIN_AMOUNT'])
MAX_AMOUNT = int(config['Settings']['MAX_AMOUNT'])
DISCOUNT_OPTIONS = [float(x) for x in config['Settings']['DISCOUNT_OPTIONS'].split(',')]

def make_doc_id() -> str:
    letters = random.choices(string.ascii_uppercase, k=3)
    digits = random.randint(1, 99999)
    return f"{''.join(letters)}-{digits:05d}"


def build_rows_for_cash(shop_num: int, cash_num: int, date_str: str) -> list[dict]:
    rows = []
    for _ in range(random.randint(MIN_RECEIPTS, MAX_RECEIPTS)):
        doc_id = make_doc_id()
        for name, category, price in random.sample(PRODUCTS,
                                                   k=random.randint(MIN_ITEMS, MAX_ITEMS)):
            discount = round(random.choice(DISCOUNT_OPTIONS) * price, 2)
            rows.append({
                'doc_id': doc_id,
                'item': name,
                'category': category,
                'amount': random.randint(MIN_AMOUNT, MAX_AMOUNT),
                'price': price,
                'discount': discount,
            })
    return rows