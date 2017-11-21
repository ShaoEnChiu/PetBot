#encoding=UTF-8

from flask import Flask, request
import requests
import json
import re
from bs4 import BeautifulSoup as bs
from aenum import Enum

requests.packages.urllib3.disable_warnings()

# 可以直接利用Line提供的SDK來處理
# from linebot import LineBotApi
# from linebot.models import TextSendMessage

# Enum 透過 name 跟 value 屬性讀取
class EventType(Enum):
	message = 1
	follow = 2
	unfollow = 3
	join = 4
	leave = 5
	postback = 6
	beacon = 7

class SourceType(Enum):
	user = 1
	group = 2
	room = 3

class MessageType(Enum):
	text = 1
	image = 2
	video = 3
	audio = 4
	file = 5
	location = 6
	sticker = 7

channeltoken='qYzIzIqCTWz82oZkTnO0A9Ggiz6bNkS1VHIMU/9kCww/M709Ff+PFDObSL+OFvhSQlLpYlTDmxkKgKS2SwbkoZs/tLEgzLlJYY+Wsf1yB6J//rQfZOuv9dLeCpt2fcBg984pT1wLpBT0uNEcmBuAaQdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)

# 測試app.py有沒有Deploy成功
@app.route("/", methods=["GET"])
def index():
	return "hello world 1>>> index", 200

# 在Line的Document當中有寫到，webhook URL會透過post request呼叫 https://{urladdress}/callback
@app.route("/callback", methods=["POST"])
def callback():
	json_data = request.get_json()
	for i in json_data['events']:
		token = i['replyToken']
		# print i['source']['userId']

		# get contentType
		# content_type = getContent_type(i['message']['type'])

		if EventType.message.name in i['type']:
			if MessageType.text.name in i['message']['type']:
				replyMessageTextApi(token, json_data, i['message']['text'])
			elif MessageType.image.name in i['message']['type']:
				replyMessageImageApi(token, json_data, i['message']['id'])
			elif MessageType.video.name in i['message']['type']:
				replyapi(token, json_data)
			elif MessageType.audio.name in i['message']['type']:
				replyapi(token, json_data)
			elif MessageType.file.name in i['message']['type']:
				replyapi(token, json_data)
			elif MessageType.location.name in i['message']['type']:
				replyapi(token, json_data)
			elif MessageType.sticker.name in i['message']['type']:
				replyapi(token, json_data)
		elif EventType.follow.name in i['type']:
			replyapi(token, json_data)
		elif EventType.unfollow.name in i['type']:
			replyapi(token, json_data)
		elif EventType.join.name in i['type']:
			replyapi(token, json_data)
		elif EventType.leave.name in i['type']:
			replyapi(token, json_data)
		elif EventType.postback.name in i['type']:
			replyapi(token, json_data)
		elif EventType.beacon.name in i['type']:
			replyapi(token, json_data)

	return "hello world >>> callback", 200

def getContent_type(content_type):
	switcher = {
		0:"text",
		1:"Image",
		2:"video",
		3:"audio",
		4:"location",
		5:"sticker"
	}
	return switcher.get(content_type, "nothing")

def processMessage(msg):
	ret = []
	mat = []
	pat = re.compile(r".*(掰掰).*")
	mat = pat.findall(msg)
	if len(mat) == 0:
		ret.append(msg)
	else:
		ret.append('慢走不送')
	return ret

def genData(accesstoken, msgs):
	data = [];
	for msg in msgs:
		data.append({'type':'text', 'text':msg})
	ret = {
		'replyToken':accesstoken,
		'messages':data
	}
	return ret

def genHeaders(channeltoken):
	ret = {
		'Content-Type':'application/json',
		'Authorization':'Bearer ' + channeltoken
	}
	return ret

def replyMessageImageApi(accesstoken, json_data, messageID):
	headers = genHeaders(channeltoken)

	url = ''.join(['https://api.line.me/v2/bot/message/', messageID.encode('utf-8'), '/content']
	img_data = [];
	res = requests.get(url, headers = headers)
	img_data.append({'type':'text', 'text':url})
	#img_data.append({'type':'text', 'text':res.text})
	data = {
		'replyToken':accesstoken,
		'messages':img_data
	}

	datajson = json.dumps(data)
	res = requests.post('https://api.line.me/v2/bot/message/reply', headers = headers, data = datajson)

def getPetStatusMsg(accesstoken, json_data):
	url = 'http://iot.cht.com.tw/iot/v1/device/4837051040/sensor/Sensor01/rawdata'
	headers = {
		'Content-Type':'application/json',
		'CK':'PKM0B5MS0SZFYE5E2M'
	}
	res = requests.get(url, headers = headers)
	ret = ''.join(['心跳：', json.loads(res.text)['value'][0].encode('utf-8'), '\n'])

	url = 'http://iot.cht.com.tw/iot/v1/device/4837051040/sensor/Sensor02/rawdata'
	headers = {
		'Content-Type':'application/json',
		'CK':'PKM0B5MS0SZFYE5E2M'
	}
	res = requests.get(url, headers = headers)
	ret = ''.join([ret, '血壓：', json.loads(res.text)['value'][0].encode('utf-8'), '\n'])

	url = 'http://iot.cht.com.tw/iot/v1/device/4837051040/sensor/Sensor04/rawdata'
	headers = {
		'Content-Type':'application/json',
		'CK':'PKM0B5MS0SZFYE5E2M'
	}
	res = requests.get(url, headers = headers)
	ret = ''.join([ret, '溫度：', json.loads(res.text)['value'][0].encode('utf-8')])

	return ret

def replyMessageTextApi(accesstoken, json_data, msg):
	ret = '我不太清楚~'
	if '寵物身體狀況' in msg.encode('utf-8'):
		ret = getPetStatusMsg(accesstoken, json_data)

	data = genData(accesstoken, [ret])
	datajson = json.dumps(data)
	headers = genHeaders(channeltoken)
	urladdress = 'https://api.line.me/v2/bot/message/reply'
	# 依照Line Document當中的定義，準備好headers和data(json格式)。
	res = requests.post(urladdress, headers = headers, data = datajson)

def replyapi(accesstoken, json_data):
	# 利用Line SDK的方式，做reply的作業。
	"""
	line_bot_api = LineBotApi(channeltoken)

	try:
		line_bot_api.reply_message(accesstoken, TextSendMessage(text='Hello World!'))
	except linebot.LineBotApiError as e:
		print e
		# error handle
	"""

	data = genData(accesstoken, [json.dumps(json_data).encode('utf-8')])
	datajson = json.dumps(data)
	headers = genHeaders(channeltoken)
	urladdress = 'https://api.line.me/v2/bot/message/reply'
	# 依照Line Document當中的定義，準備好headers和data(json格式)。
	res = requests.post(urladdress, headers = headers, data = datajson)

if __name__== '__main__':
	app.run()
