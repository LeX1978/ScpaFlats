import requests
from bs4 import BeautifulSoup as bs
import cfscrape

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

def collect_data():
       url = "http://www.cian.ru/cat.php?currency=2&deal_type=sale&demolished_in_moscow_programm=0&engine_version=2&is_first_floor=0&maxprice=24000000&mintarea=80&object_type%5B0%5D=1&offer_type=flat&only_flat=1&p=1&region=1&room3=1"
       proxies = {
              "https": "https://4szZ81:ezG2Mk@217.29.53.70:12369/"
       }
       session = get_session()
       response = session.get(url, proxies=proxies)
       print("Let's begin rock !!!")
       print(url)
       soup = bs(response.text, 'html.parser')
       print(soup)


def main():
       collect_data()

if __name__ == '__main__':
       main()