import frappe


def execute():
	if frappe.is_oracledb:
		frappe.db.sql(
			f"""
			UPDATE {frappe.conf.db_name}."tabFile"
			SET "folder" = 'Home/Attachments'
			WHERE NVL("attached_to_doctype", '') != ''
			AND "folder" = 'Home'
			"""
		)
	else:
		frappe.db.sql(
		"""
			UPDATE tabFile
			SET folder = 'Home/Attachments'
			WHERE ifnull(attached_to_doctype, '') != ''
			AND folder = 'Home'
		"""
		)
