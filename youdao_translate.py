# -*- coding:utf-8 -*-
"""
@author: XiangNan
@desc: 利用有道翻译进行翻译
"""
import time
import json
import random
import hashlib
import requests


class YoudaoTranslate:
    def __init__(self, word):
        self.word = word
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Origin': 'http://fanyi.youdao.com',
        }

    def get_params(self):
        """
        获取翻译请求所需的参数bv, ts, salt, sign
        """
        bv = hashlib.md5('/'.join(self.headers['User-Agent'].split('/')[1:]).encode()).hexdigest()
        ts = str(int(time.time() * 1000))
        salt = ts + str(random.randint(0, 9))
        sign_text = 'fanyideskweb' + str(self.word) + salt + 'n%A-rKaT5fb[Gy?;N5@Tj'
        sign = hashlib.md5(sign_text.encode()).hexdigest()
        return bv, ts, salt, sign

    def translate(self):
        """
        拼接参数，构造请求，发送翻译请求并获取结果
        """
        bv, ts, salt, sign = self.get_params()
        data = {
            'i': self.word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': bv,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }
        # 翻译请求网址
        trans_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        # 请求有道翻译首页获取cookie
        self.session.get(url=self.headers['Origin'], headers=self.headers)
        # 发送翻译请求返回结果
        response = self.session.post(url=trans_url, data=data, headers=self.headers)
        result = json.loads(response.text)['translateResult'][0][0]['tgt']
        return result


if __name__ == '__main__':
    # 所需翻译文字
    word = 'white'
    # 翻译并输出结果
    translator = YoudaoTranslate(word)
    result = translator.translate()
    print(result)