from datetime import date

import mysql
import requests
import re


def isPageExist(url: str) -> bool:
    r = requests.head(url)
    if r.ok:
        return True
    elif url == r"http://store.steampowered.com/app/" and r.is_redirect:
        return False
    elif r.ok and r.is_redirect:
        return True
    else:
        return False


def getValue(page: requests.models.Response, id: int, pattern: str) -> str:
    string = page.text.partition(r"<!-- List Items -->")[2].partition(str(id))[2].partition(r"app/")[0]
    value = re.compile(pattern).search(string).group(1)
    value.lstrip().rstrip()
    return value


def getPage(url: str) -> requests.models.Response:
    return requests.get(url, cookies={"birthtime": "0"})


def getBundleList(page: requests.models.Response) -> list:
    bundles = list(re.compile(r"bundle[\/]([0-9]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return bundles


def getAppList(page: requests.models.Response) -> list:
    apps = list(re.compile(r"app[\/]([0-9]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return apps


def getPlatformList(page: requests.models.Response) -> list:
    platforms = list(
        re.compile(r"platform_img\s([\w\S][^\"]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return platforms


def getTitle(page: requests.models.Response, id: int) -> str:
    title = ""
    pattern = r"title.>([^<]+|)"
    title = getValue(page, id, pattern)
    title = title.replace(r"&quot;", "\"")
    title = title.replace(r"&amp;", r"&")
    title = title.replace(r"&lt;", r"<")
    title = title.replace(r"&gt;", r">")
    return title


def getPrice(page: requests.models.Response, id: int) -> str:
    price = ""
    patterns = [
        r"search_price.+\s+(\d+\D+\d+[^<\s]+)",
        r"search_price.+\s+([fF]ree\s+[tT]o\s+[pP]lay)",
        r"search_price.+\s+.+strike>(\d+\D+\d+[^<\s]+)"
    ]
    for pattern in patterns:
        try:
            price = getValue(page, id, pattern)
        except:
            pass
    return price


def getDiscountPrice(page: requests.models.Response, id: int) -> str:
    discount_price = ""
    pattern = r"search_price.+\s+.+br>(\d+\D+\d+[^<\s]+)"
    try:
        discount_price = getValue(page, id, pattern)
    except:
        pass
    return discount_price


def getDiscount(page: requests.models.Response, id: int) -> str:
    discount = ""
    pattern = r"search_discount.+\s+.+(\-\d+%)"
    try:
        discount = getValue(page, id, pattern)
    except:
        pass
    return discount


def connectDB(connectionString: str) -> object:
    mysql.connector
    return None


'''
cc_list = sorted(
    {"AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR", "AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD",
     "BB", "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO", "BN", "BG", "BF", "BI", "CV",
     "KH", "CM", "CA", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI", "HR", "CU",
     "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE", "SZ", "ET", "FK", "FO", "FJ", "FI",
     "FR", "GF", "PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU", "GT", "GG", "GN", "GW",
     "GY", "HT", "HM", "VA", "HN", "HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT", "JM", "JP", "JE",
     "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MG",
     "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ",
     "MM", "NA", "NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MK", "MP", "NO", "OM", "PK", "PW", "PS",
     "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN", "LC", "MF",
     "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS",
     "ES", "LK", "SD", "SR", "SJ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR",
     "TM", "TC", "TV", "UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN", "VG", "VI", "WF", "EH", "YE",
     "ZM", "ZW"})
'''

main_url = r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=Name_ASC"  # &page=
game_list = list()
cc_price = list()


if isPageExist(main_url + "&page=1"):
    page = getPage(main_url)
    # last_page = re.compile(r";(\d+)\s+").search(page.text)
    # for page_number in range(last_page):
    apps = getAppList(page)
    bundles = getBundleList(page)
    for app in apps:
        title = getTitle(page, app)
        price = getPrice(page, app)
        discount = getDiscount(page, app)
        discount_price = getDiscountPrice(page, app)
        print(
            "App " + app + ": <" + title + ">, price <" + price + ">, discount <" + discount +
            ">, discount price <" + discount_price + ">")
    for bundle in bundles:
        title = getTitle(page, bundle)
        price = getPrice(page, bundle)
        discount = getDiscount(page, bundle)
        discount_price = getDiscountPrice(page, bundle)
        print(
            "App " + bundle + ": <" + title + ">, price <" + price + ">, discount <" + discount +
            ">, discount price <" + discount_price + ">")

