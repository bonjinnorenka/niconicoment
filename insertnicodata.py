import MySQLdb
import glob
import json
import ev

#mysqlconnection
connection = MySQLdb.connect(host=ev.mysql_host,user=ev.mysql_user,passwd=ev.mysql_password,db=ev.mysql_db)
cur = connection.cursor()

videoid = 500873

#jsonfiles = glob.glob("F:\\niconico\\sm" + str(videoid) + "er\\*.json")
jsonfiles = glob.glob("F:\\niconico\\sm" + str(videoid) + "\\*.json")
#with open("erjlist.json","r") as f:
    #karij = json.load(f)
#jsonfiles = karij["mainc"]

erj_list = []

for x in range(len(jsonfiles)):
    try:
        with open(jsonfiles[x],"r") as f:
            nowjson = json.load(f)
        datajson = nowjson["mainc"]["data"]["threads"][1]["comments"]
        if datajson != []:
            commentdata = [(r["id"],r["no"],r["vposMs"],r["body"],",".join([n for n in r["commands"]]),r["userId"],r["postedAt"],r["nicoruId"]) for r in datajson]
            cur.executemany("INSERT INTO sm" + str(videoid) + " (id,commentno,commentposition,commentcontent,commentcommand,userid,posttime,nicoru) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",commentdata)
            connection.commit()
    
    except:
        print("error occord filename:"+ jsonfiles[x])
        erj_list.append(jsonfiles[x])
        with open("erjlist.json","w") as f:
            json.dump({"mainc":erj_list},f)
connection.commit()
