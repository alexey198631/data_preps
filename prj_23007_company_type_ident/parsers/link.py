from locators.search_page_locators import SearchPageLocators


class LinkParser:

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f'<Company {self.company} link {self.link}>'

    @property
    def company(self):
        locator = SearchPageLocators.COMPANY
        company = self.parent.select_one(locator).text
        return company

    @property
    def link(self):
        locator = SearchPageLocators.LINK
        link = self.parent.select_one(locator).attrs['href']
        return link