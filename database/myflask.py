from fileinput import filename

from flask import Flask,request,render_template,flash,redirect,url_for
import sql
import time
import json

from sql import sqlAdd

app = Flask(__name__)
app.config["SECRET_KEY"]="LY123"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'json'

@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('add'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        file = request.files.get('add_file')
        if file and allowed_file(file.filename):
            new_filename = 'uploads/' + time.strftime('%Y_%m_%d_%H-%M-%S', time.localtime()) + "_" + file.filename
            file.save(new_filename)
            flash("文件上传成功")
            with open("./"+new_filename, 'r', encoding='UTF-8') as f:
                print("open success")
                load_dicts = json.load(f)
                for key in load_dicts.keys():
                    for data in load_dicts[key]:
                        sqlAdd(data,key)
            flash("数据库更新成功")
        else:
            flash("文件上传失败，文件类型错误")

    tables = sql.sqlTables()
    return render_template('add.html', tables=tables)

@app.route('/updateAndView/<table>', methods=['GET', 'POST'])
def updateAndView(table):
    results = sql.sqlSelect(table, condition="", showcoordinates=None, column="")
    #空输入会返回""
    if request.method == "POST":
        # print(request.form.get("show_entity")) on None
        # if request.form.get("show_entity") :
        #     print("1")
        # else:
        #     print("2")
        type=list(request.form.keys())[-1].split("_")[0]
        if type=="select":
            results = sql.sqlSelect(table, column=request.form.get("select_column"), condition=request.form.get("select_condition"), showcoordinates=request.form.get("show_entity"))
            # if request.form.get("select_column"):
            #     if "id" in request.form.get("select_column").split(",") and request.form.get("show_entity") == "on":
            #         flash("要显示实体信息，需指定id(eg:city.id/city_coordinates.id)、不输入id或column为空")
            #     else:
            #         results = sql.sqlSelect(table,column=request.form.get("select_column"),condition=request.form.get("select_condition"),showcoordinates=request.form.get("show_entity"))
            # else:
            #     # print("1")
            #     results = sql.sqlSelect(table,condition=request.form.get("select_condition"),showcoordinates=request.form.get("show_entity"))
        else :
            if "" in list(request.form.values()):
                flash("删除与更新不可有空输入")
            else:
                if type == "delete":
                    sql.sqlDelete(table, condition=request.form.get("delete_condition"))
                else:
                    sql.sqlUpdate(table, column=request.form.get("update_column"), condition=request.form.get("update_condition"))
                results = sql.sqlSelect(table, condition="", showcoordinates=None)
    return render_template('updateAndView.html',results=results,table=table)



app.run()
