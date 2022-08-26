import requests
import json
import os

headers = {
    "content-type": "application/json"
}
endPoints = {
    "sendMessage": os.environ.get('SEND_MESSAGE_END_POINT'),
    "history": os.environ.get('HISTORY_ENDPOINT')+os.environ.get('ROOM_ID')+"?token="+os.environ.get('TOKEN')
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
    postData["token"] = os.environ.get('TOKEN')
    postData["rid"] = os.environ.get('ROOM_ID')
    res = requests.post(endPoints["sendMessage"], data=json.dumps(postData), headers=headers)
    res = res.json()
    return res['message']['_id']

def getHistory(params=params, headers=headers):
    params["token"] = os.environ.get('TOKEN')
    params["rid"] = os.environ.get('ROOM_ID')
    res = requests.get(endPoints["history"], params=params, headers=headers)
    return res.json()

def getResponse(msg, msgID=None, history={}):
    msgID = sendMessages(msg)
    history = getHistory()
    message_index = next((index for (index, d) in enumerate(history['messages']) if d["_id"] == msgID), None)
    response_index = message_index - 1
    response = history['messages'][response_index]['msg']
    return response


