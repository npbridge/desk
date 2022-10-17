import frappe
def pull_support_emails():
	if (frappe.db.exists("Email Account", "Support")):
		email_account = frappe.get_doc("Email Account", "Support")
		
		if email_account.enable_incoming:
			email_account.receive()

def on_assignment_rule_trash(doc, event):
	if not frappe.get_all("Assignment Rule", filters={"document_type": "Ticket", "name": ["!=", doc.name]}):
		frappe.throw("There should atleast be 1 assignment rule for ticket")

def on_email_template_updated(doc, event):
	is_new_default_template = doc.default_auto_reply_template == 1
	previous_default_template = None
	try:
		previous_default_template = frappe.get_last_doc(doctype="Email Template", filters={
			"default_auto_reply_template": ["=", 1], 
			"name": ["!=", doc.subject]
			})
	except: 
		# if last doc is not found 404 error is thrown
		# if no other existing default template is there and user is creating new default template, just create a new default template.
		# if no other existing default template is there and user is marking current as false throw error.
		if not is_new_default_template: frappe.throw("Default template mandatory! First make some other template as default.")	

	if is_new_default_template:
		if previous_default_template:
			frappe.db.set_value("Email Template", previous_default_template.name, "default_auto_reply_template", 0)

		default_ticket_outgoing_email_account = frappe.get_doc("Email Account", [["use_imap", "=", 1], ["IMAP Folder","append_to","=","Ticket"], ["default_outgoing","=",1]])
		if default_ticket_outgoing_email_account.enable_auto_reply:
			frappe.db.set_value("Email Account", default_ticket_outgoing_email_account.name, "auto_reply_message", doc.response)
		else:
			frappe.throw("No default email account setup.")

def set_doc_name(doc, event):
	doc.name = doc.subject

def on_email_template_delete(doc, event):
	if doc.default_auto_reply_template == 1:
		frappe.throw("Cannot delete default template! First make some other template default.")
