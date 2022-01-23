import requests
from bs4 import BeautifulSoup
import pandas as pd

#建立dataframe欄位有productName跟price
x =0
df = pd.DataFrame(columns = ['productName','price'])

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
headers = {'User-Agent':userAgent}

#需爬蟲產品類別
productlist = ['newchairforeat','babycarrier', 'outdoor-use', 'baby-car-seat', 'baby-bottles', 'milkbottle-sterilization', 'baby-nipples',  'diaper',  'baby-food', 'Bathtub']

for l in productlist:

    pageUrl = 'https://mamilove.com.tw/market/category/'+str(l)
    pageUrlRes = requests.get(pageUrl,headers=headers)
    pageUrlSoup = BeautifulSoup(pageUrlRes.text,'html.parser')
    pageRange = pageUrlSoup.select('a[class="page"]')[-2].text

    for page in range(1,int(pageRange)+1):
        url = 'https://mamilove.com.tw/market/category/'+l+'?page='+str(page)

        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        NameandPrice = soup.select('div[class="InnerProductCard clickable"]')
        for i in NameandPrice:
            #篩選出class是title compact shorten 和 title，清除換行及空值
            productname = i.select(".title compact shorten,.title")[0].text.split('\n')[1].replace("    ","")
            productprice = i.select('div[class="highlight-price"]')[0].text.split(' ')[1]
            print(productname)
            print(productprice)
            #將爬下來的產品名稱及價格新增至DataFrame欄位內
            df.loc[x] = [productname, productprice]
            x +=1

df.to_csv(r'./Pricemamilovdata.csv',encoding = 'utf-8')