from frappedesk.learnersupport.api import get_total_messages
import frappe

# whitelisted function to return total count of uer queries on chatbot
@frappe.whitelist(allow_guest=True)
def get():
    total_messages = get_total_messages().json()
    value = total_messages["count"] if "count" in total_messages else 0
    return value
