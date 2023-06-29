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
credentials = {
    "user": os.getenv('BOT_API_USERNAME'),
    "password": os.getenv('BOT_API_PASSWORD')
}
endPoints = {
    "sendMessage": os.getenv('BOT_API_ENDPOINT') + "bot-api/query/",
    "getToken": os.getenv('BOT_API_ENDPOINT') + "api/auth/token/login/",
}

data = {
    "bot": os.getenv('BOT_API_UUID'),
    "query": "",
    "interface": os.getenv('BOT_API_INTERFACE'),
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
        res = queryAPI(postData)
        if res.status_code == 200:
            bot_message = res.json()
            bot_message = json.loads(bot_message)
            defaultResponse["response"] = bot_message["message"]
            defaultResponse["confidence"] = 1
        if res.status_code == 401:
            updatingToken = getAuthenticated()
            if updatingToken == 200:
                res = queryAPI(postData)
                if res.status_code == 200:
                    bot_message = res.json()
                    bot_message = json.loads(bot_message)
                    defaultResponse["response"] = bot_message["message"]
                    defaultResponse["confidence"] = 1
            else:
                logger.debug(f"Error while getting BOT API token")

    except requests.exceptions.Timeout as errt:
        logger.debug(f"Middleware Timeout Error: {errt}")
    except requests.exceptions.TooManyRedirects as errr:
        logger.debug(f"Middleware Too Many Redirect: {errr}")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Middleware Exception: {e}")

    return defaultResponse

def getAuthenticated():
    try:
        headers.pop("Authorization", None)
        res = requests.post(
            endPoints["getToken"],
            data=json.dumps({
                "email": credentials["user"],
                "password": credentials["password"]
            }), 
            headers=headers
        )
        if res.status_code == 200:
            response = res.json()
            os.environ["BOT_API_TOKEN"] = response["auth_token"]
    except requests.exceptions.Timeout as errt:
        logger.debug(f"Getting Token Timeout Error: {errt}")
    except requests.exceptions.TooManyRedirects as errr:
        logger.debug(f"Getting Token Too Many Redirect: {errr}")
    except requests.exceptions.RequestException as e:
        logger.debug(f"Getting Token Exception: {e}")

    return res.status_code

def queryAPI(postData):
    headers["Authorization"] = "Token " + os.environ["BOT_API_TOKEN"]
    response = requests.post(
        endPoints["sendMessage"],
        data=json.dumps(postData), 
        headers=headers
    )
    return response
