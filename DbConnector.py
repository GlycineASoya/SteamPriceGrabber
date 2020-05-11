import datetime

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

    def __init__(self, host: str = "localhost", username: str = "", password: str = "", database: str = ""):
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self.__connector = mysql.connector.connect(username=username, password=password, host=host, database=database,
                                                   port=3306)

    def getGameById(self, uid: int) -> Game:
        cursor = self.__connector.cursor()

        query = ("SELECT "
                 "steam_uid, date_time, title, is_free, platforms "
                 "FROM game "
                 "WHERE steam_uid=%(uid)s"
                 )

        data = {
            'uid': uid
        }
        try:
            cursor.execute(query, data)
            result = cursor.fetchone()
            for (steam_uid, date_time, title, is_free, platforms) in cursor:
                game = Game(steam_uid, title, is_free, 0, 0, 0, tuple(str(platforms).partition(',')))
        except:
            print(cursor.statement)

        cursor.close()
        return game


    def writeToDb(self, game: Game):
        cursor = self.__connector.cursor()

        # add_game = ("INSERT INTO test (date) VALUES ('{}')".format(datetime.datetime.utcnow().replace(microsecond=0)))

        add_game = ("INSERT INTO game "
                    "(steam_uid, date_time, title, is_free, platforms) "
                    "VALUES (%(uid)s, %(date_time)s, %(title)s, %(is_free)s, %(platforms)s)")

        data_game = {
            'uid': str(game.uid),
            'date_time': datetime.datetime.utcnow().replace(microsecond=0),
            'title': game.title,
            'is_free': game.isFree,
            'platforms': "".join(map(", ".join, game.platforms))
        }
        cursor.execute(add_game, data_game)

        self.__connector.commit()
        cursor.close()


    def connect(self):
        self.__connector.connect()


    def closeConnection(self):
        self.__connector.close()


    def checkConnection(self) -> bool:
        return self.__connector.is_connected()
