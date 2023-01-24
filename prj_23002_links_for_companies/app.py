import logging
import sqlite3
import pandas as pd

from ggl import search
from defs import *

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename='logs.txt')

logger = logging.getLogger('scraping')
print('Loading...')
logger.info('Loading...')

conn = sqlite3.connect('data_files/companies_l.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS COMPANIES')

cur.execute('''
CREATE TABLE IF NOT EXISTS COMPANIES (company TEXT, title TEXT, description TEXT, link TEXT )''')


companies = pd.read_excel('data_files/book.xlsx', sheet_name='parse')

if input('do you need an "linkedin" option? enter "yes" ') == 'yes':
    print('ok')
    addition = ' linkedin'
else:
    addition = ''


temp = []

print(len(companies))

x = 0
while x < len(companies):

    company = companies.iloc[x, 0]
    company = company + addition
    company_0 = company
    logger.debug(f'Searching for companies from the file {company}')
    y = search(company, num_results=1, lang="en", advanced=False)
    link = comp_link(y)
    logger.debug(f'Searching for companies from the line {link}')
    link = list(link)
    title = link[1]
    description = link[2]
    link = link[0]
    row = cur.fetchone()
    cur.execute('''INSERT OR IGNORE INTO COMPANIES (company, title, description, link) VALUES (?,?,?,?)''', (company_0, title, description, link))
    conn.commit()
    x += 1
    print(len(companies) - x)

cur.close()