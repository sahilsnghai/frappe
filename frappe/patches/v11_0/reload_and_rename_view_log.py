import frappe


def execute():
	if frappe.db.table_exists("View log"):
		# for mac users direct renaming would not work since mysql for mac saves table name in lower case
		# so while renaming `tabView log` to `tabView Log` we get "Table 'tabView Log' already exists" error
		# more info https://stackoverflow.com/a/44753093/5955589 ,
		# https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_lower_case_table_names

		if frappe.is_oracledb:
			# Creating a temporary table to store view log data
			frappe.db.sql(f"""CREATE TABLE {frappe.conf.db_name}."ViewLogTemp" AS SELECT * FROM {frappe.conf.db_name}."tabView log" """)

			# Deleting the old View log table
			frappe.db.sql(f'DROP TABLE {frappe.conf.db_name}."tabView log"')
			frappe.delete_doc("DocType", "View log")

			# Reloading the View log DocType to create the new `tabView Log` table
			frappe.reload_doc("core", "doctype", "view_log")

			# Moving the data to the newly created `tabView Log` table
			frappe.db.sql(f'INSERT INTO {frappe.conf.db_name}."tabView Log" SELECT * FROM {frappe.conf.db_name}."ViewLogTemp"')
			frappe.db.commit()

			# Deleting the temporary table
			frappe.db.sql(f'DROP TABLE {frappe.conf.db_name}."ViewLogTemp"')
		else:

			# here we are creating a temp table to store view log data
			frappe.db.sql("CREATE TABLE `ViewLogTemp` AS SELECT * FROM `tabView log`")

			# deleting old View log table
			frappe.db.sql("DROP table `tabView log`")
			frappe.delete_doc("DocType", "View log")

			# reloading view log doctype to create `tabView Log` table
			frappe.reload_doc("core", "doctype", "view_log")

			# Move the data to newly created `tabView Log` table
			frappe.db.sql("INSERT INTO `tabView Log` SELECT * FROM `ViewLogTemp`")
			frappe.db.commit()

			# Delete temporary table
			frappe.db.sql("DROP table `ViewLogTemp`")
	else:
		frappe.reload_doc("core", "doctype", "view_log")
