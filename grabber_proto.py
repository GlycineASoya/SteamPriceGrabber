import requests
import re

URL = "http://store.steampowered.com/app/440/Team_Fortress_2/"
r = requests.get(url=URL)
# data = json.dumps(r.text)
match = re.search('game_purchase_price price\">', r.text)
end = match.end()
# print(pos)

# big1 = re.compile('</div>').search(r.text, pos).start()
# print(big1)


price = r.text[end:re.compile('</div>').search(r.text, end).start()].lstrip().rstrip()

print(price)

'''
with open('url.json', 'w') as file:
    file.write(data)
'''
# print(data)
