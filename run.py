#coding=utf8

import bottle
from bottle import *
from models import *
from spider import get_cn_data, get_sse_data


@route("/")
@route("/index")
@view("templates/index")
def index():
    title = "hello"
    content = "hello, world!!"
    return locals()


@route("/cninfo")
@route("/cninfo/")
@view("templates/cninfo")
def index():
    rs = QA.query().filter(origin="CN").order("-id").all()
    return locals()


@route("/sseinfo")
@route("/sseinfo/")
@view("templates/sseinfo")
def index():
    rs = QA.query().filter(origin="SSE").order("-id").all()
    return locals()



@route("/get_data")
@view("templates/output")
def get_data():
    rs = get_cn_data()
    rs += get_sse_data()
    return locals()




@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')




run(host='0.0.0.0', port="8000", debug=True)
