import sys
import time
import telepot
import requests
import json
import random
from random import randint
import operator
import mandrill

from threading import Thread
from datetime import datetime, timedelta
from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, TELEGRAM_TOKEN, LOGIN_URL, LOGIN_DATA, API_TESTS_URL, MANDRILL_TOKEN, MANDRILL_EMAIL, MANDRILL_NAME

mongoDB = MongoClient(MONGO_HOST, MONGO_PORT)
database = mongoDB.blankyaks
db_groups = database.groups
db_settings = database.settings

headers = {
    'User-Agent': 'BlankyBot Aks v1.0'
}
group_id_ijak = '-19993514'
Total_test = 0
Total_error = 0
Total_error_login = 0
Last_error = False
Last_error_api = False
pengingat1 = False
pengingat2 = False
Tidur = False
var_rapat = False
blanky_versong = 1

ojix = 0
plendok = 0
fajar = 0
pendi = 0
hendra = 0

def getGroups():
    cursor = db_groups.find().sort([("$natural", -1)]).limit(10)
    return cursor

def whatsNew():
    dataout = {
        'setting_name': 'versi',
        'setting_data': blanky_versong
    }
    cursor = db_settings.find_one({"setting_name": "versi"})
    if not cursor:
        db_settings.insert_one(dataout).inserted_id
    else:
        if cursor.get('setting_data')!=blanky_versong:
            db_settings.replace_one({'setting_name': 'versi'}, dataout, upsert=True)
        else:
            return False

    for row in getGroups():
        bot.sendMessage(row['group_id'], 'Whats new!!! \n- Penambahan kemampuan cek api mandrill')

    return True

def send_mandrill(subjek, email, nama, html):
    mandrill_client = mandrill.Mandrill(MANDRILL_TOKEN)
    message = {}
    message['subject'] = subjek
    message['html'] = html
    message['to'] = [{'email':email, 'name':nama, 'type':'to'}]
    message['from_email'] = MANDRILL_EMAIL
    message['from_name'] = MANDRILL_NAME
    result = mandrill_client.messages.send(message=message, async=False)
    return result

def acakAcak():
    global group_id_ijak
    global ojix, fajar, pendi, plendok, hendra

    ojix=0;plendok=0;fajar=0;pendi=0;hendra=0

    nama = ['ojix','plendok','fajar','pendi','hendra']
    random.shuffle(nama)
    for y in xrange(1,6):
        for x in xrange(1,randint(2,20)):
            random.shuffle(nama)
            jawaban = random.sample(set(nama),2)

        if jawaban[0] == 'fajar':
            fajar +=1
        elif jawaban[0] == 'ojix':
            ojix += 1
        elif jawaban[0] == 'pendi':
            pendi += 1
        elif jawaban[0] == 'hendra':
            hendra += 1
        elif jawaban[0] == 'plendok':
            plendok += 1

        if jawaban[1] == 'fajar':
            fajar +=1
        elif jawaban[1] == 'ojix':
            ojix += 1
        elif jawaban[1] == 'pendi':
            pendi += 1
        elif jawaban[1] == 'hendra':
            hendra += 1
        elif jawaban[1] == 'plendok':
            plendok += 1

        bot.sendMessage(group_id_ijak, "["+str(y)+"] \nKandidat peserta rapat : "+jawaban[0]+" dan "+jawaban[1])
        bot.sendMessage(group_id_ijak, "Hasil sementara : \n - Fajar : %s \n - Hendra : %s \n - Plendok : %s \n - Fendi : %s \n - Oji : %s" % (fajar, hendra, plendok, pendi, ojix))
        time.sleep(30)

    bot.sendMessage(group_id_ijak, "Hasil pengacakan rapat : \n - Fajar : %s \n - Hendra : %s \n - Plendok : %s \n - Fendi : %s \n - Oji : %s" % (fajar, hendra, plendok, pendi, ojix))
    dicts = {"ojix":ojix,"fajar":fajar,"hendra":hendra,"plendok":plendok,"pendi":pendi}
    hasil = sorted(dicts.items(),key=operator.itemgetter(1),reverse=True)
    hasil0 = hasil[0]
    hasil1 = hasil[1]
    hasil2 = hasil[2]
    hasil3 = hasil[3]
    hasil4 = hasil[4]

    if hasil1[1] == hasil2[1]:
        if hasil2[1] == hasil3[1]:
            if hasil3[1] == hasil4[1]:
                bot.sendMessage(group_id_ijak, "ANGKA SAMA!! \nDILAKUKAN PENGACAKAN ANTARA "+hasil1[0]+","+hasil2[0]+","+hasil3[0]+" dan "+hasil4[0])
                time.sleep(5)
                bot.sendMessage(group_id_ijak, "Orang yang beruntung ikut rapat : "+hasil0[0]+" dan "+random.choice([hasil1[0],hasil2[0],hasil3[0]],hasil4[0]))
            else:
                bot.sendMessage(group_id_ijak, "ANGKA SAMA!! \nDILAKUKAN PENGACAKAN ANTARA "+hasil1[0]+","+hasil2[0]+" dan "+hasil3[0])
                time.sleep(5)
                bot.sendMessage(group_id_ijak, "Orang yang beruntung ikut rapat : "+hasil0[0]+" dan "+random.choice([hasil1[0],hasil2[0],hasil3[0]]))
        else:
            bot.sendMessage(group_id_ijak, "ANGKA SAMA!! \nDILAKUKAN PENGACAKAN ANTARA "+hasil1[0]+" dan "+hasil2[0])
            time.sleep(5)
            bot.sendMessage(group_id_ijak, "Orang yang beruntung ikut rapat : "+hasil0[0]+" dan "+random.choice([hasil1[0],hasil2[0]]))
    else:
        bot.sendMessage(group_id_ijak, "Orang yang beruntung ikut rapat : "+hasil0[0]+" dan "+hasil1[0])

def acakRapat():
    global var_rapat
    jam_ini = int(datetime.now().strftime("%H%M%S"))
    hari_ini = int(datetime.now().weekday())
    if hari_ini==0:
        if jam_ini > 150000:
            if var_rapat==False:
                var_rapat = True
                acakAcak()
        else:
            var_rapat = False

def Pengingat():
    global pengingat1
    global pengingat2
    global group_id_ijak

    sekarang = int(datetime.now().strftime("%H%M%S"))
    if sekarang > 110000:
        if pengingat1==False:
            pengingat1 = True
            bot.sendMessage(group_id_ijak, 'Meong \nSelamat bekerja!')
            retemail = send_mandrill('testing', 'ligerxrendy@gmail.com', '', 'tes email')
            if retemail:
                if retemail.get('status')!='sent':
                    for row in getGroups():
                        bot.sendMessage(row['group_id'], 'Meooong \nEmail mandrill error \nStatus: %s' % retemail.get('status'))

    else:
        pengingat1 = False

    if sekarang > 170000:
        if pengingat2==False:
            pengingat2 = True
            bot.sendMessage(group_id_ijak, 'Meong \nUdah waktunya pulang')
    else:
        pengingat2 = False

def TestLogin():
    global Total_test
    global Total_error
    global Total_error_login

    Total_test += 1 
    headers = {
        'User-Agent': 'BlankyBot Aks v1.0'
    }
    url = LOGIN_URL
    datapost = LOGIN_DATA

    try:
        req = requests.post(url, headers=headers, data=json.dumps(datapost))
        if req.status_code != 200:
            Total_error += 1
            Total_error_login += 1
            return 'Meong \nLogin bermasalah, status code bukan 200'

        if req.text:
            resjson = json.loads(req.text)
            if resjson['meta']['code'] != 200:
                Total_error += 1
                Total_error_login += 1
                return 'Meong \nLogin bermasalah, err message : %s' % resjson['meta'].get('error_message')
    except Exception as e:
        return 'Meong \n%s' % str(e)

    return False

def API_TESTS():
    global Last_error_api
    try:
        for url in API_TESTS_URL:
            req = requests.get(url, headers=headers)
            if req.text:
                resjson = json.loads(req.text)
                if resjson.get('status') != 1:
                    if Last_error_api==False:
                        Last_error_api=True
                        for row in getGroups():
                            bot.sendMessage(row['group_id'], resjson.get('message'))
                else:
                    if Last_error_api==True:
                        Last_error_api=False
                        for row in getGroups():
                            bot.sendMessage(row['group_id'], resjson.get('message'))

    except Exception as e:
        print 'Meong \n%s' % str(e)

    return False

def blanky_main():
    global Total_test
    global Total_error
    global Last_error
    global Total_error_login
    while True:
        if not getGroups():
            bot.sendMessage('89093938', 'Grup_id diluar kendali mastah')

        if Total_test > 1000:
            Total_test = 0
            Total_error = 0

        if Tidur==False:
            testx = TestLogin()
            if testx:
                testx = TestLogin()
                if testx:
                    Last_error=True
                    if Total_error_login > 1:
                        for row in getGroups():
                            bot.sendMessage(row['group_id'], testx)
            else:
                if Last_error==True:
                    Last_error=False
                    if Total_error_login > 1:
                        for row in getGroups():
                            bot.sendMessage(row['group_id'], 'Meong \nLogin sudah normal mas')
                    Total_error_login = 0

            API_TESTS()

        Pengingat()
        #acakRapat()
        time.sleep(60)

def handle(msg):
    global Total_test
    global Total_error
    global Tidur
    global fajar, hendra, plendok, pendi, ojix, group_id_ijak
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
        bot.sendMessage(chat_id, 'Meong \n \n Whats new : \n - Penggantian kata miauu ke meong \n - Pengacakan Rapat [HOT] \n \n List Command: \n - blanky bisaapa \n - blanky status \n - blanky dimana \n - blanky tidur \n - blanky bangun \n - blanky acak \n \n https://github.com/ojixzzz/Blanky-Aks')
        return
    
    if command[1]=='bisaapa':
        bot.sendMessage(chat_id, 'Meong \n- Monitoring api login (per menit) \n- Pengingat (proses) \n- ngiseng')
    elif command[1]=='status':
        if Tidur==True:
            bot.sendMessage(chat_id, 'Lagi tidur!')
        else:
            bot.sendMessage(chat_id, 'Meong \nMonitoring api login: \n - Total test = %s \n - Total error = %s \n \n Pengingat \n - Masih statis (tes brangkat jam 11 + pulang 17)' % (Total_test, Total_error))
    elif command[1]=='dimana':
        for row in getGroups():
            bot.sendMessage(chat_id, '- grup %s' % row['group_name'])
    elif command[1]=='tidur':
        Tidur = True
        bot.sendMessage(chat_id, 'Okee fine!')
    elif command[1]=='bangun':
        Tidur = False
        bot.sendMessage(chat_id, 'Meong')
    elif command[1]=='acak':
        acakAcak()

bot = telepot.Bot(TELEGRAM_TOKEN)
bot.message_loop(handle)
whatsNew()
print ('Listening ...')

# t = Thread(target=blanky_main)
# t.start()

blanky_main()
