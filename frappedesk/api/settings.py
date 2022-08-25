import frappe

@frappe.whitelist()
def update_helpdesk_name(name):
    doc = frappe.get_doc("Frappe Desk Settings")
    doc.helpdesk_name = name
    doc.save(ignore_permissions=True)

    return doc.helpdesk_name

@frappe.whitelist(allow_guest=True)
def update_threshold_limit_change(limit):
    doc = frappe.get_doc("Frappe Desk Settings")
    doc.threshold_limit = limit
    doc.save()

    return doc.threshold_limit

@frappe.whitelist(allow_guest=True)
def update_use_bot_answers(flag):
    doc = frappe.get_doc("Frappe Desk Settings")
    doc.use_bot_answers = flag
    doc.save()

    return doc.use_bot_answers
@frappe.whitelist()
def skip_helpdesk_name_setup():
    doc = frappe.get_doc("Frappe Desk Settings")
    doc.initial_helpdesk_name_setup_skipped = True
    doc.save(ignore_permissions=True)

    return doc
