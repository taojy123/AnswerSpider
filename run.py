#coding=utf8

from bottle import *
from models import *
from spider import get_cn_data, get_sse_data, get_tgb_data
import sys
import os
import webbrowser


if not Config.gets():
    Config(interval=60, keywords="", keysize=20).save()

@route("/")
@route("/index")
@view("templates/index")
def index():
    c = Config.get()
    interval = c.interval
    return locals()


@route("/cninfo")
@view("templates/cninfo")
def cninfo():
    rs = QA.query().filter(origin="CN").order("-id").all()
    return locals()


@route("/sseinfo")
@view("templates/sseinfo")
def sseinfo():
    rs = QA.query().filter(origin="SSE").order("-id").all()
    return locals()


@route("/tgbinfo")
@view("templates/tgbinfo")
def tgbinfo():
    rs = QA.query().filter(origin="TGB").order("-id").all()
    return locals()


@route("/get_data")
@view("templates/output")
def get_data():
    rs = []
    rs += get_cn_data()
    rs += get_sse_data()
    rs += get_tgb_data()
    return locals()


@route("/config")
@view("templates/config")
def config():
    c = Config.get()
    interval = c.interval
    keywords = c.keywords
    keysize = c.keysize
    return locals()


@post("/set_config")
def set_config():
    interval = request.params.interval
    keywords = request.params.keywords
    keysize = request.params.keysize
    c = Config.get()
    c.interval = int(interval)
    c.keywords = keywords.replace(" ", ",").replace(u"\uff0c", ",")
    c.keysize = int(keysize)
    c.save()
    redirect("/config")



@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')




if os.path.isfile("temp"):
    os.remove("temp")
    webbrowser.open_new_tab('http://127.0.0.1:8000')
else:
    open("temp", "w").write("temp")



run(host='0.0.0.0', port="8000", debug=True)

