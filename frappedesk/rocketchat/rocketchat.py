import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import frappe
from frappe.utils import logger
logger.set_log_level("DEBUG")
logger = frappe.logger("api", allow_site=True, file_count=50)
import time
import re

headers = {
	"content-type": "application/json"
}
endPoints = {
	"sendMessage": os.getenv('SEND_MESSAGE_END_POINT'),
	"history": os.getenv('HISTORY_ENDPOINT')+os.getenv('ROOM_ID'),
	"getResponse": os.getenv('GET_RESPONSE')
}

data = {
	"msg": "",
	"token": "",
	"rid": ""
}
params = {
	"token": "",
}

def sendMessages(msg, postData=data, headers=headers):
	msg = re.sub('<[^<]+?>', '', msg)
	postData["msg"] = msg
	postData["token"] = os.getenv('TOKEN')
	postData["rid"] = os.getenv('ROOM_ID')
	try:
		res = requests.post(endPoints["sendMessage"], data=json.dumps(postData), headers=headers)
	except requests.exceptions.Timeout as errt:
		logger.debug(f"Rocket Chat Timeout Error: {errt}")
		return None
	except requests.exceptions.TooManyRedirects as errr:
		logger.debug(f"Rocket Chat Too Many Redirect: {errr}")
		return None
	except requests.exceptions.RequestException as e:
		logger.debug(f"Rocket Chat Exception: {e}")
		return None

	res = res.json()
	return res['message']['_id'] if (type(res) is dict and 'message' in res and '_id' in res['message']) else None

def getHistory(params=params, headers=headers):
	params["token"] = os.getenv('TOKEN')
	try:
		res = requests.get(endPoints["history"], params=params, headers=headers)
	except requests.exceptions.Timeout as errt:
		logger.debug(f"Rocket Chat Timeout Error: {errt}")
		return None
	except requests.exceptions.TooManyRedirects as errr:
		logger.debug(f"Rocket Chat Too Many Redirect: {errr}")
		return None
	except requests.exceptions.RequestException as e:
		logger.debug(f"Rocket Chat Exception: {e}")
		return None
	return res.json()

def retrieveResponse(msgID=None):
	try:
		res = requests.get(endPoints["getResponse"]+msgID)
		return res.json()
	except requests.exceptions.Timeout as errt:
		logger.debug(f"Rocket Chat Timeout Error: {errt}")
		return {"error": errt}
	except requests.exceptions.TooManyRedirects as errr:
		logger.debug(f"Rocket Chat Too Many Redirect: {errr}")
		return {"error": errr}
	except requests.exceptions.RequestException as e:
		logger.debug(f"Rocket Chat Exception: {e}")
		return {"error": e}
	
def getResponse(msg, msgID=None, history={}):
	msgID = sendMessages(msg) if msg else None
	time.sleep(2)
	#history = getHistory()
	responses = retrieveResponse(msgID) if msgID else {}
	#if msgID and 'messages' in history:
	#	message_index = next((index for (index, d) in enumerate(history['messages']) if d["_id"] == msgID), None)
	#	response_index = message_index - 1
	#	response = history['messages'][response_index]['msg']
	#	response = "<p>" + response.replace("\n", "<br>") + "</p>"
	#	confidence = history['messages'][response_index]['confidence'] if 'confidence' in history['messages'][response_index] else 0
	#	return {'response': response, 'confidence': confidence}
	if msgID and 'response' in responses and 'confidence' in responses:
		return responses
	else:
		response = "Thank you for contacting Learner Support. I shall get back to you with answers to your queries."
		logger.debug(f"{response}")
		return {'response': response, 'confidence': 0}

