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
from erpnext.controllers.sales_and_purchase_return import make_return_doc
# import urllib
# import urllib2

@frappe.whitelist()
def test():
	return "test"


@frappe.whitelist()
def makeReturnReceipt(doc,method):
	make_return_doc("Purchase Receipt",doc)


@frappe.whitelist()
def getItemtaxes(item_code):
	item=frappe.get_doc("Item",item_code)
	return dict(([d.tax_type, d.tax_rate] for d in item.get("taxes")))

@frappe.whitelist()
def validateReference(ref_no,party):
	data=frappe.db.sql("""select mjea.idx,mje.name from `tabMaster Journal Entry` as mje inner join `tabMaster Journal Entry Account` as mjea on mje.name=mjea.parent where mjea.reference_name=%s and mjea.party=%s""",(ref_no,party),as_dict=1)
	#return len(data)
	if len(data)>=1:
		return data[0]
	else:
		return "False"
	
	


	
	
	

