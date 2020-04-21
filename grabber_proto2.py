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
    pattern = r"search_price.+\s+.+br>(\d+\D+\d+[^<\s]+)"
    try:
        discount_price = getValue(page, id, pattern)
    except:
        # print("There is no result for " + pattern + "for " + str(id))
        discount_price = ""
    return discount_price


def getDiscount(page: requests.models.Response, id: int) -> str:
    pattern = r"search_discount.+\s+.+(\-\d+%)"
    try:
        discount = getValue(page, id, pattern)
    except:
        # print("There is no result for " + pattern + "for " + str(id))
        discount = ""
    return discount


main_url = r"http://store.steampowered.com/search/?ignore_preferences=1&sort_by=Name_ASC"  # &page=
game_list = list()
cc_price = list()

# title.>([\w\S][^<]+)

exception_count = 0
if isPageExist(main_url + "&page=1"):
    page = getPage(main_url)
    # last_page = re.compile(r";(\d+)\s+").search(page.text)
    # for page_number in range(last_page):
    apps = getAppList(page)
    bundles = getBundleList(page)
    print("Apps :\t" + "\t".join(str(len(apps))))
    print("Bundles :\t" + "\t".join(str(len(bundles))))
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
'''    
    print("Titles:\t" + "\t> ".join((getTitleList(page))))
    # print("Platforms: " + "\t".join(getPlatformList(page))))
    print("Discounts:\t" + "\t".join(str(len(getDiscountList(page)))))
    print("Discount prices:\t" + "\t".join(str(len(getDiscountPriceList(page)))))
    print("Prices:\t" + "\t".join(str(len(getPriceList(page)))))
'''
