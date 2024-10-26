import json
import os
import time
import requests
from tqdm import tqdm

rain_path = './data/rain_data.json'
location_path='./data/location_search.json'

cityname = '北京市'
key = 'f429ece34d2c318d70069bfda222ed75'
url = 'https://restapi.amap.com/v5/place/text'

entity_list = []
entity_namelist = []

search_break = False

if not os.path.exists('location_search.json'):
    fp = open(location_path,'w', encoding='utf-8')
    fp.write('[]')
    fp.close()

with open(rain_path, 'r', encoding='utf-8') as f:
    daily_raindata_list = json.load(f)
    print('rain_data.json加载完毕')

with open(location_path, 'r', encoding='utf-8') as f:
    entity_list = json.load(f)
    print('location_search.json加载完毕')


#记录全部实体名称
for entity in entity_list:
    entity_namelist.append(entity['name'])

#更新实体信息
for detail_raindata in daily_raindata_list[-1]['stat']:
    if detail_raindata['region'] not in entity_namelist:
        entity = {
            'name': detail_raindata['region'],
            'coordinates': []
        }
        entity_list.extend([entity])
        entity_namelist.append(detail_raindata['region'])

#检查更新实体位置信息
for entity in tqdm(entity_list):
    if not entity['coordinates']:
        param = {
            'keywords': entity['name'],
            'region': cityname,
            'key': key
        }
        response = requests.get(url=url, params=param)
        result = response.json()

        if result['infocode'] == '10000':
            for poi in result['pois']:
                loc = poi['location'].split(',')
                longitude = loc[0]
                latitude = loc[1]
                location = {
                    'latitude': latitude,
                    'longitude': longitude
                }
                entity['coordinates'].extend([location])

            response.close()
            time.sleep(1)

        else:
            search_break = True
            print("未完成位置信息搜索")
            print(result)
            break


if not search_break:
    print('实体位置信息更新完毕')

with open(location_path, 'w', encoding='utf-8') as fp:
    json.dump(entity_list, fp, ensure_ascii=False, indent=2)
    print("存储完成")

    # # session = requests.Session()
    # location_list = []
    # print(detail_raindata['region'])
    # param = {
    #     'keywords': detail_raindata['region'],
    #     'region': cityname,
    #     'key': key
    # }
    # # result = requests.get(url=url, params=param)
    # response = requests.get(url=url, params=param)
    # result=response.json()
    #
    #
    # for poi in result['pois']:
    #     loc = poi['location'].split(',')
    #     longitude = loc[0]
    #     latitude = loc[1]
    #     location = {
    #         'latitude' : latitude,
    #         'longitude' : longitude
    #     }
    #     location_list.extend([location])
    #
    # entity = {
    #     'name' : detail_raindata['region'],
    #     'coordinates' : location_list
    # }
    #
    #
    # entity_list.extend([entity])
    #
    # response.close()
    # time.sleep(0.1)



# detail_raindata = daily_raindata_list[0]['stat'][0]
# location_list = []
# print(detail_raindata['region'])
# param = {
#     'keywords': detail_raindata['region'],
#     'region': cityname,
#     'key': key
# }
# result = requests.get(url=url, params=param).json()
#
# for poi in result['pois']:
#     loc = poi['location'].split(',')
#     longitude = loc[0]
#     latitude = loc[1]
#     location = {
#         'latitude': latitude,
#         'longitude': longitude
#     }
#     location_list.extend([location])
#
# entity = {
#     'name': detail_raindata['region'],
#     'coordinates': location_list
# }
#
# entity_list.extend([entity])
# print(entity_list)