from flask import Flask
from flask import render_template,request,jsonify,session
import json
import uuid
from module.teacher import  Teacher
from module.course import  Course
app=Flask(__name__)
app.secret_key = b'_5#t2L"F4Q8z\n\xec]/'

@app.route('/login')
def login():

    return render_template('login.html')


@app.route('/valid')
def valid():
    user_name=request.args.get('user_name', '')
    print("user_name:",user_name)
    password=request.args.get('password', '')
    print("password:", password)
    teacher=Teacher()
    r=teacher.queryByuserid(user_name)
    print("r:",r)
    result = {}
    if(r==None):
        result["result"]="用户不存在"
        print("result:",result)
        return jsonify(result)
    p=r[3]
    if(password==p):
        session["user_id"]=user_name
        result["result"]=True
    else:
        result["result"]="用户名或密码错误"

    return jsonify(result)



@app.route('/background')
def background():
    if("user_id" not in session):
        return "请访问/login进行登录。"

    user_id=session["user_id"]
    teacher=Teacher()
    result=teacher.queryByuserid(user_id)

    teacher=Teacher(*result)




    return render_template("main_page.html",teacher=teacher)

@app.route('/add')
def add():
    if ("user_id" not in session):
        return "请访问/login进行登录。"

    user_id = session["user_id"]
    teacher = Teacher()
    result = teacher.queryByuserid(user_id)

    teacher = Teacher(*result)

    return render_template("add.html", teacher=teacher)



@app.route('/uniqueurl')
def uniqueurl():
    course_url=request.args.get('course_url')
    course=Course()

    r=course.queryByurl(course_url)
    result={}
    if(r==None):
        result["result"]=False

    else:
        result["result"] = True
    print(result)
    return jsonify(result)


@app.route('/courseadd',methods=['POST'])
def courseadd():
    print("aaaaaaaa")
    print(request)
    print(request.args)
    print(request.form)
    data=json.loads(request.form["data"])
    course_id=uuid.uuid1()
    course_url=data['course_url']
    print("course_url",course_url)
    course_name=data['course_name']
    course_description=data['course_description']

    course=Course(unique_id=course_id,course_url=course_url,name=course_name,description=course_description)

    course.insert()

    r={}
    r["result"]=True
    print(r)
    return jsonify(r)