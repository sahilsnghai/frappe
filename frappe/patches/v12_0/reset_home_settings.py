import frappe


def execute():
	frappe.reload_doc("core", "doctype", "user")
	if frappe.is_oracledb:
		frappe.db.sql(
			"""
			UPDATE "tabUser"
			SET "home_settings" = ''
			WHERE "user_type" = 'System User'
			"""
		)

	else:
		frappe.db.sql(
			"""
			UPDATE `tabUser`
			SET `home_settings` = ''
			WHERE `user_type` = 'System User'
		"""
		)
