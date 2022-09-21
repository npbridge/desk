# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import itertools
import frappe
import json
from frappe.model.document import Document
from datetime import datetime, timedelta
from itertools import groupby

class TicketActivity(Document):
	pass

def log_ticket_activity(ticket, action):
	return frappe.get_doc(
		{"doctype": "Ticket Activity", "ticket": ticket, "action": action}
	).insert(ignore_permissions=True)

def mail_ticket_updates():
	send_mail_data = {}
	# get all ticket activity in last 24 hours - group by ticket
	yesterday = datetime.now() - timedelta(1)
	all_activities = frappe.db.get_all('Ticket Activity',
		fields=['ticket', 'action', 'creation', '_liked_by', 'modified_by'],
		filters={
			'creation': ['>', yesterday]
		},
		order_by='ticket'
	)
	grouped_activity_list = groupby(all_activities, lambda x: x['ticket'])

	for ticketId, grouped_activities in grouped_activity_list:
		ticket_doc = frappe.get_doc("Ticket", ticketId)
		for follower in json.loads(ticket_doc._liked_by):
			existing_data = send_mail_data[follower] if send_mail_data.get(follower) else []
			grouped_activities, grouped_activities_tee = itertools.tee(grouped_activities)
			send_mail_data[follower] = [*existing_data, {"ticket": ticketId, "content": list(grouped_activities_tee) }]

	# look through activities by ticket and mail summary of people who have followed ticket
	for follower, activity_data in send_mail_data.items():
		frappe.sendmail(
				sender="staging@npbridge.com",
				recipients=[follower],
				subject=f"Daily Ticket Summary",
				template="daily_summary",
				args={"activities" : activity_data },
			)