import frappe


def execute():
	frappe.reload_doc("workflow", "doctype", "workflow_transition")
	if frappe.is_oracledb:
		frappe.db.sql(f'update {frappe.conf.db_name}."tabWorkflow Transition" set "allow_self_approval" = 1')
	else:
		frappe.db.sql("update `tabWorkflow Transition` set allow_self_approval=1")
