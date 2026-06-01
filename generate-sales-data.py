from datetime import datetime, timedelta
import pandas as pd
import configparser
import os
import re

from utils import build_rows_for_cash
from pgdb import PGDatabase

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding='utf-8')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__),
                          config['Settings']['OUTPUT_DIR'])
DATABASE_CREDS = config['Database']
FILE_PATTERN = re.compile(r'^(\d+)_(\d+)\.csv$')
os.makedirs(OUTPUT_DIR, exist_ok=True)
SHOPS = eval(config['Shops']['SHOPS'])


today = datetime.today()
yesterday = today - timedelta(days=1)

if today.weekday() != 6:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = yesterday.strftime('%d/%m/%Y')
    generated = []

    for shop_num, num_cashes in SHOPS.items():
        for cash_num in range(1, num_cashes + 1):
            rows = build_rows_for_cash(shop_num, cash_num, date_str)
            df = pd.DataFrame(rows, columns=['doc_id', 'item', 'category',
                                             'amount', 'price', 'discount'])
            path = os.path.join(OUTPUT_DIR, f'{shop_num}_{cash_num}.csv')
            df.to_csv(path, index=False, encoding='utf-8-sig')
            generated.append(path)
            print(f'  [OK] {path}  ({len(df)} строк)')

    print(f'\nДата выгрузки : {date_str}')
    print(f'Создано файлов: {len(generated)}')

database = PGDatabase(
    host=DATABASE_CREDS['HOST'],
    database=DATABASE_CREDS['DATABASE'],
    user=DATABASE_CREDS['USER'],
    password=DATABASE_CREDS['PASSWORD'],
)

for filename in sorted(os.listdir(OUTPUT_DIR)):
    match = FILE_PATTERN.match(filename)
    if not match:
        continue
    filepath = os.path.join(OUTPUT_DIR, filename)
    sales = pd.read_csv(filepath, encoding='utf-8-sig')
    shop, cash = filename.split('.')[0].split('_')
    for i, row in sales.iterrows():
        query = f"insert into sales values ('{row['doc_id']}', '{row['item']}', " \
                f"'{row['category']}', {row['amount']}, {row['price']}, {row['discount']}, {shop}, {cash})"
        database.post(query)




