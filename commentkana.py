import MySQLdb
import pykakasi
import unicodedata
import ev

connection = MySQLdb.connect(host=ev.mysql_host,user=ev.mysql_user,passwd=ev.mysql_password,db=ev.mysql_db)
cur = connection.cursor()

videoid = 9

kks = pykakasi.kakasi()

cur.execute("select id,commentno,commentposition,commentcontent,commentcommand,userid,posttime,nicoru,commentcontent_kana from sm" + str(videoid) + " where commentcontent_kana is null")

fetchcache = cur.fetchall()

print("dataloaded!")

looplen = len(fetchcache)
loopcount = 0

for x in range(looplen):
    try:
        kks_result = kks.convert(fetchcache[x][3])
        kksconvert = "".join([unicodedata.normalize("NFKD",r["hira"]) for r in kks_result])
        commentdata = (fetchcache[x][0],fetchcache[x][1],fetchcache[x][2],fetchcache[x][3],fetchcache[x][4],fetchcache[x][5],fetchcache[x][6],fetchcache[x][7],kksconvert)
        cur.execute("INSERT INTO sm" + str(videoid) + "_sub (id,commentno,commentposition,commentcontent,commentcommand,userid,posttime,nicoru,commentcontent_kana) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",commentdata)
        loopcount += 1
        if loopcount > 999:
            connection.commit()
            print("commit!")
    except:
        print("error at " + str(fetchcache[x][0]))
connection.commit()