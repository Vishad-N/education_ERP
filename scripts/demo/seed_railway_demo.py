"""Idempotent demo-master seed for Railway staging. Uses Desk login, not production data."""

from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from http.client import RemoteDisconnected
from http.cookiejar import CookieJar
from pathlib import Path

BASE = os.environ.get("DEMO_SITE_URL", "https://web-production-7580e.up.railway.app").rstrip("/")
ENV_FILE = Path(__file__).resolve().parents[2] / "secrets" / "railway-education-erp-backend.env"
COMPANY = "T_Educators"


def _env(name: str) -> str:
	for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
		if line.startswith(f"{name}="):
			return line.split("=", 1)[1].strip()
	raise SystemExit(f"Missing {name} in {ENV_FILE}")


class Site:
	def __init__(self, base: str, password: str) -> None:
		self.base = base
		self.jar = CookieJar()
		ctx = ssl._create_unverified_context()
		self.opener = urllib.request.build_opener(
			urllib.request.HTTPSHandler(context=ctx),
			urllib.request.HTTPCookieProcessor(self.jar),
		)
		self.csrf = ""
		self._login(password)

	def _login(self, password: str) -> None:
		payload = self.call("login", {"usr": "Administrator", "pwd": password})
		if payload.get("message") != "Logged In":
			raise SystemExit(f"Login failed: {payload}")
		who = self.call("frappe.auth.get_logged_user", {})
		self.csrf = who.get("csrf_token") or self._cookie("csrf_token") or ""

	def _cookie(self, name: str) -> str:
		for cookie in self.jar:
			if cookie.name == name:
				return cookie.value
		return ""

	def call(self, method: str, data: dict) -> dict:
		body = json.dumps(data).encode("utf-8")
		headers = {"Content-Type": "application/json", "Accept": "application/json"}
		if self.csrf:
			headers["X-Frappe-CSRF-Token"] = self.csrf
		req = urllib.request.Request(f"{self.base}/api/method/{method}", data=body, headers=headers, method="POST")
		last_error: Exception | None = None
		for attempt in range(1, 6):
			try:
				with self.opener.open(req, timeout=120) as resp:
					return json.loads(resp.read().decode("utf-8"))
			except urllib.error.HTTPError as exc:
				detail = exc.read().decode("utf-8", errors="replace")
				raise RuntimeError(f"{method} failed HTTP {exc.code}: {detail[:800]}") from exc
			except (TimeoutError, RemoteDisconnected, urllib.error.URLError) as exc:
				last_error = exc
				print(f"retry {attempt}/5 {method}: {exc}", file=sys.stderr)
		raise RuntimeError(f"{method} failed after retries: {last_error}") from last_error

	def get_list(self, doctype: str, filters: dict, fields: list[str] | None = None) -> list[dict]:
		payload = {
			"doctype": doctype,
			"filters": json.dumps(filters),
			"fields": json.dumps(fields or ["name"]),
			"limit_page_length": 5,
		}
		return self.call("frappe.client.get_list", payload).get("message") or []

	def get_doc(self, doctype: str, name: str) -> dict:
		return self.call("frappe.client.get", {"doctype": doctype, "name": name})["message"]

	def insert(self, doc: dict) -> dict:
		return self.call("frappe.client.insert", {"doc": doc})["message"]

	def submit(self, doc: dict) -> dict:
		return self.call("frappe.client.submit", {"doc": doc})["message"]

	def ensure(self, doctype: str, filters: dict, values: dict) -> str:
		print(f"ensure {doctype} {filters}", flush=True)
		existing = self.get_list(doctype, filters)
		if existing:
			print(f"  exists {existing[0]['name']}", flush=True)
			return existing[0]["name"]
		payload = {"doctype": doctype, **values}
		try:
			created = self.insert(payload)
			print(f"  created {created['name']}", flush=True)
			return created["name"]
		except RuntimeError as exc:
			if "409" not in str(exc) and "DuplicateEntryError" not in str(exc):
				raise
			existing = self.get_list(doctype, filters)
			if existing:
				print(f"  exists after race {existing[0]['name']}", flush=True)
				return existing[0]["name"]
			raise

	def ensure_submitted(self, doctype: str, filters: dict, values: dict) -> str:
		existing = self.get_list(doctype, filters, ["name", "docstatus"])
		if existing:
			name = existing[0]["name"]
			if int(existing[0].get("docstatus") or 0) == 1:
				return name
			doc = self.get_doc(doctype, name)
			self.submit(doc)
			return name
		created = self.insert({"doctype": doctype, **values})
		self.submit(created)
		return created["name"]


def seed(site: Site) -> dict:
	created: dict[str, str] = {}

	created["university"] = site.ensure(
		"Education Institution Node",
		{"institution_code": "DEMO-SCHOOL"},
		{
			"institution_name": "Township High School",
			"institution_code": "DEMO-SCHOOL",
			"node_type": "University",
			"status": "Active",
			"is_group": 1,
			"company": COMPANY,
			"timezone": "Asia/Kolkata",
			"default_currency": "INR",
			"active_from": "2026-04-01",
			"address": "Demo campus for client presentation",
		},
	)
	created["campus"] = site.ensure(
		"Education Institution Node",
		{"institution_code": "DEMO-CAMPUS"},
		{
			"institution_name": "Main Campus",
			"institution_code": "DEMO-CAMPUS",
			"node_type": "Campus",
			"status": "Active",
			"is_group": 1,
			"parent_education_institution_node": created["university"],
			"company": COMPANY,
			"active_from": "2026-04-01",
		},
	)
	created["college"] = site.ensure(
		"Education Institution Node",
		{"institution_code": "DEMO-COLLEGE"},
		{
			"institution_name": "High School",
			"institution_code": "DEMO-COLLEGE",
			"node_type": "College",
			"status": "Active",
			"is_group": 1,
			"parent_education_institution_node": created["campus"],
			"company": COMPANY,
			"active_from": "2026-04-01",
		},
	)
	created["department"] = site.ensure(
		"Education Institution Node",
		{"institution_code": "DEMO-DEPT"},
		{
			"institution_name": "Middle School",
			"institution_code": "DEMO-DEPT",
			"node_type": "Department",
			"status": "Active",
			"is_group": 0,
			"parent_education_institution_node": created["college"],
			"company": COMPANY,
			"active_from": "2026-04-01",
		},
	)
	created["structure"] = site.ensure_submitted(
		"Institution Structure Version",
		{"version_title": "Demo Structure 2026"},
		{
			"version_title": "Demo Structure 2026",
			"root_institution_node": created["university"],
			"effective_from": "2026-04-01",
			"status": "Draft",
			"approved_by": "Administrator",
			"notes": "Client demo hierarchy",
		},
	)
	created["academic_year"] = site.ensure(
		"Academic Year",
		{"academic_year_name": "2026-27"},
		{
			"academic_year_name": "2026-27",
			"year_start_date": "2026-04-01",
			"year_end_date": "2027-03-31",
		},
	)
	created["academic_term"] = site.ensure(
		"Academic Term",
		{"academic_year": created["academic_year"], "term_name": "Term 1"},
		{
			"academic_year": created["academic_year"],
			"term_name": "Term 1",
			"term_start_date": "2026-04-01",
			"term_end_date": "2026-09-30",
		},
	)
	created["session_policy"] = site.ensure_submitted(
		"Academic Session Policy",
		{"academic_year": created["academic_year"]},
		{
			"academic_year": created["academic_year"],
			"admission_open_date": "2026-01-01",
			"admission_close_date": "2026-06-30",
			"status": "Draft",
		},
	)
	created["program"] = site.ensure(
		"Program",
		{"program_name": "Class 6"},
		{"program_name": "Class 6", "program_abbreviation": "C6"},
	)
	created["program_version"] = site.ensure_submitted(
		"Program Version",
		{"program": created["program"], "version_code": "2026"},
		{
			"program": created["program"],
			"version_code": "2026",
			"effective_from": "2026-04-01",
			"minimum_credits": 0,
			"maximum_credits": 40,
			"status": "Draft",
			"description": "Class 6 offering for 2026-27",
		},
	)
	created["offering"] = site.ensure(
		"Program Offering",
		{"offering_code": "DEMO-C6-2026"},
		{
			"offering_code": "DEMO-C6-2026",
			"program_version": created["program_version"],
			"institution_node": created["department"],
			"academic_year": created["academic_year"],
			"academic_term": created["academic_term"],
			"status": "Open",
			"description": "Class 6 admissions 2026-27",
		},
	)
	created["class_offering"] = site.ensure(
		"Class Offering",
		{"class_code": "DEMO-C6-CLASS"},
		{
			"class_code": "DEMO-C6-CLASS",
			"class_name": "Class 6",
			"program_offering": created["offering"],
			"status": "Open",
			"grade_level": 6,
			"max_sections": 2,
		},
	)
	created["section"] = site.ensure(
		"Academic Section",
		{"section_code": "DEMO-C6-A"},
		{
			"section_code": "DEMO-C6-A",
			"section_name": "Section A",
			"class_offering": created["class_offering"],
			"status": "Active",
			"capacity": 2,
		},
	)
	created["category"] = site.ensure(
		"Student Category",
		{"category": "General"},
		{"category": "General"},
	)
	created["intake"] = site.ensure_submitted(
		"Program Intake",
		{"program_offering": created["offering"]},
		{
			"program_offering": created["offering"],
			"status": "Draft",
			"total_capacity": 2,
			"effective_from": "2026-04-01",
			"approved_by": "Administrator",
			"category_intakes": [{"category": created["category"], "capacity": 2, "supernumerary_capacity": 0}],
			"notes": "Two-seat demo intake",
		},
	)
	created["form"] = site.ensure(
		"Admission Application Form Version",
		{"form_code": "DEMO-C6", "version": "2026.1"},
		{
			"form_code": "DEMO-C6",
			"version": "2026.1",
			"status": "Published",
			"program": created["program"],
			"academic_year": created["academic_year"],
			"published_on": "2026-04-01",
			"form_schema": json.dumps(
				{
					"fields": [
						{"fieldname": "guardianName", "fieldtype": "Data", "required": True},
						{"fieldname": "childName", "fieldtype": "Data", "required": True},
						{"fieldname": "mobile", "fieldtype": "Phone", "required": True},
					]
				},
				sort_keys=True,
			),
			"notes": "Published guardian portal form",
		},
	)
	created["eligibility"] = site.ensure(
		"Eligibility Rule Set",
		{"rule_code": "DEMO-C6", "version": "2026.1"},
		{
			"rule_code": "DEMO-C6",
			"version": "2026.1",
			"status": "Published",
			"program": created["program"],
			"academic_year": created["academic_year"],
			"effective_from": "2026-04-01",
			"rules_json": json.dumps({"minimum_score": 40}, sort_keys=True),
			"notes": "Eligible if score is 40 or more",
		},
	)
	created["merit_config"] = site.ensure(
		"Merit Configuration",
		{"configuration_code": "DEMO-MERIT-C6"},
		{
			"configuration_code": "DEMO-MERIT-C6",
			"program": created["program"],
			"academic_year": created["academic_year"],
			"status": "Active",
			"tie_breaker_json": json.dumps(["date_of_birth", "child_name"]),
			"notes": "Higher score ranks first; older child wins ties",
		},
	)
	created["seat_matrix"] = site.ensure(
		"Admission Seat Matrix",
		{"program_offering": created["offering"], "category": created["category"]},
		{
			"program_offering": created["offering"],
			"category": created["category"],
			"capacity": 2,
			"supernumerary_capacity": 0,
			"status": "Locked",
			"locked_on": "2026-04-01 09:00:00",
			"notes": "Two General seats for the live demo",
		},
	)
	created["fee_category"] = site.ensure(
		"Fee Category",
		{"category_name": "Demo Tuition"},
		{"category_name": "Demo Tuition", "description": "Class 6 tuition for the client demo"},
	)
	created["fee_code"] = site.ensure(
		"Education Fee Code",
		{"fee_code": "DEMO-TUITION"},
		{
			"fee_code": "DEMO-TUITION",
			"fee_name": "Class 6 Tuition",
			"fee_category": created["fee_category"],
			"status": "Active",
			"default_amount": 10000,
			"notes": "Annual tuition used in the client demo",
		},
	)
	created["fee_policy"] = site.ensure(
		"Education Fee Policy Version",
		{"policy_code": "DEMO-C6", "version": "2026.1"},
		{
			"policy_code": "DEMO-C6",
			"version": "2026.1",
			"status": "Published",
			"fee_code": created["fee_code"],
			"program": created["program"],
			"academic_year": created["academic_year"],
			"effective_from": "2026-04-01",
			"base_amount": 10000,
			"concession_amount": 0,
			"scholarship_amount": 0,
			"fine_amount": 0,
			"waiver_amount": 0,
			"net_amount": 10000,
			"notes": "Published Class 6 fee policy",
		},
	)
	created["birth_cert"] = site.ensure(
		"Student Document Type",
		{"document_type_code": "BIRTH"},
		{
			"document_type_code": "BIRTH",
			"document_type_name": "Birth certificate",
			"status": "Active",
		},
	)
	created["photo"] = site.ensure(
		"Student Document Type",
		{"document_type_code": "PHOTO"},
		{
			"document_type_code": "PHOTO",
			"document_type_name": "Child photo",
			"status": "Active",
		},
	)
	created["req_birth"] = site.ensure(
		"Document Requirement Matrix",
		{"requirement_code": "DEMO-C6-BIRTH"},
		{
			"requirement_code": "DEMO-C6-BIRTH",
			"document_type": created["birth_cert"],
			"mandatory": 1,
			"status": "Active",
			"program": created["program"],
			"student_category": created["category"],
		},
	)
	created["req_photo"] = site.ensure(
		"Document Requirement Matrix",
		{"requirement_code": "DEMO-C6-PHOTO"},
		{
			"requirement_code": "DEMO-C6-PHOTO",
			"document_type": created["photo"],
			"mandatory": 1,
			"status": "Active",
			"program": created["program"],
			"student_category": created["category"],
		},
	)
	created["notice"] = site.ensure(
		"Student Portal Notice",
		{"title": "Welcome to Township High School"},
		{
			"title": "Welcome to Township High School",
			"message": "Admissions for Class 6 are open. Pay fees only once. Download receipts from this page.",
			"published_on": "2026-04-01",
			"status": "Published",
			"audience": "All Students",
		},
	)
	return created


def main() -> int:
	if not ENV_FILE.exists():
		print(f"Missing {ENV_FILE}", file=sys.stderr)
		return 1
	site = Site(BASE, _env("SITE_ADMIN_PASSWORD"))
	created = seed(site)
	forms = site.call("university_erp.api.portal.get_application_context", {})
	print(json.dumps({"created": created, "published_forms": forms.get("message")}, indent=2))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
