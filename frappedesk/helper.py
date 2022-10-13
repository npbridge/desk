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

def get_report_data(from_date, to_date, range="Weekly", extra_field_name=None, filter=None, filter_based_on="opening_date"): 
	""" Return data from sql grouped by periodicity. Provide filters in a json {value: "equal_to_this"}"""
	periodicity = get_sql_periodicity(range)

	filter_clause = ""
	if filter:
		for key, value in filter.items():
			filter_clause += f",\n{key}={value}"

			
	query_where_clause = """
	WHERE 
		date({}) between '{}' and '{}'
	""".format(filter_based_on, from_date, to_date) + filter_clause

	query = """
	SELECT
		{}({}) as date_format,
		{} as {},
		count(idx) as count
	FROM tabTicket
	{}
	GROUP BY date_format
	ORDER BY date_format asc
	""".format(periodicity, filter_based_on, filter_based_on, filter_based_on, query_where_clause)

	data = frappe.db.sql(
		query,
		as_dict = 1
	)
	
	if extra_field_name: 
		return [{**ticket_count_info, "dataset": extra_field_name} for ticket_count_info in data]

	return data