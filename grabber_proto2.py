from datetime import date
from DbConnector import DbConnector
from Game import Game
from PageParser import PageParser

page_parser = PageParser()
db = DbConnector("127.0.0.1", "admin", "`123qwe", "steampricegrabber")

# collect unchangable data of the game in one thread
# collect prices in different thread
for page in range(page_parser.last_page):
    if page_parser.isPageExist(page_parser.main_url + r"&page={:d}".format(page)):
        page_parser.getPriceList()
        page_parser.getDiscountPriceList()
        page_parser.getDiscountList()
