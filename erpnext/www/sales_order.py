#copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from frappe.utils import cstr, nowdate, cint, today
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
import frappe.website.render

no_cache = 1
no_sitemap = 1

@frappe.whitelist()
def get_sales_order(city_name=None, delivery_date=None, limit=50, status=None, vehicle=None, driver=None ):
        query  = """ SELECT so.*,ad.city,ad.state,ad.country,ad.address_title,ad.address_line1,ad.latitude,ad.longitude,ad.near_by_location,ad.phone  FROM `tabSales Order` so LEFT JOIN `tabAddress` ad ON  so.shipping_address_name = ad.name LEFT JOIN `tabCustomer` cu ON cu.name = so.customer  WHERE so.customer != ''  """

        if not delivery_date or delivery_date==None or delivery_date=="":
                                                                 delivery_date=today()

        query += """ AND so.delivery_date =  %(delivery_date)s  """
        delivery_date = cstr(delivery_date)

         # search term condition
        if vehicle:
                query += """ AND so.vehicle = %(vehicle)s  """
                vehicle =  cstr(vehicle)

        if city_name:
                query += """ AND ad.city LIKE  %(city_name)s  """
                city_name = "%" + cstr(city_name) + "%"

        if status:
                 query += """ AND so.status =  %(status)s  """
                 status  = cstr(status)

        if driver:
                query += """ AND so.driver = %(driver)s  """
                driver = cstr(driver)

        query += """ LIMIT %s  """ % (cint(limit))

        data = frappe.db.sql(query, { "city_name": city_name, "delivery_date": delivery_date,  "limit": limit, "status": status, "vehicle": vehicle, "driver": driver }, as_dict=1)

        return data

@frappe.whitelist()
def updt_sales_order(sales_order_id,vehicle,driver):
	data=frappe.get_doc("Sales Order",sales_order_id)
	
	if vehicle!="":
		data.vehicle=vehicle
	if driver!="":
		data.driver=driver

	return data.save()
	#data=frappe.get_doc("Sales Order",sales_order_id)
	#if not data.vehicle:
	#data.vehicle=vehicle
	#if not data.driver:
	#data.driver=driver
	#data = json.loads(doctype)
	#for row in data.message:
	#	return row["driver"]
	
	'''if data["message"]["name"]:
		sales_order_data=frappe.get_doc("Sales Order",data["message"]["name"])
			
		if data["message"]["driver"]:
			 driver = cstr(data["message"]["driver"])
		else:
			 driver = cstr(driver)
			
		if data["message"]["vehicle"]:
			 vehicle = cstr(data["message"]["vehicle"])
		else:
			 vehicle = cstr(vehicle)
				 
		frappe.db.sql("""UPDATE `tabSales Order`  SET `driver` = %s , `vehicle` = %s  where  name = %s """, (driver,vehicle,data["message"]["name"]))
			
		return data["message"]["name"]
	else:
		return ''		
	'''

@frappe.whitelist()
def get_item_details(item_code):
        items = frappe.get_doc("Item", item_code)

        return items

