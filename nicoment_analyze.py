import csv
import MeCab
from wordcloud import WordCloud
import math
import json
import MySQLdb
import ev


videoid = 9

with open("csv/sm" + str(videoid) + ".csv",encoding="utf-8") as f:
    reader = csv.reader(f)
    nlis = [row for row in reader]
    nlis.pop(0)




connection = MySQLdb.connect(host=ev.mysql_host,user=ev.mysql_user,passwd=ev.mysql_password,db=ev.mysql_db)
cur = connection.cursor()

m = MeCab.Tagger ()

allow_pos = ["名詞","動詞","形容詞"]

yearlist = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]

#for x in range(len(yearlist)):

    #cur.execute("select part,count(1) from sm" + str(videoid) + "_part sp where exists(select 1 from sm" + str(videoid) + " sm where DATE_FORMAT(posttime, '%Y') = '" + str(yearlist[x]) +"' and sp.id = sm.id) group by part order by count(1) desc limit 1000")

    #nlis = [[r[0],r[1]] for r in cur.fetchall()]

#with open("json/sm" + str(videoid) + "/" + str(yearlist[x]) + ".json","w") as f:
    #json.dump({"mainc":nlis},f)

allowlist = []

for t in nlis:
    ndoc = m.parse(t[0]).split()
    try:
        if ndoc[4].split("-")[0] in allow_pos:
            allowlist.append(t)
    except:
        pass

#wordcloud用文字列作成

nowst = ""

for r in allowlist:
    nowst = nowst + " " + " ".join(r[0] for i in range(math.ceil(math.log(int(r[1]),3))))

fpath = "ipaexg.ttf"

wordcloud = WordCloud(background_color="white",font_path=fpath, width=600,height=400,min_font_size=15)
wordcloud.generate(nowst)

#wordcloud.to_file("pic/sm" + str(videoid) + "/wordcloud" + str(yearlist[x]) + ".png")
wordcloud.to_file("pic/sm" + str(videoid) + "/wordcloud.png")

    #print("finish!" + str(yearlist[x]))