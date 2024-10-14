import frappe


def execute():
	frappe.reload_doctype("Letter Head")

	# source of all existing letter heads must be HTML
	if frappe.is_oracledb:
		frappe.db.sql(f'''update {frappe.conf.db_name}."tabLetter Head" set "source" = 'HTML' ''')
	else:
		frappe.db.sql("update `tabLetter Head` set source = 'HTML'")
