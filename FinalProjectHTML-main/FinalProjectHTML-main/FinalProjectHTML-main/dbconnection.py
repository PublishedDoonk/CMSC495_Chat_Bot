import pymysql
import pymysql.cursors

db = pymysql.connect(host="cmscfinal.cwzwx03ifxje.us-east-1.rds.amazonaws.com",
                     user="GroupControl", password="Fr29sM5!!Y",database="cmscfinal")
cursor = db.cursor
