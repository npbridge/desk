# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
import json
from frappe import _
from frappe.utils.dashboard import cache_source


@frappe.whitelist()
@cache_source
def get(
	chart_name=None,
	chart=None,
	no_cache=None,
	filters=None,
	from_date=None,
	to_date=None,
	timespan=None,
	time_interval=None,
	heatmap_year=None,
):
	labels, datapoints = [], []
	filters = frappe.parse_json(filters)

	tickets = frappe.get_list(
		"Ticket",
		fields=["contact", "name"]
	)

	if not tickets:
		return []

	departments = {}

	for ticket in tickets:
		if (ticket.contact) :
			contact = frappe.get_doc("Contact", ticket.contact)
			if (contact.department) :
				if (contact.department not in departments) :
					departments[contact.department] = 1
				else :
					departments[contact.department] += 1

	labels.append(department_name for department_name in departments)
	datapoints.append(department_count for dep_name, department_count in departments.items())
	

	return {
		"labels": labels,
		"datasets": [{"name": _("Department"), "values": datapoints}],
		"type": "pie",
	}