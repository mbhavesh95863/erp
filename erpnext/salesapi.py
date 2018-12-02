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
	for row in data["master_sales_order_item"]:
		return data["shipping_date"]

@frappe.whitelist()
def customerAddresses(supplier):
	data1=frappe.db.sql("""select ad.name,ad.address_title from `tabAddress` as ad inner join `tabDynamic Link` as dl on ad.name=dl.parent where dl.link_doctype='Customer' and dl.link_name=%s """,supplier, as_dict=1)
	return data1


@frappe.whitelist()
def makeTemplate(mso_id,shipping_date,delivery_date,pallet_weight,usd):
	data2=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Master Sales Order Template",
						"name": "Master Sales Order Template 1",
						"mso_id": mso_id,
						"status": "Draft",
						"shipping_date": shipping_date,
						"delivery_date": delivery_date,
						"pallet_weight": pallet_weight,
						"usd": usd
					})
	d=data2.insert(ignore_permissions=True)
	return d.name


@frappe.whitelist()
def makeMasterPoOrder(po,ps):
	data=json.loads(po)
	data2=frappe.get_doc({
							"docstatus": 0,
							"naming_series": "MSO-",
							"doctype": "Master Sales Order",
							"name": "New Master Sales Order 1",
							"shipping_date": data["shipping_date"],
							"delivery_date": data["delivery_date"],
							"cad": data["cad"],
							"pallet_weight": data["pallet_weight"],
							"usd": data["usd"],
							"total_actual_cost": data["total_actual_cost"],
							"total_actual_cost_usd": data["total_actual_cost_usd"],
							"master_sales_order_item": []
						})
	d=data2.insert(ignore_permissions=True)
	if d:
		for row in data["master_sales_order_item"]:

			data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Sales Order Item",
								"name": "New Master Sales Order Item 1",
								"owner": str(frappe.session.user),
								"parent": d.name,
								"parentfield": "master_sales_order_item",
								"parenttype": "Master Sales Order",
								"qty": row["qty"],
								"price": row["price"],
								"weight": row["weight"],
								"received_qty": row["received_qty"],
								"default_currency": getCurrency(row["customer"]),
								"weight_per_unit": row["weight"],
								"gross_weight": row["gross_weight"],
								"uom": row["uom"],
								"description": row["description"],
								"purchase_pallets": row["purchase_pallets"],
								"item_code": row["item_code"],
								"item_name": row["item_name"],
								"ppk_calculation": row["ppk_calculation"],
								"customer_name": row["customer_name"],
								"customer": row["customer"],
								"row_number": row["row_number"],
								"col_number": row["col_number"],
								"address_title": row["address_title"],
								"address": row["address"],
								"po_no": row["po_no"],
								"mso_notes": row["mso_notes"]
							})
			d1=data3.insert(ignore_permissions=True)
		poname = d.name
		
		return d.name

@frappe.whitelist()
def saveMasterPoOrder(po,ps):
	data=json.loads(po)
	master_so_data=frappe.get_doc("Master Sales Order",str(data["name"]))
	
	master_so_data.status = "Saved"
	master_so_data.shipping_date = data["shipping_date"]
	master_so_data.delivery_date = data["delivery_date"]
	master_so_data.cad = data["cad"]
	master_so_data.usd = data["usd"]
	master_so_data.pallet_weight = data["pallet_weight"]
	master_so_data.total_actual_cost = data["total_actual_cost"]
	master_so_data.total_actual_cost_usd = data["total_actual_cost_usd"]
	
	master_so_data.save(ignore_permissions=True)
	
	frappe.db.sql("""delete from `tabMaster Sales Order Item` 
        where parent = %s """, master_so_data.name)
	
	for row in data["master_sales_order_item"]:

		data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Sales Order Item",
								"name": "New Master Sales Order Item 1",
								"owner": str(frappe.session.user),
								"parent": master_so_data.name,
								"parentfield": "master_sales_order_item",
								"parenttype": "Master Sales Order",
								"qty": row["qty"],
								"price": row["price"],
								"weight": row["weight"],
								"weight_per_unit": row["weight"],
								"gross_weight": row["gross_weight"],
								"uom": row["uom"],
								"description": row["description"],
								"purchase_pallets": row["purchase_pallets"],
								"item_code": row["item_code"],
								"item_name": row["item_name"],
								"ppk_calculation": row["ppk_calculation"],
								"received_qty": row["received_qty"],
								"default_currency": getCurrency(row["customer"]),
								"customer_name": row["customer_name"],
								"customer": row["customer"],
								"row_number": row["row_number"],
								"col_number": row["col_number"],
								"address_title": row["address_title"],
								"address": row["address"],
								"po_no": row["po_no"],
								"mso_notes": row["mso_notes"]
							})
		d1=data3.insert(ignore_permissions=True)
	makeso1(data["name"],ps);
	
	return master_so_data.name
		
@frappe.whitelist()
def makeso1(poname,ps):
	data=json.loads(ps)
	count=0
	i=0
	for row in data["details"]:
		so_item=[]
		for item in row[0]["items"]:
			item_json=item
			item_json["cost_center"]=getCostCenter(item["item_code"])
			so_item.append(item_json)
		
			
		data3=frappe.get_doc({
							"naming_series": "SO-",
							"doctype": "Sales Order",
							"currency": getCurrency(row[0]["customer"]),
							"selling_price_list":row[0]["default_price_list"],
							"transaction_date":row[0]["shipping_date"],
							"customer":row[0]["customer"],
							"docstatus": 0,
							"ignore_pricing_rule": 0,
							"delivery_date": row[0]["delivery_date"],
							"name": "New Sales Order 1",
							"master_so_id": poname,
							"idx": 0,
							"items": so_item,
							"price_list_currency": getCurrency1(row[0]["default_price_list"]),
							"total_boxes": row[0]["total_boxes"],
							"total_pallets": row[0]["total_pallet"],
							"total_net_weight": row[0]["total_net_weight"],
							"total_gross_weight_lbs": row[0]["total_gross_weight_lbs"],
							"total_weight_kg": row[0]["total_weight_kg"],
							"po_no": row[0]["po_no"],
							"shipping_address_name": row[0]["address"]
						})
		d=data3.insert(ignore_permissions=True)
		frappe.db.sql("""UPDATE `tabMaster Sales Order Item`  SET `sales_order` = %s
        where  parent = %s AND customer = %s AND col_number = %s """, (d.name, poname, row[0]["customer"], row[0]["col_number"]))
		count=count+1


def getCostCenter(item):
	data=frappe.db.sql("""select cost_center from `tabItem` where name=%s""",item)
	if data:
		return data[0][0]
	else:
		company=frappe.get_doc("Company","Sundine Produce")
		if company.cost_center:
			return company.cost_center
		else:
			return str() 

@frappe.whitelist()
def getCurrency(sup):
	data=frappe.db.sql("""select default_currency from `tabCustomer` where name=%s""",sup)
	if len(data):
		return data[0][0]
	else:
		return "CAD"

@frappe.whitelist()
def getCurrency1(pls):
	data=frappe.db.sql("""select currency from `tabPrice List` where name=%s""",pls)
	if len(data):
		return data[0][0]
	else:
		return "CAD"
		
@frappe.whitelist()
def makeReceivingSheet(master_sales_order):
	to_date=today()
	master_so=frappe.get_doc("Master Sales Order",str(master_sales_order))
	
	if not frappe.db.exists("Master Sales Receiving Mode",str(master_sales_order)):
		data2=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Master Sales Receiving Mode",
							"name": "New Master Sales Receiving Mode 1",
							"master_sales_order": master_sales_order,
							"shipping_date": master_so.shipping_date,
							"delivery_date": master_so.delivery_date,
							"order_type": master_so.order_type,
							"receiving_date": to_date
						})
		d=data2.insert(ignore_permissions=True)
		if d:
			return d.name
	else:
		check_sheet=frappe.get_doc("Receiving Sheet",str(master_sales_order))
		return check_sheet.name		
		

@frappe.whitelist()
def updateMasterPoOrder(po,ps):
	data=json.loads(po)
	master_so_data=frappe.get_doc("Master Sales Order",str(data["name"]))
	
	master_so_data.shipping_date = data["shipping_date"]
	master_so_data.delivery_date = data["delivery_date"]
	master_so_data.cad = data["cad"]
	master_so_data.usd = data["usd"]
	master_so_data.pallet_weight = data["pallet_weight"]
	master_so_data.total_actual_cost = data["total_actual_cost"]
	master_so_data.total_actual_cost_usd = data["total_actual_cost_usd"]
	
	master_so_data.save(ignore_permissions=True)
	
	frappe.db.sql("""delete from `tabMaster Sales Order Item` 
        where parent = %s """, master_so_data.name)
	
	for row in data["master_sales_order_item"]:

		data3=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Master Sales Order Item",
								"name": "New Master Sales Order Item 1",
								"owner": str(frappe.session.user),
								"parent": master_so_data.name,
								"parentfield": "master_sales_order_item",
								"parenttype": "Master Sales Order",
								"qty": row["qty"],
								"price": row["price"],
								"weight": row["weight"],
								"weight_per_unit": row["weight"],
								"gross_weight": row["gross_weight"],
								"uom": row["uom"],
								"description": row["description"],
								"purchase_pallets": row["purchase_pallets"],
								"item_code": row["item_code"],
								"item_name": row["item_name"],
								"ppk_calculation": row["ppk_calculation"],
								"received_qty": row["received_qty"],
								"default_currency": getCurrency(row["customer"]),
								"customer_name": row["customer_name"],
								"customer": row["customer"],
								"row_number": row["row_number"],
								"col_number": row["col_number"],
								"address_title": row["address_title"],
								"po_no": row["po_no"],
								"mso_notes": row["mso_notes"]
							})
		d1=data3.insert(ignore_permissions=True)
	
	return master_so_data.name
		
@frappe.whitelist()
def saveReceivingSheet(po,ps):
	data=json.loads(po)
	datap=json.loads(ps)
	for row in data["master_sales_order_items"]:
		
		master_so_data=frappe.get_doc("Master Sales Order Item",str(row["name"]))
		master_so_data.received_qty = row["received_qty"]
		master_so_data.save(ignore_permissions=True)
				
	for row1 in datap["details"]:
	
		data3=frappe.get_doc({
							"docstatus": 1, 
							"status": "Draft",
							"doctype": "Sales Invoice",
							"naming_series": "SINV-",
							"name": "New Sales Invoice 1",
							"currency": getCurrency(row1[0]["customer"]),
							"customer":row1[0]["customer"],
							"posting_date": today(),
							"due_date": row1[0]["delivery_date"],
							"master_so_id": row1[0]["master_sales_order"],
							"idx": 0
						})
		d=data3.insert(ignore_permissions=True)
	
	
	return data["master_sales_order"]
	
