# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	filters.range = "Day"
	columns = [
 		{"fieldname": "dataset", "label": "Dataset", "fieldtype": "Data", "width": 200},
 		{"fieldname": "as_on_date", "label": "As On Date", "fieldtype": "Data", "width": 200},
 		 {
 		 	"fieldname": "date_format", 
 		 	"label": filters.range, 
 		 	"fieldtype": "Data", 
 		 	"width": 200
 		 },
 		{
 			"fieldname": "count",
 			"fieldtype": "Data",
 			"label": "Total Tickets",
 			"width": 150,
 		},
 	]



	date_ranges = [
 		{
 			"from_date": filters.from_date_first,
 			"to_date": filters.to_date_first,
 			"extra_field_name": "First date range"
 		},
 		{
 			"from_date": filters.from_date_second,
 			"to_date": filters.to_date_second,
 			"extra_field_name": "Second date range"
 		},
 	]

	for date_range in date_ranges:

		previous_unresolved_count = """
			SELECT 
				count(resolution_date) 
			FROM tabTicket 
			WHERE 
				resolution_date IS NOT NULL
 				AND 
				DATE(resolution_date) < '2022-10-18'
		""".format(date_range["from_date"])

		query_for_empty_dates = """
 		WITH recursive all_dates(dt) as (
 		SELECT 
 			'{}' dt
 		UNION ALL
 			SELECT 
 				dt + interval 1 day
 			FROM 
 				all_dates 
 		WHERE 
 			dt < '{}'
 		)
 		""".format(date_range["from_date"], date_range["to_date"])
		
		number_of_ticket_created_on_dates = """
		SELECT 
			DATE(creation) as date,
			COUNT(creation) as created_count,
			'0' as resolved_count
		FROM tabTicket 
		WHERE 
			DATE(creation) 
				between 
				'{}' 
				and 
				'{}' 
		GROUP BY date
		""".format(date_range["from_date"], date_range["to_date"])

		number_of_ticket_resolved_on_dates = """
		SELECT 
			DATE(resolution_date) as date,
			'0' as created_count,
			COUNT(resolution_date) as resolved_count
		FROM tabTicket 
		WHERE 
			DATE(resolution_date) 
				between 
				'{}' 
				and 
				'{}' 
		GROUP BY date
		""".format(date_range["from_date"], date_range["to_date"])

		query_for_ticket_data = """
			SELECT 
				d.dt as date,  
				coalesce(tt.created_count,0) as created_count,
				coalesce(tt.resolved_count,0) as resolved_count, 
				coalesce(
					(
						SUM(tt.created_count) OVER (order by date) 
						- 
						SUM(tt.resolved_count) OVER (order by date) 
						+
						{}
					),
					0
				) as total_unresolved_count
			FROM all_dates d 
			LEFT JOIN 
				(
					SELECT 
						date,
						SUM(created_count) as created_count,
						SUM(resolved_count) as resolved_count 
					FROM 
						(
							{} 
							UNION 
							{}
						)allTicketsCount 
					GROUP BY date
				) as tabTickets 
			ON tabTickets.date=d.dt 
			ORDER BY d.dt
 		""".format(previous_unresolved_count, number_of_ticket_resolved_on_dates, number_of_ticket_created_on_dates)

		query_all_data = """
 		{}
		{}
 		""".format(query_for_empty_dates, query_for_ticket_data)

		temp_data = frappe.db.sql(
 			query_all_data,
 			as_dict = 1
 		)
		data = [*data, *temp_data]
	
	return columns, data