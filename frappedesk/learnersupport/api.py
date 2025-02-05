from frappedesk.rocketchat.rocketchat import getAuthenticated
from frappe.utils import logger
from dotenv import load_dotenv

import frappe
import json
import os
import requests
import csv

logger.set_log_level("DEBUG") # type: ignore
logger = frappe.logger("api", allow_site=True, file_count=50)

load_dotenv()

api_endpoint = os.getenv('BOT_API_ENDPOINT') 
endpoints = {
    "add_users": api_endpoint + "bot-api/hd-bulk-user/",
    "add_or_update_user": api_endpoint + "bot-api/hd-user/",
    "add_or_update_course_doc": api_endpoint + "bot-api/hd-course-doc/",
    "add_or_update_doc": api_endpoint + "bot-api/hd-doc/",
    "total_messages": api_endpoint + "bot-api/total-messages/"
}

headers = {
	"content-type": "application/json",
}

"""Util functions"""
def get_student_groups():
        settings_doc = frappe.get_doc("Frappe Desk Settings")
        student_groups = settings_doc.student_group.split(",") # type: ignore
        return student_groups

def auth_check(func):
    def wrapper_auth_check(*args,**kwargs):
        headers["Authorization"] = "Token " + os.environ["BOT_API_TOKEN"]
        res = func(*args,**kwargs)
        if res.status_code == 401:
            updatingToken = getAuthenticated()
            if updatingToken == 200:
                headers["Authorization"] = "Token " + os.environ["BOT_API_TOKEN"]
                res = func(*args,**kwargs)
                if res.status_code != 200:
                    logger.debug(f"Error while getting BOT API token")    
        return res
    return wrapper_auth_check

"""APIs"""
@auth_check
def add_users_bulk_api(users):
    data = {
        "users": users,
    }
    return requests.post(endpoints["add_users"], data=json.dumps(data), headers=headers) 

@auth_check
def add_or_update_user_api(user):
    res = requests.post(endpoints["add_or_update_user"], data=json.dumps(user), headers=headers)
    return res

@auth_check
def create_course_doc_api(course):
    bot_uuid = os.getenv("BOT_API_UUID")
    data = {
        "course": course,
        "bot": bot_uuid
    }
    res = requests.post(endpoints["add_or_update_course_doc"], data=json.dumps(data), headers=headers)
    return res 

@auth_check
def add_or_update_doc_api(document):
    bot_uuid = os.getenv("BOT_API_UUID")
    data = {
        "doc": document,
        "bot": bot_uuid
    }
    res = requests.post(endpoints["add_or_update_doc"], data=json.dumps(data), headers=headers)
    return res

@auth_check
def delete_doc_api(id):
    data = {
        "id": id,
    }
    res = requests.delete(endpoints["add_or_update_doc"], data=json.dumps(data), headers=headers)
    return res

@frappe.whitelist()
@auth_check
def get_total_messages():
    bot_uuid = os.getenv("BOT_API_UUID")
    data = {
        "bot": bot_uuid
    }
    res = requests.post(endpoints["total_messages"], data=json.dumps(data), headers=headers)
    return res 


"""Hook Functions"""
def add_users_bulk(doc, event):
    """Adding users in bulk in gpt warehouse"""
    if doc.reference_doctype == "Learner" and doc.import_file:
        student_groups = get_student_groups()
        user_filename = frappe.get_site_path() + doc.import_file
        users = []

        with open(user_filename, "r") as user_file:
            user_csv = csv.reader(user_file)
            first_line_skipped = False
            for user_details in user_csv:
                if not first_line_skipped:
                    first_line_skipped = True
                    continue
                # * By default we add is_active as True when uploading in bulk.
                user = {
                    "first_name": user_details[0],
                    "last_name": user_details[1],
                    "email": user_details[2],
                    "groups": student_groups,
                    "is_active": 1
                }
                users.append((user))

        try:
            add_users_bulk_api(users)
        except requests.exceptions.RequestException as e:
            logger.error(f"GPTWarehouse Exception on adding users in bulk: {e}")
        except Exception as e:
            logger.error(f"GPTWarehouse Exception on adding users in bulk: {e}")

@frappe.whitelist() 
def add_or_update_user(doc, event):
    """Adding or updating user in gpt warehouse"""
    if isinstance(doc, str):
        doc = json.loads(doc)
    student_groups = get_student_groups()
    user = {
        "first_name": doc["first_name"],
        "last_name": doc["last_name"],
        "email": doc["email"],
        "is_active": doc["is_active"],
        "groups": student_groups
    }
    try:
        add_or_update_user_api(user)
    except requests.exceptions.RequestException as e:
        logger.error(f"GPTWarehouse Exception on adding user {doc}: {e}")
    except Exception as e:
        logger.error(f"GPTWarehouse Exception on adding user {doc}: {e}")



@frappe.whitelist() 
def create_course_doc(doc, event):  
    """Creating doc from course info"""
    course = {
        "id": doc.name,
        "title": doc.title,
        "description": doc.description,
        "url": doc.url,
        "number": doc.number,
        "start_date": doc.start_date,
        "end_date": doc.end_date,
        "instructors": doc.instructors,
        "schedule": doc.schedule,
        "assignment": [
            {
            "title": assignment.title,
            "description": assignment.description,
            "start_date": assignment.start_date,
            "end_date": assignment.end_date,
            "type": assignment.type
            } 
            for assignment in doc.assignment
            ]
    }
    try: 
        create_course_doc_api(course)
    except requests.exceptions.RequestException as e:
        logger.error(f"GPTWarehouse Exception on creating gpt doc {doc}: {e}")
    except Exception as e:
        logger.error(f"GPTWarehouse Exception on creating gpt doc {doc}: {e}")


@frappe.whitelist()
def add_or_update_doc(doc, event):
    """Creating doc in gpt warehouse from knowledge base"""
    if doc.use_in_bot:
        document = {
            "source": "hd",
            "id": doc.name,
            "title": doc.title,
            "content": doc.content
        }
        try: 
            add_or_update_doc_api(document)
        except requests.exceptions.RequestException as e:
            logger.error(f"GPTWarehouse Exception on adding/updating document {document}: {e}")
        except Exception as e:
            logger.error(f"GPTWarehouse Exception on adding/updating document {document}: {e}")
    else:
        try: 
            delete_doc_api(doc.name)
        except requests.exceptions.RequestException as e:
            logger.error(f"GPTWarehouse Exception on deleting document {doc.name}: {e}")
        except Exception as e:
            logger.error(f"GPTWarehouse Exception on deleting document {doc.name}: {e}")
        


@frappe.whitelist()
def delete_doc(doc, event):
    """Deleting doc in gpt warehouse from knowledge base"""
    if not doc.use_in_bot:
        return
    
    try: 
        delete_doc_api(doc.name)
    except requests.exceptions.RequestException as e:
        logger.error(f"GPTWarehouse Exception on deleting document {doc.name}: {e}")
    except Exception as e:
        logger.error(f"GPTWarehouse Exception on deleting document {doc.name}: {e}")

