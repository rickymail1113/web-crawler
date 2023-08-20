import tkinter as tk
from tkinter import *
from tkinter import ttk
import EggValue
import EggPrice

str_county = [ "全地區年總產量", "連江縣", "金門縣", "臺北縣", "宜蘭縣", "桃園縣",
               "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣", "臺南縣",
               "高雄縣", "屏東縣", "臺東縣", "花蓮縣", "澎湖縣", "基隆市", "新竹市",
               "嘉義市", "臺南市", "臺北市", "高雄市", "新北市", "臺中市", "臺南市", "桃園市" ]


str_zone = [ "當日價格",	"歷史價格" ]

def buttonValue_clicked():
    cur = combo_value.get()
    EggValue.runEggYearValue(cur)


recvPriceData = []
def buttonPrice_clicked():
    cur = combo_price.get()
    if  "當日價格" == cur:
        EggPrice.runEggEggDayPrice(cur)
    else:
        EggPrice.runEggEggHistoryPrice()


window = tk.Tk()
window.title('各地雞蛋價格與產量')
window.geometry('800x600')
# 不給使用者變更視窗大小
window.resizable(False, False)
# 設定程式標題icon by png file
window.tk.call("wm", "iconphoto", window._w, tk.PhotoImage(file="line-chart.png"))

combo_value = ttk.Combobox(state="readonly", values=str_county)
button_value = Button(text="按下取得年度總產量資料", font=("Arial", 14, "bold"), padx=5, pady=5, bg="blue", fg="light green",
                command=buttonValue_clicked)

combo_value.grid(row=0, column=0)
button_value.grid(row=0, column=1)

combo_price = ttk.Combobox(state="readonly", values=str_zone)
button_price = Button(text="按下取得各區域價格資料", font=("Arial", 14, "bold"), padx=5, pady=5, bg="blue", fg="light green",
                command=buttonPrice_clicked)

combo_price.grid(row=1, column=0)
button_price.grid(row=1, column=1)

label = tk.Label(window, text="")
label.grid(row=2, column=0)

# 視窗執行loop 進入等待處理物件的狀態
window.mainloop()

