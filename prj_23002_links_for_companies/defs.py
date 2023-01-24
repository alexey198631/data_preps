# получает данные с google search
import logging

logger = logging.getLogger('scraping.defs')


def comp_link(y):
    for comp_link in y:
        print(comp_link)
        logger.debug(f'links {comp_link[0]}')
        return comp_link

def comp_title(y):
    for comp_title in y:
        print(comp_title[1])
        logger.debug(f'title {comp_title[1]}')
        return comp_title[1]


def comp_description(y):
    for comp_description in y:
        print(comp_description[2])
        logger.debug(f'description {comp_description[2]}')
        return comp_description[2]
