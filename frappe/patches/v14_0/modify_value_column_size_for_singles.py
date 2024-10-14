import frappe


def execute():
	if frappe.db.db_type == "mariadb":
		frappe.db.sql_ddl("alter table `tabSingles` modify column `value` longtext")
	elif frappe.is_oracledb:
		frappe.db.sql_ddl(f'ALTER TABLE {frappe.conf.db_name}."tabSingles" MODIFY "value" LONG')
