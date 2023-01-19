import requests
import pandas as pd
import sqlite3
import logging

from pages.search_page import LinkPage
from pages.industry_page import IndustryPage

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.DEBUG,
                    filename='data_files/logs.txt')

logger = logging.getLogger('scraping')


print('Loading...')
logger.info('Loading...')


conn = sqlite3.connect('data_files/OEM.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS OEM')

cur.execute('''
CREATE TABLE IF NOT EXISTS OEM (company TEXT, country TEXT, industry TEXT, code TEXT, address TEXT, dbname TEXT)''')

OEMS = pd.read_excel('data_files/all.xlsx', sheet_name='Sheet1')

#https://www.hithorizons.com/search?Name=Clippertech+Ltd - structure of the link with search information
base = 'https://www.hithorizons.com/'
base2 = 'https://www.hithorizons.com'
search_url = 'search?Name='
country = '&Address='
after = '&ShowBranches=false&CompanyTypes=10&CompanyTypes=11&CompanyTypes=12&CompanyTypes=160&CompanyTypes=3&CompanyTypes=14&CompanyTypes=102&CompanyTypes=120&CompanyTypes=151&CompanyTypes=167&CompanyTypes=13&CompanyTypes=107&CompanyTypes=154&CompanyTypes=100&CompanyTypes=0&CompanyTypes=999'

x = 0
print(len(OEMS))
while x < 100:

    company = OEMS.iloc[x, 0]
    country_0 = OEMS.iloc[x, 1]
    company_input = company.replace(' ', '%20')
    country_input = country_0.replace(' ', '%20')
    search_page = base + search_url + company_input + country + country_input + after
    search_page_content = requests.get(search_page).content

    logger.debug('Searching for OEMs from the file')

    try:

        link_page = LinkPage(search_page_content)
        industry_page = base2 + link_page.link
        industry_page_content = requests.get(industry_page).content

        logger.debug('Searching industry OEMs')

        industry_page = IndustryPage(industry_page_content)
        print(x, f'from {len(OEMS)} {industry_page.name} {industry_page.code} country {link_page.lcountry}')

        row = cur.fetchone()
        cur.execute(
            '''INSERT OR IGNORE INTO OEM (company, country, industry, code, address, dbname) VALUES (?,?,?,?,?,?)''', (
            industry_page.name, link_page.lcountry, industry_page.industry, industry_page.code, industry_page.address,
            company))
        conn.commit()
        x += 1

    except:

        print('There is a mistake')
        x += 1

cur.close()


















