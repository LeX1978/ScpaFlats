import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs
import cfscrape
import time
import re

page_list = set()
page_url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1&room3=1"
stop_flag = False


def get_session():
    session = requests.Session()
    session.headers = {
        'authority': 'www.cian.ru',
        'method': 'GET',
        'path': '/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&is_first_floor=0&maxprice=24000000&mintarea=80&object_type[0]=1&offer_type=flat&only_flat=1&p=1&region=1&room3=1',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'cf_clearance=9sbqPpEMUou2ECDSffdP90.Or3Msw20kFGxXRenA0HY-1661873407-0-250; _CIAN_GK=492d92d0-1acf-472b-b315-74e744d627f0; _gcl_au=1.1.605214168.1661873412; sopr_utm={"utm_source":+"direct",+"utm_medium":+"None"}; uxfb_usertype=searcher; _ym_d=1661873412; _ym_uid=1661873412716829818; _gid=GA1.2.1333067266.1661873412; _ga=GA1.2.157340443.1661873412; uxs_uid=a34ccf60-2878-11ed-aaa5-631ddc29c6a7; tmr_lvidTS=1661873411934; tmr_lvid=f3397bb57f462601fa69b06bf7450250; _ym_isad=2; _gpVisits={"isFirstVisitDomain":true,"todayD":"Tue Aug 30 2022","idContainer":"10002511"}; afUserId=0aa0c694-6710-4f23-9ba4-575effc7838d-p; AF_SYNC=1661873412663; adrdel=1; adrcid=AbOd8IJc1K5lBmlGm-Frfzg; _cc_id=6e513fea263251f75eaef0e60ebf19f3; panoramaId_expiry=1662478234268; panoramaId=ce29063093635d8d640ed3a483974945a702cdc86a23d988a2b551560b6fde0d; session_region_id=1; session_main_town_region_id=1; __cf_bm=FRvFkVOQwMj8Tz6eQLKCpEz3OEP1Vr8x_DTNI1A15GU-1661875611-0-AWGS1EPVJxfEfj/6OSc+lAczT+da+G8Q3egQizZGU1CdjcQ2yZ9FKPu7D6OCwC2h2zsfXli5Z+lePs6Rnkn91dw=; login_mro_popup=1; _ym_visorc=b; sopr_session=051530367cbf42be; _dc_gtm_UA-30374201-1=1; _gp10002511={"hits":3,"vc":1,"ac":1,"a6":1}; tmr_detect=0|1661875615649; tmr_reqNum=13',
        'origin': 'https://www.cian.ru',
        'referer': 'https://www.cian.ru/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.1.966 Yowser/2.5 Safari/537.36'
    }
    return cfscrape.create_scraper(sess=session)


# Установка соединения с сайтом
def set_connection(page_url):
    session = get_session()
    try:
        response = session.get(page_url)
        time.sleep(8)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'Other error occured: {err}')
    else:
        soup = bs(response.text, 'html.parser')
        return soup


# Процедура поиска ссылок на страницы
def page_links(soup):
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
def get_flat_info(soup):
    # Находим все блоки с информацией о квартире
    blocks = soup.findAll("div", {'data-name': 'LinkArea'})
    for block in blocks:
        # Определяем ссылку на конкретную квартиру
        link_flat = block.find('a', class_='_93444fe79c--link--eoxce')
        if link_flat is not None:
            if 'href' in link_flat.attrs:
                link = link_flat.attrs['href']
                print(link)
                match = re.search(r'\d{9}', link)
                flat_id = match[0] if match else 0
                print(flat_id)
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

print(page_url)
bf = set_connection(page_url)
print(bf)

# Собираем все ссылки на страницы квартир
# while stop_flag is False:
#    if url not in page_list:
#         page_list.add(url)
#         bf = setConnection(url)
#         url = pageLinks(bf)
#    else:
#         stop_flag = True
#    time.sleep(8)  # Сон в 8 секунды
#
# #Берем список линков и по каждой собираем инфу о квартире
# for link in page_list:
#     print(link)
#     bf = setConnection(link)
#     getFlatInfo(bf)
#     time.sleep(8)
