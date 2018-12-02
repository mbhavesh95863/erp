from __future__ import unicode_literals
import frappe

from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections


@frappe.whitelist()
def test(po):
	data=json.loads(po)
	for row in data["master_purchase_order_item"]:
		return data["shipping_date"]

@frappe.whitelist()
def makepo1(poname,ps):
	data=json.loads(ps)
	count=0
	i=0
	for row in data["details"]:
	
		data3=frappe.get_doc({
							"naming_series": "PO-",
							"doctype": "Purchase Order",
							"conversion_rate": row[0]["conversion_rate"],
							"currency": getCurrency(row[0]["supplier"]),
							"transaction_date":row[0]["shipping_date"],
							"supplier":row[0]["supplier"],
							"order_type": row[0]["order_type"],
							"docstatus": 0,
							"ignore_pricing_rule": 0,
							"schedule_date": row[0]["arrival_date"],
							"name": "New Purchase Order 1",
							"master_po_id": poname,
							"col_number": row[0]["col_number"],
							"idx": 0,
							"items": row[0]["items"],
							"price_list_currency": getCurrency(row[0]["supplier"]),
							"plc_conversion_rate": row[0]["plc_conversion_rate"],
							"total_boxes": row[0]["total_boxes"],
							"total_pallet": row[0]["total_pallet"],
							"total_net_weight": row[0]["total_net_weight"],
							"total_gross_weight_lbs": row[0]["total_gross_weight_lbs"],
							"total_weight_kg": row[0]["total_weight_kg"]
						})
		d=data3.insert(ignore_permissions=True)
		frappe.db.sql("""UPDATE `tabMaster Purchase Order Item`  SET `purchase_order` = %s
        where  parent = %s AND supplier = %s AND col_number = %s """, (d.name, poname, row[0]["supplier"], row[0]["col_number"]))
		count=count+1

@frappe.whitelist()
def makePurchaseorder(ps):
	data=json.loads(ps)
	count=0
	i=0
	for row in data["taxes"]:
	
		data3=frappe.get_doc({
							"naming_series": "PO/Lc-",
							"doctype": "Purchase Order",
							"currency": getCurrency(data["supplier"]),
							"transaction_date":data["creation"],
							"supplier":data["supplier"],
							"docstatus": 0,
							"ignore_pricing_rule": 0,
							"schedule_date": data["creation"],
							"name": "New Purchase Order 1",
							"lcv_id": data["name"],
							"idx": 0,
							"items": [
								"qty": 1,
								"price": row["amount"],
								"rate": row["rate"],
								"expected_delivery_date": data["creation"],
								"description": row["description"],
								"item_code": "",
								"item_name": "",
							],
							"create_po": 'Y'
						})
		if row['create_po'] == 'N':		
			d=data3.insert(ignore_permissions=True)
			count=count+1
	
	return count
		
@frappe.whitelist()
def getCurrency(sup):
	data=frappe.db.sql("""select default_currency from `tabSupplier` where name=%s""",sup)
	if len(data):
		return data[0][0]
	else:
		return "CAD"
@frappe.whitelist()