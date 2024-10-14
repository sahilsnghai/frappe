"""
Run this after updating country_info.json and or
"""
import frappe


def execute():
	if frappe.is_oracledb:
		for col in ("field", "doctype"):
			frappe.db.sql_ddl(f'alter table {frappe.conf.db_name}."tabSingles" modify {col} varchar2(255)')
	else:
		for col in ("field", "doctype"):
			frappe.db.sql_ddl(f"alter table `tabSingles` modify column `{col}` varchar(255)")
