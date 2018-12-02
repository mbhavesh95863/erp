# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint
import time


@frappe.whitelist()
def test(doc,warehouse_field):
	frappe.msgprint("Call")

@frappe.whitelist()
def set_batch_nos(doc_name, warehouse_field, throw = False):

	'''Automatically select `batch_no` for outgoing items in item table'''
	doc=frappe.get_doc("Sales Invoice",doc_name)
	for d in doc.items:
		frappe.msgprint(d.get('qty'))
		qty = d.get('stock_qty') or d.get('transfer_qty') or d.get('qty') or 0
		has_batch_no = frappe.db.get_value('Item', d.item_code, 'has_batch_no')
		warehouse = d.get(warehouse_field, None)
		if has_batch_no and warehouse and qty > 0:
			if not d.batch_no:
				d.batch_no = get_batch_no(d.item_code, warehouse, qty, throw,d.name)
			else:
				batch_qty = get_batch_qty(batch_no=d.batch_no, warehouse=warehouse)
				if flt(batch_qty, d.precision("qty")) < flt(qty, d.precision("qty")):
					frappe.throw(_("Row #{0}: The batch {1} has only {2} qty. Please select another batch which has {3} qty available or split the row into multiple rows, to deliver/issue from multiple batches").format(d.idx, d.batch_no, batch_qty, qty))


@frappe.whitelist()
def multiBatchSet(name,doc_name,item_code,warehouse,qty,throw=False):
	has_batch_no = frappe.db.get_value('Item',item_code, 'has_batch_no')
	if has_batch_no:
		doc=frappe.get_doc("Stock Entry",name)
		itemdoc=frappe.get_doc("Stock Entry Detail",doc_name)
		batches = get_batches(item_code, warehouse, qty, throw)
		set_batch=False
		#for batch in batches:
		#	if cint(qty) <= cint(batch.qty):
				#batch_no = batch.batch_id
				#itemAddupdate(doc_name,batch_no,True)
		#		set_batch=True

		if set_batch==False:
			total=0
			for batch in batches:
				total=cint(total)+cint(batch.qty)

			if cint(total)<cint(qty):
				#frappe.throw("Insufficient All Batch Qty To Fullfill Order Quantity")
				frappe.throw(_("Row #{0}: Insufficient Batch Qty To Fullfill Transfer Quantity. Batch's Qty is {1} and Transfer Qty is {2}.").format(itemdoc.idx,total,qty))

			rem_qty=cint(qty)
			count=0
			for batch2 in batches:
				if cint(batch2.qty)>0:
					if not cint(rem_qty)==0:
						if cint(batch2.qty)<=cint(rem_qty):
							#frappe.msgprint(str(batch2.batch_id))
							if count==0:
								itemAddUpdate(doc_name,batch2.batch_id,batch2.qty,True)
								rem_qty=rem_qty-batch2.qty
								count=count+1
								#doc.insert()
								#doc1=frappe.get_doc("Sales Invoice Item")
							else:
								itemAddUpdate(doc_name,batch2.batch_id,batch2.qty)
								rem_qty=rem_qty-batch2.qty

						else:
							if count==0:
								itemAddUpdate(doc_name,batch2.batch_id,rem_qty,True)
							else:
								itemAddUpdate(doc_name,batch2.batch_id,rem_qty)
			
							break
	
	#time.sleep(15)
	#doc_final=frappe.get_doc("Sales Invoice",name)
	#doc_final.save()
	#frappe.db.commit()



@frappe.whitelist()
def updatevalue(name):
	doc=frappe.get_doc("Stock Entry",name)
	doc.save()
	

										
			
			
	
		
			
			
			
		


@frappe.whitelist()
def itemAddUpdate(name,batch_no,qty=None,flag=False):
	if flag==True:
		quntity=0
		item_doc=frappe.get_doc("Stock Entry Detail",name)
		if quntity==None:
			quntity=item_doc.qty
		else:
			quntity=qty
		item_doc.batch_no=batch_no
		item_doc.qty=quntity
		item_doc.cost_center=getCostCenter(item_doc.item_code)
		item_doc.save()

	if flag==False:
		quntity=0	
		item_doc=frappe.get_doc("Stock Entry Detail",name)
		if quntity==None:
			quntity=item_doc.qty
		else:
			quntity=qty


		doc1=frappe.get_doc({
					"t_warehouse":str(item_doc.t_warehouse),
					"transfer_qty":str(quntity),
					"qty":str(quntity),
					"owner":str(frappe.session.use),
					"cost_center":str(item_doc.cost_center),
					"stock_uom":str(item_doc.stock_uom),
					"item_name":str(item_doc.item_name),
					"conversion_factor":str(item_doc.conversion_factor),
					"docstatus": 0,
					"uom":str(item_doc.uom),
					"basic_rate":flt(item_doc.basic_rate),
					"description":str(item_doc.description),
					"parent": str(item_doc.parent),
					"item_code":str(item_doc.item_code),
					"doctype": "Stock Entry Detail",
					"expense_account":str(item_doc.expense_account),
					"name":"New Stock Entry Detail 1",
					"s_warehouse":str(item_doc.s_warehouse),
					"parenttype": "Stock Entry",
					"batch_no":str(batch_no),
					"parentfield": "items"
				})
		doc1.insert()




	'''	doc1=frappe.get_doc({
				"doctype":"Sales Invoice Item",
				"name":"New Sales Invoice Item 1",
				"parent":str(item_doc.parent),
				"item_code":str(item_doc.item_code),
				"item_name":str(item_doc.item_name),
				"price_list_rate":str(item_doc.price_list_rate),
				"rate":str(item_doc.rate),
				"parenttype":"Sales Invoice",
				"parentfield":"items",
				"hst":item_doc.hst,
				"qty":str(quntity),
				"batch_no":str(batch_no),
				"actual_qty":str(item_doc.actual_qty) if not item_doc.actual_qty==None else "",
				"cost_center":getCostCenter(item_doc.item_code),
				"discount_percentage":str(item_doc.discount_percentage) if not item_doc.discount_percentage==None else ""		
			})
		doc1.insert()'''
	#doc_final=frappe.get_doc("Sales Invoice",item_doc.parent)
	#doc_final.save()

@frappe.whitelist()
def getCostCenter(name):
	data=frappe.db.sql("""select cost_center from `tabItem` where name=%s""",name)
	if data:
		if not data[0][0]==None:
			return data[0][0]
		else:
			return str()
	else:
		return str()	
		


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
