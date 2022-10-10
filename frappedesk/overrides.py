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
	if doc.default_auto_reply_template == 1:
		# set previous default template to 0 
		previous_default_template = None
		try:
			previous_default_template = frappe.get_last_doc(doctype="Email Template", filters={"default_auto_reply_template": ["=", 1]})
		except: 
			# if last doc is not found 404 error is thrown, which we ignore here and just create a new default template.
			frappe.log_error("No default auto reply template found")			
		if previous_default_template:
			previous_default_template.default_auto_reply_template = 0 
			previous_default_template.save()

		# set auto reply mail text to new one
		default_ticket_outgoing_email_account = frappe.get_doc("Email Account", [["use_imap", "=", 1], ["IMAP Folder","append_to","=","Ticket"], ["default_outgoing","=",1]])
		if default_ticket_outgoing_email_account.enable_auto_reply:
			default_ticket_outgoing_email_account.auto_reply_message = doc.response
			default_ticket_outgoing_email_account.save()
		else:
			frappe.throw("No default email account setup.")

def set_doc_name(doc, event):
	doc.name = doc.subject
