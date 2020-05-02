#爬取外匯資料
import requests
from bs4 import BeautifulSoup

#設定目標：擷取外匯金額資料
url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
raw_html = resp.text

soup = BeautifulSoup(raw_html, "html.parser")
#print(soup)

dollars = soup.select("#ie11andabove tbody div:nth-of-type(3)")
d_value_1 = soup.select("#ie11andabove tbody td:nth-of-type(3)") #現金匯款
d_value_2 = soup.select("#ie11andabove tbody td:nth-of-type(5)") #即期匯率

exchange_dict={}

for x in range(0,len(dollars)):    
    if (d_value_2[x].text.strip()!='-'):
        exchange_value=float(d_value_2[x].text.strip())
    else:
        exchange_value=float(d_value_1[x].text.strip())
    exchange_dict[dollars[x].text.strip()]=exchange_value

#-----------------------------------------
#建立GUI
import tkinter as tk
import tkinter.ttk as tt

window = tk.Tk()
window.title('Currency Exchange')
window.geometry('400x320')

labName = tk.Label(window, text = 'NTD amount:', justify=tk.RIGHT, width=150)
labName.place(x=10, y=10, width=100, height=20)

varName = tk.StringVar()
varName.set('')
entName = tk.Entry(window, width = 120, textvariable = varName)
entName.place(x=110, y=10, width=120, height=20)

labGrade = tk.Label(window, text = 'Currency:', justify=tk.RIGHT, width=150)
labGrade.place(x=10, y=40, width=100, height=20)

def value_show(event):
    exchange_key = comGrade.get()
    exchange_value=float(exchange_dict.get(exchange_key))
    labexchange.config(text= 'current rate:' + str(exchange_value))
    
comGrade = tt.Combobox(window, width=50, values=list(exchange_dict.keys()))
comGrade.bind("<<ComboboxSelected>>",value_show)  #繫結事件,(下拉選單框被選中時，繫結go()函式)
comGrade.place(x=110, y=40, width=120, height=20)

labexchange = tk.Label(window, text = '', justify=tk.LEFT, width=150)
labexchange.place(x=230, y=40, width=150, height=20)

def count_value():
    exchange_key = comGrade.get()
    exchange_value=float(entName.get())/float(exchange_dict.get(exchange_key))
    labName.config(text='You will get:'+str(exchange_value)+str(exchange_key))
    
btn_exg = tk.Button(window, text='To Exchange', command=count_value)
btn_exg.place(x=110, y=100, width=100, height=20)

labName = tk.Label(window, text = '', justify=tk.LEFT, width=400)
labName.place(x=50, y=120, width=400, height=20)

window.mainloop()

                             