import re
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
}

city = '重庆'

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

obj1 = re.compile(
    r'"(?P<city>.*?)":"重庆","lastUpdateTime":".*?","date":".*?","weather":"(?P<weather>.*?)","temp":(?P<temp>.*?),"humidity":".*?","wind":".*?","pm25":.*?,"pm10":.*?,"low":(?P<low>.*?),"high":(?P<high>.*?),"airData":".*?","airQuality":"(?P<airQuality>.*?)","dateLong":.*?,"weatherType":.*?,"windLevel":.*?,"province":"重庆"')
obj2 = re.compile(r'"name":"新增本土","data":\[.*,(?P<local_number>.*?)\]}\],"updateDate"')
obj3 = re.compile(r'"data":"(?P<data>.*?)"')


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    resp = requests.get(url, headers=headers)
    resp.close()
    result1 = obj1.finditer(resp.text)
    for i in result1:
        weather = i.group('weather')
        temp = i.group('temp')
        high = i.group('high')
        low = i.group('low')
        airQuality = i.group('airQuality')
    return weather, temp, high, low, airQuality


def get_local_number():
    url = 'https://voice.baidu.com/newpneumonia/getv2?from=mola-virus&stage=publish&target=trendCity&area=重庆-沙坪坝区'
    resp = requests.get(url, headers=headers)
    resp.close()
    result2 = obj2.finditer(resp.text)
    for i in result2:
        local_number = i.group('local_number')
    return local_number


def get_words():
    url = 'https://www.iamwawa.cn/home/lizhi/ajax'
    resp = requests.get(url, headers=headers)
    resp.close()
    resp = resp.text.encode('utf-8').decode('unicode-escape')
    result = obj3.finditer(resp)
    for i in result:
        words = i.group('data')
    return words


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather, temp, high, low, airQuality = get_weather()
local_number = get_local_number()
words = get_words()
data = {"local_number": {"value": local_number, "color": get_random_color()},
        "weather": {"value": weather, "color": get_random_color()},
        "temp": {"value": temp, "color": get_random_color()},
        "airQuality": {"value": airQuality, "color": get_random_color()},
        "words": {"value": words, "color": get_random_color()},
        "high": {"value": high, "color": get_random_color()},
        "low": {"value": low, "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
