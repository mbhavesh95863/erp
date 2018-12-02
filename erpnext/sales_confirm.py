from __future__ import unicode_literals
import frappe

from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime,flt
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice,update_status
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
from erpnext.controllers.sales_and_purchase_return import make_return_doc
# import urllib


@frappe.whitelist()
def checkConfirmSales(name):
	doc=frappe.get_doc("Sales Invoice",name)
	flag=False
	for item in doc.items:
		so=frappe.get_doc("Sales Order",item.sales_order)
		if not len(so.items)==len(doc.items):
			return True
		so_item=frappe.get_doc("Sales Order Item",item.so_detail)
		if not flt(so_item.qty)==flt(item.qty):
			return True
	return False



@frappe.whitelist()
def makeRemainItemOrder(name):	
	doc=frappe.get_doc("Sales Invoice",name)
	so_item=[]
	total_box=0
	total_pallet=0
	total_lbs_box=0
	so_no=''
	for item in doc.items:
		item_json={}
		so_detail=frappe.get_doc("Sales Order Item",item.so_detail)
		if not flt(so_detail.qty)==flt(item.qty):
			item_json["item_code"]=str(so_detail.item_code)
			item_json["qty"]=flt(so_detail.qty)-flt(item.qty)
			item_json["cost_center"]=getCostCenter(so_detail.item_code)
			qty=flt(so_detail.qty)-flt(item.qty)
			total_box=total_box+qty
			total_pallet=total_pallet+(qty/so_detail.sale_pallets)
			total_lbs_box=qty*so_detail.gross_weight_lbs
			so_item.append(item_json)
		so_no=item.sales_order
	so_data=frappe.get_doc("Sales Order",so_no)
	for row1 in so_data.items:
		flag2=False
		for row2 in doc.items:
			if row1.name==row2.so_detail:
				flag2=True
				break
		if flag2==False:
			item_json2={}
			item_json2["item_code"]=row1.item_code
			item_json2["qty"]=row1.qty
			item_json2["cost_center"]=getCostCenter(row1.item_code)
			qty=flt(row1.qty)
			total_box=total_box+qty
			total_pallet=total_pallet+(qty/row1.sale_pallets)
			total_lbs_box=qty*row1.gross_weight_lbs
			so_item.append(item_json2)
	if not len(so_item)==0:
		so_name=makeSalesOrder(so_data.name,so_item,total_box,total_lbs_box,total_pallet)
		return so_name




@frappe.whitelist()
def makeSOFromSo(name):
	so_item=[]
	total_box=0
	total_pallet=0
	total_lbs_box=0
	so_data=frappe.get_doc("Sales Order",name)
	for row1 in so_data.items:
		if(row1.qty>row1.delivered_qty):
			item_json2={}
			item_json2["item_code"]=row1.item_code
			item_json2["qty"]=row1.qty-row1.delivered_qty
			item_json2["cost_center"]=getCostCenter(row1.item_code)
			qty=flt(row1.qty)-flt(row1.delivered_qty)
			total_box=total_box+qty
			total_pallet=total_pallet+(qty/row1.sale_pallets)
			total_lbs_box=qty*row1.gross_weight_lbs
			so_item.append(item_json2)
		
	if not len(so_item)==0:
		so_name=makeSalesOrder(name,so_item,total_box,total_lbs_box,total_pallet)
		return so_name


@frappe.whitelist()
def makeSalesOrder(name,item_obj,total_box,total_lbs_box,total_pallet):
	doc=frappe.get_doc("Sales Order",name)
	so_data=frappe.get_doc(dict(
		doctype="Sales Order",
		customer=str(doc.customer),
		delivery_date=add_days(doc.delivery_date,2),
		transaction_date=str(today()),
		selling_price_list=str(doc.selling_price_list),
		items=item_obj,
		total_boxes=total_box,
		total_gross_weight_lbs=total_lbs_box,
		total_weight_kg=flt(total_lbs_box)*0.45359237,
		total_pallets=total_pallet,
		is_back_order=1,
		sales_order_ref=name
	)).insert()
	update_status('Closed',name)
	return so_data.name	


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
	
				
			
			
			
