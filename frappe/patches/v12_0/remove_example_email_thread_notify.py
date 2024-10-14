import frappe


def execute():
	# remove all example.com email user accounts from notifications
	if frappe.is_oracledb:
		frappe.db.sql(
			f"""
			UPDATE {frappe.conf.db_name}."tabUser"
			SET "thread_notify" = 0, "send_me_a_copy" = 0
			WHERE "email" LIKE '%@example.com'
			"""
		)
	else:
		frappe.db.sql(
			"""UPDATE `tabUser`
		SET thread_notify=0, send_me_a_copy=0
		WHERE email like '%@example.com'"""
		)
