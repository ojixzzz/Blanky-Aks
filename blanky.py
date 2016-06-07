import sys
import time
import telepot
import requests
import json
from threading import Thread
from datetime import datetime, timedelta
from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, TELEGRAM_TOKEN, LOGIN_URL, LOGIN_DATA

mongoDB = MongoClient(MONGO_HOST, MONGO_PORT)
database = mongoDB.blankyaks
db_groups = database.groups

Total_test = 0
Total_error = 0
Last_error = False
pengingat1 = False
pengingat2 = False
def getGroups():
    cursor = db_groups.find().sort([("$natural", -1)]).limit(10)
    return cursor

def Pengingat():
    global pengingat1
    global pengingat2

    sekarang = int(datetime.now().strftime("%H%M%S"))
    if sekarang > 110000:
        if pengingat1==False:
            pengingat1 = True
            for row in getGroups():
                bot.sendMessage(row['group_id'], 'Miaauuu \nSelamat bekerja dap!')
    else:
        pengingat1 = False

    if sekarang > 170000:
        if pengingat2==False:
            pengingat2 = True
            for row in getGroups():
                bot.sendMessage(row['group_id'], 'Miaauuu \nUdah waktunya pulang')
    else:
        pengingat2 = False

def TestLogin():
    global Total_test
    global Total_error

    Total_test += 1 
    headers = {
        'User-Agent': 'BlankyBot Aks v1.0'
    }
    url = LOGIN_URL
    datapost = LOGIN_DATA
    req = requests.post(url, headers=headers, data=json.dumps(datapost))
    if req.status_code != 200:
        Total_error += 1
        return 'Miaauuu \nLogin bermasalah kang, status code bukan 200'

    if req.text:
        resjson = json.loads(req.text)
        if resjson['meta']['code'] != 200:
            Total_error += 1
            return 'Miaauuu \nLogin bermasalah kang, err message : %s' % resjson['meta'].get('error_message')
        
    return False

def blanky_main():
    global Total_test
    global Total_error
    global Last_error
    while True:
        if not getGroups():
            bot.sendMessage('89093938', 'Grup_id diluar kendali mastah')

        if Total_test > 1000:
            Total_test = 0
            Total_error = 0

        testx = TestLogin()
        if testx:
            testx = TestLogin()
            if testx:
                Last_error=True
                for row in getGroups():
                    bot.sendMessage(row['group_id'], testx)
        else:
            if Last_error==True:
                Last_error=False
                for row in getGroups():
                    bot.sendMessage(row['group_id'], 'Miaauuu \nLogin sudah normal mas')

        Pengingat()
        time.sleep(60)

def handle(msg):
    global Total_test
    global Total_error
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != 'text':
        return

    if chat_type == 'group':
        cursor = db_groups.find_one({"group_id": chat_id})
        if not cursor:
            dataout = {
                'group_id': chat_id,
                'group_name': msg['chat']['title']
            }
            db_groups.insert_one(dataout).inserted_id

    command = msg['text'].split(' ')
    if command[0] != 'blanky':
        return

    if len(command) < 2:
        bot.sendMessage(chat_id, 'Miaauuu \n \nList Command: \n - blanky bisaapa \n - blanky status \n - blanky dimana \n \n https://github.com/ojixzzz/Blanky-Aks')
        return
    
    if command[1]=='bisaapa':
        bot.sendMessage(chat_id, 'Miaauuu \n- Monitoring api login (per menit) \n- Pengingat (proses) \n- ngiseng')
    elif command[1]=='status':
        bot.sendMessage(chat_id, 'Miaauuu \nMonitoring api login: \n - Total test = %s \n - Total error = %s \n \n Pengingat \n - Masih statis (tes brangkat jam 11 + pulang 17)' % (Total_test, Total_error))
    elif command[1]=='dimana':
        for row in getGroups():
            bot.sendMessage(chat_id, '- grup %s' % row['group_name'])

bot = telepot.Bot(TELEGRAM_TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# t = Thread(target=blanky_main)
# t.start()

blanky_main()
