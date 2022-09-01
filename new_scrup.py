import requests
from bs4 import BeautifulSoup as bs


def collect_data():
       url = "http://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1&room3=1"
       proxies = {
              "https": "https://4szZ81:ezG2Mk@217.29.53.70:12369/"
       }

       hdr = {
              'authority': 'mc.yandex.ru',
              'method': 'POST',
              'scheme': 'https',
              'accept': '*/*',
              'accept - encoding': 'gzip, deflate, br',
              'accept - language': 'ru, en;q = 0.9',
              'content - length': '0',
              'origin': 'https://www.cian.ru',
              'referer': 'https://www.cian.ru/',
              'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.796 Yowser/2.5 Safari/537.36'
       }

       response = requests.get(url, proxies=proxies, headers = hdr)
       print(url)
       soup = bs(response.text, 'html.parser')
       print(soup)


def main():
       collect_data()

if __name__ == '__main__':
       main()