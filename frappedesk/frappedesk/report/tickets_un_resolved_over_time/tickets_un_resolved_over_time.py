# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	filters.range = "Day"
	columns = [
		{"fieldname": "dataset", "label": "Dataset", "fieldtype": "Data", "width": 200},
		{
			"fieldname": "date", 
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
				count(creation) 
			FROM tabTicket 
			WHERE 
				resolution_date IS NULL
				AND 
				DATE(creation) < '{from_date}'
		""".format(from_date= date_range["from_date"])

		previous_data = frappe.db.sql(
			previous_unresolved_count
		)
		if previous_data:
			previous_unresolved_tickets = previous_data[0][0]
		else:
			previous_unresolved_tickets = 0

		query_for_empty_dates = """
		WITH recursive all_dates(dt) as (
		SELECT 
			'{from_date}' dt
		UNION ALL
			SELECT 
				dt + interval 1 day
			FROM 
				all_dates 
		WHERE 
			dt < '{to_date}'
		)
		""".format(from_date= date_range["from_date"], to_date= date_range["to_date"])
		
		number_of_ticket_created_on_dates = """
		SELECT 
			DATE(creation) as date,
			COUNT(creation) as created_count,
			'0' as resolved_count
		FROM tabTicket 
		WHERE 
			DATE(creation) 
				between 
				'{from_date}' 
				and 
				'{to_date}' 
		GROUP BY date
		""".format(from_date= date_range["from_date"], to_date= date_range["to_date"])

		number_of_ticket_resolved_on_dates = """
		SELECT 
			DATE(resolution_date) as date,
			'0' as created_count,
			COUNT(resolution_date) as resolved_count
		FROM tabTicket 
		WHERE
			resolution_date IS NOT NULL
			AND
			DATE(resolution_date) 
				between 
				'{from_date}' 
				and 
				'{to_date}' 
		GROUP BY date
		""".format(from_date= date_range["from_date"], to_date= date_range["to_date"])

		query_for_ticket_data = """
			SELECT 
				d.dt as date,
				coalesce(
					(
						SUM(tabT.created_count) OVER (order by date) 
						- 
						SUM(tabT.resolved_count) OVER (order by date) 
						+
						{previous_unresolved_count}
					),
					0
				) as count
			FROM all_dates d 
			LEFT JOIN 
				(
					SELECT 
						date,
						SUM(created_count) as created_count,
						SUM(resolved_count) as resolved_count 
					FROM 
						(
							{resolved_on_date_count} 
							UNION 
							{created_on_date_count}
						)allTicketsCount 
					GROUP BY date
				) as tabT 
			ON tabT.date=d.dt 
			ORDER BY d.dt
		""".format(previous_unresolved_count= previous_unresolved_tickets, resolved_on_date_count= number_of_ticket_resolved_on_dates, created_on_date_count= number_of_ticket_created_on_dates)

		query_all_data = """
		{all_dates_from_range}
		{ticket_data}
		""".format(all_dates_from_range= query_for_empty_dates, ticket_data= query_for_ticket_data)

		tmp_data = frappe.db.sql(
			query_all_data,
			as_dict = 1
		)

		tmp_data = [{**ticket_count_info, "dataset": date_range["extra_field_name"]} for ticket_count_info in tmp_data]

		data = [*data, *tmp_data]

	return columns, data
