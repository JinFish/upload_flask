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
    user_id=session["user_id"]
    teacher_id=Teacher().queryidByuser(user_id)[0]

    course_id=uuid.uuid1()
    course=Course(unique_id=course_id,teacher=teacher_id)

    return render_template("add.html", course=course)



@app.route('/uniqueurl')
def uniqueurl():
    course_url=request.args.get('course_url')
    course_id=request.args.get('course_id')
    course=Course()

    r=course.queryByurl(course_url)
    result={}
    if(r==None):
        result["result"]=False

    else:
        uid=r[0]
        if(uid==course_id):
            result["result"]=False
        else:
            result["result"] = True
    print(result)
    return jsonify(result)


@app.route('/courseadd',methods=['POST'])
def courseadd():
    data=json.loads(request.form["data"])

    course_id=data["course_id"]
    teacher=data["teacher_id"]

    course_url=data['course_url']
    print("course_url",course_url)
    course_name=data['course_name']
    course_description=data['course_description']
    print("course_description",course_description)

    course=Course(unique_id=course_id,course_url=course_url,name=course_name,description=course_description,teacher=teacher)
    r=course.queryByid(course_id)
    if(r!=None):
        course.update()
    else:
        course.insert()


    r={}
    r["result"]=True
    print(r)
    return jsonify(r)


@app.route('/loadtable')
def loadtable():
    if ("user_id" not in session):
        return "请访问/login进行登录。"

    user_id=session["user_id"]
    print("user_id:",user_id)
    course=Course()
    unique_id=Teacher().queryidByuser(user_id)[0]
    course_all=course.query_allByteacher(unique_id)
    print("course_all:",course_all)

    result=[]
    for c in course_all:
        dict={}
        dict["unique_id"]=c[0]
        dict["course_url"]=c[1]
        dict["name"]=c[2]
        dict["description"]=c[3]
        teacher=Teacher()
        t=teacher.queryByid(c[4])
        if(t!=None):
            dict["teacher"]=t[1]
        else:
            dict["teacher"]=t
        result.append(dict)

    result=jsonify(result)
    return result



@app.route('/edit/<id>')
def edit(id):

    course=Course()
    info=course.queryByid(id)
    print("info:",info)
    course=Course(*info)


    return render_template("add.html",course=course)

