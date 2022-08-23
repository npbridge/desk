frappe.provide("frappe.dashboards.chart_sources")

frappe.dashboards.chart_sources["Tickets Grouped Over Department"] = {
  method:
    "frappedesk.frappedesk.dashboard_chart_source.tickets_grouped_over_department.tickets_grouped_over_department.get",
  filters: [],
}
