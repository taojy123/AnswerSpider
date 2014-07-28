from nanorm import *


class QA(Model):
    origin = CharField()
    question = CharField()
    answer = CharField()
    url = CharField()

class Config(Model):
    interval = IntegerField()
    keywords = CharField()
        


set_db_name("data.db")
QA.try_create_table()