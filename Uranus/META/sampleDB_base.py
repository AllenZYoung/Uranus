import pymysql as MySQLDB
from random import Random

def sampleDB():
    mysql = MySQLDB.connect(host='127.0.0.1', port=3306, user='uranus', passwd='uranus', db='uranus', charset='utf8')
    cursor = mysql.cursor()

    # Add User
    for i in range(14211000,14211050):
        name = random_str()
        sql='INSERT INTO app_user(username,password,name,role,gender) VALUES(%d,"123","%s","student","male");' %(i, name)
        try:
            cursor.execute(sql)
        except:
            pass
    for i in range(14211050,14211100):
        name = random_str()
        sql='INSERT INTO app_user(username,password,name,role,gender) VALUES(%d,"123","%s","student","female")' %(i, name)
        try:
            cursor.execute(sql)
        except:
            pass

    for i in range(100,150):
        name = random_str()
        sql='INSERT INTO app_user(username,password,name,role,gender) VALUES(%d,"123","%s","teacher","female")' %(i, name)
        try:
            cursor.execute(sql)
        except:
            pass

    for i in range(1,10):
        name = random_str()
        sql='INSERT INTO app_user(username,password,name,role,gender) VALUES(%d,"123","%s","admin","male")' %(i, name)
        try:
            cursor.execute(sql)
        except:
            pass

    # Add Term
    for i in range(2010,2018):
        info = random_str()
        sql='INSERT INTO app_term(info,year,semester,startWeek,endWeek) VALUES("%s",%d,"autumn",18,20)' %(info, i)
        try:
            cursor.execute(sql)
        except:
            pass
    for i in range(2010,2018):
        info = random_str()
        sql='INSERT INTO app_term(info,year,semester,startWeek,endWeek) VALUES("%s",%d,"spring",16,18)' %(info, i)
        try:
            cursor.execute(sql)
        except:
            pass

    # Add Course
    # TOO HARD!!!

    mysql.commit()
    cursor.close()
    mysql.close()


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


# Main Entry
sampleDB()