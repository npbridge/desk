frappe.provide("frappe.dashboards.chart_sources")

frappe.dashboards.chart_sources["Contacts Grouped Over Department"] = {
  method:
    "frappedesk.frappedesk.dashboard_chart_source.contacts_grouped_over_department.contacts_grouped_over_department.get",
  filters: [],
}
