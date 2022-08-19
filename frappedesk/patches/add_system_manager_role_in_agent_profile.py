import frappe

def execute():
    role_profile = frappe.get_doc("Role Profile", "Agent")
    role_profile.append("roles", {"role": "Helpdesk Agent"})
    role_profile.save()
