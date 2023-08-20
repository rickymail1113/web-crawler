import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as BS
import time
import numpy as np

priceData = None


def getEggDayPriceData(strArea):
    global priceData
    if priceData is None:
        try:
            time.sleep(1)
            url_price = "https://tw.chinyieggs.com/"
            price_data = requests.get(url_price)
        except:
            print(price_data)

    dataSoup = BS(price_data.text, 'html.parser')
    table = dataSoup.select("table[class='egg_table']")[0]
    strday = ""

    for i in table.find_all("th"):
        strday = i.text

    # 找地區的三個標籤內容
    tds = table.find_all("td")
    tdArea = []
    for i in tds[2:5]:
        tdArea.append(i.text)

    strPrice = []
    strPrice.append(int(tds[6].text[3:5])) # 取台北價格
    strPrice.append(int(tds[7].text[3:5])) # 取台中價格
    strPrice.append(int(tds[8].text))   # 取台南價格

    priceData = pd.DataFrame(strPrice, index=tdArea, columns=["price"])
    priceData.plot(kind="bar", title=f"台灣區域雞蛋平均價格 {strday}", xlabel="地區", ylabel="價格(元/600克/未稅)", legend=True,
                   figsize=(10, 5))

    for x, y in enumerate(strPrice):
        plt.text(x, y + 1, "%s" % round(y, 1), ha="center")

    plt.show()


def runEggEggDayPrice(strArea):
    return getEggDayPriceData(strArea)
# ===========================================================================================================


def runEggEggHistoryPrice():
    getEggHistoryData()


historyData = None


def getEggHistoryData():
    global historyData
    if historyData is None:
        try:
            time.sleep(1)
            url_history = "https://data.coa.gov.tw/Service/OpenData/FromM/PoultryTransBoiledChickenData.aspx?IsTransData=1&UnitId=056"
            historyData = pd.read_json(url_history)
        except:
            historyData = pd.read_json("history.json")

    else:
        historyData = pd.read_json("history.json")

    print(historyData.describe())
    """
    list_date = []
    list_price = []
    dict_history = {}
    for i in historyData["日期"]:
        # tmp = f"{i[0:4] + i[5:7]}"
        list_date.append(i)

    pre_data = 0
    for i in historyData["雞蛋(產地)"]:
        try:
            tmp = float(i)
            pre_data = tmp
            list_price.append(pre_data)
        except:
            list_price.append(pre_data)

    list_date.reverse()
    list_price.reverse()
    df = pd.DataFrame(list_price, index=list_date, columns=["price"])
    df.plot(title=f"歷年雞蛋價格", xlabel="", ylabel="產地平均價格", legend=True,
                figsize=(12, 7))
    """
    list_date = []
    list_price = []
    dict_data = month_avg()
    list_date = list(dict_data.keys())
    list_date.reverse()
    list_price = list(dict_data.values())
    list_price.reverse()
    df = pd.DataFrame(list_price, index=list_date, columns=["price"])
    df.plot(title=f"歷年雞蛋價格", xlabel="", ylabel="產地平均價格", legend=True,
                figsize=(12, 7))

    plt.show()


# 計算月均價 回傳新dict
def month_avg():

    dict_month = {}
    for i in range(0,historyData.shape[0]):
        # print(historyData.iloc[i]["日期"][0:7])
        tmp = f"{historyData.iloc[i]['日期'][0:7]}"
        tmp_price = 0
        if None == dict_month.get(tmp):
            dict_month[tmp] = list()
            try:
                tmp_price = float(historyData.iloc[i]["雞蛋(產地)"])
            except:
                continue
        else:
            try:
                tmp_price = float(historyData.iloc[i]["雞蛋(產地)"])
            except:
                continue

        dict_month[tmp].append(tmp_price)

    for each_key in dict_month:
        avg = round(np.mean(dict_month[each_key]), 1)
        dict_month[each_key] = avg

    return dict_month


# ===========================================================================================================


def getPassDays():
    import datetime
    today = datetime.date.today()
    d1 = datetime.date(2023, 1, 1)
    d2 = datetime.date(2023, 3, 1)
    # d2 = datetime.date(today.year, today.month, today.day)
    return d2 - d1