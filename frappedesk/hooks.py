app_name = "frappedesk"
app_title = "FrappeDesk"
app_publisher = "Frappe Technologies"
app_description = "Customer Service Software"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hello@frappe.io"
app_license = "AGPLv3"

before_install = "frappedesk.setup.install.before_install"
after_install = "frappedesk.setup.install.after_install"

# TODO: the logic for has_website_permission is minimised a little for now, will need to re-check
has_website_permission = {
	"Ticket": "frappedesk.frappedesk.doctype.ticket.ticket.has_website_permission",
}

doc_events = {
	"*": {
		"validate": "frappedesk.frappedesk.doctype.service_level_agreement.service_level_agreement.apply",
	},
	"Communication": {
		"on_update": [
			"frappedesk.frappedesk.doctype.service_level_agreement.service_level_agreement.on_communication_update",
			"frappedesk.frappedesk.doctype.ticket.ticket.set_first_response_time",
		],
		"after_insert": [
			"frappedesk.frappedesk.doctype.ticket.ticket.set_descritption_from_communication",
			"frappedesk.frappedesk.doctype.ticket.ticket.create_communication_via_bot",
		]
	},
	"Contact": {"on_trash": "frappedesk.frappedesk.doctype.ticket.ticket.update_ticket"},
	"Assignment Rule": {"on_trash": "frappedesk.overrides.on_assignment_rule_trash"},
	"Agent": {"before_insert": "frappedesk.limits.validate_agent_count"},
	"Email Template": {
		"before_insert": "frappedesk.overrides.set_doc_name",
		"validate": "frappedesk.overrides.on_email_template_updated",
		"on_trash": "frappedesk.overrides.on_email_template_delete"
		},
    "Data Import": {
        "after_insert": "frappedesk.learnersupport.api.add_users_bulk"
	},
    "Course": {
        "on_update": "frappedesk.learnersupport.api.create_course_doc"
	},
    "Article": {
        "on_update": "frappedesk.learnersupport.api.add_or_update_doc",
        "on_trash": "frappedesk.learnersupport.api.delete_doc"
	}
}

scheduler_events = {
	"daily": [
		"frappedesk.frappedesk.doctype.ticket.ticket.auto_close_tickets",
		"frappedesk.frappedesk.doctype.service_level_agreement.service_level_agreement.check_agreement_status",
		"frappedesk.frappedesk.doctype.ticket_activity.ticket_activity.mail_ticket_updates"
	],
	"cron": {
		"* * * * * 0/5": [
			"frappedesk.overrides.pull_support_emails"
		]
	},
}

website_route_rules = [
	# Desk
	{"from_route": "/frappedesk/<path:app_path>", "to_route": "frappedesk"},
	# Customer Portal
	{"from_route": "/support/tickets", "to_route": "frappedesk"},
	{"from_route": "/support/tickets/<path:app_path>", "to_route": "frappedesk"},
	# Customer Portal Login/Signup/Verigication
	{"from_route": "/support/login", "to_route": "frappedesk"},
	{"from_route": "/support/signup", "to_route": "frappedesk"},
	{"from_route": "/support/verify", "to_route": "frappedesk"},
	{"from_route": "/support/verify/<path:app_path>", "to_route": "frappedesk"},
	{"from_route": "/support/impersonate", "to_route": "frappedesk"},
]

website_redirects = [
	{"source": "/about", "target": "/home"},
	{"source": "/contact", "target": "/home"},
	{"source": "/message", "target": "/home"},
	{"source": "/qrcode", "target": "/home"},
	{"source": "/search", "target": "/home"},
	{"source": "/third_party_apps", "target": "/home"},
    {"source": "/learner-bulk/list", "target": "/learner/list"}
	]

fixtures = [
	"Custom Field"
]
