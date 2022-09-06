import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import frappe
from frappe.utils import logger
logger.set_log_level("WARNING")
logger = frappe.logger("api", allow_site=True, file_count=50)


headers = {
	"content-type": "application/json"
}
endPoints = {
	"sendMessage": os.getenv('SEND_MESSAGE_END_POINT'),
	"history": os.getenv('HISTORY_ENDPOINT')+os.getenv('ROOM_ID')+"?token="+os.getenv('TOKEN')
}

data = {
	"msg": "",
	"token": "",
	"rid": ""
}
params = {
	"token": "",
	"rid": ""
}

def sendMessages(msg, postData=data, headers=headers):
	postData["msg"] = msg
	postData["token"] = os.getenv('TOKEN')
	postData["rid"] = os.getenv('ROOM_ID')
	try:
		res = requests.post(endPoints["sendMessage"], data=json.dumps(postData), headers=headers)
	except requests.exceptions.Timeout as errt:
		logger.debug(f"Rocket Chat Timeout Error: {errt}")
		return False
	except requests.exceptions.TooManyRedirects as errr:
		logger.debug(f"Rocket Chat Too Many Redirect: {errr}")
		return False
	except requests.exceptions.RequestException as e:
		logger.debug(f"Rocket Chat Exception: {e}")
		return False

	res = res.json()
	return res['message']['_id']

def getHistory(params=params, headers=headers):
	params["token"] = os.getenv('TOKEN')
	params["rid"] = os.getenv('ROOM_ID')
	try:
		res = requests.get(endPoints["history"], params=params, headers=headers)
	except requests.exceptions.Timeout as errt:
		logger.debug(f"Rocket Chat Timeout Error: {errt}")
		return False
	except requests.exceptions.TooManyRedirects as errr:
		logger.debug(f"Rocket Chat Too Many Redirect: {errr}")
		return False
	except requests.exceptions.RequestException as e:
		logger.debug(f"Rocket Chat Exception: {e}")
		return False
	return res.json()

def getResponse(msg, msgID=None, history={}):
	msgID = sendMessages(msg)
	history = getHistory()
	if messageID and history:
		message_index = next((index for (index, d) in enumerate(history['messages']) if d["_id"] == msgID), None)
		response_index = message_index - 1
		response = history['messages'][response_index]['msg']
		response = "<p>" + response.replace("\n", "<br>") + "</p>"
		return response
	else:
		response = "Bot can't respond this time, Please try after some time"
		logger.debug(f"{response}")
		return response

