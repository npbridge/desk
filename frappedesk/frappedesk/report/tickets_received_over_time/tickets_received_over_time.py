# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappedesk.helper import get_sql_periodicity, get_report_data


def execute(filters=None):
	columns, data = [], []

	columns = [
		{"fieldname": "dataset", "label": "Dataset", "fieldtype": "Data", "width": 200},
		{"fieldname": "opening_date", "label": "As On Date", "fieldtype": "Date", "width": 200},
		{"fieldname": "date_format", "label": filters.range, "fieldtype": "Data", "width": 200},
		{
			"fieldname": "count",
			"fieldtype": "Data",
			"label": "Total Tickets",
			"width": 150,
		},
	]

	first_dataset = get_report_data(filters.from_date_first, filters.to_date_first, filters.range, "First date range")
	second_dataset = get_report_data(filters.from_date_second, filters.to_date_second, filters.range, "Second date range")

	data = [		
		*first_dataset,
		*second_dataset
	]
	return columns, data



