# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappedesk.helper import  get_report_data


def execute(filters=None):
	columns, data = [], []

	columns = [
		{"fieldname": "dataset", "label": "Dataset", "fieldtype": "Data", "width": 200},
		{"fieldname": "opening_date", "label": "As On Date", "fieldtype": "Data", "width": 200},
		{
			"fieldname": "date_format", 
			"label": filters.range, 
			"fieldtype": "Date" if filters.range == "Day" else "Data", 
			"width": 200
		},
		{
			"fieldname": "count",
			"fieldtype": "Data",
			"label": "Total Tickets",
			"width": 150,
		},
	]

	first_dataset = get_report_data(filters.from_date_first, filters.to_date_first, filters.range, extra_field_name="First date range")
	second_dataset = get_report_data(filters.from_date_second, filters.to_date_second, filters.range, extra_field_name="Second date range")

	data = [		
		*first_dataset,
		*second_dataset
	]
	return columns, data



