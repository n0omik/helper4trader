import requests
from bs4 import BeautifulSoup
import re
from Main_bot.utils.redis_storage import storage
import json


def pars_news():
    url = 'https://www.coindesk.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_wrapper = soup.find('div', class_="leaderboard")
    news_pattern = re.compile(
        r'^defaultstyles__LeaderboardWrapper-sc|static-cardstyles__StaticCardWrapper-sc|side-cover-cardstyles__SideCoverCardWrapper-sc')
    all_news = news_wrapper.find_all(class_=news_pattern)
    news_list = []
    for news_item in all_news:
        news_list.append({
            'title': news_item.find('h2').text,
            'link': f"{url}{news_item.find_all('a')[0]['href']}",
            'text': news_item.find_all('p')[0].text,
            'date': news_item.find(class_='hcIsFR').text,
        })
    data = json.dumps({'news':news_list})
    storage.set("news",data)



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

