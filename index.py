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
     
    firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    link = "<a href=/webhook>查詢分類</a><hr>"
    link += "<a href=/menu>菜單</a><hr>"
    return link

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]

   if action == "typeChoice":
    parameters = req["queryResult"].get("parameters", {})
    rate = parameters.get("type", "")
   
    if not rate:
        return make_response(jsonify({"fulfillmentText": "您打算喝甚麼種類的飲品呢？（例如：那堤、咖啡飲品、星冰樂）"}))
        
    info = f"我是星巴克機器人，為您找到相關飲品資訊：\n\n"
    db = firestore.client()
    collection_ref = db.collection("星巴克")
    docs = collection_ref.get()
    
    result = ""
    found_any = False
  
    rate_str = str(rate).strip()
    
    for doc in docs:
        drink_dict = doc.to_dict()
        
        db_type = str(drink_dict.get("type", ""))
        db_name = str(drink_dict.get("name", ""))
       
        if rate_str in db_type or rate_str in db_name:
            found_any = True
         
            price = drink_dict.get("how much(large size)", drink_dict.get("how much", "暫無資料"))
            coffeein = drink_dict.get("coffeein", "暫無資料")
            
            result += f"飲品名稱：{db_name}\n"
            result += f"價格(大杯)：{price} 元\n"
            result += f"咖啡因含量：{coffeein} mg\n"
            result += "-------------------\n"
            
    if found_any:
        info += result
    else:
        info = f"抱歉，目前我的資料庫裡還沒有與「{rate_str}」相關的飲品。您可以試試搜尋其他飲品！"

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
    # 確保是 storesearch (去掉了中間的 re)
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
        
        # 這裡直接呼叫，不要再重複 initialize_app 囉
        db = firestore.client()
        count = 0
        
        for store_item in store_items:
            title_element = store_item.find("div", class_="filmtitle")
            address_element = store_item.find("div", class_="runtime")
            
            if title_element and address_element:
                title = title_element.text.strip()
                address = address_element.text.replace("地址 :", "").strip()
                
                # 防止特殊符號導致 Firebase 報錯
                store_name = title.replace("/", "-").strip()
                
                doc = {
                    "title": title,
                    "address": address
                }
                
                # 寫入 Firebase
                db.collection("門市分店").document(store_name).set(doc)
                count += 1
        
        return f"爬蟲及存檔完畢！共成功匯入 {count} 筆門市資料至 Firebase。"
        
    except Exception as e:
        return f"程式執行失敗，錯誤原因: {str(e)}", 500