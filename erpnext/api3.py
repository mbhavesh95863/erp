from __future__ import unicode_literals
import frappe
from frappe.utils import cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
import frappe.permissions
import frappe.share
import re
import string
import random
import json
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import collections
import math
import logging
from frappe.client import delete

d1=[]
d2=[]


@frappe.whitelist(allow_guest=True)
def changeLevel(data):
	from frappe.auth import LoginManager
	login_manager = LoginManager()
	login_manager.authenticate("Administrator","heyram108")
	login_manager.post_login()
	company=json.loads(data)
	logging.warning("blank+"+str(json.dumps(company)))
	if company["l1"]==None or company["l1"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='Small'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l2"]==None or company["l2"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='Med'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l3"]==None or company["l3"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='Wholesale'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l4"]==None or company["l4"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='SMR'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l5"]==None or company["l5"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='CC'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l6"]==None or company["l6"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='OR/DUN'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l7"]==None or company["l7"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='OM'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l8"]==None or company["l8"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='BV'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l9"]==None or company["l9"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='SFM'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l10"]==None or company["l10"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IFL/AFCH'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l11"]==None or company["l11"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IPP'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l12"]==None or company["l12"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='GMBL'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l13"]==None or company["l13"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='MNLY'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l14"]==None or company["l14"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='HWAI'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l15"]==None or company["l15"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='PANCH'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l16"]==None or company["l16"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='NSS'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l17"]==None or company["l17"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='WIN'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l18"]==None or company["l18"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IBF/R'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l19"]==None or company["l19"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IBI/K'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])

	if company["l20"]==None or company["l20"]=='':
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='BOND'""",company["name"])
		if data:
			delete(doctype='Item Price',name=data[0][0])



	if company["l1"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='Small'""",company["name"])
		if data:
			if not int(company["l1"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"Small",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "Small",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l1"]
					})
			d1=d.insert(ignore_permissions=True)
			

	if company["l2"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='Med'""",company["name"])
		if data:
			if not int(company["l2"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"Med",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "Med",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l2"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l3"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='Wholesale'""",company["name"])
		if data:
			if not int(company["l3"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"Wholesale",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "Wholesale",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l3"]
					})
			d1=d.insert(ignore_permissions=True)
	

	if company["l4"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='SMR'""",company["name"])
		if data:
			if not int(company["l4"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"SMR",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "SMR",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l4"]
					})
			d1=d.insert(ignore_permissions=True)
	

	if company["l5"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='CC'""",company["name"])
		if data:
			if not int(company["l5"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"CC",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "CC",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l5"]
					})
			d1=d.insert(ignore_permissions=True)
	

	if company["l6"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='OR/DUN'""",company["name"])
		if data:
			if not int(company["l6"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"OR/DUN",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "OR/DUN",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l6"]
					})
			d1=d.insert(ignore_permissions=True)
	

	if company["l7"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='OM'""",company["name"])
		if data:
			if not int(company["l7"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"OM",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "OM",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l7"]
					})
			d1=d.insert(ignore_permissions=True)
	
	if company["l8"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='BV'""",company["name"])
		if data:
			if not int(company["l8"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"BV",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "BV",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l8"]
					})
			d1=d.insert(ignore_permissions=True)
	
	if company["l9"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='SFM'""",company["name"])
		if data:
			if not int(company["l9"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"SFM",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "SFM",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l9"]
					})
			d1=d.insert(ignore_permissions=True)
	
	if company["l10"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IFL/AFCH'""",company["name"])
		if data:
			if not int(company["l10"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l1"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"IFL/AFCH",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "IFL/AFCH",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l10"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l11"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IPP'""",company["name"])
		if data:
			if not int(company["l11"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l11"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"IPP",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "IPP",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l11"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l12"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='GMBL'""",company["name"])
		if data:
			if not int(company["l12"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l12"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"GMBL",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "GMBL",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l12"]
					})
			d1=d.insert(ignore_permissions=True)


	if company["l13"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='MNLY'""",company["name"])
		if data:
			if not int(company["l13"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l13"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"MNLY",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "MNLY",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l13"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l14"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='HWAI'""",company["name"])
		if data:
			if not int(company["l14"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l14"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"HWAI",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "HWAI",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l14"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l15"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='PANCH'""",company["name"])
		if data:
			if not int(company["l15"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l15"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"PANCH",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "PANCH",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l15"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l16"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='NSS'""",company["name"])
		if data:
			if not int(company["l16"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l16"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"NSS",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "NSS",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l16"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l17"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='WIN'""",company["name"])
		if data:
			if not int(company["l17"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l17"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"WIN",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "WIN",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l17"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l18"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IBF/R'""",company["name"])
		if data:
			if not int(company["l18"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l18"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"IBF/R",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "IBF/R",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l18"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l19"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='IBI/K'""",company["name"])
		if data:
			if not int(company["l19"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l19"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"IBI/K",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "IBI/K",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l19"]
					})
			d1=d.insert(ignore_permissions=True)

	if company["l20"]:
		data=frappe.db.sql("""select name,price_list_rate from `tabItem Price` where item_code=%s and price_list='BOND'""",company["name"])
		if data:
			if not int(company["l20"])==int(data[0][1]):
				logging.warning("Inside+"+str(data[0][0]))
				d2=frappe.get_doc("Item Price",data[0][0])
				d=frappe.get_doc({
							"price_list_rate": company["l20"],
							"selling": 1,
							"name": data[0][0],
							"currency": "INR",
							"price_list":"BOND",
							"item_code": company["name"],
							"doctype": "Item Price",
							"docstatus": 0,
							"buying": 0,
							"modified":d2.modified
						})
				d1=d.save()
		else:
			d=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Item Price",
						"name": "New Item Price 1",
						"owner": "Administrator",
						"currency": "INR",
						"price_list": "BOND",
						"buying": 0,
						"selling": 1,
						"item_code": str(company["name"]),
						"price_list_rate": company["l20"]
					})
			d1=d.insert(ignore_permissions=True)


@frappe.whitelist()
def setSupplier():
	doc=frappe.get_all("Supplier",filters={},fields=["name"])
	for row in doc:
		doc_data=frappe.get_doc("Supplier",row["name"])
		if len(doc_data.taxes)>=1:
			doc_data.hst="Yes"
			doc_data.save()
		else:
			doc_data.hst="No"
			doc_data.save()


@frappe.whitelist()
def getTaxRate(supplier):
	data=frappe.db.sql("""select tax_rate from `tabItem Tax` where parent=%s""",supplier)
	if data:
		if not data[0][0]==None:
			return data[0][0]
		else:
			return "False"
	else:
		return "False"


	
		
	
	
	
