from nanorm import *
import time

set_db_name("data.db")

class QA(Model):
    origin = CharField()
    question = CharField()
    answer = CharField()
    url = CharField()
    time = CharField()


    def text_show(self, text):
    	text_show = text
        keywords = Config.get().keywords
        keysize = Config.get().keysize
    	for keyword in keywords.split(","):
            if keyword:
    		  text_show = text_show.replace(keyword, "<b style='color:red;font-size:%dpx;'>%s</b>" % (keysize, keyword) )
    	return text_show

    @property
    def question_show(self):
    	return self.text_show(self.question)

    @property
    def answer_show(self):
    	return self.text_show(self.answer)

    # overwrite
    def save(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time = now
        super(QA, self).save()





class Config(Model):
    interval = IntegerField()
    keywords = CharField()
    keysize = IntegerField()
        
