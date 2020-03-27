import requests
import re


def getPage(url: str) -> requests.models.Response:
    if isPageExist(url):
        return requests.get(url)
    else:
        return None


def getName(url: str) -> str:
    text = getPage(url).text
    match = re.search('itemprop=\"name\">', text)
    return text[match.end():re.compile('</').search(text, match.end()).start()].lstrip().rstrip()


def getPrice(url: str) -> int:
    text = getPage(url).text
    match = re.search(r"\"game_area_purchase_game", text)
    if match is not None:
        discount_match = re.compile(r"discount_final_price\">").search(text, match.end())
        price_match = re.compile(r"game_purchase_price price\">").search(text, match.end())
        if discount_match.start() < price_match.start():
            # if discount price is the first option choose discount price
            price = text[
                    discount_match.end():re.compile('</').search(text, discount_match.end()).start()].lstrip().rstrip()
        else:
            # if usual price is the first option choose usual price
            price = text[price_match.end():re.compile('</').search(text, price_match.end()).start()].lstrip().rstrip()
    return price


def isPageExist(url: str) -> bool:
    r = requests.head(url)
    if r.status_code == 200 or r.status_code == 302:
        return True
    else:
        return False


def getIdsOnPage(url: str) -> set:
    r = requests.get(url)
    existed_pages = set(re.compile(r"app/([0-9]+)").findall(r.text))
    return existed_pages


# URL = "http://store.steampowered.com/app/440/?cc=us" #use ?cc=us after the number of the game to get all the currencies
# URL = "http://store.steampowered.com/app/435150"
url = "http://store.steampowered.com/app/"

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
