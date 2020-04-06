from datetime import date
from prettytable import PrettyTable
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


def getPage(url: str) -> requests.models.Response:
    return requests.get(url, cookies={"birthtime": "0"})


def getIdList(page: requests.models.Response) -> list:
    ids = list(re.compile(r"app[\/]([0-9]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return ids


def getPlatformList(page: requests.models.Response) -> list:
    platforms = list(
        re.compile(r"platform_img\s([\w\S][^\"]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return platforms


def getTitleList(page: requests.models.Response) -> list:
    titles = list(re.compile(r"title.>([\w\S][^<]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return titles


def getPriceList(page: requests.models.Response) -> list:
    prices = list(set(re.compile(r"search_price.+\s+([\d,]+[\S]+)|>([\d,]+[\S]+)<\/strike").findall(
        page.text.partition(r"<!-- List Items -->")[2])))
    result = map(lambda x: x[0] if (x[1] == '') else x[1], prices)
    return list(result)


def getDiscountPriceList(page: requests.models.Response) -> list:
    discount_prices = list(
        re.compile(r"search_price.+\s+.+br>([\d,]+[\S]+)").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return discount_prices


def getDiscountList(page: requests.models.Response) -> list:
    discounts = list(
        re.compile(r"search_discount.+\s+.+([\s\S]{4})<").findall(page.text.partition(r"<!-- List Items -->")[2]))
    return discounts


main_url = r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=_ASC"  # &page=
game_list = list()
cc_price = list()

# title.>([\w\S][^<]+)


if isPageExist(main_url):
    page = getPage(main_url)
    # last_page = re.compile(r";(\d+)\s+").search(page.text)
    # for page_number in range(last_page):
    print("IDs:\t" + "\t".join(getIdList(page)))
    print("Titles:\t" + "\t".join(getTitleList(page)))
    #print("Platforms: " + "\t".join(getPlatformList(page)))
    print("Discounts:\t" + "\t".join(getDiscountList(page)))
    print("Discount prices:\t" + "\t".join(getDiscountPriceList(page)))
    print("Prices:\t" + "\t".join(getPriceList(page)))
