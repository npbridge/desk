import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

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
    res = requests.post(endPoints["sendMessage"], data=json.dumps(postData), headers=headers)
    res = res.json()
    return res['message']['_id']

def getHistory(params=params, headers=headers):
    params["token"] = os.getenv('TOKEN')
    params["rid"] = os.getenv('ROOM_ID')
    res = requests.get(endPoints["history"], params=params, headers=headers)
    return res.json()

def getResponse(msg, msgID=None, history={}):
    msgID = sendMessages(msg)
    history = getHistory()
    message_index = next((index for (index, d) in enumerate(history['messages']) if d["_id"] == msgID), None)
    response_index = message_index - 1
    response = history['messages'][response_index]['msg']
    return response


