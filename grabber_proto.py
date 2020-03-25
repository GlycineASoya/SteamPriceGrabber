import requests
import re


def find_name(text: str) -> str:
    match = re.search('itemprop=\"name\">', text)
    return text[match.end():re.compile('</').search(text, match.end()).start()].lstrip().rstrip()


def find_price(text: str) -> int:
    match = re.search(r"\"game_area_purchase_game", text)
    if match != None:
        discount_match = re.compile(r"discount_final_price\">").search(text, match.end())
        price_match = re.compile(r"game_purchase_price price\">").search(text, match.end())
        if discount_match.start() < price_match.start():
            #if discount price is the option choose discount price
            price = text[discount_match.end():re.compile('</').search(text, discount_match.end()).start()].lstrip().rstrip()
        else:
            #if usual price is the option choose usual price
            price = text[price_match.end():re.compile('</').search(text, price_match.end()).start()].lstrip().rstrip()
    return price


def is_page_exist(url: str) -> bool:
    r = requests.head("http://store.steampowered.com/app/0")
    if r.status_code == 200:
        return True
    else:
        return False


#URL = "http://store.steampowered.com/app/440/?cc=us" #use ?cc=us after the number of the game to get all the currencies
#URL = "http://store.steampowered.com/app/435150"
existed_pages = set()
non_existed_pages = set()

url = r"http://store.steampowered.com/app/"
i = 0
while i <= 400:
    if is_page_exist(url + str(i)):
        existed_pages.add(i)
    else:
        non_existed_pages.add(i)
    i += 1

#r = requests.get(url=url)
#print(find_name(r.text), find_price(r.text))

print(existed_pages)

'''
with open('url.json', 'w') as file:
    file.write(data)
'''
# print(data)
