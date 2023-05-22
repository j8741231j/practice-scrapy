import requests,re,json
from bs4 import BeautifulSoup

# # 指定要爬取的網址
# url = 'https://www.youtube.com/playlist?list=PLOS_sffDs6Q7AkC3JaIaemBDv2j3wIGqL'

# # 發送GET請求並獲取網頁內容
# response = requests.get(url)

# # 使用BeautifulSoup解析網頁內容
# soup = BeautifulSoup(response.text, 'html.parser')

# # print(soup.prettify())
# # 找到所有的播放清單項目
# script_tags = soup.find_all('script')
# id_list=[]
# title_list=[]
# merge_list=[]
# for script_tag in script_tags:
#     if script_tag.text is not None:
#         for script_tag in script_tags:
#             if script_tag.text is not None:
#                 # 使用正則表達式找到所有的"videoId":"..."
#                 pattern = r'"videoId":"([^"]*)"'
#                 matches = re.findall(pattern, script_tag.text)
#                 for match in matches:
#                     if match not in id_list:
#                         id_list.append(match)
#                 pattern = r'"label":"([^"]*)"'
#                 matches = re.findall(pattern, script_tag.text)
#                 for match in matches:
#                     if "【娛樂百分百】" in match and match not in title_list:
#                         title_list.append(match)

# for i in range(len(id_list)):
#     merge_list.append({
#         "CreateTime":title_list[i][7:17],
#         "Url":"https://www.youtube.com/watch?v="+id_list[i],
#         "Title":title_list[i]
#     })
# print(merge_list)

import requests

# 設定請求的URL和參數
url = 'https://www.youtube.com/youtubei/v1/browse'
params = {
    'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
    'prettyPrint': 'false'
}
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101\
            Safari/537.36', }

# 發送POST請求
response = requests.post(url, params=params,headers=headers)

# 檢查響應狀態碼
if response.status_code == 200:
    # 成功獲取響應
    content = response.json()  # 將響應轉換為JSON格式
    # 在這裡對獲取的數據進行處理
    # ...
else:
    # 請求失敗，處理錯誤
    print('Request failed with status code:', response.status_code)
