import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

x =0
df = pd.DataFrame(columns = ['productName','price'])

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
headers = {'User-Agent':userAgent}

product = ['2700400000','2701300000','2700200000','2704700000','2704100000','2704300000','2702700000']

for productlist in product:
    for page in range(50):
        url = 'https://m.momoshop.com.tw/category.momo?cn='+str(productlist)+'&page='+str(page)+'&sortType=6&imgSH=fourCardStyle'

        res = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        error=soup.select('.errorBox')
        if len(error) > 0:

            print(url)
            listsoup = soup.select('.productInfo')
            for i in listsoup:
                ProductName = i.select(".prdName")[0].text
                ProductPrice = i.select(".price")[0].text
                print(ProductName)
                print(ProductPrice)
                df.loc[x] = [ProductName, ProductPrice]
                x += 1
        time.sleep(random.randint(10, 40) / 100)


df.to_csv(r'./Pricemomodata.csv', encoding='utf-8')