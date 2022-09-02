import re
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random
import os
import time


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
# 消息接收者
user_id = os.environ["USER_ID"]
# 自定义规则
template_id = os.environ["TEMPLATE_ID"]


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
}


obj1 = re.compile(r'<div class="pull-left day actived">.*?<div class="day-item">.*?<br/>.*?</div>.*?<div class="day-item dayicon"><img src=".*?"/></div>.*?<div class="day-item">(?P<day_item1>.*?)</div>.*?<div class="day-item">.*?</div>.*?<div class="day-item">.*?</div>.*?<div class="day-item bardiv"><div class="bar" style=.*?><div class="high">(?P<high>.*?)</div><div class="low">(?P<low>.*?)</div></div></div>.*?<div class="day-item nighticon"><img src=".*?"/></div>.*?<div class="day-item">(?P<day_item2>.*?)</div>.*?<div class="day-item">.*?</div>.*?<div class="day-item">.*?</div>', re.S)
obj2 = re.compile(r'"data":"(?P<motivational_sentence>.*?)"')
obj3 = re.compile(r'{"content":"(?P<chicken_soup_for_the_soul>.*?)"}')


# 天气weather，温度temp
def get_weather():
    url = "https://weather.cma.cn/web/weather/57516"
    resp = requests.get(url, headers=headers)
    resp.close()
    # print(resp.text)
    result1 = obj1.finditer(resp.text)
    for i in result1:
        weather1 = i.group('day_item1').replace(' ', '')
        weather2 = i.group('day_item2').replace(' ', '')
        high = i.group('high').replace(' ', '')
        low = i.group('low').replace(' ', '')
        return weather1, weather2, high, low
        break


weather1, weather2, high, low = get_weather()
if weather1 == weather2:
    weather = weather1
else:
    weather = weather1 + '转' + weather2
temp = low + '~' + high


# 励志句子motivational_sentence
def get_motivational_sentence():
    url = 'https://www.iamwawa.cn/home/lizhi/ajax'
    resp = requests.get(url, headers=headers)
    resp.close()
    resp = resp.text.encode('utf-8').decode('unicode-escape')
    result = obj2.finditer(resp)
    for i in result:
        motivational_sentence = i.group('motivational_sentence')
    return motivational_sentence


motivational_sentence = get_motivational_sentence()


# 毒鸡汤chicken_soup_for_the_soul
def get_chicken_soup_for_the_soul():
    url = 'https://uapi.woobx.cn/app/alapi'
    data = {
        'path': '/api/soul',
        'params': '{"format":"json"}'
    }
    resp = requests.post(url, headers=headers, data=data)
    resp.close()
    resp = resp.content.decode('utf-8')
    result = obj3.finditer(resp)
    for i in result:
        chicken_soup_for_the_soul = i.group('chicken_soup_for_the_soul')
    return chicken_soup_for_the_soul


chicken_soup_for_the_soul = get_chicken_soup_for_the_soul()


# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 不动如山
client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)


data = {
    "weather": {"value": weather, "color": get_random_color()},
    "temp": {"value": temp, "color": get_random_color()},
    "motivational_sentence": {"value": motivational_sentence, "color": get_random_color()},
    "chicken_soup_for_the_soul": {"value": chicken_soup_for_the_soul, "color": get_random_color()}
}


res = wm.send_template(user_id, template_id, data)
