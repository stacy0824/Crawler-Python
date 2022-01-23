import requests
from bs4 import BeautifulSoup
import json
import time
import random
import pandas as pd

x =0
df = pd.DataFrame(columns = ['productName','Content','Name','Time','Url'])

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
headers = {'User-Agent':userAgent}

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

        #找每個商品的標題
        #div[class="title"]會連同推薦區的品項也跑出來→要找'div[class="BaseProductList"]'裡的'div[class="title"]'
        productName = soup.select('div[class="ProductSectionList"]')


        for j in productName:
            for k in j.select('a[class="item"]'):
                productnb = k['href'].split('/')[2]
                activePage = 0

                newproductCommentUrl = 'https://mamilove.com.tw/v2/shopping/market/detail/'+str(productnb)+'/reviews?page='+str(activePage)
                headers = {'User-Agent': userAgent,'referer': 'https://mamilove.com.tw/market/'+str(productnb)+'/review'}
                newPdCommUrlRes = requests.get(newproductCommentUrl, headers=headers)
                jsonData = json.loads(newPdCommUrlRes.text)

                while len(jsonData["data"]["review"]) > 0:
                    newproductCommentUrl = 'https://mamilove.com.tw/v2/shopping/market/detail/'+str(productnb)+'/reviews?page='+str(activePage)
                    headers = {'User-Agent': userAgent,'referer': 'https://mamilove.com.tw/market/'+str(productnb)+'/review'}
                    newPdCommUrlRes = requests.get(newproductCommentUrl, headers=headers)
                    jsonData = json.loads(newPdCommUrlRes.text)
                    if len(jsonData["data"]["review"]) > 0:


                        for i in jsonData["data"]["review"]:
                            user_comment = i['reviews'][0]['user_comment']
                            if len(user_comment) > 0:

                                product_Name = jsonData["data"]['name']
                                reviewer_name = i['reviewer_name']
                                created_at = i['reviews'][0]['created_at']

                                df.loc[x] = [product_Name,user_comment,reviewer_name,created_at,'https://mamilove.com.tw/market/' + str(productnb) + '/review']
                                x +=1
                                time.sleep(random.randint(10,15)/100)


                    activePage += 1
df.to_csv(r'./mamilovdataBathtub.csv',encoding = 'utf-8')
