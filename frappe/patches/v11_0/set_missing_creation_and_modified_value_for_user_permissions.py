import frappe


def execute():
	if frappe.is_oracledb:
		frappe.db.sql(
		f"""UPDATE {frappe.conf.db_name}."tabUser Permission"
		SET "modified"=NOW(), "creation"=NOW()
		WHERE "creation" IS NULL"""
	)
	else:
		frappe.db.sql(
			"""UPDATE `tabUser Permission`
			SET `modified`=NOW(), `creation`=NOW()
			WHERE `creation` IS NULL"""
		)
