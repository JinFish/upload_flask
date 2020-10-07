import pymysql




class DB:
    def __init__(self):
        self.address = "localhost"
        self.username = "root"
        self.password = "root"
        self.database = "test"


    def connection(self):
        self.db=pymysql.connect(self.address,self.username,self.password,self.database,use_unicode=True,charset='utf8')
        self.cursor=self.db.cursor()

        return self.cursor

    def close(self):
        self.db.close()

if __name__ == '__main__':
    db=DB()
    cursor=db.connection()
    print(db.db)
    db.close()
    print(db.db)

