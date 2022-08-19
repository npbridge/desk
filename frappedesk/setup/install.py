import frappe
from ..config.loginPage import app_data

def before_install():
	set_home_page_to_kb()
	set_login_page()
	add_support_redirect_to_tickets()

def after_install():
	add_default_categories()
	add_default_ticket_types()
	add_default_ticket_priorities()
	add_default_sla()
	add_on_ticket_create_script()
	add_default_ticket_template()
	add_default_agent_groups()
	update_agent_role_permissions()
	add_default_assignment_rule()

def set_login_page():
	website_settings = frappe.get_doc("Website Settings")

	website_settings.app_name = app_data["app_name"]
	website_settings.app_logo = app_data["app_logo"]
	website_settings.disable_signup = 1
	website_settings.save()


def set_home_page_to_kb():
	website_settings = frappe.get_doc("Website Settings")

	if not website_settings.home_page:
		website_settings.home_page = "home"
		website_settings.save()

def add_support_redirect_to_tickets():
    website_settings = frappe.get_doc("Website Settings")

    for route_redirects in website_settings.route_redirects:
        if(route_redirects.source == "support"):
            return

    base_route = frappe.get_doc({
        "doctype": "Website Route Redirect",
        "source": "support" ,
        "target": "support/tickets"
    })

    website_settings.append("route_redirects", base_route)
    website_settings.save()

def add_default_categories():
	frappe.get_doc({
		"doctype": "Category",
		"category_name": "FAQ",
		"description": "Description for your FAQs",
		"is_group": True
	}).insert()

	frappe.get_doc({
		"doctype": "Category",
		"category_name": "Getting Started",
		"description": "Description for your Getting Started",
		"is_group": True
	}).insert()

def add_default_sla():

	add_default_ticket_priorities()
	add_default_holidy_list()
	enable_track_service_level_agreement_in_support_settings()

	sla_doc = frappe.new_doc("Service Level Agreement")
	
	sla_doc.service_level = "Default"
	sla_doc.document_type = "Ticket"
	sla_doc.default_service_level_agreement = 1
	sla_doc.enabled = 1

	low_priority = frappe.get_doc({
		"doctype": "Service Level Priority",
		"default_priority": 0,
		"priority": "Low",
		"response_time": 60 * 60 * 24,
		"resolution_time": 60 * 60 * 72,
	})

	medium_priority = frappe.get_doc({
		"doctype": "Service Level Priority",
		"default_priority": 1,
		"priority": "Medium",
		"response_time": 60 * 60 * 8,
		"resolution_time": 60 * 60 * 24,
	})

	high_priority = frappe.get_doc({
		"doctype": "Service Level Priority",
		"default_priority": 0,
		"priority": "High",
		"response_time": 60 * 60 * 1,
		"resolution_time": 60 * 60 * 4,
	})

	urgent_priority = frappe.get_doc({
		"doctype": "Service Level Priority",
		"default_priority": 0,
		"priority": "Urgent",
		"response_time": 60 * 30,
		"resolution_time": 60 * 60 * 2,
	})

	sla_doc.append("priorities", low_priority)
	sla_doc.append("priorities", medium_priority)
	sla_doc.append("priorities", high_priority)
	sla_doc.append("priorities", urgent_priority)

	sla_fullfilled_on_resolved = frappe.get_doc({
		"doctype": "SLA Fulfilled On Status",
		"status": "Resolved"
	})

	sla_fullfilled_on_closed = frappe.get_doc({
		"doctype": "SLA Fulfilled On Status",
		"status": "Closed"
	})

	sla_doc.append("sla_fulfilled_on", sla_fullfilled_on_resolved)
	sla_doc.append("sla_fulfilled_on", sla_fullfilled_on_closed)

	sla_paused_on_replied = frappe.get_doc({
		"doctype": "Pause SLA On Status",
		"status": "Replied"
	})

	sla_doc.append("pause_sla_on", sla_paused_on_replied)

	sla_doc.holiday_list = "Default"

	for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
		service_day = frappe.get_doc({
			"doctype": "Service Day",
			"workday": day,
			"start_time": "10:00:00",
			"end_time": "18:00:00"
		})
		sla_doc.append("support_and_resolution", service_day)

	sla_doc.insert()

def add_default_holidy_list():
	from datetime import datetime
	frappe.get_doc({
		"doctype": "Service Holiday List",
		"holiday_list_name": "Default",
		"from_date": datetime.strptime(f"Jan 1 {datetime.now().year}", "%b %d %Y"),
		"to_date": datetime.strptime(f"Jan 1 {datetime.now().year + 1}", "%b %d %Y"),
	}).insert()

	frappe.db.commit()

def enable_track_service_level_agreement_in_support_settings():
	support_settings = frappe.get_doc("Support Settings")
	support_settings.track_service_level_agreement = True
	support_settings.save()
	frappe.db.commit()

def add_default_ticket_template():
	if (frappe.db.exists("Ticket Template", "Default")): 
		return

	template = frappe.new_doc("Ticket Template")
	
	template.template_name = "Default"
	template.append("fields", {
		"label": "Subject",
		"fieldname": "subject",
		"fieldtype": "Data",
		"reqd": True
	})
	template.append("fields", {
		"label": "Description",
		"fieldname": "description",
		"fieldtype": "Text Editor",
		"reqd": True
	})

	template.insert()

def add_default_ticket_types():
	ticket_types = ["Question", "Bug", "Incident"]

	for type in ticket_types:
		if not frappe.db.exists("Ticket Type", type):
			type_doc = frappe.new_doc("Ticket Type")
			type_doc.name = type
			type_doc.insert()

def add_default_ticket_priorities():
	ticket_priorities = ["Low", "Medium", "High", "Urgent"]

	for priority in ticket_priorities:
		if not frappe.db.exists("Ticket Priority", priority):
			priority_doc = frappe.new_doc("Ticket Priority")
			priority_doc.name = priority
			priority_doc.insert()

def add_default_agent_groups():
	agent_groups = ["Billing", "Product Experts"]

	for agent_group in agent_groups:
		if not frappe.db.exists("Agent Group", agent_group):
			agent_group_doc = frappe.new_doc("Agent Group")
			agent_group_doc.team_name = agent_group
			agent_group_doc.insert()

def add_on_ticket_create_script():
	if not frappe.db.exists("Server Script", "Ticket Auto Set Custom Fields"):
		script_doc = frappe.new_doc("Server Script")
		script_doc.name = "Ticket Auto Set Custom Fields"
		script_doc.script_type = "DocType Event"
		script_doc.module = "FrappeDesk"
		script_doc.reference_doctype = "Ticket"
		script_doc.doctype_event = "Before Insert"
		script_doc.script = "# Do Nothing"
		script_doc.insert()

def update_agent_role_permissions():
	if frappe.db.exists("Role", "Agent"):
		agent_role_doc = frappe.get_doc("Role", "Agent")
		agent_role_doc.search_bar = True
		agent_role_doc.notifications = True
		agent_role_doc.list_sidebar = True
		agent_role_doc.bulk_actions = True
		agent_role_doc.view_switcher = True
		agent_role_doc.form_sidebar = True
		agent_role_doc.form_sidebar = True
		agent_role_doc.timeline = True
		agent_role_doc.dashboard = True
		agent_role_doc.save()

def add_default_assignment_rule():
	if frappe.get_list("Assignment Rule", filters={"document_type": "Ticket"}):
		return
	
	rule_doc = frappe.new_doc("Assignment Rule")
	rule_doc.name = "Support Rotation"
	rule_doc.document_type = "Ticket"
	rule_doc.description = "Automatic Ticket Assignment"
	rule_doc.assign_condition = "status == 'Open'"
	rule_doc.rule = "Round Robin"

	for agent in frappe.get_all("Agent", fields=['user']):
		user_doc = frappe.get_doc({
			"doctype": "Assignment Rule User",
			"user": agent.user
		})
		rule_doc.append("users", user_doc)

	for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
		day_doc = frappe.get_doc({
    	    "doctype": "Assignment Rule Day",
			"day": day
		})
		rule_doc.append("assignment_days", day_doc)
	
	rule_doc.save()