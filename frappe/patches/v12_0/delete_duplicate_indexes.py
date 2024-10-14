import frappe

# This patch deletes all the duplicate indexes created for same column
# The patch only checks for indexes with UNIQUE constraints


def execute():
	if frappe.db.db_type != "mariadb":
		return

	all_tables = frappe.db.get_tables()
	final_deletion_map = frappe._dict()

	for table in all_tables:
		indexes_to_keep_map = frappe._dict()
		indexes_to_delete = []

		if frappe.is_oracledb:
			index_info = frappe.db.sql(
					f"""
					SELECT "INDEX_NAME", "COLUMN_NAME", "TABLE_NAME"
					FROM "ALL_IND_COLUMNS"
					WHERE "TABLE_NAME" = '{table.upper()}'
					AND "COLUMN_POSITION" = 1
					AND "INDEX_OWNER" = '{frappe.conf.db_name.upper()}'
					AND "UNIQUE" = 'Y'
					""",
					as_dict=True,
				)
		else:
			index_info = frappe.db.sql(
				f"""SHOW INDEX FROM `{table}`
					WHERE Seq_in_index = 1
					AND Non_unique=0""",
				as_dict=1,
			)

		for index in index_info:
			if not indexes_to_keep_map.get(index.Column_name):
				indexes_to_keep_map[index.Column_name] = index
			else:
				indexes_to_delete.append(index.Key_name)

		if indexes_to_delete:
			final_deletion_map[table] = indexes_to_delete

	for table_name, index_list in final_deletion_map.items():
		for index in index_list:
			try:
				if is_clustered_index(table_name, index):
					continue
				if frappe.is_oracledb:
					frappe.db.sql_ddl(f"""ALTER TABLE {frappe.conf.db_name}."{table_name}" DROP INDEX "{index}" """)
				else:
					frappe.db.sql_ddl(f"ALTER TABLE `{table_name}` DROP INDEX `{index}`")
			except Exception as e:
				frappe.log_error("Failed to drop index")
				print(f"x Failed to drop index {index} from {table_name}\n {e!s}")
			else:
				print(f"✓ dropped {index} index from {table}")


def is_clustered_index(table, index_name):
	if frappe.is_oracledb:
		return bool(
			frappe.db.sql(
				f"""SELECT * FROM {frappe.conf.db_name}."{table}"
				WHERE "Key_name" = '{index_name}'
					AND "Seq_in_index" = 2 """,
				as_dict=True,
			)
		)
	return bool(
		frappe.db.sql(
			f"""SHOW INDEX FROM `{table}`
			WHERE Key_name = "{index_name}"
				AND Seq_in_index = 2
			""",
			as_dict=True,
		)
	)
