from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import re

page_list = set()
page_url = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2' \
      '&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1' \
      '&room3=1 '
stop_flag = False


def get_session(url):
    EXE_PATH = r'C:\Work\python\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=EXE_PATH)
    driver.get(url)
    # Проверка на страницу проверки
    response = driver.page_source
    soup = bs(response, 'html.parser')
    flag = soup.findAll("div", {'class':'cf-browser-verification cf-im-under-attack'})
    if flag is not None:
        time.sleep(5)
        driver.get(url)
        response = driver.page_source
        soup = bs(response, 'html.parser')
    print(url)
    return soup


# Процедура поиска ссылок на страницы
def page_links(soup):
    link = ""
    p_url = ""
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
            p_url = link
    return p_url

# Поцедура получения информации о квартирах на странице
def get_flatinfo(soup):
    # Находим все блоки с информацией о квартире
    blocks = soup.findAll("div", {'data-name': 'LinkArea'})
    for block in blocks:
        # Определяем ссылку на конкретную квартиру
        link_flat = block.find('a', class_='_93444fe79c--link--eoxce')
        if link_flat is not None:
            if 'href' in link_flat.attrs:
                link = link_flat.attrs['href']
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


def collect_data():
    global page_url
    global stop_flag
    global page_list

    # Собираем все ссылки на страницы квартир
    while stop_flag is False:
        if page_url not in page_list:
            page_list.add(page_url)
            bf = get_session(page_url)
            page_url = page_links(bf)
        else:
            stop_flag = True

    # Берем список линков и по каждой собираем инфу о квартире
    for link in page_list:
        bf = get_session(link)
        get_flatinfo(bf)

def main():
    collect_data()

if __name__ == '__main__':
    main()
