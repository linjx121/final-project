import firebase_admin
from firebase_admin import credentials, firestore
import requests
from bs4 import BeautifulSoup

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

url = "https://www.starbucks.com.tw/stores/storesearch.jspx"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

payload = {
    "all": "true"  
}

print("正在發送請求至星巴克伺服器...")
response = requests.post(url, headers=headers, data=payload)
response.encoding = "utf-8"

sp = BeautifulSoup(response.text, "html.parser")

result = sp.select(".filmListAllX li") 

print(f"共抓取到 {len(result)} 筆門市資料")

for item in result:
    try:
        title_div = item.find("div", class_="filmtitle")
        runtime_div = item.find("div", class_="runtime")
        
        if title_div and runtime_div:
            title = title_div.text.strip()
            
            a_tag = title_div.find("a")
            store = a_tag.text.replace("/", "").strip() if a_tag else title
            
            address = runtime_div.text.replace("地址 :", "").strip()
            
            doc = {
                "title": title,
                "address": address,
            }
            
            print(f"將【{store}】寫入 Firebase...")
            doc_ref = db.collection("門市分店").document(store)
            doc_ref.set(doc)
            
    except Exception as e:
        print(f"處理單筆資料時發生錯誤: {e}")

print("程序執行完畢！")