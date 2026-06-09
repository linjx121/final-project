import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

docs =[
{
  "name": "黑糖風味奶香咖啡",
  "type": "咖啡飲品",
  "how much(large size)":160 ,
  "coffeein":293
},
{
  "name": "蘋果山茶花風味美式",
  "type": "咖啡飲品",
  "how much(large size)":135 ,
  "coffeein":163
},
{
  "name": "鹹焦糖奶油爆米花風味那堤",
  "type": "咖啡飲品",
  "how much(large size)":185 ,
  "coffeein":182
},
{
  "name": "椰香綿雲那堤",
  "type": "咖啡飲品",
  "how much(large size)":200 ,
  "coffeein":163
},
{
  "name": "那堤",
  "type": "咖啡飲品",
  "how much(large size)":140 ,
  "coffeein":182
},
{
  "name": "焦糖瑪奇朵",
  "type": "咖啡飲品",
  "how much(large size)":175 ,
  "coffeein":195
},
{
  "name": "馥列白",
  "type": "咖啡飲品",
  "how much(large size)":155 ,
  "coffeein":247
},
{
  "name": "可可瑪奇朵",
  "type": "咖啡飲品",
  "how much(large size)":160 ,
  "coffeein":195
},
{
  "name": "美式咖啡",
  "type": "咖啡飲品",
  "how much(large size)":115 ,
  "coffeein":293
},
{
  "name": "卡布奇諾",
  "type": "咖啡飲品",
  "how much(large size)":140 ,
  "coffeein":195
},
{
  "name": "摩卡",
  "type": "咖啡飲品",
  "how much(large size)":155 ,
  "coffeein":228
},
{
  "name": "特選馥郁那堤",
  "type": "咖啡飲品",
  "how much(large size)":165 ,
  "coffeein":348
},
{
  "name": "草莓風味抹茶那堤",
  "type": "茶瓦納",
  "how much(large size)":175 ,
  "coffeein":146
},
{
  "name": "伯爵茶那堤",
  "type": "茶瓦納",
  "how much(large size)":170 ,
  "coffeein":282
},
{
  "name": "福吉茶那堤",
  "type": "茶瓦納",
  "how much(large size)":155 ,
  "coffeein":130
},
{
  "name": "經典紅茶那堤",
  "type": "茶瓦納",
  "how much(large size)":155 ,
  "coffeein":277
},
{
  "name": "醇濃抹茶那堤",
  "type": "茶瓦納",
  "how much(large size)":160 ,
  "coffeein":253
},
{
  "name": "咖啡星冰樂",
  "type": "星冰樂(咖啡)",
  "how much(large size)":135 ,
  "coffeein":96
},
{
  "name": "焦糖星冰樂",
  "type": "星冰樂(咖啡)",
  "how much(large size)":160 ,
  "coffeein":130
},
{
  "name": "摩卡可可碎片星冰樂",
  "type": "星冰樂(咖啡)",
  "how much(large size)":175 ,
  "coffeein":95
},
{
  "name": "焦糖可可碎片星冰樂",
  "type": "星冰樂(咖啡)",
  "how much(large size)":175 ,
  "coffeein":130
},
{
  "name": "巧克力可可碎片星冰樂",
  "type": "星冰樂",
  "how much(large size)":150 ,
  "coffeein":30
},
{
  "name": "醇濃抹茶星冰樂",
  "type": "星冰樂",
  "how much(large size)":175 ,
  "coffeein":160
},
{
  "name": "香草風味星冰樂",
  "type": "星冰樂",
  "how much(large size)":125 ,
  "coffeein":0
},
{
  "name": "雙果果汁星冰樂",
  "type": "星冰樂",
  "how much(large size)":145 ,
  "coffeein":0
},
{
  "name": "醇濃抹茶那堤",
  "type": "星冰樂",
  "how much(large size)":160 ,
  "coffeein":253
},
{
  "name": "紅心芭樂冷萃咖啡",
  "type": "冷萃咖啡",
  "how much(large size)":160 ,
  "coffeein":195
},
{
  "name": "冷萃咖啡",
  "type": "冷萃咖啡",
  "how much(large size)":145 ,
  "coffeein":369
},
{
  "name": "經典特調冷萃咖啡",
  "type": "冷萃咖啡",
  "how much(large size)":170 ,
  "coffeein":352
},
{
  "name": "香檸蜜柚冷萃咖啡",
  "type": "冷萃咖啡",
  "how much(large size)":160 ,
  "coffeein":323
},
{
  "name": "夏日冰柚冷萃咖啡",
  "type": "冷萃咖啡",
  "how much(large size)":160 ,
  "coffeein":225
},
{
  "name": "檸檬冷萃咖啡",
  "type": "冷萃咖啡",
  "how much(large size)":160 ,
  "coffeein":323
},
{
  "name": "鹹焦糖風味氮氣歐蕾",
  "type": "冷萃咖啡(氮氣)",
  "how much(large size)":190 ,
  "coffeein":437
},
{
  "name": "經典特調氮氣冷萃咖啡",
  "type": "冷萃咖啡(氮氣)",
  "how much(large size)":200 ,
  "coffeein":450
},
{
  "name": "氮氣冷萃咖啡",
  "type": "冷萃咖啡(氮氣)",
  "how much(large size)":175 ,
  "coffeein":475
},
{
  "name": "氮氣冷萃咖啡歐蕾",
  "type": "冷萃咖啡(氮氣)",
  "how much(large size)":175 ,
  "coffeein":437
},
{
  "name": "草莓巴西莓風味冰雪星沁爽",
  "type": "星沁爽",
  "how much(large size)":130 ,
  "coffeein":75
},
{
  "name": "芒果火龍果冰雪星沁爽",
  "type": "星沁爽",
  "how much(large size)":130 ,
  "coffeein":81
},
{
  "name": "蘋果山竹風味爆爆檸檬星沁爽",
  "type": "星沁爽",
  "how much(large size)":125 ,
  "coffeein":163
},
{
  "name": "蘋果山竹風味爆爆椰奶星沁爽",
  "type": "星沁爽",
  "how much(large size)":135 ,
  "coffeein":163
},
{
  "name": "芒果火龍果檸檬星沁爽",
  "type": "星沁爽",
  "how much(large size)":110 ,
  "coffeein":54
},
{
  "name": "芒果火龍果椰奶星沁爽",
  "type": "星沁爽",
  "how much(large size)":110 ,
  "coffeein":49
},
{
  "name": "草莓巴西莓檸檬風味星沁爽",
  "type": "星沁爽",
  "how much(large size)":190 ,
  "coffeein":437
},
{
  "name": "草莓巴西莓椰奶風味星沁爽",
  "type": "星沁爽",
  "how much(large size)":120 ,
  "coffeein":49
},
{
  "name": "經典巧克力",
  "type": "其他飲料",
  "how much(large size)":160 ,
  "coffeein":48
},
{
  "name": "冰經典巧克力",
  "type": "其他飲料",
  "how much(large size)":160 ,
  "coffeein":37
},
]
# doc_ref = db.collection("星巴克").document("Final project")
# doc_ref.set(doc)

for doc in docs:
    drink_name = doc["name"]
    db.collection("星巴克").document(drink_name).set(doc)
    print(f"成功寫入飲品：{drink_name}")
