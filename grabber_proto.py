from datetime import date
from pickle import FALSE

import requests
import re


def getPage(url: str) -> requests.models.Response:
    return requests.get(url, cookies={"birthtime": "0"})


def getName(page: requests.models.Response) -> str:
    match = re.compile(r"AppName.+>(.+)<\/").search(page.text)
    return match.group(1)


def getPrice(page: requests.models.Response) -> str:
    match = re.compile(r"This.game.is.not.yet.available.on.Steam").search(page.text)
    if match is not None:
        return r"Not yet released"
    else:
        match = re.compile(r"game_area_purchase_platform").search(page.text)
        # add a solution to pass agechecker by adding at the end of the URL /ViewProductPage()
        if match is not None:
            price_match = re.compile(r"game_purchase_price\s+price").search(page.text, pos=match.end())
            discount_match = re.compile(r"discount_final_price").search(page.text, pos=match.end())
            if price_match is not None and discount_match is not None:
                if discount_match.start() < price_match.start():
                    # if discount price is the first option choose discount price
                    price = re.compile(r"([0-9]+,[0-9]+[^\s]+)").search(page.text, discount_match.end()).group(
                        1).lstrip().rstrip()
                elif discount_match is None or discount_match.start() > price_match.start():
                    # if usual price is the first option choose usual price
                    price = re.compile(r"([0-9]+,[0-9]+[^\s]+)").search(page.text, price_match.end()).group(
                        1).lstrip().rstrip()
            elif price_match is not None and discount_match is None:
                price = re.compile(r"([0-9]+,[0-9]+[^\s]+)").search(page.text, price_match.end()).group(
                    1).lstrip().rstrip()
            elif price_match is None and discount_match is not None:
                price = re.compile(r"([0-9]+,[0-9]+[^\s]+)").search(page.text, price_match.end()).group(
                    1).lstrip().rstrip()
        else:
            print("The page either agechecked or does not have price")
            return "The page either agechecked or does not have price"
    return price
    #    print("Check getPrice " + str(url))
    #   return r"Cannot retrieve the price"


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


def getIdsOnPage(page: requests.models.Response) -> set:
    pages = set(re.compile(r"app[/\\]([0-9]+)").findall(page.text))
    return pages


'''
List of the Country Codes
AF, AX, AL, DZ, AS, AD, AO, AI, AQ, AG, AR, AM, AW, AU, AT, AZ, BS, BH, BD, BB, BY, BE, BZ, BJ, BM, BT, BO, BQ, 
BA, BW, BV, BR, IO, BN, BG, BF, BI, CV, KH, CM, CA, KY, CF, TD, CL, CN, CX, CC, CO, KM, CG, CD, CK, CR, CI, HR, CU, 
CW, CY, CZ, DK, DJ, DM, DO, EC, EG, SV, GQ, ER, EE, SZ, ET, FK, FO, FJ, FI, FR, GF, PF, TF, GA, GM, GE, DE, GH, GI, 
GR, GL, GD, GP, GU, GT, GG, GN, GW, GY, HT, HM, VA, HN, HK, HU, IS, IN, ID, IR, IQ, IE, IM, IL, IT, JM, JP, JE, JO, 
KZ, KE, KI, KP, KR, KW, KG, LA, LV, LB, LS, LR, LY, LI, LT, LU, MO, MG, MW, MY, MV, ML, MT, MH, MQ, MR, MU, YT, MX, 
FM, MD, MC, MN, ME, MS, MA, MZ, MM, NA, NR, NP, NL, NC, NZ, NI, NE, NG, NU, NF, MK, MP, NO, OM, PK, PW, PS, PA, PG, 
PY, PE, PH, PN, PL, PT, PR, QA, RE, RO, RU, RW, BL, SH, KN, LC, MF, PM, VC, WS, SM, ST, SA, SN, RS, SC, SL, SG, SX, 
SK, SI, SB, SO, ZA, GS, SS, ES, LK, SD, SR, SJ, SE, CH, SY, TW, TJ, TZ, TH, TL, TG, TK, TO, TT, TN, TR, TM, TC, TV, 
UG, UA, AE, GB, US, UM, UY, UZ, VU, VE, VN, VG, VI, WF, EH, YE, ZM, ZW '''


def getCcPage(url: str) -> requests.models.Response:
    return None


# URL = "http://store.steampowered.com/app/440/?cc=us" #use ?cc=us after the number of the game to get all the currencies
# URL = "http://store.steampowered.com/app/435150"
url = "http://store.steampowered.com/app/"

print(getPrice(getPage(url + "391220")))

# printge(url + "1146930"))

existed_pages = set()
non_existed_pages = set()
if isPageExist(url):
    page = getPage(url)
    existed_pages = set(getIdsOnPage(page))
    print(existed_pages)
else:
    print("The page " + url + " does not exist")

game_list = list()  # list of dicts# [{"id": "<number>", "name": "<get_name()>", "price": "<get_price()>",
# "datetime": "<timestamp>", "isExist": "<bool>"}]

for page_id in existed_pages:
    if isPageExist(url + str(page_id)):
        page = getPage(url + str(page_id))
        game_list.append(
            {"datetime": str(date.today()), "id": page_id, "name": getName(page), "price": getPrice(page),
             "isExist": "True"}
        )
    else:
        non_existed_pages.add(page_id)
        print("The page " + url + str(page_id) + " couldn't be found")

print("\n\r".join(game_list))

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
