from module.db import DB
import uuid

class Course:
    def __init__(self,unique_id,course_url,name,description,teacher,spare1,spare2,spare3,spare4):
        self.unique_id=unique_id
        self.course_url=course_url
        self.name=name
        self.description=description
        self.teacher=teacher
        self.spare1=spare1
        self.spare2=spare2
        self.spare3=spare3
        self.spare4=spare4


    def insert(self):
        # 加载db类，用于连接数据库
        db=DB()
        # 获取cursor
        cursor=db.connection()
        mysql="insert into course(unique_id,course_url,name,description,teacher,spare1,spare2,spare3,spare4)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
              %(self.unique_id,self.course_url,self.name,self.description,self.teacher,self.spare1,self.spare2,self.spare3,self.spare4)
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
        mysql="update course set course_url='%s',name='%s',description='%s',teacher='%s',spare1='%s',spare2='%s',\
        spare3='%s',spare4='%s' where unique_id='%s'" %(self.course_url,self.name,self.description,self.teacher,
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
        mysql="delete from course where unique_id='%s'"%(self.unique_id)

        try:
            cursor.execute(mysql)
            db.db.commit()
        except:
            db.db.rollback()

        db.db.close()


    def query_all(self):
        db=DB()
        cursor=db.connection()
        mysql="select * from course"

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
        mysql="select * from course where unique_id='%s'" %(id)
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

    unique_id='859af6cc-04a4-11eb-9435-3413e89fe484'
    course_url="internet_network"
    name="network基础"
    description="这是一个非常简答且基础的网络课程"
    teacher=""
    spare1=""
    spare2=""
    spare3=""
    spare4=""
    course=Course(unique_id,course_url,name,description,teacher,spare1,spare2,spare3,spare4)

    r=course.queryByid('859af6cc-04a4-11eb-9435-3413e89fe484')
    print(r)



