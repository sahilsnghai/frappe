import frappe


def execute():
	frappe.reload_doctype("Translation")
	if frappe.is_oracledb:
		frappe.db.sql(
    		f"""UPDATE {frappe.conf.db_name}."tabTranslation" SET "translated_text" = 'target_name', "source_text" = 'source_name, "contributed" = 0"""
		)
	else:
		frappe.db.sql(
			"UPDATE `tabTranslation` SET `translated_text`=`target_name`, `source_text`=`source_name`, `contributed`=0"
		)
