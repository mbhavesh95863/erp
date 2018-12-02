# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint
import time
import json
import collections


@frappe.whitelist()
def getColumn(date):
	last_plist=frappe.db.sql("""select name1 as 'name' from `tabPriceList Arrangement Order` order by idx ASC""",as_dict=1)
	if last_plist:
		return last_plist
	else:
		data=frappe.db.sql("""select name  from `tabPrice List` order by modified DESC limit 10""",as_dict=1)
		return data


@frappe.whitelist()
def getData(pricelist_obj,filters):
	query="select name from `tabItem` where disabled=0"
	fil=json.loads(filters)
		
	if not fil['item_code']==None and not fil['item_group']==None:
		item_list=frappe.db.sql("""select name from `tabItem` where disabled=0 and item_code=%s and item_group=%s""",(fil['item_code'],fil['item_group']))
	elif not fil['item_group']==None:
		item_list=frappe.db.sql("""select name from `tabItem` where disabled=0 and item_group=%s""",fil['item_group'])
	elif not fil['item_code']==None:
		item_list=frappe.db.sql("""select name from `tabItem` where disabled=0 and item_code=%s""",fil['item_code'])
	else:
		item_list=frappe.db.sql("""select name from `tabItem` where disabled=0""")
	
	dataobj=[]
	for item in item_list:
		obj={}
		count=0
		obj["item"]=item[0]
		for row in json.loads(pricelist_obj):
			obj[str(row["name"])]=getPrice(item[0],row["name"])
			count=count+1
		dataobj.append(obj)

	return dataobj

def getPrice(item,name):
	data=frappe.db.sql("""select price_list_rate from `tabItem Price` where price_list=%s and item_code=%s""",(name,item))
	if data:
		if not data[0][0]==None:
			return data[0][0]
		else:
			return 0
	else:
		return 0


@frappe.whitelist()
def updatePriceListValue(item_code,price_list_name,rate):
	if not rate==0:
		name=frappe.db.sql("""select name from `tabItem Price` where item_code=%s and price_list=%s""",(item_code,price_list_name))
		if name:
			if not name[0][0]==None:
				doc=frappe.get_doc("Item Price",name[0][0])
				doc.price_list_rate=flt(rate)
				doc.save()
				return "true"
			else:
				doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Item Price",
							"name": "New Item Price 1",
							"owner": frappe.session.user,
							"price_list":str(price_list_name),
							"item_name":getItemName(item_code),
							"item_description":getItemDesc(item_code),
							"item_code":str(item_code),
							"price_list_rate":rate
						})
				doc.insert()
				return "true"
		else:
			doc=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": frappe.session.user,
						"price_list":str(price_list_name),
						"item_name":getItemName(item_code),
						"item_description":getItemDesc(item_code),
						"item_code":str(item_code),
						"price_list_rate":rate
					})
			doc.insert()
			return "true"
		
	

def getItemName(item_code):
	data=frappe.db.sql("""select item_name from `tabItem` where item_code=%s""",item_code)
	if data:
		if not data[0][0]==None:
			return data[0][0]
		else:
			return str()
	else:
		return str()

def getItemDesc(item_code):
	data=frappe.db.sql("""select description from `tabItem` where item_code=%s""",item_code)
	if data:
		if not data[0][0]==None:
			return data[0][0]
		else:
			return str()
	else:
		return str()



@frappe.whitelist()
def addPriceList(object_val):
	doc_name=frappe.get_all("PriceList Arrangement",filters={},fields=["name"])
	for row in doc_name:
		frappe.delete_doc("PriceList Arrangement",row["name"])
	doc=frappe.get_doc({
			"doctype":"PriceList Arrangement",
			"arrangements":json.loads(object_val)		
			
		})
	doc1=doc.insert()
	if doc1:
		return "True"
	else:
		return "False"
	
