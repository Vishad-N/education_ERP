from __future__ import annotations

import frappe


def run_master_proof() -> dict:
	"""Create and validate a synthetic P3.1 institution/academic master chain."""

	university = _ensure_institution_node(
		"P31-UNIV",
		"P3.1 Proof University",
		"University",
		is_group=1,
	)
	campus = _ensure_institution_node(
		"P31-CAMPUS",
		"P3.1 Proof Campus",
		"Campus",
		parent=university,
		is_group=1,
	)
	college = _ensure_institution_node(
		"P31-COLLEGE",
		"P3.1 Proof College",
		"College",
		parent=campus,
		is_group=1,
	)
	department = _ensure_institution_node(
		"P31-DEPT",
		"P3.1 Proof Department",
		"Department",
		parent=college,
		is_group=0,
	)

	structure_version = _ensure_submitted(
		"Institution Structure Version",
		"P31 Structure 2026",
		{
			"version_title": "P31 Structure 2026",
			"root_institution_node": university,
			"effective_from": "2026-04-01",
			"status": "Draft",
		},
	)

	academic_year = _ensure_doc(
		"Academic Year",
		"P31 Academic Year 2026-27",
		{
			"academic_year_name": "P31 Academic Year 2026-27",
			"year_start_date": "2026-04-01",
			"year_end_date": "2027-03-31",
		},
	)
	academic_term = _ensure_doc(
		"Academic Term",
		"P31 Academic Year 2026-27 (Term 1)",
		{
			"academic_year": academic_year,
			"term_name": "Term 1",
			"term_start_date": "2026-04-01",
			"term_end_date": "2026-09-30",
		},
	)
	session_policy = _ensure_submitted(
		"Academic Session Policy",
		"P31 Academic Year 2026-27",
		{
			"academic_year": academic_year,
			"admission_open_date": "2026-01-01",
			"admission_close_date": "2026-03-31",
			"status": "Draft",
		},
	)
	academic_calendar = _ensure_doc(
		"Academic Calendar",
		"P31-CALENDAR-2026",
		{
			"calendar_code": "P31-CALENDAR-2026",
			"academic_year": academic_year,
			"institution_node": department,
			"status": "Published",
			"calendar_days": [
				{
					"calendar_date": "2026-04-01",
					"day_type": "Working",
					"description": "Academic year opens",
				},
				{
					"calendar_date": "2026-08-15",
					"day_type": "Holiday",
					"description": "Independence Day",
				},
			],
		},
	)
	program = _ensure_doc(
		"Program",
		"P31 Proof Program",
		{
			"program_name": "P31 Proof Program",
			"program_abbreviation": "P31",
		},
	)
	program_version = _ensure_submitted(
		"Program Version",
		"PV-P31 Proof Program-2026",
		{
			"program": program,
			"version_code": "2026",
			"effective_from": "2026-04-01",
			"minimum_credits": 0,
			"maximum_credits": 120,
			"status": "Draft",
		},
	)
	course = _ensure_doc(
		"Course",
		"P31 English",
		{
			"course_name": "P31 English",
			"description": "Synthetic P3.1 proof course",
		},
	)
	curriculum_version = _ensure_submitted(
		"Curriculum Version",
		"P31 Curriculum 2026",
		{
			"program_version": program_version,
			"version_code": "CUR-2026",
			"effective_from": "2026-04-01",
			"status": "Draft",
			"curriculum_courses": [
				{
					"course": course,
					"classification": "Core",
					"credits": 4,
					"sequence_number": 1,
				}
			],
		},
	)
	program_offering = _ensure_doc(
		"Program Offering",
		"P31-OFFER-2026",
		{
			"offering_code": "P31-OFFER-2026",
			"program_version": program_version,
			"institution_node": department,
			"academic_year": academic_year,
			"academic_term": academic_term,
			"status": "Open",
		},
	)
	class_offering = _ensure_doc(
		"Class Offering",
		"P31-CLASS-2026",
		{
			"class_code": "P31-CLASS-2026",
			"program_offering": program_offering,
			"class_name": "P3.1 Proof Class",
			"sequence_number": 1,
			"status": "Open",
		},
	)
	section = _ensure_doc(
		"Academic Section",
		"P31-A",
		{
			"section_code": "P31-A",
			"class_offering": class_offering,
			"section_name": "Section A",
			"capacity": 40,
			"status": "Active",
		},
	)
	subject_offering = _ensure_doc(
		"Subject Offering",
		"P31-ENG-2026",
		{
			"subject_offering_code": "P31-ENG-2026",
			"class_offering": class_offering,
			"course": course,
			"academic_term": academic_term,
			"credits": 4,
			"status": "Open",
		},
	)
	instructor = _ensure_instructor()
	faculty_assignment = _ensure_doc(
		"Faculty Assignment",
		"P31-ENG-FAC-2026",
		{
			"assignment_code": "P31-ENG-FAC-2026",
			"subject_offering": subject_offering,
			"instructor": instructor,
			"effective_from": "2026-04-01",
			"weekly_load_hours": 6,
			"status": "Active",
		},
	)
	timetable_slot = _ensure_doc(
		"Timetable Slot",
		"P31-MON-0900",
		{
			"slot_code": "P31-MON-0900",
			"day_of_week": "Monday",
			"start_time": "09:00:00",
			"end_time": "09:45:00",
		},
	)
	timetable_entry = _ensure_doc(
		"Timetable Entry",
		"P31-TT-ENG-001",
		{
			"entry_code": "P31-TT-ENG-001",
			"subject_offering": subject_offering,
			"academic_section": section,
			"timetable_slot": timetable_slot,
			"instructor": instructor,
			"room": "P31-R1",
			"status": "Scheduled",
		},
	)
	timetable_conflict_rejected = _assert_timetable_conflict(
		subject_offering,
		section,
		timetable_slot,
		instructor,
	)
	audit_versions = _ensure_audit_version("Academic Section", section)
	category = _ensure_doc(
		"Student Category",
		"P31 General",
		{
			"category": "P31 General",
		},
	)
	program_intake = _ensure_submitted(
		"Program Intake",
		"P31-OFFER-2026",
		{
			"program_offering": program_offering,
			"total_capacity": 40,
			"effective_from": "2026-04-01",
			"status": "Draft",
			"category_intakes": [
				{
					"category": category,
					"capacity": 40,
					"reservation_percent": 100,
				}
			],
		},
	)

	result = {
		"doctype_count": _count_p31_doctypes(),
		"permission_count": _count_required_permissions(),
		"institution_nodes": [university, campus, college, department],
		"structure_version": structure_version,
		"academic_year": academic_year,
		"academic_term": academic_term,
		"session_policy": session_policy,
		"academic_calendar": academic_calendar,
		"program": program,
		"program_version": program_version,
		"course": course,
		"curriculum_version": curriculum_version,
		"program_offering": program_offering,
		"class_offering": class_offering,
		"section": section,
		"subject_offering": subject_offering,
		"instructor": instructor,
		"faculty_assignment": faculty_assignment,
		"timetable_slot": timetable_slot,
		"timetable_entry": timetable_entry,
		"timetable_conflict_rejected": timetable_conflict_rejected,
		"audit_versions": audit_versions,
		"student_category": category,
		"program_intake": program_intake,
	}
	_assert_master_result(result)
	frappe.db.commit()
	return result


def _ensure_institution_node(
	code: str,
	name: str,
	node_type: str,
	parent: str | None = None,
	is_group: int = 0,
) -> str:
	if frappe.db.exists("Education Institution Node", code):
		return code

	doc = frappe.get_doc(
		{
			"doctype": "Education Institution Node",
			"institution_code": code,
			"institution_name": name,
			"node_type": node_type,
			"parent_education_institution_node": parent,
			"is_group": is_group,
			"status": "Active",
			"active_from": "2026-04-01",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_doc(doctype: str, name: str, values: dict) -> str:
	if frappe.db.exists(doctype, name):
		return name

	doc = frappe.get_doc({"doctype": doctype, **values})
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_instructor() -> str:
	settings = frappe.get_single("Education Settings")
	if settings.instructor_created_by != "Full Name":
		settings.instructor_created_by = "Full Name"
		settings.save(ignore_permissions=True)

	if instructor := frappe.db.exists("Instructor", {"instructor_name": "P31 Proof Instructor"}):
		return instructor

	doc = frappe.get_doc(
		{
			"doctype": "Instructor",
			"instructor_name": "P31 Proof Instructor",
			"status": "Active",
		}
	)
	doc.insert(ignore_permissions=True)
	return doc.name


def _ensure_submitted(doctype: str, name: str, values: dict) -> str:
	if existing := _find_submitted_candidate(doctype, name, values):
		doc = frappe.get_doc(doctype, existing)
	else:
		doc = frappe.get_doc({"doctype": doctype, **values})
		doc.insert(ignore_permissions=True)

	if doc.docstatus == 0:
		doc.submit()
	return doc.name


def _find_submitted_candidate(doctype: str, name: str, values: dict) -> str | None:
	if frappe.db.exists(doctype, name):
		return name

	key_fields = {
		"Academic Session Policy": {"academic_year": values.get("academic_year")},
		"Curriculum Version": {
			"program_version": values.get("program_version"),
			"version_code": values.get("version_code"),
		},
		"Institution Structure Version": {"version_title": values.get("version_title")},
		"Program Version": {
			"program": values.get("program"),
			"version_code": values.get("version_code"),
		},
		"Program Intake": {"program_offering": values.get("program_offering")},
	}
	filters = {key: value for key, value in key_fields.get(doctype, {}).items() if value}
	if not filters:
		return None
	return frappe.db.exists(doctype, filters)


def _assert_timetable_conflict(subject_offering, section, slot, instructor) -> bool:
	try:
		frappe.get_doc(
			{
				"doctype": "Timetable Entry",
				"entry_code": "P31-TT-CONFLICT",
				"subject_offering": subject_offering,
				"academic_section": section,
				"timetable_slot": slot,
				"instructor": instructor,
				"room": "P31-R2",
				"status": "Scheduled",
			}
		).insert(ignore_permissions=True)
	except frappe.ValidationError:
		frappe.clear_messages()
		return True
	return False


def _ensure_audit_version(doctype: str, name: str) -> int:
	doc = frappe.get_doc(doctype, name)
	original_status = doc.status
	doc.status = "Inactive"
	doc.save(ignore_permissions=True)
	doc.status = original_status
	doc.save(ignore_permissions=True)
	return frappe.db.count("Version", {"ref_doctype": doctype, "docname": name})


def _count_p31_doctypes() -> int:
	doctypes = [
		"Academic Calendar",
		"Academic Calendar Day",
		"Academic Section",
		"Academic Session Policy",
		"Category Intake",
		"Class Offering",
		"Curriculum Course",
		"Curriculum Version",
		"Education Institution Node",
		"Faculty Assignment",
		"Institution Structure Version",
		"Program Intake",
		"Program Offering",
		"Program Version",
		"Subject Offering",
		"Timetable Entry",
		"Timetable Slot",
	]
	return frappe.db.count(
		"DocType",
		{
			"module": "University ERP",
			"name": ["in", doctypes],
		},
	)


def _count_required_permissions() -> int:
	doctypes = [
		"Academic Calendar",
		"Academic Section",
		"Academic Session Policy",
		"Class Offering",
		"Curriculum Version",
		"Education Institution Node",
		"Faculty Assignment",
		"Institution Structure Version",
		"Program Intake",
		"Program Offering",
		"Program Version",
		"Subject Offering",
		"Timetable Entry",
		"Timetable Slot",
	]
	return frappe.db.count(
		"DocPerm",
		{
			"parent": ["in", doctypes],
			"role": ["in", ["System Manager", "Academics User"]],
			"read": 1,
		},
	)


def _assert_master_result(result: dict) -> None:
	if result["doctype_count"] != 17:
		frappe.throw("P3.1 proof failed: expected seventeen custom master DocTypes.")

	if result["permission_count"] < 28:
		frappe.throw("P3.1 proof failed: expected System Manager and Academics User permissions.")

	if len(result["institution_nodes"]) != 4:
		frappe.throw("P3.1 proof failed: expected four institution hierarchy nodes.")

	if frappe.db.get_value("Program Version", result["program_version"], "status") != "Published":
		frappe.throw("P3.1 proof failed: Program Version was not published on submit.")

	if frappe.db.get_value("Academic Session Policy", result["session_policy"], "status") != "Published":
		frappe.throw("P3.1 proof failed: Academic Session Policy was not published on submit.")

	if frappe.db.get_value("Institution Structure Version", result["structure_version"], "status") != "Published":
		frappe.throw("P3.1 proof failed: Institution Structure Version was not published on submit.")

	if frappe.db.get_value("Curriculum Version", result["curriculum_version"], "total_credits") != 4:
		frappe.throw("P3.1 proof failed: Curriculum Version total credits did not calculate.")

	if frappe.db.get_value("Program Intake", result["program_intake"], "status") != "Approved":
		frappe.throw("P3.1 proof failed: Program Intake was not approved on submit.")

	capacity = frappe.db.get_value("Academic Section", result["section"], "capacity")
	if capacity != 40:
		frappe.throw("P3.1 proof failed: section capacity did not persist.")

	if not result["timetable_conflict_rejected"]:
		frappe.throw("P3.1 proof failed: timetable conflict was not rejected.")

	if result["audit_versions"] < 1:
		frappe.throw("P3.1 proof failed: expected audit Version evidence for Academic Section.")
