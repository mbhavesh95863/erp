frappe.query_reports["Qty Adjustment Log"] = {
	"filters": [

		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"default":frappe.datetime.get_today()
		}
	]
}
