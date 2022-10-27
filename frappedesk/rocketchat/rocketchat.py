import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import frappe
from frappe.utils import logger
logger.set_log_level("DEBUG")
logger = frappe.logger("api", allow_site=True, file_count=50)

headers = {
	"content-type": "application/json"
}
endPoints = {
	"sendMessage": os.getenv('SEND_MESSAGE_END_POINT')
}

data = {
	"message": ""
}

def getResponse(msg, postData=data, headers=headers):
	postData["message"] = msg
	defaultResponse = {
		"response": "Thank you for contacting Learner Support. I shall get back to you with answers to your queries.",
		"confidence": 0
	}
	try:
		res = requests.post(endPoints["sendMessage"], data=json.dumps(postData), headers=headers)
		defaultResponse = res.json()
	except requests.exceptions.Timeout as errt:
		logger.debug(f"Middleware Timeout Error: {errt}")
	except requests.exceptions.TooManyRedirects as errr:
		logger.debug(f"Middleware Too Many Redirect: {errr}")
	except requests.exceptions.RequestException as e:
		logger.debug(f"Middleware Exception: {e}")

	return defaultResponse
