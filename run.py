#coding=utf8

import bottle
from bottle import *
from models import *
from spider import get_cn_data, get_sse_data


if not Config.gets():
    Config(interval=60, keywords="").save()

@route("/")
@route("/index")
@view("templates/index")
def index():
    c = Config.get()
    interval = c.interval
    keywords = c.keywords
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


@route("/get_data")
@view("templates/output")
def get_data():
    rs = get_cn_data()
    rs += get_sse_data()
    return locals()


@route("/config")
@view("templates/config")
def config():
    c = Config.get()
    interval = c.interval
    keywords = c.keywords
    return locals()


@post("/set_config")
def set_config():
    interval = request.params.interval
    keywords = request.params.keywords
    c = Config.get()
    c.interval = int(interval)
    c.keywords = keywords.replace(" ", ",").replace(u"\uff0c", ",")
    c.save()
    redirect("/config")



@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')




run(host='0.0.0.0', port="8000", debug=True)
