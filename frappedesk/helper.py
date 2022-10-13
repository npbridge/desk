import frappe

def get_sql_periodicity(range):
	periodicity = "WEEK"
	if range == "Day":
		periodicity = "DATE"
	elif range == "Week":
		periodicity = "WEEK"
	elif range == "Month":
		periodicity = "MONTH"
	elif range == "Quarter":
		periodicity = "QUARTER"
	elif range == "Year":
		periodicity = "YEAR"

	return periodicity

def get_report_data(from_date, to_date, range="Weekly", extra_field_name=None, filter=None): 
	""" Return data from sql grouped by periodicity. Provide filters in a json {value: "equal_to_this"}"""
	periodicity = get_sql_periodicity(range)

	if filter:
		query = """
		SELECT
			{}(opening_date) as date_format,
			opening_date as opening_date,
			count(idx) as count
		FROM tabTicket
		WHERE
			date(opening_date) between '{}' and '{}',
			'''add filter'''
		GROUP BY date_format
		ORDER BY date_format asc
	""".format(periodicity, from_date, to_date)

	else:
		query = """
			SELECT
				{}(opening_date) as date_format,
				opening_date as opening_date,
				count(idx) as count
			FROM tabTicket
			WHERE
				date(opening_date) between '{}' and '{}'
			GROUP BY date_format
			ORDER BY date_format asc
		""".format(periodicity, from_date, to_date)

	data = frappe.db.sql(
		query,
		as_dict = 1
	)
	
	if extra_field_name: 
		return [{**ticket_count_info, "dataset": extra_field_name} for ticket_count_info in data]

	return data