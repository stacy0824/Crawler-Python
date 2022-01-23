import requests
from bs4 import BeautifulSoup
import json
import time
import random
import pandas as pd

x =0
df = pd.DataFrame(columns = ['articleTitle','articleUrl','articleTime','articleContent','CommentNB','CommentTime','Comment'])

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
headers = {'User-Agent':userAgent}
url = 'https://www.dcard.tw/service/api/v2/forums/parentchild/posts?limit=30&before=237540544'
res = requests.get(url, headers=headers)
jsonData = json.loads(res.text)


for pagedata in jsonData:
    articleid = pagedata['id']
    print(articleid)
    articleUrl = 'https://www.dcard.tw/f/parentchild/p/' + str(pagedata['id'])
    articleTitle = pagedata['title']
    articleCreatedAt = pagedata['createdAt']
    articleRes = requests.get(url=articleUrl, headers=headers)
    articleSoup = BeautifulSoup(articleRes.text, 'html.parser')
    articleContent = articleSoup.findAll(class_="phqjxq-0 gFINpq")[0].text
    articleTime = articleSoup.findAll(class_="sc-1eorkjw-0 dqGaqV")[0].findAll(class_="sc-1eorkjw-4 bhVPrQ")[1].text
    articleComment = articleSoup.findAll(id="comment")
    time.sleep(random.randint(10, 15) / 10)

    for j in articleComment:
        for i in j.findAll(class_="sc-1ybqnaa-0 fhyYWe"):
            try:
                CommentNB = i.findAll(class_="pi0hc4-3 hdkEmj")[0].text
                CommentTime = str(i.findAll(class_="pi0hc4-2 eCtXmy")[0]).split('"')[5]
                Comment = i.findAll(class_="phqjxq-0 gFINpq")[0].text

            except:
                pass
            df.loc[x] = [articleTitle,articleUrl,articleTime,articleContent,CommentNB,CommentTime,Comment]
            x += 1
df.to_csv(r'./dcard.csv',encoding = 'utf-8')





