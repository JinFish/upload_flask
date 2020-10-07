from flask import Flask
from flask import render_template,request,jsonify,session,send_from_directory,make_response,send_file
import json
import uuid
from module.teacher import  Teacher
from module.course import  Course
from module.file import File
import os
import time
from urllib.parse import quote
import shutil


from datetime import datetime
app=Flask(__name__)
app.secret_key = b'_5#t2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'rar', 'zip'])  # 允许上传的文件后缀


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


@app.route('/deletecourse/<id>')
def deletecourse(id):
    course=Course(unique_id=id)
    file=File.queryByCid(id)
    print("File:",file)
    if(len(file)>0):
        file_path=file[0][2]
        file_path=file_path.rsplit('/',1)[0]
        print("file_path:",file_path)
        shutil.rmtree(file_path)
    File.deleteallBycourseid(id)

    course.delete()

    return jsonify({"dd":"dd"})


# 判断文件是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 获取文件列表
def get_files(path):
    return ([] if not os.path.exists(path) else os.listdir(path))


# 获取文件数据集
def get_file_data(fileid):
    result = File.queryById(fileid)
    fdata = {"id": "",
             "name": "",
             "url": "",
             "cid": "",
             "time": ""}
    for key, value in zip(fdata, result):
        fdata[key] = value

    return fdata


# 数据展示
@app.route('/api/show', methods=['GET', 'POST'], strict_slashes=False)
def api_show():

    cid = request.form.get("cid")
    print("cid:",cid)
    print("request_data:",request.data)

    # 按课程id查询文件
    result = File.queryByCid(cid)
    print("result:",result)
    # json数据
    jdata = {"code": 0,
             "msg": "",
             "count": len(result),
             "data": []}
    # data填充
    for row in result:
        data_row = {"fid": "",
                    "fname": "",
                    "furl": "",
                    "fcid": "",
                    "ftime": ""}

        for key, value in zip(data_row, row):


            data_row[key] = str(value)

        jdata["data"].append(data_row)
    print("jdata:",jdata)

    #     print(cid)
    #     print(result)
    #     print(jdata)
    #     print(jsonify(jdata))
    return jsonify(jdata)


# 具有上传功能的页面
@app.route('/upload/<cid>')
def upload_page(cid):
    #     path = os.getcwd() + '/' + UPLOAD_FOLDER
    #     files = get_files(path)

    return render_template('upload.html',cid=cid)


#    return render_template('upload.html', files=files)

@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():

    if ("user_id" not in session):
        return "请访问/login进行登录。"

    #获取教师的id,通过user_id
    teacher_id=Teacher().queryidByuser(session["user_id"])[0]

    # 获取教师和课程信息

    cid = request.form.get("cid")
    #通过cid获得课程名称
    course=Course().queryByid(cid)
    cname = course[2]
    cdir = teacher_id + '/' + cname

    file_dir = os.path.join(basedir, cdir)  # 拼接成合法文件夹地址
    file_dir=file_dir.replace('\\','/')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建

    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = f.filename
        print("fname:",fname)
        uptime = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
        print("uptime:", uptime)
        uid = str(uuid.uuid1())
        print("uid:", uid)
        file_path = file_dir + '/' + uptime + fname
        print("file_path:", file_path)
        spare1 = ""
        spare2 = ""
        spare3 = ""
        spare4 = ""

        # 插入数据库
        newfile = File(uid, fname, file_path, cid, uptime, spare1, spare2, spare3, spare4)
        print("newfile:",newfile)
        newfile.insert();

        f.save(os.path.join(file_path))  # 保存文件到upload目录

        return jsonify({"code": 0, "msg": "上传成功"})
        # return redirect('/upload')


# @app.route("/downloadd", methods=['GET'])
# def downloader():
#     fid = request.args.get('fid')
#     print(fid)
#     file_data = get_file_data(fid)
#     fname = file_data['name']
#     furl = file_data['url']
#
#     fpath = furl[:len(furl) - len(fname)]  # 截取文件路径
#
#     return send_from_directory(fpath, fname, as_attachment=True, attachment_filename=fname[19:])  # as_attachment=True 一定要写，不然会变成打开，而不是下载；attachment_filename='我是重命名后的文件.xxx'；fname[19:]去掉时间戳，截取文件名称


@app.route("/download", methods=['GET'])
def getter():
    fid = request.args.get('fid')
    file_data = get_file_data(fid)
    fname = file_data['name']
    ftime = file_data['time']
    furl = file_data['url']
    ftime=str(ftime)
    ftime=ftime.replace(' ','-').replace(":",'-')



    print(fid)
    print(file_data)
    print(ftime)
    print(fname)

    fpath = furl[:len(furl) - len(fname) - len(ftime)]  # 截取文件路径
    print(furl)
    print(fname)
    print(ftime)
    print(fpath)
    fpath=fpath
    print("fpath:",fpath)
    filetarget=ftime+fname
    # response=make_response(send_from_directory(fpath, filetarget, as_attachment=True,
    #                                            attachment_filename=fname) )
    # response.headers["Content-Disposition"] = "attachment; filename{}".format(filetarget.encode().decode('latin-1'))

    filename=fpath+filetarget
    response = make_response(send_file(filename))
    basename = os.path.basename(filename)
    basename =basename[19:]
    response.headers["Content-Disposition"] = \
        "attachment;" \
        "filename*=UTF-8''{utf_filename}".format(
            utf_filename=quote(basename.encode('utf-8'))
        )

    return response


# 删除文件及数据
@app.route('/api/delete', methods=['POST'], strict_slashes=False)
def api_delete():
    fid = request.form.get('fid')
    file_data = get_file_data(fid)

    os.remove(file_data['url'])

    File.deleteById(file_data['id'])

    return jsonify({"code": 0, "msg": "删除成功"})


