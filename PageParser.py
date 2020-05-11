import mysql
import requests
import re


class PageParser:
    __main_url: str = r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=Name_ASC"  # &self.__page.
    last_page: int = 0
    __cc_list: list = sorted(
        {"AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU", "AT", "AZ", "BS", "BH",
         "BD", "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO", "BN", "BG", "BF",
         "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR",
         "CI", "HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE", "SZ", "ET",
         "FK", "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP",
         "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE",
         "IM", "IL", "IT", "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS",
         "LR", "LY", "LI", "LT", "LU", "MO", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX",
         "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG",
         "NU", "NF", "MK", "MP", "NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR",
         "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN", "LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS",
         "SC", "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES", "LK", "SD", "SR", "SJ", "SE", "CH",
         "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV", "UG", "UA", "AE",
         "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"})

    @property
    def page(self):
        return self.__page

    @property
    def main_url(self):
        return self.__page

    @main_url.setter
    def main_url(self, url: str):
        self.__main_url = url

    @property
    def last_page(self):
        return self.__last_page

    def __init__(self, url=r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=Name_ASC"):
        self.main_url = url
        self.__last_page = self.__getLastPage()

    def __isPageExist(self, url: str) -> bool:
        r = requests.head(url)
        if r.ok:
            return True
        elif url == r"http://store.steampowered.com/app/" and r.is_redirect:
            return False
        elif r.ok and r.is_redirect:
            return True
        else:
            return False

    def __getValue(self, uid: int, pattern: str) -> str:
        string = self.__page.text.partition(r"<!-- List Items -->")[2].partition(str(uid))[2].partition(r"app/")[0]
        value = re.compile(pattern).search(string).group(1)
        value.lstrip().rstrip()
        return value

    def __getPage(self, url: str) -> requests.models.Response:
        self.__page = requests.get(url, cookies={"birthtime": "0"})

    def __getBundleList(self, page: requests.models.Response) -> list:
        bundles = list(re.compile(r"bundle[\/]([0-9]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
        return list(map(int, bundles))

    def __getAppList(self, page: requests.models.Response) -> list:
        apps = list(re.compile(r"app[\/]([0-9]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
        return list(map(int, apps))

    def getPlatformList(self, uid: int) -> tuple:
        platforms = []
        pattern = r"platform_img\s([\w\S][^\"]+)"
        try:
            result = self.getValue(uid, pattern)
            if result is not None:
                platforms = result
        except:
            pass
        return platforms

    def getTitle(self, uid: int) -> str:
        title = ""
        pattern = r"title.>([^<]+|)"
        title = self.getValue(uid, pattern)
        title = title.replace(r"&quot;", "\"")
        title = title.replace(r"&amp;", r"&")
        title = title.replace(r"&lt;", r"<")
        title = title.replace(r"&gt;", r">")
        return title

    def isFree(self, uid: int) -> bool:
        isFree: bool = False
        patterns = {
            r"search_price.+\s+([fF]ree\s+[tT]o\s+[pP]lay)",
            r"search_price.+\s+([fF]ree\s+[dD]emo)"
        }
        for pattern in patterns:
            try:
                if self.getValue(uid, pattern) is not None:
                    isFree = True
            except:
                pass
        return isFree

    # [^<\s]+
    def __getPrice(self, uid: int) -> float:
        price: float = 0
        patterns = {
            r"search_price.+\s+(\d+\D+\d+)",
            r"search_price.+\s+.+strike>(\d+\D+\d+)"
        }
        for pattern in patterns:
            try:
                result = self.getValue(uid, pattern)
                if result is not None:
                    if result.isdigit():
                        price = result
            except:
                pass
        return price

    def getPriceList(self, uid: int) -> dict:

        priceList: dict = {}
        game_list: list

        for countryCode in self.__cc_list:
            page = self.__getPage(self.current_url + "&cc={:s}".format(countryCode))
            game_list = [self.__getAppList(page), self.__getBundleList(page)]
            for app in game_list:
                if self.__isTheGame(app):
                    price = self.__getPrice(uid)
                    priceList[app] = {countryCode, price}

        return priceList

    def getDiscountPrice(self, uid: int) -> int:
        discount_price: int = 0
        pattern = r"search_price.+\s+.+br>(\d+\D+\d+[^<\s]+)"
        try:
            result = self.getValue(uid, pattern)
            if result is not None:
                if result.isdigit():
                    discount_price = result
        except:
            pass
        return discount_price

    def getDiscount(self, uid: int) -> str:
        discount = ""
        pattern = r"search_discount.+\s+.+(\-\d+%)"
        try:
            discount = self.getValue(uid, pattern)
        except:
            pass
        return discount

    def __isTheGame(self, uid: int) -> bool:
        isTheGame: bool = False
        string = self.__page.text
        pattern = "app.+{:d}".format(uid)
        try:
            value = re.compile(pattern).search(string).group(1)
            if value is not None:
                isTheGame = True
        except:
            pass
        return isTheGame

    def __getLastPage(self) -> int:
        pattern = r"nItemCount.+\s+(\d+);"
        page = self.__getPage(self.main_url)
        value = float(re.compile(pattern).search(page.string).group(1))
        return int(round(value))
