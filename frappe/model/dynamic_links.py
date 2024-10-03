# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import frappe

# select doctypes that are accessed by the user (not read_only) first, so that the
# the validation message shows the user-facing doctype first.
# For example Journal Entry should be validated before GL Entry (which is an internal doctype)

dynamic_link_queries = [
	"""select `tabDocField`.parent,
		`tabDocType`.read_only, `tabDocType`.in_create,
		`tabDocField`.fieldname, `tabDocField`.options
	from `tabDocField`, `tabDocType`
	where `tabDocField`.fieldtype='Dynamic Link' and
	`tabDocType`.`name`=`tabDocField`.parent and `tabDocType`.is_virtual = 0
	order by `tabDocType`.read_only, `tabDocType`.in_create""",
	"""select `tabCustom Field`.dt as parent,
		`tabDocType`.read_only, `tabDocType`.in_create,
		`tabCustom Field`.fieldname, `tabCustom Field`.options
	from `tabCustom Field`, `tabDocType`
	where `tabCustom Field`.fieldtype='Dynamic Link' and
	`tabDocType`.`name`=`tabCustom Field`.dt
	order by `tabDocType`.read_only, `tabDocType`.in_create""",
]


def get_dynamic_link_map(for_delete=False):
	"""Build a map of all dynamically linked tables. For example,
	        if Note is dynamically linked to ToDo, the function will return
	        `{"Note": ["ToDo"], "Sales Invoice": ["Journal Entry Detail"]}`

	Note: Will not map single doctypes
	"""
	if getattr(frappe.local, "dynamic_link_map", None) is None or frappe.flags.in_test:
		# Build from scratch
		dynamic_link_map = {}
		for df in get_dynamic_links():
			meta = frappe.get_meta(df.parent)
			if meta.issingle:
				# always check in Single DocTypes
				dynamic_link_map.setdefault(meta.name, []).append(df)
			else:
				try:
					if frappe.is_oracledb:
						links = frappe.db.sql_list(
							"""
							select distinct "{options}" from "tab{parent}"
							""".format(**df)
						)
					else:
						links = frappe.db.sql_list(
							"""select distinct `{options}` from `tab{parent}`""".format(**df)
						)
					for doctype in links:
						dynamic_link_map.setdefault(doctype, []).append(df)
				except frappe.db.TableMissingError:
					pass

		frappe.local.dynamic_link_map = dynamic_link_map
	return frappe.local.dynamic_link_map


def get_dynamic_links():
	"""Return list of dynamic link fields as DocField.
	Uses cache if possible"""
	df = []
	if frappe.is_oracledb:
		global dynamic_link_queries
		dynamic_link_queries = [
			f"""select tabDocField."parent",
				tabDocType."read_only", tabDocType."in_create",
				tabDocField."fieldname", tabDocField."options"
			from {frappe.conf.db_name}."tabDocField" tabDocField, {frappe.conf.db_name}."tabDocType" tabDocType
			where tabDocField."fieldtype"='Dynamic Link' and
			tabDocType."name"=tabDocField."parent" and tabDocType."is_virtual" = 0
			order by tabDocType."read_only", tabDocType."in_create"
			""",
			f"""select tabCustom_Field."dt" parent,
				tabDocType."read_only", tabDocType."in_create",
				tabCustom_Field."fieldname", tabCustom_Field."options"
			from {frappe.conf.db_name}."tabCustom Field" tabCustom_Field,{frappe.conf.db_name}."tabDocType" tabDocType
			where tabCustom_Field."fieldtype"='Dynamic Link' and
			tabDocType."name"=tabCustom_Field."dt"
			order by tabDocType."read_only", tabDocType."in_create"
			""",
		]

	for query in dynamic_link_queries:
		df += frappe.db.sql(query, as_dict=True)
	return df
