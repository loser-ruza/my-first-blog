import fitbit
import datetime
import pandas as pd
from ast import literal_eval

# tokenファイルを上書きする関数
def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return

# ユーザ情報の定義
CLIENT_ID =  '23BC6R'
CLIENT_SECRET  = 'b888b16df4a934f27ce4267964d19223'
TOKEN_FILE = "token1.txt"

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

# 睡眠効率取得
dataTxt = str(client.sleep(date = today))

minutesAsleepAd = dataTxt.find('minutesAsleep')
minutesAsleep = dataTxt[minutesAsleepAd+16:minutesAsleepAd+19]

timeInBedAd = dataTxt.find('timeInBed')
timeInBed = dataTxt[timeInBedAd+12:timeInBedAd+15]

sleepEfficiency = int(int(minutesAsleep) / int(timeInBed) * 100)
