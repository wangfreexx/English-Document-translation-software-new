from google_trans_new import  google_translator  

translator = google_translator()  
translate_text = translator.translate('美国下一届总统将会是谁？',lang_src='zh-cn',lang_tgt='en')  
print(translate_text)
