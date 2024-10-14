import frappe


def execute():
	"""
	Remove the doctype "Custom Link" that was used to add Custom Links to the
	Dashboard since this is now managed by Customize Form.
	Update `parent` property to the DocType and delte the doctype
	"""
	frappe.reload_doctype("DocType Link")
	if frappe.db.has_table("Custom Link"):
		for custom_link in frappe.get_all("Custom Link", ["name", "document_type"]):
			if frappe.is_oracledb:
				frappe.db.sql(
			    f"""UPDATE {frappe.conf.db_name}."tabDocType Link" SET "custom" = 1,
				"parent" = '{custom_link.document_type}' WHERE "parent" = '{custom_link.name}'""",
			    (),
			)
			else:
				frappe.db.sql(
					"update `tabDocType Link` set custom=1, parent=%s where parent=%s",
					(custom_link.document_type, custom_link.name),
				)
		frappe.delete_doc("DocType", "Custom Link")
