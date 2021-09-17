import binascii
import configparser
import hashlib
import hmac
import http.client
import json
import random
import sys
import time

import urllib
import urllib.parse
import urllib.request

from google_trans_new import google_translator


def get_extra_result_of_single_word(word, translator):
    """

    :param word: single word string contain no space
    :param translator: google translator object
    :return: result string
    """
    translate_res = translator.translate(word, dest='zh-cn')
    extra_data = translate_res.extra_data
    all_translations_list = extra_data['all-translations']
    result = ''
    if all_translations_list is None:
        result = translate_res.text
        pass
    else:
        for translation in all_translations_list:
            word_class = translation[0]
            result += word_class + '\n    '
            word_tsl_list = translation[2]
            for tsl in word_tsl_list:
                tsl_res = tsl[0]
                tsl_src_list = tsl[1]
                tsl_src = ''
                # obj = ''
                # confidence = 0
                if tsl_src_list is None:
                    pass
                else:
                    for i in tsl_src_list:
                        tsl_src += i + ' '
                # if len(tsl) <3:
                #     pass
                # else:
                #     obj = tsl[2]
                #     confidence = tsl[3]
                result += '{0} [{1}]\n    '.format(tsl_res, tsl_src)
            result += '\n'
    return result

    pass

# 谷歌翻译


def get_translation_by_google(text_input):
    ft = google_translator(timeout=10)
    lang = 'zh-cn'
    return ft.translate(text_input, lang)


# 百度翻译
def baidu_translate(appid, secretKey, content):
    # appid = '20151113000005349'
    # secretKey = 'osubCEzlGjzvw8qdQc41'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'auto'  # 源语言
    toLang = 'zh'  # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        return dst
    except Exception as e:
        return "百度翻译出错"
    finally:
        if httpClient:
            httpClient.close()


def configfile_read():
    #confile = open("config.ini", "wb")
    config2 = configparser.ConfigParser()
    # -read读取ini文件
    config2.read("config.ini", encoding='UTF-8')
    baidu_appidstr = config2.get('baidu', 'appid')
    baidu_secretKeystr = config2.get('baidu', 'secretKey')

    ten_appidstr = config2.get('Tencent', 'appid')
    ten_secretKeystr = config2.get('Tencent', 'secretKey')
    return baidu_appidstr, baidu_secretKeystr, ten_appidstr, ten_secretKeystr
    # confile.close()


def sign(secretKey, signStr, signMethod):
    '''
    该方法主要是实现腾讯云的签名功能
    :param secretKey: 用户的secretKey
    :param signStr: 传递进来字符串，加密时需要使用
    :param signMethod: 加密方法
    :return:
    '''
    if sys.version_info[0] > 2:
        signStr = signStr.encode("utf-8")
        secretKey = secretKey.encode("utf-8")

    # 根据参数中的signMethod来选择加密方式
    if signMethod == 'HmacSHA256':
        digestmod = hashlib.sha256
    elif signMethod == 'HmacSHA1':
        digestmod = hashlib.sha1

    # 完成加密，生成加密后的数据
    hashed = hmac.new(secretKey, signStr, digestmod)
    base64 = binascii.b2a_base64(hashed.digest())[:-1]

    if sys.version_info[0] > 2:
        base64 = base64.decode()

    return base64


def dictToStr(dictData):
    '''
    本方法主要是将Dict转为List并且拼接成字符串
    :param dictData:
    :return: 拼接好的字符串
    '''
    tempList = []
    for eveKey, eveValue in dictData.items():
        tempList.append(str(eveKey) + "=" + str(eveValue))
    return "&".join(tempList)


# 用户必须准备好的secretId和secretKey
# 可以在 https://console.cloud.tencent.com/capi 获取

def tencent_translate(secretId, secretKey, content):
    # 在此处定义一些必须的内容
    timeData = str(int(time.time()))  # 时间戳
    nonceData = int(random.random() * 10000)  # Nonce，官网给的信息：随机正整数，与 Timestamp 联合起来， 用于防止重放攻击
    actionData = "TextTranslate"  # Action一般是操作名称
    uriData = "tmt.tencentcloudapi.com"  # uri，请参考官网
    signMethod = "HmacSHA256"  # 加密方法
    requestMethod = "GET"  # 请求方法，在签名时会遇到，如果签名时使用的是GET，那么在请求时也请使用GET
    regionData = "ap-hongkong"  # 区域选择
    versionData = '2018-03-21'  # 版本选择

# 签名时需要的字典
# 首先对所有请求参数按参数名做字典序升序排列，所谓字典序升序排列，
# 直观上就如同在字典中排列单词一样排序，按照字母表或数字表里递增
# 顺序的排列次序，即先考虑第一个“字母”，在相同的情况下考虑第二
# 个“字母”，依此类推。
    signDictData = {
        'Action': actionData,
        'Nonce': nonceData,
        'ProjectId': 0,
        'Region': regionData,
        'SecretId': secretId,
        'SignatureMethod': signMethod,
        'Source': "en",
        'SourceText':content,
        'Target': "zh",
        'Timestamp': int(timeData),
        'Version': versionData,
    }

# 获得拼接的字符串，用于签名
# 此步骤生成请求字符串。 将把上一步排序好的请求参数格式化成“参数名称”=“参数值”的形式，如对Action参数，
# 其参数名称为"Action"，参数值为"DescribeInstances"，因此格式化后就为Action=DescribeInstances。
# 注意：“参数值”为原始值而非url编码后的值。
# 然后将格式化后的各个参数用"&"拼接在一起，最终生成请求字符串。
# 此步骤生成签名原文字符串。 签名原文字符串由以下几个参数构成:
# 1) 请求方法: 支持 POST 和 GET 方式，这里使用 GET 请求，注意方法为全大写。
# 2) 请求主机:查看实例列表(DescribeInstances)的请求域名为：cvm.tencentcloudapi.com。实际的请求域名根据接口所属模块的不同而不同，详见各接口说明。
# 3) 请求路径: 当前版本云API的请求路径固定为 / 。 4) 请求字符串: 即上一步生成的请求字符串。
# 签名原文串的拼接规则为:
#   请求方法 + 请求主机 +请求路径 + ? + 请求字符串
    requestStr = "%s%s%s%s%s" % (requestMethod, uriData, "/", "?", dictToStr(signDictData))

# 调用签名方法，同时将结果进行url编码，官方文档描述如下：
# 生成的签名串并不能直接作为请求参数，需要对其进行 URL 编码。 注意：如果用户的请求方法是GET，则对所有请求参
# 数值均需要做URL编码。 如上一步生成的签名串为 EliP9YW3pW28FpsEdkXt/+WcGeI= ，最终得到的签名串请求参数(Signature)
# 为： EliP9YW3pW28FpsEdkXt%2f%2bWcGeI%3d ，它将用于生成最终的请求URL。
    signData = urllib.parse.quote(sign(secretKey, requestStr, signMethod))

# 上述操作是实现签名，下面即进行请求
# 先建立请求参数, 此处参数只在签名时多了一个Signature
    actionArgs = signDictData
    actionArgs["Signature"] = signData

# 根据uri构建请求的url
    requestUrl = "https://%s/?" % (uriData)
    #requestUrl=urllib.parse.quote_plus(requestUrl)
# 将请求的url和参数进行拼接
    requestUrlWithArgs = requestUrl + dictToStr(actionArgs)
    requestUrlWithArgs=requestUrlWithArgs.replace(' ','+')

# 获得response
    responseData = urllib.request.urlopen(requestUrlWithArgs).read().decode("utf-8")
    
# 获得到的结果形式：
#  {"Response":{"RequestId":"0fd2e5b4-0beb-4e01-906f-e63dd7dd33af","Source":"en","Target":"zh","TargetText":"\u4f60\u597d\u4e16\u754c"}}
    if "Error" in responseData:
        print(responseData)
        return "腾讯翻译错误"
    return (json.loads(responseData)["Response"]["TargetText"])
