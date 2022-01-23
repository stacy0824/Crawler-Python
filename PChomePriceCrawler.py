import requests
import json
import pandas as pd


x =0
df = pd.DataFrame(columns = ['productName','price'])

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
headers = {'cookie': 'ECC=GoogleBot','User-Agent':userAgent}
#PChome產品類別的代號
list = ['DEAU','DEAI','DAAO']
#for迴圈帶入網址
for pdlist in list:
    allpdUrl = 'https://ecapi.pchome.com.tw/cdn/ecshop/cateapi/v1.6/region/'+str(pdlist)+'/menu&_callback=jsonp_nemu&5467205?_callback=jsonp_nemu'
    allres = requests.get(allpdUrl,headers=headers)
    #將try{jsonp_nemu([ 與 );}catch(e){if(window.console){console.log(e);} 去除，取出json格式
    alljsondatas = allres.text.replace('try{jsonp_nemu(','').replace(');}catch(e){if(window.console){console.log(e);}}','')
    alljsondata = json.loads(alljsondatas)
    pdlist = []

    for allpdid in alljsondata:
        for allpdId in allpdid['Nodes']:
            pdlist += [allpdId['Id']]

    for pdnb in pdlist:
        sum = 5
        for k in range(10):
            url = 'https://ecapi.pchome.com.tw/cdn/ecshop/prodapi/v2/store/'+str(pdnb)+'/prod&offset='+str(sum)+'&limit=36&fields=Id,Nick,Pic,Price,Discount,isSpec,Name,isCarrier,isSnapUp,isBigCart,OriginPrice,iskdn,isPreOrder24h,PreOrdDate,isWarranty,isFresh,isBidding,isETicket,ShipType,isO2O&_callback=jsonp_prodgrid?_callback=jsonp_prodgrid'
            res = requests.get(url,headers=headers)
            if res.text == 'try{jsonp_prodgrid([]);}catch(e){if(window.console){console.log(e);}}':
                break
            jsondatas = res.text.replace('try{jsonp_prodgrid(','').replace(');}catch(e){if(window.console){console.log(e);}}','').replace('\/',"/")
            jsondata = json.loads(jsondatas)

            for i in jsondata:
                productname = i['Name']
                productprice = i['Price']['P']
                df.loc[x] = [productname, productprice]
                x += 1

            sum += 36

df.to_csv(r'./PricePChomedata.csv',index=0, encoding='utf-8')