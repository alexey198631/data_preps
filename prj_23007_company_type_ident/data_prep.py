import pandas as pd
import sqlite3
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename='data_files/logs_prep.txt')

logger = logging.getLogger('db')

data = pd.read_excel('data_files/OI_data.xlsx', sheet_name='Customers')
opcos = pd.read_excel('data_files/OI_data.xlsx', sheet_name='Countires')

new = data.loc[(data['new_type'] == 'OEM') & (data['Company'] == 'YEF-G')]


conn = sqlite3.connect('data_files/db.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Germany')
cur.execute('DROP TABLE IF EXISTS Country')

cur.execute('''
CREATE TABLE IF NOT EXISTS Germany (Customer TEXT, opco TEXT, old_type TEXT, new_type TEXT)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Country (opco TEXT, country TEXT)''')

x = 0
while x < len(new):

    Customer = new.iloc[x, 2]
    opco = new.iloc[x, 0]
    old_type = new.iloc[x, 3]
    new_type = new.iloc[x, 4]

    logger.debug(f'reading data {Customer} ')

    row = cur.fetchone()
    cur.execute('''INSERT OR IGNORE INTO Germany (Customer, opco, old_type, new_type) VALUES (?,?,?,?)''',
                (Customer, opco, old_type, new_type))
    logger.debug(f'writing data {Customer} ')
    x += 1

conn.commit()

y = 0
while y < len(opcos):

    opco = opcos.iloc[y, 2]
    country = opcos.iloc[y, 0]
    logger.debug(f'reading data {y} {opco},{country}')


    row = cur.fetchone()
    cur.execute('''INSERT OR IGNORE INTO Country (opco, country) VALUES (?,?)''',
                (opco, country))
    logger.debug(f'writing {country}')
    y += 1

conn.commit()

cur.execute('''UPDATE Germany SET opco = 'Germany' ''')
conn.commit()



# sqlstr = 'SELECT Customer, opco FROM Germany ORDER BY Customer DESC LIMIT 10'
#
# for row in cur.execute(sqlstr):
#     print(str(row[0]), row[1])
#
# cur.close()


