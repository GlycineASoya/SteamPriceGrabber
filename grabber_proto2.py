from datetime import date

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
    ids = list(re.compile(r"app[\/]([0-9]+)").findall(page.text))
    return ids


def getPlatformList(page: requests.models.Response) -> list:
    platforms = list(re.compile(r"platform_img\s([\w\S][^\"]+)").findall(page.text))
    return platforms


def getTitleList(page: requests.models.Response) -> list:
    titles = list(re.compile(r"title.>([\w\S][^<]+)").findall(page.text))
    return titles


def getPriceList(page: requests.models.Response) -> list:
    prices = list(set(re.compile(r"search_price.+\s+([\d,]+[\S]+)|>([\d,]+[\S]+)<\/strike").findall(page.text)))
    return prices


def getDiscountPriceList(page: requests.models.Response) -> list:
    discount_prices = list(re.compile(r"search_price.+\s+.+br>([\d,]+[\S]+)").findall(page.text))
    return discount_prices


def getDiscountList(page: requests.models.Response) -> list:
    discounts = list(re.compile(r"search_discount.+\s+.+([\s\S]{4})<").findall(page.text))
    return discounts


main_url = r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=_ASC" #&page=
game_list = list()
cc_price = list()

#title.>([\w\S][^<]+)


if isPageExist(main_url):
    page = getPage(main_url)
    last_page = re.compile(r";(\d+)\s+").search(page.text)
    #for page_number in range(last_page):
    print("IDs: " + str(getIdList(page)))
    print("Titles: " + str(getTitleList(page)))
    print("Platforms: " + str(getPlatformList(page)))
    print("Discounts: " + str(getDiscountList(page)))
    print("Discount prices: " + str(getDiscountPriceList(page)))
    print("Prices: " + str(getPriceList(page)))




