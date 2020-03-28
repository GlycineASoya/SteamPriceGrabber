import requests
import re


def getPage(url: str) -> requests.models.Response:
    if isPageExist(url):
        return requests.get(url)
    else:
        return None


def getName(url: str) -> str:
    text = getPage(url).text

    match = re.compile(r"<title>(.+)<\/title>").search(text)
    return match.group(1)


def getPrice(url: str) -> str:
    try:
        text = getPage(url).text
    except:
        print("Cannot retrieve text from " + url)
        return "Page does not exist"
    try:
        match = re.compile(r"This.game.is.not.yet.available.on.Steam").search(text)
        if match is not None:
            return r"Not yet released"
        else:
            match = re.compile(r"game_area_purchase_platform").search(text)
            if match is not None:
                price_match = re.compile(r"game_purchase_price\s+price").search(text, pos=match.end())
                discount_match = re.compile(r"discount_final_price").search(text, pos=match.end())
                if discount_match.start() < price_match.start() or price_match is None:
                    # if discount price is the first option choose discount price
                    price = re.compile(r"([0-9]+,[0-9]+[^\s]+)").search(text, discount_match.end()).lstrip().rstrip()
                elif discount_match.start() > price_match.start() or discount_match is None:
                    # if usual price is the first option choose usual price
                    price = re.compile(r"([0-9]+,[0-9]+[^\s]+)").search(text, price_match.end()).group(
                        1).lstrip().rstrip()
        return price
    except:
        print("Check getPrice " + str(url))
        return r"Cannot retrieve the price"


def isPageExist(url: str) -> bool:
    r = requests.head(url)
    if r.status_code == 200:
        return True
    else:
        return False


def getIdsOnPage(url: str) -> set:
    r = requests.get(url)
    pages_list = set(re.compile(r"app[/\\]([0-9]+)").findall(r.text))
    return pages_list


def getCcPage(url: str) -> requests.models.Response:
    return None


# URL = "http://store.steampowered.com/app/440/?cc=us" #use ?cc=us after the number of the game to get all the currencies
# URL = "http://store.steampowered.com/app/435150"
url = "http://store.steampowered.com/app/"

print(getPrice(url + "114693x"))

# print(getIdsOnPage(url + "1146930"))

'''

existed_pages = set()
existed_pages = set(getIdsOnPage(r"http://store.steampowered.com"))
print(existed_pages)

game_list = list()  # list of dicts# [{"id": "<number>", "name": "<get_name()>", "price": "<get_price()>"}]

for page_id in existed_pages:
    game_list.append(
        {"id": page_id, "name": getName(url + str(page_id)), "price": getPrice(url + str(page_id))}
    )

print(game_list)

'''
'''
url = r"http://store.steampowered.com/app/"
i = 0

if is_page_exist(url + str(i)):
    existed_pages.add(i)
else:
    non_existed_pages.add(i)
i += 1

#r = requests.get(url=url)
#print(find_name(r.text), find_price(r.text))

print(existed_pages)

'''

# print(data)
