import requests
from bs4 import BeautifulSoup
import threading
import time,json,re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import html,random

# 獲取頁數
# 创建Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080") # 因為要做滾輪操作 一定要設置size
driver = webdriver.Chrome(options=chrome_options)

# 打開頁面
playlist_url = 'https://www.104.com.tw/jobs/search/?keyword=AR VR MR XR&page=1'
driver.get(playlist_url)
select_element = driver.find_element(By.CSS_SELECTOR, 'select.page-select.js-paging-select.gtm-paging-top')
option_elements = select_element.find_elements(By.TAG_NAME, 'option')
# 獲取<option>元素的数量
option_count = len(option_elements)
print(f"頁数：{option_count}")
driver.quit()


link_list=[]
def list_page(index):
    url = 'https://www.104.com.tw/jobs/search/'
    print(f'現在爬取第{index+1}頁')
    params = {
        'keyword':'AR VR MR XR',
        'page':index+1,
    }

    # 傳送 GET 請求獲取網頁內容
    response = requests.get(url, params=params)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析網頁內容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 在這裡進行資料的萃取和處理
        # 可以使用 soup.select 或其他相關方法選取指定的元素或屬性
        # 例如，獲取標題元素
        title_element = soup.select_one('title')
        if title_element:
            title = title_element.text
            # print('網頁標題:', title)

        # 獲取所有 class="b-block__left" 的 div 元素
        divs = soup.find_all('div', class_='b-block__left')
        # 輸出每個 div 的內容
        for div in divs:
            if div.find('svg', class_='b-icon--gray b-icon--w18'):
                continue
            links = div.find_all('a', class_='js-job-link')
            # 輸出每個 <a> 元素的 link 和 text
            for link in links:
                link_url = 'https:'+link['href']
                link_text = link.text
                link_list.append(link_url)
                # print("Text:", link_text)
    else:
        print('請求失敗:', response.status_code)

# 建立 n 個子執行緒
threads = []
for i in range(option_count):
  threads.append(threading.Thread(target = list_page, args = (i,)))
  threads[i].start()

# 等待所有子執行緒結束
for i in range(option_count):
  threads[i].join()


with open('職缺連結清單.json', 'w', encoding='utf-8') as file:
    json.dump(link_list, file, ensure_ascii=False, indent=4)
    print("保存職缺連結清單JSON檔")
print("Done.")

# 讀取資料
with open('職缺連結清單.json') as f:
    link_list = json.load(f)
    print(len(link_list))
description_list=[]


def get_description(index):
    url = link_list[index]
    print(f'正在處理 {url}')
    # 傳送 GET 請求獲取網頁內容
    response = requests.get(url)
    # 檢查請求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析網頁內容
        soup = BeautifulSoup(response.text, 'html.parser')
        # 可以使用 soup.select 或其他相關方法選取指定的元素或屬性
        try:
            script_content = soup.select('html script[type="application/ld+json"]')[0].contents[0]
        except:
            return
        article_str = re.sub(r"[\r\n\b]","",script_content) #他的json個是會有換行錯誤
        data = json.loads(article_str)
        for m in data:
            if "description" in m:
                decoded_string = html.unescape(m["description"])
                soup = BeautifulSoup(decoded_string, 'html.parser')
                text = soup.get_text().replace('\t','').replace('／','/')
                # 切割字串
                segments = text.split("- ")
                result = {"職缺名稱":m["title"],"職缺網址":url}
                for segment in segments:
                    if "【工作內容】" in segment:
                        end_index = segment.find("】")
                        value = segment[end_index+1:]
                        result["工作內容"] = value
                    else:
                        key_value = segment.split("：")
                        key = key_value[0].strip()
                        result[key] = "" if len(key_value)<2 else key_value[1].strip()
                description_list.append(result)
                break
    else:
        print('請求失敗:', response.status_code)


# 建立 n 個子執行緒
threads = []
error_list=[]
for i in range(len(link_list)):
    delay = random.uniform(0, 0.05)
    time.sleep(delay)
    threads.append(threading.Thread(target = get_description, args = (i,)))
    try:
        threads[i].start()
    except:
        error_list.append(i)

# 等待所有子執行緒結束
for i in range(len(link_list)):
    threads[i].join()

print("Done.")
print('被封鎖的',error_list)

with open('職缺內容.json', 'w', encoding='utf-8') as file:
    json.dump(description_list, file, ensure_ascii=False, indent=4)
    print("職缺內容JSON檔")
