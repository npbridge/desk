# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
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
		"Ticket"
	)

	contacts = frappe.get_list(
		"Contact",
		fields=[ "department", "count(department) department_count"],
		group_by="department",
	)

	if not contacts:
		return []

	for contact in contacts:
		if (contact.department):
			labels.append(_(contact.get("department")))
			datapoints.append(contact.get("department_count"))

	return {
		"labels": labels,
		"datasets": [{"name": _("Department"), "values": datapoints}],
		"type": "pie",
	}