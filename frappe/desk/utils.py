# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# License: MIT. See LICENSE

import re

import frappe


def convert_mariadb_to_orcaledb(string, check_alias: bool = False):
	if not frappe.is_oracledb:
		return string
	pattern = '`(?P<alias>\w+( \w+)*)`.`?(?P<column>\w+)`?'
	is_replace = False
	while _match := re.search(pattern=pattern, string=string):
		alias, column = _match.groupdict().values()
		template = '{alias}."{column}"'.format(alias=alias.replace(' ', '_'), column=column)
		string = string.replace(string[_match.start():_match.end()], template)
		is_replace = True

	# Check alias name with underscore (_) symbol
	if check_alias:
		pattern = ' (?P<alias_name>_\w+)$'
		if _match := re.search(pattern=pattern, string=string):
			alias_name = list(_match.groupdict().values())[0]
			string = string.replace(alias_name, '"' + alias_name + '"')

	if is_replace:
		return string

	if re.search('\w+\."\w+"', string):
		return string
	elif re.search('"\w+"', string):
		return string
	return f'"{string}"'


def convert_list(fields: list):
	return [
		convert_mariadb_to_orcaledb(string=string, check_alias=True)
		for string in fields
	]

def convert_order_by(order_by_clause, fields):
	def check_is_alias(column_name):
		return not column_name.startswith("_") and any(col.endswith(column_name)
													   for col in fields['fields'])

	if re.search(' asc$', order_by_clause, re.IGNORECASE):
		col = order_by_clause[:-4]
		if check_is_alias(' ' + col):
			order_by = col + ' asc'
		else:
			order_by = convert_mariadb_to_orcaledb(col) + ' asc'
	elif re.search(' desc$', order_by_clause, re.IGNORECASE):
		col = order_by_clause[:-5]
		if check_is_alias(' ' + col):
			order_by = col + ' desc'
		else:
			order_by = convert_mariadb_to_orcaledb(col) + ' desc'
	else:
		if check_is_alias(' ' + order_by_clause):
			order_by = order_by_clause
		else:
			order_by = convert_mariadb_to_orcaledb(order_by_clause)
	return order_by


def convert_fields(fields: dict):
	fields['fields'] = convert_list(fields['fields'])


	if frappe.is_oracledb:
		if fields.get("order_by"):
			# if multiple orderby pass.
			order_by = [convert_order_by(order_by_clause, fields)
						for order_by_clause in fields.get("order_by").split(",")]
			fields["order_by"] = ", ".join(order_by)
		if fields.get("group_by"):
			fields["group_by"] = ", ".join([convert_mariadb_to_orcaledb(group_by_clause)
											for group_by_clause in fields.get("group_by").split(',')])


def validate_route_conflict(doctype, name):
	"""
	Raises exception if name clashes with routes from other documents for /app routing
	"""

	if frappe.flags.in_migrate:
		return

	all_names = []
	for _doctype in ["Page", "Workspace", "DocType"]:
		all_names.extend(
			[slug(d) for d in frappe.get_all(_doctype, pluck="name") if (doctype != _doctype and d != name)]
		)

	if slug(name) in all_names:
		frappe.msgprint(frappe._("Name already taken, please set a new name"))
		raise frappe.NameError


def slug(name):
	return name.lower().replace(" ", "-")


def pop_csv_params(form_dict):
	"""Pop csv params from form_dict and return them as a dict."""
	from csv import QUOTE_NONNUMERIC

	from frappe.utils.data import cint, cstr

	return {
		"delimiter": cstr(form_dict.pop("csv_delimiter", ","))[0],
		"quoting": cint(form_dict.pop("csv_quoting", QUOTE_NONNUMERIC)),
	}


def get_csv_bytes(data: list[list], csv_params: dict) -> bytes:
	"""Convert data to csv bytes."""
	from csv import writer
	from io import StringIO

	file = StringIO()
	csv_writer = writer(file, **csv_params)
	csv_writer.writerows(data)

	return file.getvalue().encode("utf-8")


def provide_binary_file(filename: str, extension: str, content: bytes) -> None:
	"""Provide a binary file to the client."""
	from frappe import _

	frappe.response["type"] = "binary"
	frappe.response["filecontent"] = content
	frappe.response["filename"] = f"{_(filename)}.{extension}"
