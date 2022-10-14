# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	# columns = [
	# 	{"fieldname": "dataset", "label": "Dataset", "fieldtype": "Data", "width": 200},
	# 	{"fieldname": "as_on_date", "label": "As On Date", "fieldtype": "Data", "width": 200},
	# 	{
	# 		"fieldname": "date_format", 
	# 		"label": filters.range, 
	# 		"fieldtype": "Data", 
	# 		"width": 200
	# 	},
	# 	{
	# 		"fieldname": "count",
	# 		"fieldtype": "Data",
	# 		"label": "Total Tickets",
	# 		"width": 150,
	# 	},
	# ]



	# date_ranges = [
	# 	{
	# 		"from_date": filters.from_date_first,
	# 		"to_date": filters.to_date_first,
	# 		"extra_field_name": "First date range"
	# 	},
	# 	{
	# 		"from_date": filters.from_date_second,
	# 		"to_date": filters.to_date_second,
	# 		"extra_field_name": "Second date range"
	# 	},
	# ]

	# for date_range in date_ranges:

	# 	query_for_empty_dates = """
	# 	WITH recursive all_dates(dt) as (
	# 	SELECT 
	# 		'{}' dt
	# 	UNION ALL
	# 		SELECT 
	# 			dt + interval 1 day
	# 		FROM 
	# 			all_dates 
	# 	WHERE 
	# 		dt < '{}'
	# 	)
	# 	""".format(date_range["from_date"], date_range["to_date"])


	# 	query_for_ticket_data = """
	# 		SELECT 
	# 			date_format,
	# 			as_on_date as as_on_date,
	# 			count
	# 		FROM (
	# 			SELECT
	# 				CASE WHEN resolution_date THEN {}(resolution_date) ELSE {}(opening_date) END as date_format,
	# 				CASE WHEN resolution_date THEN resolution_date ELSE opening_date END as as_on_date,
	# 				(
	# 					COUNT(opening_date) OVER (ROWS UNBOUNDED PRECEDING) 
	# 					-
	# 					COUNT(resolution_date) OVER (ROWS UNBOUNDED PRECEDING)
	# 				) as count
	# 			FROM tabTicket
	# 			ORDER BY as_on_date asc
	# 		) AS T
	# 		WHERE 
	# 			date(as_on_date) between '{}' and '{}' 
	# 		GROUP BY date_format
	# 		ORDER BY date_format asc
	# 		""".format(filters.range, filters.range, date_range["from_date"], date_range["to_date"])

	# 	query_all_ticket_data_with_missing_dates = """
	# 	{}
	# 	SELECT 
	# 		DATE_FORMAT(date(as_on_date), '%d-%m-%Y') as as_on_date,
	# 		date_format as date_format,
	# 		coalesce(sum(count)) as count
	# 	FROM(
	# 		SELECT 
	# 			d.dt as as_on_date, 
	# 			{}(d.dt) as date_format,
	# 			coalesce(t.count, 0) as count 
	# 		FROM all_dates d
	# 		LEFT JOIN ({}) t 
	# 		ON t.as_on_date = d.dt
	# 	) as p
	# 	GROUP BY date_format
	# 	""".format(query_for_empty_dates, filters.range, query_for_ticket_data)

	# 	temp_data = frappe.db.sql(
	# 		query_all_ticket_data_with_missing_dates,
	# 		as_dict = 1
	# 	)

	# 	updated_temp_data = [{**ticket_count_info, "dataset": date_range["extra_field_name"] } for ticket_count_info in temp_data]

	# 	data = [*data, *updated_temp_data]

	return columns, data
