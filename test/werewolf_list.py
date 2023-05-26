import time,re,json,csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

# 创建Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080") # 因為要做滾輪操作 一定要設置size
driver = webdriver.Chrome(options=chrome_options)

# 打開YouTube播放列表頁面
playlist_url = 'https://www.youtube.com/playlist?list=PLOS_sffDs6Q7AkC3JaIaemBDv2j3wIGqL'
driver.get(playlist_url)
print("開啟目標網站")

# 模擬滾動
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script('return document.documentElement.scrollHeight')

while True:
    # 滾動到底部
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    
    # 等待頁面加載
    time.sleep(SCROLL_PAUSE_TIME)
    
    # 計算新的滾動高度並檢查是否到達頁面底部
    new_height = driver.execute_script('return document.documentElement.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

# 獲取整個頁面的HTML
html_content = driver.page_source

# 將HTML保存到文本文件
with open('page.html', 'w', encoding='utf-8') as file:
    file.write(html_content)
    print("保存頁面資料HTML檔")

# 關閉瀏覽器
driver.quit()
print("關閉網頁")

# ==========================================================================================================

# 讀取本地HTML文件
with open('page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用BeautifulSoup解析網頁內容
soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有的播放清單項目
playlist_items = soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})
playlist=[]
# 逐項擷取標題和連結
for item in playlist_items:
    title = item.text.strip()  # 標題文字
    link = 'https://www.youtube.com' + item['href']  # 影片連結
    # 使用正則表達式找到日期和玩家列表
    pattern = r"(\d{4}\.\d{2}\.\d{2}-*\d{0,2}-*\d{0,2}\.*\d{0,2})(《[^》]+》(?:[^\(]*\((?:上|下)\) )?)(.+)"
    matches = re.findall(pattern, title)
    if matches:
        date = matches[0][0][:10]
        title = matches[0][1]
        temp = matches[0][2].replace("│","、",1).split('│')
        players = temp[0].split('、')
        if len(temp)>1:
            title+=temp[1]
        # print(title,date,players)
        playlist.append({
            'Title':title,
            'Date': date,
            'Players': players,
            'Link': link,
        })
    else:
        print("No match found.")
        print(f'{title}')
sorted_data = sorted(playlist, key=lambda x: x['Date'])

with open('狼人殺節目資料.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_data, file, ensure_ascii=False, indent=4)
    print("保存狼人殺節目資料JSON檔")
# 欄位名稱
fieldnames = ['Title', 'Date', 'Players','Link']

# 開啟 CSV 檔案並寫入資料
# with open("狼人殺節目清單.csv", 'w',encoding="utf-8", newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     # 寫入欄位名稱
#     writer.writeheader()
#     # 寫入資料
#     for item in sorted_data:
#         writer.writerow(item)
# print('CSV 檔案儲存完成')

# 將字典陣列轉換為 DataFrame
df = pd.DataFrame(sorted_data)
df = df.rename(columns={'Title': '標題', 'Date': '日期', 'Players': '玩家', 'Link': '連結'})
# 儲存為 Excel 檔案
df.to_excel('狼人殺節目清單.xlsx', index=False)
print("保存狼人殺節目資料EXCEL檔")
print("==========Done==========")