// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tickets Replied To Over Time"] = {
	filters: [
		{
			fieldname: "from_date_first",
			label: __("From Date (first)"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.nowdate(), -60),
			reqd: 1,
		},
		{
			fieldname: "to_date_first",
			label: __("To Date (first)"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.nowdate(), -30),
			reqd: 1,
		},
		{
			fieldname: "from_date_second",
			label: __("From Date (second)"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.nowdate(), -30),
			reqd: 1,
		},
		{
			fieldname: "to_date_second",
			label: __("To Date (second)"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.nowdate()),
			reqd: 1,
		},
		{
			fieldname: "range",
			label: __("Range"),
			fieldtype: "Select",
			options: [
				{ value: "Day", label: __("Daily") },
				{ value: "Week", label: __("Weekly") },
				{ value: "Month", label: __("Monthly") },
				{ value: "Quarter", label: __("Quarterly") },
				{ value: "Year", label: __("Yearly") },
			],
			default: "Week",
			reqd: 1,
		},
	],
	get_chart_data: (_columns, result) => {
		let firstDataset = []
		let secondDataset = []

		result.forEach((ticketData) => {
			if (ticketData.dataset === "First date range")
				firstDataset.push(ticketData)
			else if (ticketData.dataset === "Second date range")
				secondDataset.push(ticketData)
		})

		const isFirstLarger = firstDataset.length > secondDataset.length
		const largerDataSet = isFirstLarger ? firstDataset : secondDataset
		const difference = Math.abs(firstDataset.length - secondDataset.length)
		const arrayToFillSmallerDataset = Array(difference).fill(0)

		const labels = largerDataSet.map(
			(data, index) =>
				`${
					firstDataset[index]
						? firstDataset[index].first_responded_on
						: "-"
				}|
         ${
				secondDataset[index]
					? secondDataset[index].first_responded_on
					: "-"
			}`
		)
		const firstDataSetValues = firstDataset.map((d) => d.count)
		const secondDatasetValues = secondDataset.map((d) => d.count)

		return {
			data: {
				labels: labels,
				datasets: [
					{
						name: "First date range",
						values: isFirstLarger
							? firstDataSetValues
							: [
									...firstDataSetValues,
									...arrayToFillSmallerDataset,
							  ],
					},
					{
						name: "Second date range",
						values: isFirstLarger
							? [
									...secondDatasetValues,
									...arrayToFillSmallerDataset,
							  ]
							: secondDatasetValues,
					},
				],
			},
			type: "line",
			tooltipOptions: {
				formatTooltipY: (d) => d + " tickets",
			},
			barOptions: {
				spaceRatio: 0.3, // default: 1
			},
		}
	},
}
