from datetime import date, datetime
import re
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
}

city = '重庆'

app_id = 'wx892de2a69a031f02'
app_secret = '3b372768c55f6093b5366181e6abcf89'

user_id = 'oBgGw6uckKo_zoqdYGD0BoN6jQIY'
template_id = 'CFkShEZ9-j1Ifq9XgZ53B_2gLQLDxPgbU-r8G11yxEc'

obj = re.compile(
    r'"(?P<city>.*?)":"重庆","lastUpdateTime":".*?","date":".*?","weather":"(?P<weather>.*?)","temp":(?P<temp>.*?),"humidity":".*?","wind":".*?","pm25":.*?,"pm10":.*?,"low":(?P<low>.*?),"high":(?P<high>.*?),"airData":".*?","airQuality":"(?P<airQuality>.*?)","dateLong":.*?,"weatherType":.*?,"windLevel":.*?,"province":"重庆"')


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    resp = requests.get(url, headers=headers)
    resp.close()
    result1 = obj.finditer(resp.text)
    for i in result1:
        weather = i.group('weather')
        temp = i.group('temp')
        high = i.group('high')
        low = i.group('low')
        airQuality = i.group('airQuality')
    return weather, temp, high, low, airQuality


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather, temp, high, low, airQuality = get_weather()
data = {"weather": {"value": weather, "color": get_random_color()},
        "temp": {"value": temp, "color": get_random_color()},
        "airQuality": {"value": airQuality, "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()},
        "high": {"value": high, "color": get_random_color()},
        "low": {"value": low, "color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
