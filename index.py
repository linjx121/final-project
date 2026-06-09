from google import genai
from google.genai import types 

import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template,request,make_response,jsonify
from datetime import datetime

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 判斷是在 Vercel 還是本地
if os.path.exists('serviceAccountKey.json'):
    # 本地環境：讀取檔案
    cred = credentials.Certificate('serviceAccountKey.json')
else:
    # 雲端環境：從環境變數讀取 JSON 字串
    firebase_config = os.getenv('FIREBASE_CONFIG')
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)

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

    if (action == "typeChoice"):
        rate =  req["queryResult"]["parameters"]["type"]
        info = "我是星巴克機器人，您選擇飲品是：" + type + "，推薦飲品：\n"
        db = firestore.client()
        collection_ref = db.collection("星巴克")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["type"]:
                result += "價格：" + dict["how much(large size)"] + "\n"
                result += "咖啡因含量：" + dict["coffeein"] + "\n\n"
        info += result

    elif(action == "input.unknown"):
        #info = req["queryResult"]["queryText"]
        instruction_text = (
            "你是一個熱心且知識豐富的專業智慧助理。"
            "對於使用者的提問，請回覆重點的關鍵字，不要重述問題。"         
        )


        ai_config = types.GenerateContentConfig(
            max_output_tokens=500, 
            system_instruction=instruction_text
        )
        response = client.models.generate_content(
            model='gemini-3.1-flash-lite', 
            contents=req["queryResult"]["queryText"],
            config=ai_config,
        )

        if response.text:
            info = response.text
        else:
            info = "抱歉，我現在無法生成回應，請稍後再試。"

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