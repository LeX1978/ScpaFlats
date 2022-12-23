from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs

page_list = set()
page_url = 'https://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2' \
      '&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1' \
      '&room3=1 '
stop_flag = False


def get_session(url):
    EXE_PATH = r'C:\Work\python\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=EXE_PATH)
    driver.get(url)
    time.sleep(8)
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
        time.sleep(8)  # Сон в 8 секунды


def main():
    collect_data()


if __name__ == '__main__':
    main()
