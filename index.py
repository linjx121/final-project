import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template, request, make_response, jsonify

import firebase_admin
from firebase_admin import credentials, firestore


firebase_creds_str = os.environ.get('FIREBASE_CREDENTIALS')

if not firebase_admin._apps:
    if firebase_creds_str:
        cred_dict = json.loads(firebase_creds_str)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    else:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

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
    query_result = req.get("queryResult", {})
    action = query_result.get("action", "")

    if action == "typeChoice":
        parameters = query_result.get("parameters", {})
        rate = parameters.get("type", "")
        
        if isinstance(rate, list):
            rate = rate[0] if len(rate) > 0 else ""
            
        rate_str = str(rate).strip()
        
        db = firestore.client()
        collection_ref = db.collection("星巴克")
        docs = collection_ref.get()
      
        if rate_str == "" or rate_str == "飲品查詢" or rate_str == "咖啡飲品":
            info = f"為您列出星巴克精選飲品菜單：\n"
        else:
            info = f"為您找到「{rate_str}」的相關飲品結果：\n"
        info += "━━━━━━━━━━━━━━━━━\n"
        
        result = ""
        found_any = False
        
        for doc in docs:
            drink_dict = doc.to_dict()
            
            db_type = str(drink_dict.get("type", "")).strip()
            db_name = str(drink_dict.get("name", "")).strip()
            
            if rate_str == "" or rate_str == "飲品查詢" or rate_str == "咖啡飲品" or (rate_str in db_type) or (rate_str in db_name):
                found_any = True
        
                price = drink_dict.get("how much(large size)", "暫無資料")
                coffeein = drink_dict.get("coffeein", "暫無資料")
                
                result += f"🔹 飲品名稱：{db_name}\n"
                result += f"💰 價格(大杯)：{price} 元\n"
                result += f"⚡ 咖啡因含量：{coffeein} mg\n"
                result += "---------------------------------\n"
                
        if found_any:
            info += result
        else:
            info = f"抱歉，目前我的資料庫裡還沒有與「{rate_str}」相關的飲品。您可以試試搜尋其他飲品！"
            
        return make_response(jsonify({"fulfillmentText": info}))
  
    return make_response(jsonify({"fulfillmentText": "讓我想想喝甚麼！"}))

if __name__ == "__main__":
    app.run(debug=True)
