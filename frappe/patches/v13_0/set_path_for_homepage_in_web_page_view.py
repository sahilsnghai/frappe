import frappe


def execute():
	frappe.reload_doc("website", "doctype", "web_page_view", force=True)
	if frappe.is_oracledb:
		frappe.db.sql(f"""UPDATE {frappe.conf.db_name}."tabWeb Page View" SET "path" = '/' WHERE "path" = ''""")
	else:
		frappe.db.sql("""UPDATE `tabWeb Page View` set path='/' where path=''""")
