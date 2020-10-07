from module.db import DB
import uuid
import time


class File:
    def __init__(self, unique_id="", file_name="", file_url="", course_id="", upload_time="", spare1="", spare2="", spare3="",
                 spare4=""):
        self.unique_id = unique_id
        self.file_name = file_name
        self.file_url = file_url
        self.course_id = course_id
        self.upload_time = upload_time
        self.spare1 = spare1
        self.spare2 = spare2
        self.spare3 = spare3
        self.spare4 = spare4

    def insert(self):
        # 加载db类，用于连接数据库
        db = DB()
        # 获取cursor
        cursor = db.connection()
        mysql = "insert into file(unique_id,file_name,file_url,course_id,upload_time,spare1,spare2,spare3,spare4)" \
                " values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                % (self.unique_id, self.file_name, self.file_url, self.course_id, self.upload_time, self.spare1,
                   self.spare2, self.spare3, self.spare4)
        print("Mysql:",mysql)
        try:
            # 执行sql语句
            cursor.execute(mysql)
            db.db.commit()
            print("insert sucess")
        except:
            db.db.rollback()
            print("insert failure")
        db.db.close()

    def update(self):
        db = DB()
        cursor = db.connection()
        mysql = "update file set file_name='%s',file_url='%s',course_id='%s',upload_time='%s',spare1='%s',spare2='%s',\
        spare3='%s',spare4='%s' where unique_id='%s'" % (
        self.file_name, self.file_url, self.course_id, self.upload_time,
        self.spare1, self.spare2, self.spare3, self.spare4, self.unique_id)

        try:
            cursor.execute(mysql)
            db.db.commit()

        except:
            db.db.rollback()

        db.db.close()

    def delete(self):
        db = DB()
        cursor = db.connection()
        mysql = "delete from file where unique_id='%s'" % (self.unique_id)

        try:
            cursor.execute(mysql)
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()

    def query_all(self):
        db = DB()
        cursor = db.connection()
        mysql = "select * from file"

        try:
            cursor.execute(mysql)
            results = cursor.fetchall()
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()
        return results


    def queryById(uid):
        db = DB()
        cursor = db.connection()
        mysql = "select * from file where unique_id='%s'" % (uid)
        result = None
        try:
            cursor.execute(mysql)
            result = cursor.fetchone()
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()
        return result


    def queryByCid(cid):
        db = DB()
        cursor = db.connection()
        mysql = "select * from file where course_id='%s'" % (cid)
        result = None
        try:
            cursor.execute(mysql)
            result = cursor.fetchall()
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()
        return result


    def deleteById(uid):
        db = DB()
        cursor = db.connection()
        mysql = "delete from file where unique_id='%s'" % (uid)

        try:
            cursor.execute(mysql)
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()

    def deleteallBycourseid(courseid):
        db = DB()
        cursor = db.connection()
        mysql = "delete from file where course_id='%s'" % (courseid)

        try:
            cursor.execute(mysql)
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()


if __name__ == '__main__':
    unique_id = "38d41dd4-04a7-11eb-a22e-3413e89fe484"
    file_name = "php教程"
    file_url = "e:/upload/" + str(unique_id)
    course_id = "3232"
    upload_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    spare1 = ""
    spare2 = ""
    spare3 = ""
    spare4 = ""
    file = File(unique_id, file_name, file_url, course_id, upload_time, spare1, spare2, spare3, spare4)

    r = file.queryByid(unique_id)
    print(r)




