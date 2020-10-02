from module.db import DB
import uuid

class Teacher:
    def __init__(self,unique_id,name,user_id,password,spare1,spare2,spare3,spare4):
        self.unique_id=unique_id
        self.name=name
        self.user_id=user_id
        self.password=password
        self.spare1=spare1
        self.spare2=spare2
        self.spare3=spare3
        self.spare4=spare4


    def insert(self):
        # 加载db类，用于连接数据库
        db=DB()
        # 获取cursor
        cursor=db.connection()
        mysql="insert into teacher(unique_id,name,user_id,password,spare1,spare2,spare3,spare4)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s')"\
              %(self.unique_id,self.name,self.user_id,self.password,self.spare1,self.spare2,self.spare3,self.spare4)
        try:
        # 执行sql语句
            cursor.execute(mysql)
            db.db.commit()
        except:
            db.db.rollback()
        db.db.close()

    def update(self):
        db=DB()
        cursor=db.connection()
        mysql="update teacher set name='%s',user_id='%s',password='%s',spare1='%s',spare2='%s',\
        spare3='%s',spare4='%s' where unique_id='%s'" %(self.name,self.user_id,self.password,
        self.spare1,self.spare2,self.spare3,self.spare4,self.unique_id)

        try:
            cursor.execute(mysql)
            db.db.commit()

        except:
            db.db.rollback()

        db.db.close()

    def delete(self):
        db=DB()
        cursor=db.connection()
        mysql="delete from teacher where unique_id='%s'"%(self.unique_id)

        try:
            cursor.execute(mysql)
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()


    def query_all(self):
        db=DB()
        cursor=db.connection()
        mysql="select * from teacher"
        results=None

        try:
            cursor.execute(mysql)
            results =cursor.fetchall()
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()
        return results


    def queryByid(self,id):
        db=DB()
        cursor=db.connection()
        mysql="select * from teacher where unique_id='%s'" %(id)
        result=None
        try:
            cursor.execute(mysql)
            result=cursor.fetchone()
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()
        return result


if __name__ == '__main__':
    unique_id="1212"
    name="taiyele"
    user_id="huang"
    password="1234567"
    spare1=""
    spare2=""
    spare3=""
    spare4=""

    teacher=Teacher(unique_id,name,user_id,password,spare1,spare2,spare3,spare4)
    # teacher.insert()
    results=teacher.query_all()
    print(results)


