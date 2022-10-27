# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappedesk.helper import get_report_data

def execute(filters=None):
	columns, data = [], []
	filters.range = "Day"
	columns = [
		{"fieldname": "dataset", "label": "Dataset", "fieldtype": "Data", "width": 200},
		{"fieldname": "first_responded_on", "label": "First Replied On", "fieldtype": "Date", "width": 200},
		# {
		# 	"fieldname": "date_format", 
		# 	"label": filters.range, 
		# 	"fieldtype": "Date" if filters.range == "Day" else "Data", 
		# 	"width": 200
		# },
		{
			"fieldname": "count",
			"fieldtype": "Data",
			"label": "Total Tickets",
			"width": 150,
		},
	]

	first_dataset = get_report_data(filters.from_date_first, filters.to_date_first, filters.range, extra_field_name="First date range", filter_based_on="first_responded_on", )
	second_dataset = get_report_data( filters.from_date_second, filters.to_date_second, filters.range, extra_field_name="Second date range", filter_based_on="first_responded_on",)

	data = [		
		*first_dataset,
		*second_dataset
	]
	return columns, data
