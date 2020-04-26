from datetime import date
from DbConnector import DbConnector
from Game import Game
from PageParser import PageParser

page_parser = PageParser()
db = DbConnector("127.0.0.1", "admin", "`123qwe", "steampricegrabber")

if page_parser.isPageExist(page_parser.main_url + r"&page=1"):
    page_parser.getPage(page_parser.main_url + r"&page=1")
    page_parser.getAppList()
    page_parser.getBundleList()
    for app in page_parser.game_list:
        game = Game(
            uid=app,
            title=page_parser.getTitle(app))
        game.price = page_parser.getPrice(app)
        game.discount = page_parser.getDiscount(app)
        game.discount_price = page_parser.getDiscountPrice(app)
        game.printValues()
        if db.checkConnection():
            #db.writeToDb(game)
            db.closeConnection()
        del game
