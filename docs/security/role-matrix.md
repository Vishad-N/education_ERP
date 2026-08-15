# Baseline Role Matrix

This is the P7.2 starting matrix. Site isolation and institution/campus scope apply to every role; server-side permissions remain authoritative.

| Role | Read | Write/approve | Restricted actions |
|---|---|---|---|
| Applicant/Guardian | Own portal draft, documents, dues and receipts | Own draft and document upload | No staff records, exports, or cross-student access |
| Admissions Officer | Enquiries, applications, documents, eligibility | Scrutiny and non-financial workflow actions | No merit publication, refunds, concessions or role changes |
| Academic Officer | Academic masters, offerings, intake and sections | Approved academic configuration | No financial posting or restricted identity export |
| Finance Officer | Fee demands, invoices, payments and reconciliations | Collection and reconciliation actions | Refunds, write-offs and concessions require approval |
| Registrar | Student identity and lifecycle | Approved correction and enrollment actions | No credential administration or unrestricted exports |
| Institution Administrator | Institution-scoped operations and reports | Approved configuration and user administration | Cannot bypass audit or site isolation |
| System Manager | Technical configuration and operational diagnostics | Infrastructure/app configuration | No routine business approval; all privileged actions audited |

P7.2 follow-up must map these roles to Frappe Role Permission Manager, field permission levels, User Permissions, workflow approvals and negative tests before production readiness.
