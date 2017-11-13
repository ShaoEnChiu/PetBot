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

app = Flask(__name__)

# 測試app.py有沒有Deploy成功
@app.route("/", methods=["GET"])
def index():
	return "hello world 3 >>> index", 200

# 在Line的Document當中有寫到，webhook URL會透過post request呼叫 https://{urladdress}/callback
@app.route("/callback", methods=["POST"])
def callback():
	temp = request.get_json()
	for i in temp['events']:
		ttt = i['replyToken']
		print i['source']['userId']
		if i['message']['type']=='text':
			msg = i['message']['text']
		replyapi(ttt, msg)
	return "hello world >>> callback", 200

def processMessage(msg):
	ret = []
	mat = []
	pat = re.compile(r".*(掰掰).*")
	mat = pat.findall(msg)
	if len(mat) == 0:
		ret.append('朕知道了')
		ret.append('可以退下了')
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

def replyapi(accesstoken, msg):
	channeltoken='qYzIzIqCTWz82oZkTnO0A9Ggiz6bNkS1VHIMU/9kCww/M709Ff+PFDObSL+OFvhSQlLpYlTDmxkKgKS2SwbkoZs/tLEgzLlJYY+Wsf1yB6J//rQfZOuv9dLeCpt2fcBg984pT1wLpBT0uNEcmBuAaQdB04t89/1O/w1cDnyilFU='

	# 利用Line SDK的方式，做reply的作業。
	"""
	line_bot_api = LineBotApi(channeltoken)

	try:
		line_bot_api.reply_message(accesstoken, TextSendMessage(text='Hello World!'))
	except linebot.LineBotApiError as e:
		print e
		# error handle
	"""

	t = msg.encode('utf-8')
	data = {}
	data = genData(accesstoken, processMessage(t))

	headers = genHeaders(channeltoken)

	urladdress = 'https://api.line.me/v2/bot/message/reply'
	datajson = json.dumps(data)
	# 依照Line Document當中的定義，準備好headers和data(json格式)。
	res = requests.post(urladdress, headers = headers, data = datajson)

if __name__== '__main__':
	app.run()