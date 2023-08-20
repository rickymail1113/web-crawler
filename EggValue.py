import numpy
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as BS
import time

countyDict = { "09007":"連江縣", "09020":"金門縣", "10001":"臺北縣", "10002":"宜蘭縣", "10003":"桃園縣", "10004":"新竹縣",
               "10005":"苗栗縣", "10007":"彰化縣", "10008":"南投縣", "10009":"雲林縣", "10010":"嘉義縣", "10011":"臺南縣",
               "10012":"高雄縣", "10013":"屏東縣", "10014":"臺東縣", "10015":"花蓮縣", "10016":"澎湖縣", "10017":"基隆市",
               "10018":"新竹市", "10020":"嘉義市", "10021":"臺南市", "63000":"臺北市", "64000":"高雄市", "65000":"新北市",
               "66000":"臺中市", "67000":"臺南市", "68000":"桃園市" }


yearValueData = None


def getEggYearValueData(type):
    global yearValueData
    if yearValueData is None:
        time.sleep(1)
        if 0 == type:
            try:
                # 抓網路資料
                url_year = "https://data.coa.gov.tw/service/opendata/agrstatUnit.aspx?item_code=225102230100&dimension_code=LD045&IsTransData=1&UnitId=580"
                yearValueData = pd.read_json(url_year)
            except:
                yearValueData = pd.read_json("egg.json")
        else:
            # 使用本機端檔案(上面網路資料無法取得時)
            yearValueData = pd.read_json("egg.json")

    return yearValueData


def getYearValueData_GropByCounty(strCounty, dataFrame):
    pd_data_group = dataFrame.groupby("dname1")
    key = ""
    for k, v in countyDict.items():
        if v == strCounty:
            key = k
            break

    if "" == key:
        return dataFrame
    else:
        return dataFrame[dataFrame.dname1 == key]


def chageIndexToyear(groupedDf):
    print(type(groupedDf))
    for i in range(1,len(groupedDf)):
        print(groupedDf.iloc(i))



plt.rcParams["font.sans-serif"] = "mingliu"
plt.rcParams["axes.unicode_minus"] = False


def runEggYearValue(strLocation):
    df = getEggYearValueData(type=0)
    convert_dict = {"date": int}  # 時間為字串 排序會不正確 轉整數
    df = df.astype(convert_dict)
    print(df.keys())
    print(len(df))
    # 縣市代碼, 品項名稱, 統計年分, 數量, 單位

    print("=============================")
    if strLocation in countyDict.values():
        grouped_df = getYearValueData_GropByCounty(strCounty=strLocation, dataFrame=df)  # 取單一指定縣市
        grouped_df.rename(columns={"dname1": "countyId", "dname2": "itemName", "date": "year"}, inplace=True)
        sort_df = grouped_df.sort_values(by="year", ascending=True)  # 年份排序 最新在後
        new_df = sort_df.set_index("year")
        print(new_df)

        # 圖表標題 x軸說明文字 y軸說明文字 是否顯示圖例
        new_df.plot(title=f"歷年{strLocation}雞蛋產量查詢", xlabel="年度統計", ylabel="數量", legend=True,
                    figsize=(10, 5))

    else:
        grouped_df = df.groupby("date")["value"].sum() # 取全國年度總合
        print(grouped_df)
        grouped_df.plot(title=f"歷年全國雞蛋產量查詢", xlabel="年度統計", ylabel="數量", legend=True,
                    figsize=(10, 5))

    plt.show()