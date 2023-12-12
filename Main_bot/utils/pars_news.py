import requests
from bs4 import BeautifulSoup
from datetime import datetime


# def get_latest_news(symbol):
#     sources = [
#         {"name": "CoinDesk", "url": "https://www.coindesk.com/"},
#     ]
#     news_list = []
#     for source in sources:
#         source_name = source["name"]
#         source_url = source["url"]
#         if source_name == "CoinDesk":
#             coin_desk_news = parse_coindesk_news(symbol, source_url)
#             news_list.extend(coin_desk_news)
#     sorted_news_list = sorted(news_list, key=lambda x: x["date"], reverse=True)
#     response_text = f"Here are the latest news updates for {symbol}:\n"
#     for idx, news in enumerate(sorted_news_list, start=1):
#         response_text += f"{idx}. {news['title']}\n"
#         response_text += f"   - Source: {news['source']}\n"
#         response_text += f"   - Date: {news['date'].strftime('%B %d, %Y')}\n"
#         response_text += f"   - Summary: {news['summary']}\n"
#
#     return response_text
#
#
# def parse_coindesk_news(symbol):
#     url = 'https://www.coindesk.com/'
#     news_list = []
#     full_url = f"{url}{symbol}"
#     response = requests.get(full_url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     news_titles = soup.find_all("h3", class_="heading")
#     # Пройдемся по каждому заголовку и добавим в список
#     for title in news_titles:
#         news_list.append({
#             "title": title.text.strip(),
#             "source": "CoinDesk",
#             "date": datetime.now(),  # Мы используем текущую дату как пример, вы можете заменить ее на дату из новости
#             "summary": ""  # Заглушка для краткого содержания
#         })
#     return news_list


# print(parse_coindesk_news("Bitcoin"))


urls = ["https://www.coindesk.com/",]

def get_coindesk_headlines():
    url = "https://www.coindesk.com/"
    response = requests.get(url)
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text,'html.parser')
    news_wrapper = soup.find('div',class_ ="leaderboard")
    #news_title = news_wrapper.find_all('a')
    news_time = news_wrapper.find_all('date')
    #for news in news_title:
        #print(news.text)
    print(news_time)



get_coindesk_headlines()


Twitter_accounts = [
    "@100trillionUSD",
    "@aantonop",
    "@AltcoinGordon",
    "@ASvanevik",
    "@APompliano",
    "@BanklessHQ",
    "@BTC_Archive",
    "@Bybit_Official",
    "@cz_binance",
    "@koeppelmann",
    "@lrettig",
    "@ricburton",
    "@gavofyork",
    "@evan_van_ness",
    "@CryptoDiffer",
    "@CryptoKaleo",
    "@CryptoWendyO",
    "@AriDavidPaul",
    "@NickSzabo4",
    "@avsa",
    "@brian_armstrong",
    "@0xstark",
    "@twobitidiot",
    "@Disruptepreneur",
    "@leashless",
    "@defi_mochi",
    "@FEhrsam",
    "@laurashin",
    "@ErikVoorhees",
    "@ethereumJoseph",
    "@girlgone_crypto",
    "@garyvee",
    "@IvanOnTech",
    "@nlw",
    "@KennethBosak",
    "@LynAldenContact",
    "@spencernoon"
    "@lopp",
    "@MDudas",
    "@trentmc0",
    "@Melt_Dem",
    "@naval",
    "@@tayvano_",
    "@cburniske",
    "@MessariCrypto",
    "@masonnystrom",
    "@nic__carter",
    "@opensea",
    "@PaikCapital",
    "@pecksield",
    "@SushiSwap",
    "@saylor",
    "@TheCryptoDog",
    "@TheMoonCarl",
    "@ToneVays",
    "@TyDanielSmith",
    "@VladZamfir",
    "@VitalikButerin",
    "@WatcherGuru"
    "@whale_alert",
    "@WillClementeIII",
    "@SatoshiLite",
    "@CoinDesk",
    "@Cointelegraph",
    "@TheBlock__",
    "@CryptoSlate",
    "@decryptmedia",
    "@@jchervinsky",
    "@SEC_News",
    "@ethereum",
    "@Bitcoin",
    "@LitecoinProject",
    "@krakenfx",
    "@BitMEXResearch",
    "@Gemini",
    "@Ledger",
    "@woonomic",
    "@skewdotcom",
    "@coinmetrics",
    "@balajis"
]

