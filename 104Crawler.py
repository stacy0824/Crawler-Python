import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

keyword = "資料分析師"


x =0
df = pd.DataFrame(columns = ['jobName','job_company','job_content','jobskill','workExp','major','other_skill','url'])

#網頁開發人員工作內的userAgent
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
headers = {'User-Agent':userAgent}

#range變更，可變更爬文頁數
page = 1
for i in range(10):
    #url 網址內的page會變動，所以用for迴圈更新page
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword='+ str(keyword) + 'page=' + str(page) + '&mode=s&jobsource=2018indexpoc&langFlag=0'
    #requests請求，網頁為get,使用requests.get()
    res= requests.get(url=url,headers=headers)
    #排版爬取到的資料，轉為text
    soup = BeautifulSoup(res.text, 'html.parser')
    #用Beautifulsoup 找全部有"-js-job-link"的class_標籤
    job_tits = soup.findAll(class_="js-job-link")
    #for迴圈 print出每個職缺的網址及網址內相關的內容
    for jobname in job_tits:
        #因為原先print出來的網址只有"//www.104.com.tw/job/6k2x6?jobsource=jolist_c_relevance"
        #所以加上"https:// 用變數objecturl接住
        #用get取出網址
        objecturl = 'https:' + (jobname.get('href'))
        #對每個職缺的網址進行請求
        resobject = requests.get(objecturl,headers=headers)
        objectsoup = BeautifulSoup(resobject.text, 'html.parser')
        # ***可print出objectsoup 但joncontent是空白
        joncontent = objectsoup.findAll(class_=".mb-5.r3.job-description__content.text-break")

        #因為職缺網頁內也是動態網頁，需要給Referer 才能對requests進行請求，所以headers要多加Referer
        #headers的type是字典，以字典方式新增，若會影響resobjest的headers就需另外設變數
        headers['Referer'] = objecturl
        #對職缺網頁內的動態網頁進行請求
        resapi = requests.get(url='https://www.104.com.tw/job/ajax/content/'+objecturl.split("/")[4].split("?")[0],headers=headers)
        # #轉成json格式
        resapi_dict = resapi.json()
        #找出json內所需要的資料
        jobName = resapi_dict['data']['header']['jobName']
        job_company = resapi_dict['data']['header']['custName']
        job_content = resapi_dict['data']['jobDetail']['jobDescription']
        workExp = resapi_dict['data']['condition']['workExp']
        major = resapi_dict['data']['condition']['major']
        job_skill_ = resapi_dict['data']['condition']['specialty']
        other_skill = resapi_dict['data']['condition']['other']
        jobskills =""
        for jobskill in job_skill_:
            jobskills += str(jobskill['description'])+","

        print(jobName)
        print(job_company)
        print(job_content)
        print(workExp)
        print(major)
        print(other_skill)
        print(jobskills)


        df.loc[x] = [jobName,job_company,job_content,jobskills,workExp,major,other_skill,objecturl]
        x += 1
    # 對搜尋的網頁page+1，進行多頁爬取
    page += 1
df.to_csv(r'./104crawler.csv',encoding = 'utf-8')









