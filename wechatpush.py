import re
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
}

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

obj1 = re.compile(r'<br>.*?</div>.*?<div class="day-item dayicon">.*?<img src=".*?">.*?</div>.*?<div class="day-item">(?P<day_item1>.*?)</div>.*?<div class="day-item">.*?</div>.*?<div class="day-item">.*?</div>.*?<div class="day-item bardiv">.*?<div class="bar" style="top:0px; bottom:0px;">.*?<div class="high">.*?(?P<high>.*?)</div>.*?<div class="low">.*?(?P<low>.*?)</div>.*?</div>.*?</div>.*?<div class="day-item nighticon">.*?<img src=".*?">.*?</div>.*?<div class="day-item">(?P<day_item2>.*?)</div>.*?<div class="day-item">.*?</div>.*?<div class="day-item">.*?</div>.*?</div>.*?<div class="pull-left day ">.*?<div class="day-item">.*?',re.S)
obj2 = re.compile(r'"name":"新增本土","data":\[.*,(?P<local_number>.*?)\]}\],"updateDate"')
obj3 = re.compile(r'"data":"(?P<data>.*?)"')


def get_weather():
    url = "https://weather.cma.cn/web/weather/57516"
    resp = requests.get(url, headers=headers)
    resp.close()
    result1 = obj1.finditer(resp.text)
    for i in result1:
        weather1 = i.group('day_item1').replace(' ', '')
        weather2 = i.group('day_item2').replace(' ', '')
        high = i.group('high').replace(' ', '')
        low = i.group('low').replace(' ', '')
        break
    return weather1, weather2, high, low


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
weather1, weather2, high, low = get_weather()
weather = weather1 + '转' + weather2
temp = low + '~' + high
local_number = get_local_number()
words = get_words()
data = {
    "local_number": {"value": local_number, "color": get_random_color()},
    "weather": {"value": weather, "color": get_random_color()},
    "temp": {"value": temp, "color": get_random_color()},
    "words": {"value": words, "color": get_random_color()}
}
res = wm.send_template(user_id, template_id, data)
