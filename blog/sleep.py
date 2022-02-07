import fitbit #FitbitAPI用
import datetime #日付取得用
import pandas as pd #消しても大丈夫かも
from ast import literal_eval #文字列処理用

# tokenファイルを上書きする関数
def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return

# ユーザ情報の定義
CLIENT_ID =  '#####'
CLIENT_SECRET  = '#####'
TOKEN_FILE = "token.txt"

# ファイルからtoken情報を読み込む
tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']

# .FitbitでClient情報を取得
# refresh_cbに関数を定義する事で期限切れのtokenファイルを自動更新する
client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET,
                       access_token = access_token,
                       refresh_token = refresh_token,
                       refresh_cb = updateToken)

# 日付
now = datetime.datetime.now()
today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

# 睡眠データ取得
dataTxt = str(client.sleep(date = today)

#睡眠データから実際に寝た時間とベッドにいた時間を切り抜く
#例外処理：睡眠時間が100分未満のとき、切り抜く範囲を2桁にする
#例外処理：念のため切り取った部分が数値でなかったとき、睡眠効率を0にしエラー画面にする
minutesAsleepAd = dataTxt.find('minutesAsleep')
minutesAsleep = dataTxt[minutesAsleepAd+16:minutesAsleepAd+19]
try:
    minutesAsleep = int(minutesAsleep)
except ValueError:
    try:
        minutesAsleep = int(dataTxt[minutesAsleepAd+16:minutesAsleepAd+18])
    except ValueError:
        minutesAsleep = 0

timeInBedAd = dataTxt.find('timeInBed')
timeInBed = dataTxt[timeInBedAd+12:timeInBedAd+15]
try:
    timeInBed = int(timeInBed)
except ValueError:
    try:
        timeInBed = int(dataTxt[timeInBedAd+12:timeInBedAd+14])
    except ValueError:
        timeInBed = 1

try:
    sleepEfficiency = int(minutesAsleep / timeInBed * 100)
except ValueError:
    sleepEfficiency = 0

#print(dataTxt)
#print(minutesAsleep)
#print(timeInBed)
#print(sleepEfficiency)
