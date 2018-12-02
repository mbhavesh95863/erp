from __future__ import unicode_literals
import frappe

from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime,flt
from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
from datetime import datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
from erpnext.controllers.sales_and_purchase_return import make_return_doc
from erpnext.setup.utils import get_exchange_rate


@frappe.whitelist()
def makeJournalEntry(master_doc1,method=None):
	master_doc=json.loads(str(master_doc1))
	for row in master_doc["accounts"]:
		if row["party"]:
			if master_doc["multi_currency"]:
				if int(master_doc["multi_currency"])==1:
					exchange_rate=get_exchange_rate('USD','CAD',row["bill_date"])
					debit_amount=flt(row["debit_in_account_currency"])*flt(exchange_rate)
					hst_amount=flt(flt(row["hst_amount"]))*flt(exchange_rate)
					#frappe.msgprint(str(row["tax_type"]))
					if row["tax_type"]=="No" or row["tax_type"]==None:
						#frappe.msgprint("if"+str(row["party"]))
						exchange_rate=get_exchange_rate('USD','CAD',row["bill_date"])
						debit_amount=flt(row["debit_in_account_currency"])*flt(exchange_rate)	
						doc=frappe.get_doc({
									"docstatus": 0,
									"doctype": "Journal Entry",
									"name": "New Journal Entry 1",
									"owner":frappe.session.user,
									"voucher_type": "Journal Entry",
									"naming_series": "JV-",
									"accounts": [{
										"docstatus": 0,
										"doctype": "Journal Entry Account",
										"name": "New Journal Entry Account 1",
										"owner":frappe.session.user,
										"party_type": "Supplier",
										"tax_type": "No",
										"reference_type": "",
										"parent": "New Journal Entry 1",
										"parentfield": "accounts",
										"parenttype": "Journal Entry",
										"idx": 1,
										"account":master_doc["account"],
										"credit_in_account_currency":row["debit_in_account_currency"],
										"credit": 0,
										"party":str(row["party"])
									}, {
										"docstatus": 0,
										"doctype": "Journal Entry Account",
										"name": "New Journal Entry Account 2",
										"owner": "Administrator",
										"party_type": "",
										"parent": "New Journal Entry 1",
										"parentfield": "accounts",
										"parenttype": "Journal Entry",
										"account": row["expense_account"],
										"party": "",
										"debit": 0,
										"debit_in_account_currency":debit_amount,
									}],
									"posting_date":str(row["bill_date"]),
									"multi_currency":1,
									"master_journal_entry_ref":master_doc["name"],
									"cheque_no":row["reference_name"] if not row["reference_name"]==None else ''
								})
						doc1=doc.insert()
						doc1.submit()
					else:
						#frappe.msgprint("else"+str(row["party"]))
						#hst=(flt(row["debit_in_account_currency"])*13)
						#debit=flt(row["debit_in_account_currency"]+flt(hst)
						#credit=row["debit_in_account_currency"]
						#hst=row["debit_in_account_currency"]*13
						#final_hst=hst/100
						debit=flt(row["debit_in_account_currency"])-flt(row["hst_amount"])
						exchange_rate=get_exchange_rate('USD','CAD',row["bill_date"])
						debit_amount=flt(debit)*flt(exchange_rate)
						hst_amount=flt(flt(row["hst_amount"]))*flt(exchange_rate)

						doc=frappe.get_doc({
									"docstatus": 0,
									"doctype": "Journal Entry",
									"name": "New Journal Entry 1",
									"owner":frappe.session.user,
									"voucher_type": "Journal Entry",
									"naming_series": "JV-",
									"accounts": [{
										"docstatus": 0,
										"doctype": "Journal Entry Account",
										"name": "New Journal Entry Account 1",
										"owner":frappe.session.user,
										"party_type": "Supplier",
										"tax_type": "No",
										"reference_type": "",
										"parent": "New Journal Entry 1",
										"parentfield": "accounts",
										"parenttype": "Journal Entry",
										"idx": 1,
										"account":master_doc["account"],
										"credit_in_account_currency":flt(row["debit_in_account_currency"]),
										"credit": 0,
										"party":str(row["party"])
									}, {
										"docstatus": 0,
										"doctype": "Journal Entry Account",
										"name": "New Journal Entry Account 2",
										"owner": "Administrator",
										"party_type": "Supplier",
										"parent": "New Journal Entry 1",
										"parentfield": "accounts",
										"parenttype": "Journal Entry",
										"account": row["expense_account"],
										"party":"",
										"debit": 0,
										"debit_in_account_currency":flt(debit_amount)
									},
									{
										"docstatus": 0,
										"doctype": "Journal Entry Account",
										"name": "New Journal Entry Account 1",
										"owner":frappe.session.user,
										"tax_type": "No",
										"reference_type": "",
										"parent": "New Journal Entry 1",
										"parentfield": "accounts",
										"parenttype": "Journal Entry",
										"account":master_doc["hst_account"],
										"debit_in_account_currency":flt(hst_amount),
										"credit": 0
									}],
									"posting_date":str(row["bill_date"]),
									"multi_currency":1,
									"master_journal_entry_ref":master_doc["name"],
									"cheque_no":row["reference_name"] if not row["reference_name"]==None else ''
								})
						doc1=doc.insert()
						doc1.submit()
			else:
			

			
				if row["tax_type"]=="No" or row["tax_type"]==None:	
					doc=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Journal Entry",
								"name": "New Journal Entry 1",
								"owner":frappe.session.user,
								"voucher_type": "Journal Entry",
								"naming_series": "JV-",
								"accounts": [{
									"docstatus": 0,
									"doctype": "Journal Entry Account",
									"name": "New Journal Entry Account 1",
									"owner":frappe.session.user,
									"party_type": "Supplier",
									"tax_type": "No",
									"reference_type": "",
									"parent": "New Journal Entry 1",
									"parentfield": "accounts",
									"parenttype": "Journal Entry",
									"idx": 1,
									"account":master_doc["account"],
									"credit_in_account_currency":row["debit_in_account_currency"],
									"credit": 0,
									"party":str(row["party"])
								}, {
									"docstatus": 0,
									"doctype": "Journal Entry Account",
									"name": "New Journal Entry Account 2",
									"owner": "Administrator",
									"party_type": "",
									"parent": "New Journal Entry 1",
									"parentfield": "accounts",
									"parenttype": "Journal Entry",
									"account": row["expense_account"],
									"party": "",
									"debit": 0,
									"debit_in_account_currency":row["debit_in_account_currency"],
								}],
								"posting_date":str(row["bill_date"]),
								"master_journal_entry_ref":master_doc["name"],
								"cheque_no":row["reference_name"] if not row["reference_name"]==None else ''
							})
					doc1=doc.insert()
					doc1.submit()
				else:
					#hst=(flt(row["debit_in_account_currency"])*13)
					#debit=flt(row["debit_in_account_currency"]+flt(hst)
					#credit=row["debit_in_account_currency"]
					#hst=row["debit_in_account_currency"]*13
					#final_hst=hst/100
					debit=flt(row["debit_in_account_currency"])-flt(row["hst_amount"])

					doc=frappe.get_doc({
								"docstatus": 0,
								"doctype": "Journal Entry",
								"name": "New Journal Entry 1",
								"owner":frappe.session.user,
								"voucher_type": "Journal Entry",
								"naming_series": "JV-",
								"accounts": [{
									"docstatus": 0,
									"doctype": "Journal Entry Account",
									"name": "New Journal Entry Account 1",
									"owner":frappe.session.user,
									"party_type": "Supplier",
									"tax_type": "No",
									"reference_type": "",
									"parent": "New Journal Entry 1",
									"parentfield": "accounts",
									"parenttype": "Journal Entry",
									"idx": 1,
									"account":master_doc["account"],
									"credit_in_account_currency":flt(row["debit_in_account_currency"]),
									"credit": 0,
									"party":str(row["party"])
								}, {
									"docstatus": 0,
									"doctype": "Journal Entry Account",
									"name": "New Journal Entry Account 2",
									"owner": "Administrator",
									"party_type": "Supplier",
									"parent": "New Journal Entry 1",
									"parentfield": "accounts",
									"parenttype": "Journal Entry",
									"account": row["expense_account"],
									"party":"",
									"debit": 0,
									"debit_in_account_currency":flt(debit)
								},
								{
									"docstatus": 0,
									"doctype": "Journal Entry Account",
									"name": "New Journal Entry Account 1",
									"owner":frappe.session.user,
									"tax_type": "No",
									"reference_type": "",
									"parent": "New Journal Entry 1",
									"parentfield": "accounts",
									"parenttype": "Journal Entry",
									"account":master_doc["hst_account"],
									"debit_in_account_currency":flt(row["hst_amount"]),
									"credit": 0
								}],
								"posting_date":str(row["bill_date"]),
								"master_journal_entry_ref":master_doc["name"],
								"cheque_no":row["reference_name"] if not row["reference_name"]==None else ''
							})
					doc1=doc.insert()
					doc1.submit()
			



def getAccount(party):
	data=frappe.db.sql("""select account from `tabParty Account` where parent=%s limit 1""",party)
	if data:
		if not data[0][0]:
			return data[0][0]
		else:
			return str()
	else:
		return str()


@frappe.whitelist()
def cancelJournalEntry(doc_name):
	j_entry=frappe.db.sql("""select name from `tabJournal Entry` where master_journal_entry_ref=%s""",doc_name)
	if j_entry:
		for row in j_entry:
			doc=frappe.get_doc("Journal Entry",row[0])
			doc.cancel()
	
