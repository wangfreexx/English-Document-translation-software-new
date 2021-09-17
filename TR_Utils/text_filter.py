import re
import os
import sys

class TextFilter():
    def __init__(self):
        self.english_dictionary = []
        self.english_dictionary_path = os.path.join(os.getcwd(), "dictionary", "words_alpha.txt")
        if sys.platform == "win32":
            self.english_dictionary_path = self.english_dictionary_path.replace('\\', '/')
        self.__loadDictFromTxt(self.english_dictionary_path)

    def __loadDictFromTxt(self,fn):
        with open(fn,'r') as f:
            for line in f:
                self.english_dictionary.append(line.strip('\n'))

    def removeDashLine(self,input_text):
        input_text = input_text.replace('\r\n', ' ')      # 把message中的所有'\r\n'替换成空格
        input_text = input_text.replace('\2', '')          # 删除单词中间的换行连字符
        return input_text