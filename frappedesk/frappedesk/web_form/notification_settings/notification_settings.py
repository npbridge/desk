import frappe

def get_context(context):
	# do your magic here
	site_path = frappe.local.path
	user = frappe.session.user
	if (user not in site_path):
		frappe.local.response["type"] = "redirect"
		frappe.local.response["location"] = f"/notification-settings/{user}"
		raise frappe.Redirect
