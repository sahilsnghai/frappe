"""
    Modify the Integer 10 Digits Value to BigInt 20 Digit value
    to generate long Naming Series

"""
import frappe


def execute():
    if frappe.is_oracledb:
        frappe.db.sql(f'ALTER TABLE {frappe.conf.db_name}."tabSeries" MODIFY current NUMBER(19)')
    else:
	    frappe.db.sql(""" ALTER TABLE `tabSeries` MODIFY current BIGINT """)
