from datetime import date

import mysql
import mysql.connector

from Game import Game


class DbConnector:
    _host: str
    _username: str
    _password: str
    _database: str

    @property
    def connector(self):
        return self.__connector

    __connector: mysql.connector.MySQLConnection = None

    def __init__(self):
        pass

    def __init__(self, host="localhost", username="", password="", database=""):
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self.__connector = mysql.connector.connect(username=username, password=password, host=host, database=database,
                                                   port=3306)

    def writeToDb(self, game: Game):
        cursor = self.__connector.cursor()

        add_game = ("INSERT INTO main_table "
                    "(steam_id, date_time, type_of_item, title, price, discount_price, discount, platforms) "
                    "VALUES (%(steam_id)s, %(date_time)s, %(type_of_item)s, %(title)s), %(price)s), %(discount_price)s), %(discount)s), %(platforms)s)")

        data_game = {
            "steam_id": game.uid,
            "date_time": date.today(),
            "type_of_item": "",
            "title": game.title,
            "price": game.price,
            "discount_price": game.discountPrice,
            "discount": game.discount,
            "platforms": ""
        }

        cursor.execute(add_game, data_game)

        self.__connector.commit()

        cursor.close()

    def closeConnection(self):
        self.__connector.close()

    def checkConnection(self) -> bool:
        return self.__connector.is_connected()
