from typing import Optional, Match

import requests
import re

def find_name(text: str) -> str:
    match: Optional[Match[object]] = re.search('itemprop=\"name\">', text)
    return text[match.end():re.compile('</').search(text, match.end()).start()].lstrip().rstrip()

def find_price(text: str) -> int:
    if "discount_final_price" in text:
        match: Optional[Match[object]] = re.search('discount_final_price\">', text)
    else:
        match: Optional[Match[object]] = re.search('game_purchase_price price\">', text)
    return text[match.end():re.compile('</').search(text, match.end()).start()].lstrip().rstrip()


URL = "http://store.steampowered.com/app/440/Team_Fortress_2/"
URL = "http://store.steampowered.com/app/435150/Divinity_Original_Sin_2__Definitive_Edition/"
r = requests.get(url=URL)

print(find_name(r.text), find_price(r.text))

'''
with open('url.json', 'w') as file:
    file.write(data)
'''
# print(data)
