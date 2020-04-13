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
    # title = re.compile(r"title.>([^<]+|)").match(page.text.partition(str(id))[2])
    string = page.text.partition(r"<!-- List Items -->")[2].partition(str(id))[2]
    title = re.compile(r"title.>([^<]+|)").search(string).group(1).lstrip().rstrip()
    title = title.replace(r"&quot;", "\"")
    title = title.replace(r"&amp;", r"&")
    title = title.replace(r"&lt;", r"<")
    title = title.replace(r"&gt;", r">")
    return title


def getPrice(page: requests.models.Response, id: int) -> list:
    prices = list(
        set(re.compile(r"search_price[^_].+\s+([\d,]+[\d]+[\S]+)|(Free\s+to\s+Play)|>([\d,]+[\S]+)<\/strike").findall(
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


main_url = r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=Name_ASC"  # &page=
game_list = list()
cc_price = list()

# title.>([\w\S][^<]+)


if isPageExist(main_url + "&page=1"):
    page = getPage(main_url)
    # last_page = re.compile(r";(\d+)\s+").search(page.text)
    # for page_number in range(last_page):
    apps = getAppList(page)
    print("Apps :\t" + "\t".join(str(len(apps))))
    print("Bundles :\t" + "\t".join(str(len(getBundleList(page)))))
    for app in apps:
        print(app + ": " + getTitle(page, app))

'''    
    print("Titles:\t" + "\t> ".join((getTitleList(page))))
    # print("Platforms: " + "\t".join(getPlatformList(page))))
    print("Discounts:\t" + "\t".join(str(len(getDiscountList(page)))))
    print("Discount prices:\t" + "\t".join(str(len(getDiscountPriceList(page)))))
    print("Prices:\t" + "\t".join(str(len(getPriceList(page)))))
'''
