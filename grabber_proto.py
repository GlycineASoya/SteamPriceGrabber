from typing import Optional, Match

import requests
import re


def find_name(text: str) -> str:
    match: Optional[Match[object]] = re.search('itemprop=\"name\">', text)
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


URL = "http://store.steampowered.com/app/440/?cc=us" #use ?cc=us after the number of the game to get all the currencies
#URL = "http://store.steampowered.com/app/435150"
r = requests.get(url=URL)

print(find_name(r.text), find_price(r.text))

'''
with open('url.json', 'w') as file:
    file.write(data)
'''
# print(data)
