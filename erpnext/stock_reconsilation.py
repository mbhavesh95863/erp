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
from frappe.utils import flt, cint
import json
import collections
from erpnext.controllers.sales_and_purchase_return import make_return_doc

@frappe.whitelist()
def addMaterialIssue(obj,doc_name):
	#obj=''
	res_obj=[]
	res_obj1=[]
	res_obj2=[]
	for row in json.loads(obj):
		obj1={}
		obj2={}
		if 'adj_quantity' in row:
			if not flt(row["adj_quantity"])==0.0:
				if not flt(row["current_qty"])<flt(row["qty"]):	
					result=multiBatchSet(row["item_code"],"Sundine Kestrel- . - .",row["adj_quantity"],True)
					for row_res in result:
						res_obj.append(row_res)

			if not flt(row["adj_quantity"])==0.0:
				if flt(row["current_qty"])<flt(row["qty"]):
					obj1["item_code"]=row["item_code"]
					obj1["qty"]=flt(row["qty"])-flt(row["current_qty"])
					obj1["expense_account"]="5250 - Inventory Adjustment - ."
					res_obj2.append(obj1)

		if flt(row["current_qty"])==0.0:
			if not 'adj_quantity' in row:
				obj2["item_code"]=row["item_code"]
				obj2["qty"]=row["qty"]
				#rate=getValuationRate(row["item_code"])
				#if not rate:
				#	frappe.throw(_("No Valuation Rate Available In System For Item {0}.").format(row["item_code"]))
				res_obj1.append(obj2)
		
	#return res_obj	
	if not len(res_obj)==0:	
		addStockEntry(res_obj,doc_name)
	if not len(res_obj1)==0:
		addStockEntry1(res_obj1,doc_name)
	if not len(res_obj2)==0:
		addStockEntry1(res_obj2,doc_name)
	#return res_obj


@frappe.whitelist()
def addStockEntry(item,name):
	doc=frappe.get_doc({
				"docstatus": 0,
				"doctype": "Stock Entry",
				"name": "New Stock Entry 2",
				"naming_series": "STE-",
				"purpose": "Material Issue",
				"custom_purpose":"Qty Adjusted",	
				"company": "Sundine Produce",
				"items":item,
				"from_warehouse": "Sundine Kestrel- . - .",
				"stock_reconsilation":str(name)
			})
	res=doc.insert()
	res.submit()
	return res

@frappe.whitelist()
def addStockEntry1(item,name):
	doc1=frappe.get_doc({
				"docstatus": 0,
				"doctype": "Stock Entry",
				"name": "New Stock Entry 2",
				"naming_series": "STE-",
				"purpose": "Material Receipt",
				"custom_purpose":"Qty Adjusted",
				"company": "Sundine Produce",
				"items":item,
				"to_warehouse": "Sundine Kestrel- . - .",
				"stock_reconsilation":str(name)
			})
	res1=doc1.insert()
	res1.submit()


@frappe.whitelist()
def getValuationRate(item_code):
	last_valuation_rate = frappe.db.sql("""select valuation_rate
		from `tabStock Ledger Entry`
		where item_code = %s and warehouse ='Sundine Kestrel- . - .'
		and valuation_rate >= 0
		order by posting_date desc, posting_time desc, name desc limit 1""",item_code)
	return last_valuation_rate


	

	
	



@frappe.whitelist()
def multiBatchSet(item_code,warehouse,qty,throw=False):
	#doc=frappe.get_doc("Sales Invoice",name)
	#itemdoc=frappe.get_doc("Sales Invoice Item",doc_name)
	batches = get_batches(item_code, warehouse, qty, throw)
	set_batch=False
	response_batch=[]
	#for batch in batches:
	#	res_batch={}
	#	if cint(qty) <= cint(batch.qty):
	#		res_batch["item_code"]=item_code
	#		res_batch["qty"]=qty
	#		res_batch["batch_no"]=batch.batch_id
	#		res_batch["expense_account"]="5250 - Inventory Adjustment - ."
	#		set_batch=True
	#		response_batch.append(res_batch)
	#frappe.msgprint(json.dumps(response_batch))
	#return response_batch

	if set_batch==False:
		total=0
		for batch in batches:
			total=cint(total)+cint(batch.qty)

		if cint(total)<cint(qty):
			#frappe.throw("Insufficient All Batch Qty To Fullfill Order Quantity")
			frappe.throw(_("Insufficient Batch Qty For Item {0} and quantity is {1} and available quantity in All batchs is {2}").format(item_code,qty,total))

		rem_qty=cint(qty)
		count=0
		for batch2 in batches:

			if cint(batch2.qty)>0:
				if not cint(rem_qty)==0:
					res_batch={}
					if cint(batch2.qty)<=cint(rem_qty):
						if count==0:
							#itemAddUpdate(doc_name,batch2.batch_id,batch2.qty,True)
							res_batch["item_code"]=item_code
							res_batch["qty"]=batch2.qty
							res_batch["batch_no"]=batch2.batch_id
							res_batch["expense_account"]="5250 - Inventory Adjustment - ."
							rem_qty=rem_qty-batch2.qty
							count=count+1
							response_batch.append(res_batch)
							#doc.insert()
							#doc1=frappe.get_doc("Sales Invoice Item")
						else:
							res_batch["item_code"]=item_code
							res_batch["qty"]=batch2.qty
							res_batch["batch_no"]=batch2.batch_id
							res_batch["expense_account"]="5250 - Inventory Adjustment - ."
							response_batch.append(res_batch)
							#itemAddUpdate(doc_name,batch2.batch_id,batch2.qty)
							rem_qty=rem_qty-batch2.qty

					else:
						if count==0:
							res_batch["item_code"]=item_code
							res_batch["qty"]=rem_qty
							res_batch["batch_no"]=batch2.batch_id
							res_batch["expense_account"]="5250 - Inventory Adjustment - ."
							rem_qty=rem_qty-batch2.qty
							response_batch.append(res_batch)

						else:
							
							res_batch["item_code"]=item_code
							res_batch["qty"]=rem_qty
							res_batch["batch_no"]=batch2.batch_id
							res_batch["expense_account"]="5250 - Inventory Adjustment - ."
							response_batch.append(res_batch)
						#itemAddUpdate(doc_name,batch2.batch_id,rem_qty)
						break
		return response_batch
	
	#time.sleep(5)
	#doc_final=frappe.get_doc("Sales Invoice",name)
	#doc_final.save()
	#frappe.db.commit()

		


def get_batches(item_code, warehouse, qty=1, throw=False):
	batches = frappe.db.sql(
		'select batch_id, sum(actual_qty) as qty from `tabBatch` join `tabStock Ledger Entry` '
		'on `tabBatch`.batch_id = `tabStock Ledger Entry`.batch_no '
		'where `tabStock Ledger Entry`.item_code = %s and  `tabStock Ledger Entry`.warehouse = %s '
		'and (`tabBatch`.expiry_date >= CURDATE() or `tabBatch`.expiry_date IS NULL)'
		'group by batch_id '
		'order by `tabBatch`.expiry_date ASC, `tabBatch`.creation ASC',
		(item_code, warehouse),
		as_dict=True
	)

	return batches
			
	
