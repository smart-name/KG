import json
import requests
import datetime
from tqdm import tqdm

#为什么最后一个是梁各庄显示南各庄

start_date = datetime.datetime.strptime('2024-01-01',"%Y-%m-%d")
today_date = datetime.datetime.today() - datetime.timedelta(days=1)
url = 'https://nsbd.swj.beijing.gov.cn/service/jinRainList/list'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
}

# 当天早八点前没有昨天早八到今天早八数据
daily_raindata_list = []
ignore_stcdt = ['1111','2222','3333','4444','5555','6666','7777']
while start_date < today_date:
    print(start_date.strftime("%Y-%m-%d"))
    detail_raindata_list = []

    #爬取数据
    start_date = start_date + datetime.timedelta(days=1)
    data = {
        "queryDate": start_date.strftime("%Y-%m-%d")
    }

    result = requests.post(url=url, headers=headers, data=json.dumps(data)).json()

    #取出地区与降雨量并封装
    for detail in result['data']['rain_data']:
        #不记录平均降水量等内容
        if detail['stcdt'] not in ignore_stcdt:
            detail_raindata = {
                'region': detail['replace_name'],
                'rain': detail['RNFL']
            }
            detail_raindata_list.extend([detail_raindata])

    daily_raindata = {
        'date': (start_date - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        'stat': detail_raindata_list
    }
    daily_raindata_list.extend([daily_raindata])



with open('data/rain_data.json', 'w', encoding='utf-8') as fp:
    json.dump(daily_raindata_list,fp,ensure_ascii=False,indent=2)
    print("存储完成")

