import threading
import time
from TR_Utils.controller import con
from TR_Utils.translate import get_translation_by_google
from TR_Utils.translate import configfile_read
from TR_Utils.translate import baidu_translate
from TR_Utils.translate import tencent_translate


class WatchClip(threading.Thread):
    def __init__(self):
        super(WatchClip, self).__init__()
        self.name = ""
        self.expire = False
        self.text = ''

    def run(self):
        recent_text = self.text
        while True and not self.expire:
            cur_text = self.text
            if cur_text == recent_text:
                time.sleep(0.1)
            else:
                recent_text = cur_text
                self.update(cur_text)

    def setTranslateText(self, inputText):
        self.text = inputText

    def update(self, cur_text):
        reslut_text = "谷歌翻译:" + "\n"
        reslut_text = reslut_text + get_translation_by_google(cur_text) + "\n"
        baidu_appidstr, baidu_secretKeystr,ten_appidstr, ten_secretKeystr = configfile_read()
        if len(baidu_appidstr) != 0 and len(baidu_secretKeystr) != 0:           
            reslut_text = reslut_text + "百度翻译:" + "\n"
            reslut_text = reslut_text + baidu_translate(baidu_appidstr, baidu_secretKeystr, cur_text)+"\n"
        if len(ten_appidstr)!=0 and len(ten_secretKeystr)!=0:
            reslut_text = reslut_text + "腾讯翻译:" + "\n"
            reslut_text = reslut_text + tencent_translate(ten_appidstr, ten_secretKeystr, cur_text)+"\n"


        con.translationChanged.emit(reslut_text)

    def expired(self):
        self.expire = True
