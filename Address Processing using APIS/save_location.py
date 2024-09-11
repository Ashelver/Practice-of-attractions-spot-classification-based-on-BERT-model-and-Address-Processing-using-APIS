import json

# with open('香港\马蜂窝\香港数据酒店数据.json','r',encoding="utf-8") as fp:
#     hotels = json.load(fp)

# result = []

# for hotel in hotels:
#     temp = {}
#     temp['Name'] = hotel['CName']
#     location = hotel['Introduction']['adress']
#     if isinstance(location,str):
#         temp['Location'] = location
#     else:
#         temp['Location'] = ''
#     # temp['Location'] = hotel['Introduction']['Location']
#     result.append(temp)

#     with open('Location.json', 'w', encoding='utf-8') as fp:
#         json.dump(result, fp=fp, ensure_ascii=False,indent=4)

# ----------------------------------------------------------------------


with open('香港/马蜂窝/香港地址翻译数据.json','r',encoding="utf-8") as fp:
    location = json.load(fp)

with open('香港\马蜂窝\香港数据酒店数据.json','r',encoding="utf-8") as fp:
    hotels = json.load(fp)

temp = []
for i in range(len(location)):
    data = {}
    data['Hotel'] = hotels[i]['CName']
    data['original_address'] = hotels[i]['Introduction']["adress"]
    try:
        data['processed_address'] = location[i]['trans_result'][0]['dst']
    except:
        data['processed_address'] = ""
    temp.append(data)

with open('Location.json', 'w', encoding='utf-8') as fp:
    json.dump(temp, fp=fp, ensure_ascii=False,indent=4)