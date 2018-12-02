# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt
def execute(filters=None):
	columns, data = [], []
	return columns, data

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns(filters)
	item_map = get_item_details()
	pl = get_price_list()

	from erpnext.accounts.utils import get_currency_precision
	precision = get_currency_precision() or 2
	data = []
	for item in sorted(item_map):
		data.append([item, item_map[item]["item_name"],item_map[item]["standard_rate"],
			item_map[item]["stock_uom"],item_map[item]["weight_per_unit"],
			pl.get(item, {}).get("Selling"),
		])

	return columns, data

def get_columns(filters):
	"""return columns based on filters"""

	columns = [_("Item") + ":Link/Item:100", _("Item Name") + ":Link/Item Group:125", _("Description") + "::150", _("UOM") + "::180", _("BOM Rate") + ":Currency:90"]

	return columns

def get_item_details():
	"""returns all items details"""

	item_map = {}

	for i in frappe.db.sql("select name, item_group, item_name, weight_per_unit, standard_rate, stock_uom from tabItem \
		order by item_code, item_group", as_dict=1):
			item_map.setdefault(i.name, i)

	return item_map

def get_price_list():
	"""Get selling & buying price list of every item"""

	rate = {}

	price_list = frappe.db.sql("""select ip.item_code, ip.buying, ip.selling,
		concat(ifnull(cu.symbol,ip.currency), " ", round(ip.price_list_rate,2), " - ", ip.price_list) as price
		from `tabItem Price` ip, `tabPrice List` pl, `tabCurrency` cu
		where ip.price_list=pl.name and pl.currency=cu.name and pl.enabled=1""", as_dict=1)

	for j in price_list:
		if j.price:
			rate.setdefault(j.item_code, {}).setdefault("Buying" if j.buying else "Selling", []).append(j.price)
	item_rate_map = {}

	for item in rate:
		for buying_or_selling in rate[item]:
			item_rate_map.setdefault(item, {}).setdefault(buying_or_selling,
				", ".join(rate[item].get(buying_or_selling, [])))

	return item_rate_map
