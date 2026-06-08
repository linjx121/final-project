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

client = genai.Client()

@app.route("/")
def index():
    link += "<a href=/webhook>查詢分類</a><hr>"
    link += "<a href=/webdemo>聊天機器人</a><hr>"
    link += "<a href=/AI>gmini</a><hr>"
    link += "<a href=/ask>輸入問題</a><hr>"
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


@app.route("/spidermovie")
def spidermovie():
    R  = ""
    db = firestore.client()

    import requests
    from bs4 import BeautifulSoup
    url = "http://www.atmovies.com.tw/movie/next/"
    Data = requests.get(url)
    Data.encoding = "utf-8"
   
    sp = BeautifulSoup(Data.text, "html.parser")
    lastUpdate = sp.find(class_="smaller09").text.replace("更新時間：","")

    result=sp.select(".filmListAllX li")
    total = 0 
    for item in result:
        total += 1
        movie_id = item.find("a").get("href").replace("/movie/","").replace("/","")
        title = item.find(class_="filmtitle").text
        picture = "https://www.atmovies.com.tw" + item.find("img").get("src")
        hyperlink = "https://www.atmovies.com.tw" + item.find("a").get("href")
        showDate = item.find(class_="runtime").text[5:15]
          

        doc = {
              "title": title,
              "picture": picture,
              "hyperlink": hyperlink,
              "showDate": showDate,
              "lastUpdate": lastUpdate
        }

        doc_ref = db.collection("電影2B").document(movie_id)
        doc_ref.set(doc)

        R += "網站最近更新日期：" + lastUpdate + "<br>"
        R += "總共爬取" + str(total) + "部電影到資料庫"
    return R


@app.route("/movie1", methods=['GET', 'POST'])
def movie1():
    keyword = ""
    movies = []  # 用來存放篩選後的電影資料
    
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        
        url = "http://www.atmovies.com.tw/movie/next/"
        Data = requests.get(url)
        Data.encoding = "utf-8"
        sp = BeautifulSoup(Data.text, "html.parser")
        result = sp.select(".filmListAllX li")
        
        for item in result:
            title = item.find("img").get("alt") # 電影名稱
            
            # 關鍵字篩選：如果名稱包含關鍵字，才加入清單
            if keyword in title:
                link = "https://www.atmovies.com.tw" + item.find("a").get("href")
                img_src = "https://www.atmovies.com.tw" + item.find("img").get("src")
                
                # 存成字典方便 HTML 讀取
                movies.append({
                    "title": title,
                    "link": link,
                    "img": img_src
                })

    return render_template("movie1.html", movies=movies, keyword=keyword)


@app.route("/menu")
def menu():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("星巴克")    
    docs = collection_ref.get()
    docs = collection_ref.order_by(direction=firestore.Query.DESCENDING).limit(5).get()    
    for doc in docs:         
        Result += str(doc.to_dict()) + "<br>"    
    return Result
