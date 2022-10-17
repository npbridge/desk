import frappe
from datetime import timedelta

def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days

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

def get_report_data(from_date, to_date, range="Weekly", extra_field_name="Random Dataset", filter=None, filter_based_on="opening_date"): 
	""" Return data from sql grouped by periodicity. Provide filters in a json {value: "equal_to_this"}"""
	periodicity = get_sql_periodicity(range)

	filter_clause = ""
	if filter:
		for key, value in filter.items():
			filter_clause += f"AND {key}='{value}'"

			
	query_where_clause = """
	WHERE 
		date({}) between '{}' and '{}'
	""".format(filter_based_on, from_date, to_date) + filter_clause

	query_for_ticket_data = """
	SELECT
		{}({}) as date_format,
		date({}) as {},
		count(idx) as count
	FROM tabTicket 
	{}
	GROUP BY date_format
	ORDER BY DATE_FORMAT(date_format,'%Y-%m-%d') asc
	""".format(periodicity, filter_based_on, filter_based_on, filter_based_on, query_where_clause)

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
	""".format(from_date, to_date)
	
	query_all_ticket_data_with_missing_dates = """
	{}
	SELECT 
		coalesce(sum(count)) as count,
		DATE_FORMAT(date({}), '%d-%m-%Y') as {},
		date_format
	FROM(
		SELECT 
			d.dt as {}, 
			{}(d.dt) as date_format,
			coalesce(t.count, 0) as count 
		FROM all_dates d
		LEFT JOIN ({}) t 
		ON t.{} = d.dt
	) as p
	GROUP BY date_format
	""".format(query_for_empty_dates,filter_based_on,filter_based_on, filter_based_on, periodicity, query_for_ticket_data, filter_based_on)

	frappe.log_error("final query", f"{query_all_ticket_data_with_missing_dates}")
	final_data = frappe.db.sql(
		query_all_ticket_data_with_missing_dates,
		as_dict= 1 
	)
	
	return [{**ticket_count_info, "dataset": extra_field_name} for ticket_count_info in final_data]
