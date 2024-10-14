import re

import frappe


def execute():
	if frappe.is_oracledb:
		fields = frappe.db.sql(
			f"""
			SELECT "COLUMN_NAME", "TABLE_NAME", "DATA_TYPE"
			FROM {frappe.conf.db_name}."USER_TAB_COLUMNS"
			WHERE "DATA_TYPE" IN ('NUMBER', 'FLOAT', 'DECIMAL') AND "NULLABLE" = 'Y'
			""",
			as_dict=1,
		)
	else:
		fields = frappe.db.sql(
			"""
				SELECT COLUMN_NAME , TABLE_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
				WHERE DATA_TYPE IN ('INT', 'FLOAT', 'DECIMAL') AND IS_NULLABLE = 'YES'
			""",
			as_dict=1,
		)

	update_column_table_map = {}

	for field in fields:
		update_column_table_map.setdefault(field.TABLE_NAME, [])

		update_column_table_map[field.TABLE_NAME].append(
			f"`{field.COLUMN_NAME}`=COALESCE(`{field.COLUMN_NAME}`, 0)"
		)

	for table in frappe.db.get_tables():
		if update_column_table_map.get(table) and frappe.db.exists("DocType", re.sub("^tab", "", table)):
			if frappe.is_oracledb:
				frappe.db.sql(
					f""" UPDATE "{table}"
						SET ({', '.join(update_column_table_map.get(table))})
					""",
			)
			else:
				frappe.db.sql(
					"""UPDATE `{table}` SET {columns}""".format(
						table=table, columns=", ".join(update_column_table_map.get(table))
					)
				)
