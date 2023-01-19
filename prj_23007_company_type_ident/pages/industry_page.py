import logging
from bs4 import BeautifulSoup
from locators.industry_page_locators import IndustryPageLocators

logger = logging.getLogger('scraping.search_page')


class IndustryPage:

    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def industry(self):
        logger.debug(f'searching using {IndustryPageLocators.INDUSTRY}')
        locator = IndustryPageLocators.INDUSTRY
        industry_one = self.soup.select(locator)
        industry = industry_one[0].text.strip()
        logger.debug(f'industry was found {industry}')
        return industry

    @property
    def code(self):
        logger.debug(f'searching using {IndustryPageLocators.CODE}')
        locator = IndustryPageLocators.CODE
        code_one = self.soup.select(locator)
        code = code_one[0].text.strip()
        logger.debug(f'code was found {code}')
        return code

    @property
    def name(self):
        logger.debug(f'searching using {IndustryPageLocators.NAME}')
        locator = IndustryPageLocators.NAME
        name_one = self.soup.select(locator)
        name = name_one[0].text.strip()
        logger.debug(f'name was found {name}')
        return name

    @property
    def address(self):
        logger.debug(f'searching using {IndustryPageLocators.ADDRESS}')
        locator = IndustryPageLocators.ADDRESS
        address_one = self.soup.select(locator)
        address = address_one[0].text.strip()
        logger.debug(f'address was found {address}')
        return address
