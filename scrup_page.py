import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs
import re
import time


page_list = set()
url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1&room3=1"
stop_flag = False

# Установка соединения с сайтом
def setConnection(url):
    session = requests.Session()
    hdr = {'authority': 'top-fwz1.mail.ru',
            'method': 'POST',
            'path': '/tracker?js=13;id=2775447;u=https%3A//www.cian.ru/cat.php%3Fcurrency%3D2%26deal_type%3Dsale%26demolished_in_moscow_programm%3D0%26engine_version%3D2%26is_first_floor%3D0%26maxprice%3D24000000%26mintarea%3D80%26object_type%255B0%255D%3D1%26offer_type%3Dflat%26only_flat%3D1%26p%3D1%26region%3D1%26room3%3D1;st=1654099866688;title=%D0%9A%D1%83%D0%BF%D0%B8%D1%82%D1%8C%203-%D0%BA%D0%BE%D0%BC%D0%BD%D0%B0%D1%82%D0%BD%D1%83%D1%8E%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83%20%D0%B2%20%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5%20-%20927%20%D0%BE%D0%B1%D1%8A%D1%8F%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B9;s=1920*1080;vp=939*915;touch=0;hds=1;frame=0;flash=;sid=d1b945b7f28e6e80;ver=60.3.0;tz=-180%2FEurope%2FMoscow;ni=10//4g/0/0/;detect=0;lvid=1648888798200%3A1654099883576%3A263%3A8f638f50d6b2831c3b3cc9cec5115878;opts=dl%2Cjst-gtag-ga;visible=true;_=0.6560150825955811;e=PVT/15',
            'scheme': 'https',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9',
            'content-length': '0',
            'content-type': 'text/plain;charset=UTF-8',
            'cookie': 'p=l70AAGHC8OYA; searchuid=5676853861646464360; b=i0oCAKBgnW0Ae0oOCAEAAAinR8iF4XRNVDMA; c=xpBhYgAAAD/1aAIRAAQAtAABAAIA; _ym_d=1653584997; _ym_uid=1653584997474935865; i=AQATj5diCAATAAiCK3YAAc4AAdkAARwBAR8BAUUBARcEAUYEAVsEAYsEATgFATkFARAGAbIHAVoIAYAIAYEIAYIIAYYIATwJAS0LAUILAXcLAVgMAZcMAfUMAfYMAfcMARgNARkNAXoOAYsOAYwOAY0OAY4OAZEOAZwOAZ4OAaEOAXseAfUgAfYgAfEiAbsBCAQBAQABkwIIYSBtAAGkAQEDAgEEAgEHAgEJAgEPAgESAgEXAgFuAwETBAFKBQFPBQFgBQFtBQFxBQF1BQGgBQGhBQGjBQGmBQGpBQGBBgHFCwHICwHJCwHMCwHOCwFzDQF4DQGVDQGiYwHcBAgEAQEAAeEECQEB4gQKBBoCugfWBggEAQEAAb0HCAQBghUB; act=d59bc23967424111ab1898c170343392; VID=1MQ7eq1lyG2A00000c1CH4oA:::0-0-7b03d5c-761c3cd:CAASEITeco0rxo3DfLrEcmpcqFoacN8C9Ulmrps6rpyhpFHGBfWFv8ogFVqOOtf9FmS1oTaVyaL2fF6ixBfrmetU9Qr7riHotLN1ofxGZAyIMhspt5i1QzaKNpt19xCFEsu_p-1kCvxNkxxOGlj-CgkltubD_CWolDz1pKEdSM9Ewv3f6gU',
            'origin': 'https://www.cian.ru',
            'referer': 'https://www.cian.ru/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Yandex";v="22"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.1.966 Yowser/2.5 Safari/537.36'
    }

    try:
        response = session.get(url, headers = hdr)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured: {err}')
    else:
        soup = bs(response.text, 'html.parser')
        return soup

#Процедура поиска ссылок на страницы
def pageLinks(soup):
    link = ""
    url = ""
    pages = soup.findAll("a", {'class': '_93444fe79c--list-itemLink--BU9w6'})
    for p_link in pages:
        page_num = p_link.text
        if 'href' in p_link.attrs:
            link = p_link.attrs['href']
            if "https://www.cian.ru" not in link:
                link = "https://www.cian.ru" + link
        if page_num != "..":
            if link not in page_list:
                page_list.add(link)
        else:
            url = link
    return url

# Поцедура получения информации о квартирах на странице
def getFlatInfo(soup):
    # Находим все блоки с информацией о квартире
    Blocks = soup.findAll("div", {'data-name': 'LinkArea'})
    for block in Blocks:
        # Определяем ссылку на конкретную квартиру
        linkflat = block.find('a', class_='_93444fe79c--link--eoxce')
        if linkflat is not None:
            if 'href' in linkflat.attrs:
                link = linkflat.attrs['href']
                print(link)
                match = re.search(r'\d{9}', link)
                flatID = match[0] if match else 0
                print(flatID)
        # Ищем название ссылки
        link_spans = block.find("span", {'class': ''})
        link_text = link_spans.get_text().encode("utf8")
        link_text_decoded = link_text.decode('utf8')
        print(link_text_decoded)

        # Ищем метро
        metro_block = block.findAll("a", {'class': '_93444fe79c--link--BwwJO'})
        for metro in metro_block:
            metro_name = metro.find("div", {'class': ''})
            print(metro_name.text)
        # Ищем цену
        price_block = block.findAll("span", {'data-mark': 'MainPrice'})
        for price in price_block:
            price_num = price.find("span")
            flat_price = price_num.get_text()
            print(flat_price)
            
###############################################################################            
# 1. Необходимо добавить проверку на капчу. Если включается капча то ее кликать и продолжить с той же страницы - пока отложил
# 2. Необходимо разобрать информацию по квартире на отдельные элементы
##############################################################################

################################################################################
## Основная программа
################################################################################

#Собираем все ссылки на страницы квартир
while stop_flag is False:
   if url not in page_list:
        page_list.add(url)
        bf = setConnection(url)
        url = pageLinks(bf)
   else:
        stop_flag = True
   time.sleep(8)  # Сон в 8 секунды

#Берем список линков и по каждой собираем инфу о квартире
for link in page_list:
    print(link)
    bf = setConnection(link)
    getFlatInfo(bf)
    time.sleep(8)