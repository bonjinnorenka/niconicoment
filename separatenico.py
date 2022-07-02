import MySQLdb
import pykakasi
import unicodedata
import ev

connection = MySQLdb.connect(host=ev.mysql_host,user=ev.mysql_user,passwd=ev.mysql_password,db=ev.mysql_db)
cur = connection.cursor()

videoid = 2057168

kks = pykakasi.kakasi()

cur.execute("select id,commentno,commentcontent from sm" + str(videoid) + " sm where not exists(select 1 from sm" + str(videoid) +"_part sp where sp.id = sm.id)")

fetchcache = cur.fetchall()

looplen = len(fetchcache)
loopcount = 0

for x in range(looplen):
    try:
        loopcount += 1
        resultres = kks.convert(fetchcache[x][2])
        response_mysql = [(fetchcache[x][0],fetchcache[x][1],r["orig"],unicodedata.normalize("NFKD",r["hira"])) for r in resultres]
        if response_mysql!=[]:
            cur.executemany("insert into sm" + str(videoid) + "_part (id,commentno,part,part_kana) VALUES (%s,%s,%s,%s)",response_mysql)
        
        if loopcount >= 1000:
            connection.commit()
            loopcount = 0
    except:
        print("er occored at " + str(fetchcache[x][0]))