from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import json
import xml.etree.ElementTree as ET 
import datetime
import math
import copy


session = requests.session()
url = "https://secure.nicovideo.jp/secure/login?site=niconico"
params = {
    "mail": "",
    "password": ""
}

response=session.post(url, params=params)
user_session = session.cookies.get("user_session") #セッション情報
user_id = response.headers.get("x-niconico-id") #ユーザーID

videoid = 500873

def reload_thread():
    nstatus = 190
    source = ""
    while nstatus!=200:
        try:
            source = session.get("https://nicovideo.jp/watch/sm" + str(videoid))
            nstatus = source.status_code
        except:
            nstatus = 190
    soup = BeautifulSoup(source.text, "html.parser")
    elem = soup.select_one("#js-initial-watch-data")
    js = json.loads(elem.get("data-api-data"))
    nvComment = js["comment"]["nvComment"]

    return nvComment

nvComment = reload_thread()

headers = {#共通
  "X-Frontend-Id": "6",
  "X-Frontend-Version": "0",
  "Content-Type": "application/json",
}

infoapi = requests.get("https://ext.nicovideo.jp/api/getthumbinfo/sm" + str(videoid))
nowxml = ET.fromstring(infoapi.text)
dtobj = int(datetime.datetime.fromisoformat(nowxml[0][4].text).timestamp())

#nowetime = int(time.time())

ercount = 0

def getcomment(getunixtime,nvComment):#初期500件　後半のほうは1000~1600件くらい
    parms = {
        "params": nvComment["params"],
        "additionals": {"when":getunixtime},#10分単位で取得
        "threadKey": nvComment["threadKey"]
    }

    nstatus = 189
    while nstatus!=200:
        try:
            commentdata = session.post(nvComment["server"]+"/v1/threads",headers=headers,data=json.dumps(parms))
            nstatus = commentdata.status_code
        except:
            nstatus = 189
            nvComment = reload_thread()

    jscomment = commentdata.json()
    with open("F:\\niconico\\sm" + str(videoid) + "\\" + str(getunixtime) + ".json","w") as f:
        json.dump({"mainc":jscomment,"getepoctime":getunixtime},f)
    remain_ratelimit = int(commentdata.headers["X-RateLimit-Remaining"])
    if remain_ratelimit < 6:
        nvComment = reload_thread()
        print("レートリミット制限付近")
        time.sleep(15)
    try:
        lastcommentnumber = int(jscomment["data"]["globalComments"][0]["count"])
    except:
        pass
    if commentdata.status_code==400:
        ercount += 1
        nvComment = reload_thread()
        time.sleep(60)
        lastcommentnumber = getcomment(getunixtime)
    
    return lastcommentnumber,nvComment

startunixtime = dtobj
#startunixtime = 1199081760
endunixtime = int(time.time())
latestcommentcount = 0
#latestcommentcount = 2058732
default_diff = 600
upcountdiff = 1200
nowdiff = copy.copy(default_diff)
latestunix = copy.copy(startunixtime)

skipcount = 0

while True:
    nowcommentcount,nvComment = getcomment(latestunix,nvComment=nvComment)
    if nowcommentcount >= latestcommentcount+490 and skipcount < 3:#コメント数追いきれなかったときただし5回まで
        latestunix += -(math.floor(nowdiff/2))
        skipcount += 1
        nowdiff = math.floor(nowdiff/2)
        if nowdiff <= default_diff:
            nowdiff = copy.copy(default_diff)
    elif skipcount > 2:
        latestcommentcount = copy.copy(nowcommentcount)
        skipcount = 0
        latestunix += (nowdiff + 3600)
        print("強制執行")
    else:#コメント数追いきれた
        if nowcommentcount < latestcommentcount+200:#余裕で追いきれた時
            nowdiff += upcountdiff
        else:#変更なし
            pass
        latestunix += nowdiff
        latestcommentcount = copy.copy(nowcommentcount)
        skipcount = 0
    if endunixtime < latestunix:
        break
    print(nowdiff)

"""
for x in range(repeat_count):
    if x > skip:

        parms = {
            "params": nvComment["params"],
            "additionals": {"when":dtobj + diff*x},#10分単位で取得
            "threadKey": nvComment["threadKey"]
        }

        commentdata = session.post(nvComment["server"]+"/v1/threads",headers=headers,data=json.dumps(parms))
        jscomment = commentdata.json()
        with open("F:\\niconico\\sm9\\" + str(x) + ".json","w") as f:
            json.dump({"mainc":jscomment,"getepoctime":dtobj + diff*x},f)
        remain_ratelimit = int(commentdata.headers["X-RateLimit-Remaining"])
        if remain_ratelimit < 7:
            nvComment = reload_thread()
            print("レートリミット制限付近")
            time.sleep(10)
        if commentdata.status_code==400:
            print(str(x) + "\t on error")
            nvComment = reload_thread()

    else:
        pass
"""