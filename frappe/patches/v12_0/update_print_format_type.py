import frappe


def execute():
	if frappe.is_oracledb:
		frappe.db.sql(
		    f"""UPDATE {frappe.conf.db_name}."tabPrint Format"
		    SET "print_format_type" = 'Jinja'
		    WHERE "print_format_type" IN ('Server', 'Client')"""
		)
		frappe.db.sql(
		    f"""UPDATE {frappe.conf.db_name}."tabPrint Format"
		    SET "print_format_type" = 'JS'
		    WHERE "print_format_type" = 'Js'"""
		)
	else:
		frappe.db.sql(
			"""
			UPDATE `tabPrint Format`
			SET `print_format_type` = 'Jinja'
			WHERE `print_format_type` in ('Server', 'Client')
		"""
		)
		frappe.db.sql(
			"""
			UPDATE `tabPrint Format`
			SET `print_format_type` = 'JS'
			WHERE `print_format_type` = 'Js'
		"""
		)
