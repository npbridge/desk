# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe.utils.dashboard import cache_source
from frappe import _

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

	query_for_ticket_data = """
			SELECT 
				date_format as date_format,
				DATE_FORMAT(as_on_date, "%d-%m-%Y") as as_on_date,
				count
			FROM (
				SELECT
					CASE WHEN resolution_date THEN {}(resolution_date) ELSE {}(opening_date) END as date_format,
					CASE WHEN resolution_date THEN resolution_date ELSE opening_date END as as_on_date,
					(
						COUNT(opening_date) OVER (ROWS UNBOUNDED PRECEDING) 
						-
						COUNT(resolution_date) OVER (ROWS UNBOUNDED PRECEDING)
					) as count
				FROM tabTicket
				ORDER BY as_on_date asc
			) AS T
			WHERE 
				date(as_on_date) between '{}' and '{}' 
			GROUP BY date_format
			ORDER BY date_format asc
			""".format("DAY", "DAY", "2022-09-14", "2022-10-14")

	data = frappe.db.sql(
			query_for_ticket_data,
			as_dict=1
		)

	for ticket_data in data:
		labels.append(ticket_data["as_on_date"])
		datapoints.append(ticket_data["count"])

	return {
		"labels": labels,
		"datasets": [{"name": _("Tickets"), "values": datapoints}],
		"type": "line",
	}