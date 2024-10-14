# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe


def execute():
	"""Enable all the existing Client script"""

	if frappe.is_oracledb:
		frappe.db.sql(
    		f"""UPDATE {frappe.conf.db_name}."tabClient Script" SET "enabled" = 1"""
		)
	else:
		frappe.db.sql(
			"""
			UPDATE `tabClient Script` SET enabled=1
		"""
		)
