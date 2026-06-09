from google import genai

from google.genai import types 

import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template,request,make_response,jsonify
from datetime import datetime

import os
import json
from firebase_admin import credentials, initialize_app

# 讀取環境變數中的 Firebase 金鑰字串
firebase_creds_str = os.environ.get('FIREBASE_CREDENTIALS')

if firebase_creds_str:
    # 將字串轉換為字典 (Dict) 格式
    cred_dict = json.loads(firebase_creds_str)
    cred = credentials.Certificate(cred_dict)
else:
    # 備用方案：如果本地跑還是想用檔案形式
    cred = credentials.Certificate("serviceAccountKey.json")
     
    initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    link = "<a href=/webhook>查詢分類</a><hr>"
    link += "<a href=/menu>菜單</a><hr>"
    link += "<a href=/webdemo>聊天機器人</a><hr>"
    return link

@app.route("/webdemo")
def webdemo():
    return render_template("webdemo.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]

    if action == "typeChoice":
        parameters = req["queryResult"].get("parameters", {})
        rate = parameters.get("type", "")
        
        if not rate:
            return make_response(jsonify({"fulfillmentText": "您打算喝甚麼種類的飲品呢？\n(例如：那堤、咖啡、星冰樂)"}))
                
            db = firestore.client()
            collection_ref = db.collection("星巴克")
            docs = collection_ref.get()
            
            info = f"為您找到「{rate}」的相關飲品結果：\n"
            info += "━━━━━━━━━━━━━━━\n" # 分隔線
            
            result = ""
            found_any = False
            rate_str = str(rate).strip()
            
            for doc in docs:
                drink_dict = doc.to_dict()
                db_type = str(drink_dict.get("type", ""))
                db_name = str(drink_dict.get("name", ""))
              
                if rate_str in db_type or rate_str in db_name:
                    found_any = True
                    
                    price = drink_dict.get("how much(large size)", "暫無資料")
                    caffeine = drink_dict.get("coffeein", "暫無資料")
                  
                    result += f"飲品：{db_name}\n"
                    result += f"價格：{price} 元\n"
                    result += f"咖啡因：{caffeine} mg\n"
                    result += "--------------------------------\n"
                    
            if found_any:
                info += result
                info += "\n點擊下方選單可以查詢更多資訊喔！"
            else:
                info = f"抱歉，我找不到「{rate_str}」。\n試試看搜尋「那堤」或「咖啡」？"

            return make_response(jsonify({"fulfillmentText": info}))

@app.route("/menu")
def menu():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("星巴克")
    docs = collection_ref.order_by("name", direction=firestore.Query.DESCENDING).limit(5).get()
    
    for doc in docs:
        Result += str(doc.to_dict()) + "<br>"
    return Result

@app.route("/store")
def store():
    url = "https://www.starbucks.com.tw/stores/storesearch.jspx"
    
    payload = {
        "all": "true"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        Data = requests.post(url, data=payload, headers=headers, timeout=10)
        Data.encoding = "utf-8"
        
        soup = BeautifulSoup(Data.text, "html.parser")
        store_items = soup.select(".filmListAllX li")
     
        db = firestore.client()
        count = 0
        
        for store_item in store_items:
            title_element = store_item.find("div", class_="filmtitle")
            address_element = store_item.find("div", class_="runtime")
            
            if title_element and address_element:
                title = title_element.text.strip()
                address = address_element.text.replace("地址 :", "").strip()
              
                store_name = title.replace("/", "-").strip()
                
                doc = {
                    "title": title,
                    "address": address
                }
            
                db.collection("門市分店").document(store_name).set(doc)
                count += 1
        
        return f"爬蟲及存檔完畢！共成功匯入 {count} 筆門市資料至 Firebase。"
        
    except Exception as e:
        return f"程式執行失敗，錯誤原因: {str(e)}", 500