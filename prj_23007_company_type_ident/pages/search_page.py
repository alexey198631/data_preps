import logging
from bs4 import BeautifulSoup
from locators.search_page_locators import SearchPageLocators

logger = logging.getLogger('scraping.search_page')


class LinkPage:
    def __init__(self, page):
        # logger.debug('parsing search page')
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def company(self):
        logger.debug(f'searching using {SearchPageLocators.COMPANY}')
        locator = SearchPageLocators.COMPANY
        company = self.soup.select_one(locator).text
        logger.debug(f'company was found {company}')
        return company

    @property
    def link(self):
        logger.debug(f'searching using {SearchPageLocators.LINK}')
        locator = SearchPageLocators.LINK
        link = self.soup.select_one(locator).attrs['href']
        logger.debug(f'link was found {link}')
        return link

    @property
    def lcountry(self):
        logger.debug(f'searching using {SearchPageLocators.LINK}')
        locator = SearchPageLocators.COUNTRY
        lcountry = self.soup.select_one(locator).text
        logger.debug(f'link was found {lcountry}')
        return lcountry.strip()