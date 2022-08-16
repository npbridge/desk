import frappe

@frappe.whitelist(allow_guest=True)
def update_helpdesk_name(name):
    doc = frappe.get_doc("Support Settings")
    doc.helpdesk_name = name
    doc.save(ignore_permissions=True)

    return doc.helpdesk_name

@frappe.whitelist(allow_guest=True)
def update_threshold_limit_change(limit):
    doc = frappe.get_doc("Support Settings")
    doc.threshold_limit = limit
    doc.save()

    return doc.threshold_limit

@frappe.whitelist(allow_guest=True)
def update_use_bot_answers(flag):
    doc = frappe.get_doc("Support Settings")
    doc.use_bot_answers = flag
    doc.save()

    return doc.use_bot_answers