import frappe


def execute():
	frappe.reload_doc("website", "doctype", "web_page_view", force=True)
	site_url = frappe.utils.get_site_url(frappe.local.site)
	if frappe.is_oracledb:
		frappe.db.sql(f"""UPDATE {frappe.conf.db_name}."tabWeb Page View" SET "is_unique" = 1 WHERE "referrer" LIKE '%{site_url}%'""")
	else:
		frappe.db.sql(f"""UPDATE `tabWeb Page View` set is_unique=1 where referrer LIKE '%{site_url}%'""")
