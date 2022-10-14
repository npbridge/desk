frappe.provide("frappe.dashboards.chart_sources")

frappe.dashboards.chart_sources["Tickets Un-resolved Over Time"] = {
	method: "frappedesk.frappedesk.dashboard_chart_source.tickets_un_resolved_over_time.tickets_un_resolved_over_time.get",
	filters: [],
}
