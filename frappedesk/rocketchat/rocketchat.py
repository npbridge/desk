import requests
from requests.auth import HTTPBasicAuth
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
credentials = {
    "user": os.getenv('BOT_API_USERNAME'),
    "password": os.getenv('BOT_API_PASSWORD')
}
endPoints = {
	"sendMessage": os.getenv('BOT_API_QUERY_ENDPOINT')
}

data = {
	"bot": os.getenv('BOT_UUID'),
    "query": "",
    "interface": os.getenv('BOT_INTERFACE'),
    "ticket": {
        "id": "",
        "user": ""
    }
}

def getResponse(query, user, ticket_id, postData=data, headers=headers):
    postData["query"] = query
    postData["ticket"]["id"] = ticket_id
    postData["ticket"]["user"] = user
    defaultResponse = {
		"response": "Thank you for contacting Learner Support. I shall get back to you with answers to your queries.",
		"confidence": 0
	}
    try:
        res = requests.post(
            endPoints["sendMessage"],
            auth=HTTPBasicAuth(credentials["user"], credentials["password"]), 
            data=json.dumps(postData), 
            headers=headers
        )
        defaultResponse["response"] = res.text
        defaultResponse["confidence"] = 1
    except requests.exceptions.Timeout as errt:
        logger.debug(f"Middleware Timeout Error: {errt}")
    except requests.exceptions.TooManyRedirects as errr:
        logger.debug(f"Middleware Too Many Redirect: {errr}")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Middleware Exception: {e}")

    return defaultResponse
