# ADA Internship Portal — Detailed Data Model

> Companion to the project spec. Target database: **PostgreSQL 16**. All primary keys are `uuid` (default `gen_random_uuid()`), all timestamps `timestamptz`, all enums either native PG enums or `text + CHECK`. Table names snake_case, singular concept / plural table.

---

## 1. Design principles

1. **One logical model, two physical databases.** The Intranet database holds the full model. The Internet (DMZ) database holds only a strict subset (§9 channel matrix). Sync tables exist on both sides.
2. **Referral codes are never stored in plaintext.** Only `code_hash = sha256(code + pepper)` and status cross the boundary.
3. **Aadhaar is never stored as a searchable full number.** `aadhaar_masked` (last 4) + encrypted scan in `files`; full number never leaves the document image.
4. **Every state change is written twice:** once in `applications.status` (current state) and once in `application_status_history` (append-only timeline). The tracker reads the history.
5. **Audit is append-only.** No UPDATE/DELETE grants on `audit_logs` for application roles.
6. **Seat quotas are enforced transactionally** (`SELECT … FOR UPDATE` on `intake_windows` / `directorate_quotas`), never by counting rows at render time.
7. **Soft delete via `deleted_at`** only where policy allows; applications and certificates are never hard-deleted (retention policy anonymises instead).

---

## 2. Enumerations

| Enum | Values |
|---|---|
| `role_code` | `STUDENT`, `EMPLOYEE_ADA`, `EMPLOYEE_DRDO`, `HR_ADMIN`, `PORTAL_ADMIN`, `COMMITTEE_MEMBER`, `DIRECTOR_HR`, `TECH_DIRECTOR`, `GUIDE`, `DEPT_COORDINATOR` |
| `org_type` | `ADA`, `DRDO_OTHER` |
| `verification_status` | `PENDING`, `VERIFIED`, `REJECTED` |
| `relationship_type` | `CHILD`, `WARD`, `PROFESSIONAL_REFERRAL` |
| `referral_status` | `PENDING_VERIFICATION`, `ACTIVE`, `REDEEMED`, `EXPIRED`, `REVOKED` |
| `intake_status` | `DRAFT`, `OPEN`, `CLOSED`, `ARCHIVED` |
| `degree_type` | `UG`, `PG` |
| `application_status` | `DRAFT`, `SPONSOR_PENDING`, `COLLEGE_PENDING`, `SUBMITTED`, `UNDER_SCRUTINY`, `SCRUTINY_REJECTED`, `IN_COMMITTEE`, `COMMITTEE_NOT_RECOMMENDED`, `COMMITTEE_RECOMMENDED`, `DIRECTOR_DECISION`, `DIRECTOR_REJECTED`, `APPROVED`, `DIRECTORATE_ASSIGNED`, `AWAITING_REPORTING`, `NO_SHOW`, `REPORTED`, `ACTIVE`, `TERMINATED`, `COMPLETION_PENDING`, `CERTIFICATE_ISSUED`, `CLOSED` |
| `document_type` | `PHOTO`, `AADHAAR`, `COLLEGE_ID`, `MARKSHEET`, `RECOMMENDATION_LETTER`, `RECOMMENDATION_SCAN`, `UNDERTAKING_SIGNED`, `POLICE_CLEARANCE`, `PROJECT_REPORT`, `OTHER` |
| `document_status` | `PENDING`, `VERIFIED`, `REJECTED` |
| `endorsement_status` | `AWAITING`, `CONFIRMED`, `MISMATCH`, `EXPIRED` |
| `scrutiny_verdict` | `ELIGIBLE`, `INELIGIBLE`, `NEEDS_INFO` |
| `committee_recommendation` | `RECOMMEND`, `NOT_RECOMMEND`, `ABSTAIN` |
| `director_decision` | `APPROVED`, `REJECTED` |
| `letter_type` | `SELECTION`, `REJECTION`, `SECURITY_PASS`, `CLEARANCE`, `CERTIFICATE` |
| `sync_direction` | `TO_INTRANET`, `TO_INTERNET` |
| `sync_status` | `PENDING`, `SENT`, `ACKED`, `FAILED`, `DEAD` |
| `notification_status` | `QUEUED`, `SENT`, `FAILED` |
| `channel` | `INTERNET`, `INTRANET` |

---

## 3. Identity & organisation

### 3.1 `users`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| email | citext | UNIQUE NOT NULL (lower-cased) |
| password_hash | text | NULL for SSO/OTP-only users |
| phone | text | NULL allowed |
| role_code | role_code | NOT NULL (primary role) |
| is_active | boolean | DEFAULT true |
| mfa_enabled | boolean | must be true for ADMIN/HR/DIRECTOR roles (app-enforced) |
| email_verified_at | timestamptz | |
| last_login_at | timestamptz | |
| created_at / updated_at | timestamptz | |

Indexes: `(email)`, `(role_code)`.

### 3.2 `employees`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| user_id | uuid | FK → users, UNIQUE |
| employee_no | text | UNIQUE per organisation |
| org_type | org_type | NOT NULL |
| lab_name | text | 'ADA' for ADA staff; lab name for others |
| designation | text | |
| directorate_id | uuid | FK → directorates, NULL for non-ADA |
| verified_status | verification_status | DEFAULT 'PENDING' (ADA staff auto-VERIFIED on import/SSO) |
| verified_by_user_id | uuid | FK → users, NULL |
| verified_at | timestamptz | |
| referral_cap_override | int | NULL; else global cap applies |

### 3.3 `students`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| user_id | uuid | FK → users, UNIQUE |
| full_name | text | NOT NULL |
| date_of_birth | date | NOT NULL |
| father_name | text | |
| gender | text | CHECK in ('M','F','O') |
| nationality | text | DEFAULT 'Indian', CHECK = 'Indian' |
| aadhaar_masked | text | last 4 digits only |
| aadhaar_file_id | uuid | FK → files |
| photo_file_id | uuid | FK → files |
| alt_phone | text | |
| permanent_address | text | |
| local_address | text | |
| created_at / updated_at | timestamptz | |

Duplicate detection index: `(lower(full_name), date_of_birth, college_id)` where an application exists.

### 3.4 `colleges`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| name | text | NOT NULL, UNIQUE |
| address | text | |
| city / state | text | |
| principal_name | text | |
| university_name | text | |
| affiliation_no | text | |
| aicte_code | text | |
| dte_code | text | |
| email | citext | |
| phone | text | |
| fax | text | |
| is_blacklisted | boolean | DEFAULT false (Annexure-I rule 7) |
| blacklist_reason | text | |
| blacklisted_by_user_id | uuid | FK → users |

### 3.5 `faculty_coordinators`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| college_id | uuid | FK → colleges |
| name | text | NOT NULL |
| designation | text | |
| department | text | |
| affiliation_id | text | |
| email | citext | |

---

## 4. Intake windows & referrals (the only entry door)

### 4.1 `intake_windows`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| academic_year | text | e.g. '2026-27' |
| title | text | |
| opens_at / closes_at | timestamptz | CHECK opens_at < closes_at |
| ug_seats | int | DEFAULT 50 |
| pg_seats | int | DEFAULT 25 |
| status | intake_status | DEFAULT 'DRAFT' |
| created_by_user_id | uuid | FK → users |

Seat usage is derived transactionally: `SELECT count(*) FROM applications WHERE intake_window_id = :id AND degree = 'UG' AND status IN (approved-or-later) FOR UPDATE`.

### 4.2 `referrals`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| intake_window_id | uuid | FK → intake_windows |
| employee_id | uuid | FK → employees (sponsor) |
| student_email | citext | NOT NULL (bound at issue; must match redemption) |
| student_name | text | NOT NULL |
| relationship | relationship_type | NOT NULL |
| code_hash | text | UNIQUE NOT NULL — sha256(code + pepper) |
| status | referral_status | DEFAULT 'PENDING_VERIFICATION' for DRDO_OTHER, 'ACTIVE' for ADA |
| expires_at | timestamptz | = intake window close + grace |
| redeemed_at | timestamptz | |
| application_id | uuid | FK → applications, NULL until redeemed |
| created_at | timestamptz | |

Constraints:
- UNIQUE `(student_email, intake_window_id)` WHERE status IN ('ACTIVE','PENDING_VERIFICATION','REDEEMED') — one live referral per student per window.
- App-enforced: active referrals per employee ≤ cap; per lab cap.

### 4.3 `referral_events` (audit trail of issue/redeem/revoke)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| referral_id | uuid | FK → referrals |
| event | text | ISSUED / VERIFIED / REVOKED / REDEEMED / EXPIRED |
| actor_user_id | uuid | FK → users |
| channel | channel | |
| detail | jsonb | |
| created_at | timestamptz | |

---

## 5. Applications & documents

### 5.1 `applications`
| Column | Type | Constraints / notes |
|---|---|---|
| id | uuid | PK |
| application_no | text | UNIQUE NOT NULL (ADA/TRG/2026/00042) |
| intake_window_id | uuid | FK → intake_windows |
| referral_id | uuid | FK → referrals, UNIQUE (one application per referral) |
| student_id | uuid | FK → students |
| college_id | uuid | FK → colleges |
| degree | degree_type | NOT NULL |
| discipline | text | |
| branch_code | text | |
| semester_current / semester_completed | int | |
| year_current / year_completed | text | |
| cgpa | numeric(4,2) | CHECK 0–10 when provided |
| cgpa_scale | numeric(3,1) | DEFAULT 10 |
| percentage | numeric(5,2) | CHECK 0–100 |
| achievements | text | |
| project_topic | text | NOT NULL |
| synopsis | text | NOT NULL, CHECK char_length ≤ 1200 (≈150 words, app-validated) |
| area_of_interest | text | |
| requested_start_date | date | CHECK ≥ CURRENT_DATE + 30 at submission |
| requested_end_date | date | |
| duration_weeks | int | UG: 12–20; PG: 26–52 (app + CHECK) |
| status | application_status | DEFAULT 'DRAFT' |
| status_changed_at | timestamptz | |
| sponsor_employee_id | uuid | FK → employees (snapshot of referral sponsor) |
| sponsor_org_type | org_type | snapshot |
| submitted_at | timestamptz | |
| approved_period_start / approved_period_end | date | set by Director |
| directorate_id | uuid | FK → directorates, NULL until assigned |
| guide_employee_id | uuid | FK → employees, NULL until assigned |
| rejection_reason | text | internal |
| created_at / updated_at | timestamptz | |

Indexes: `(status)`, `(intake_window_id, degree)`, `(college_id)`, `(sponsor_employee_id)`, `(directorate_id)`.

### 5.2 `files` (document store abstraction)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| storage_key | text | UNIQUE; S3/MinIO object key |
| original_name | text | |
| mime_type | text | CHECK in allowed list |
| size_bytes | bigint | CHECK ≤ configured limit |
| sha256 | text | integrity check |
| is_encrypted | boolean | DEFAULT true |
| antivirus_status | text | PENDING / CLEAN / INFECTED |
| uploaded_by_user_id | uuid | FK → users |
| channel | channel | which side received it |
| created_at | timestamptz | |

### 5.3 `application_documents`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications |
| document_type | document_type | NOT NULL |
| file_id | uuid | FK → files |
| status | document_status | DEFAULT 'PENDING' |
| verified_by_user_id | uuid | FK → users |
| verified_at | timestamptz | |
| rejection_note | text | |
| UNIQUE | (application_id, document_type) | one active file per type |

### 5.4 `application_status_history` (tracker source of truth)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications |
| from_status | application_status | NULL for first entry |
| to_status | application_status | NOT NULL |
| actor_user_id | uuid | FK → users, NULL for system |
| reason | text | internal only, never rendered publicly |
| channel | channel | where the transition happened |
| created_at | timestamptz | |

Index: `(application_id, created_at DESC)`.

### 5.5 `college_endorsements`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| token_hash | text | UNIQUE — sha256 of the emailed link token |
| recipient_email | citext | |
| expires_at | timestamptz | 14-day default |
| status | endorsement_status | DEFAULT 'AWAITING' |
| confirmed_at | timestamptz | |
| confirmed_by_name | text | |
| confirmed_by_designation | text | |
| mismatch_note | text | |
| scan_file_id | uuid | FK → files (signed letter scan) |

---

## 6. Scrutiny, committee & decisions

### 6.1 `scrutiny_records`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| auto_checks | jsonb | {nationality:true, duration:true, dates:true, docs_complete:true, duplicate:false} |
| verdict | scrutiny_verdict | |
| reviewer_user_id | uuid | FK → users |
| notes | text | |
| decided_at | timestamptz | |

### 6.2 `committees`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| intake_window_id | uuid | FK → intake_windows, UNIQUE (one committee per cycle, or allow multiple) |
| name | text | |
| quorum_required | int | DEFAULT 3 |
| status | text | FORMING / ACTIVE / CLOSED |
| created_by_user_id | uuid | FK → users (ADMIN) |

### 6.3 `committee_members`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| committee_id | uuid | FK → committees |
| employee_id | uuid | FK → employees |
| member_role | text | CHAIR / MEMBER |
| added_by_user_id | uuid | FK → users |
| is_active | boolean | DEFAULT true |
| UNIQUE | (committee_id, employee_id) | |

### 6.4 `committee_assignments` (which applications each member sees)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| committee_id | uuid | FK → committees |
| application_id | uuid | FK → applications |
| assigned_to_employee_id | uuid | FK → employees, NULL = whole committee |
| assigned_by_user_id | uuid | FK → users |
| assigned_at | timestamptz | |
| UNIQUE | (application_id, assigned_to_employee_id) | |

### 6.5 `committee_reviews`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications |
| committee_member_id | uuid | FK → committee_members |
| scores | jsonb | {cgpa:…, branch:…, synopsis:…, achievements:…} |
| total_score | numeric(5,2) | computed |
| recommendation | committee_recommendation | |
| comments | text | internal |
| reviewed_at | timestamptz | |
| UNIQUE | (application_id, committee_member_id) | |

### 6.6 `director_decisions`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| decision | director_decision | |
| reason | text | optional per policy |
| period_start / period_end | date | |
| decided_by_user_id | uuid | FK → users |
| decided_at | timestamptz | |

### 6.7 `letters`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, NULL for non-application letters |
| letter_type | letter_type | |
| ref_no | text | UNIQUE per type/year |
| file_id | uuid | FK → files |
| issued_by_user_id | uuid | FK → users |
| issued_at | timestamptz | |
| emailed_to | jsonb | array of addresses |
| qr_token | text | UNIQUE, NULL except certificate |

---

## 7. Training lifecycle

### 7.1 `directorates`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| code | text | UNIQUE |
| name | text | |
| head_employee_id | uuid | FK → employees |

### 7.2 `directorate_quotas`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| directorate_id | uuid | FK → directorates |
| academic_year | text | |
| allotted | int | from Appendix 'A' |
| used | int | DEFAULT 0 (incremented transactionally) |
| UNIQUE | (directorate_id, academic_year) | CHECK used ≤ allotted |

### 7.3 `directorate_assignments`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| directorate_id | uuid | FK → directorates |
| academic_year | text | |
| assigned_by_user_id | uuid | FK → users (ADMIN) |
| assigned_at | timestamptz | |

### 7.4 `guide_assignments`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| guide_employee_id | uuid | FK → employees |
| assigned_by_user_id | uuid | FK → users (TECH_DIRECTOR) |
| topic_approved | boolean | DEFAULT false |
| topic_notes | text | |
| assigned_at | timestamptz | |

### 7.5 `reporting_checklists`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| pcc_verified | boolean | DEFAULT false |
| pcc_file_id | uuid | FK → files |
| photo_id_verified | boolean | DEFAULT false |
| undertaking_file_id | uuid | FK → files (countersigned scan) |
| verified_by_user_id | uuid | FK → users |
| reported_at | timestamptz | |

### 7.6 `attendance_months`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications |
| month | char(7) | 'YYYY-MM' |
| working_days | int | |
| days_present | int | CHECK days_present ≤ working_days |
| percentage | numeric(5,2) | generated |
| entered_by_user_id | uuid | FK → users |
| remarks | text | |
| UNIQUE | (application_id, month) | |

### 7.7 `clearances`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| guide_employee_id | uuid | FK → employees |
| report_received | boolean | DEFAULT false |
| data_surrendered | boolean | DEFAULT false |
| remarks | text | |
| cleared_at | timestamptz | |

### 7.8 `certificates`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| serial_no | text | UNIQUE |
| qr_token | text | UNIQUE — random 256-bit; URL-safe |
| pdf_file_id | uuid | FK → files |
| issued_by_user_id | uuid | FK → users (DIRECTOR_HR) |
| issued_at | timestamptz | |
| revoked_at | timestamptz | NULL; policy forbids re-issue, but revocation flag allowed |

Public verification view exposes: full_name, college_name, degree, project_topic, period_start, period_end, serial_no, issued_at, revoked flag. Nothing else.

### 7.9 `security_pass_requests`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, UNIQUE |
| letter_id | uuid | FK → letters |
| status | text | REQUESTED / ISSUED |
| issued_at | timestamptz | |

---

## 8. Admin, config, audit & notifications

### 8.1 `feature_flags`
| Column | Type | Notes |
|---|---|---|
| key | text | PK, e.g. 'channel.internet.enabled' |
| enabled | boolean | DEFAULT true |
| scope | text | GLOBAL / INTERNET / INTRANET |
| description | text | |
| updated_by_user_id | uuid | FK → users |
| updated_at | timestamptz | |

Seeded keys: `channel.internet.enabled`, `channel.intranet.enabled`, `module.referrals.enabled`, `module.referrals.drdo_external`, `module.intake_window`, `module.tracker.public`, `module.committee`, `module.certificates`, `sync.auto`.

### 8.2 `audit_logs` (append-only)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| actor_user_id | uuid | FK → users, NULL for system |
| actor_role | role_code | |
| action | text | e.g. APPLICATION_STATUS_CHANGED |
| entity_type | text | |
| entity_id | uuid | |
| before / after | jsonb | |
| channel | channel | |
| ip_address | inet | |
| created_at | timestamptz | |

Indexes: `(entity_type, entity_id)`, `(created_at)`, `(actor_user_id)`.

### 8.3 `notifications`
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| application_id | uuid | FK → applications, NULL |
| recipient | text | email or phone |
| template_code | text | |
| payload | jsonb | merge fields |
| status | notification_status | DEFAULT 'QUEUED' |
| attempts | int | DEFAULT 0 |
| last_error | text | |
| sent_at | timestamptz | |

### 8.4 `system_settings` (non-flag config)
| Column | Type | Notes |
|---|---|---|
| key | text | PK |
| value | jsonb | e.g. referral caps, rubric weights, retention months |
| updated_by_user_id | uuid | |
| updated_at | timestamptz | |

---

## 9. Dual-channel sync & channel exposure

### 9.1 `sync_outbox` (both databases)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| direction | sync_direction | |
| event_type | text | see §10 |
| entity_type / entity_id | text / uuid | |
| payload | jsonb | minimal, signed |
| idempotency_key | text | UNIQUE |
| status | sync_status | DEFAULT 'PENDING' |
| attempts | int | DEFAULT 0 |
| last_error | text | |
| created_at / processed_at | timestamptz | |

### 9.2 `sync_inbox` (idempotent receive log)
| Column | Type | Notes |
|---|---|---|
| id | uuid | PK |
| idempotency_key | text | UNIQUE |
| source | text | INTERNET / INTRANET |
| checksum | text | payload sha256 |
| received_at | timestamptz | |

### 9.3 Channel exposure matrix

| Table | Internet (DMZ) DB | Intranet DB | Notes |
|---|---|---|---|
| `users` | students only | all roles | staff accounts never in DMZ |
| `students` | ✅ | ✅ | |
| `employees` | ❌ | ✅ | never leaves intranet |
| `referrals` | subset: `code_hash`, `student_email`, `expires_at`, `status` | ✅ full | sponsor identity stays internal |
| `applications` | form fields + `status` | ✅ | internal notes/directorate/guide not in DMZ |
| `files` | uploads only (encrypted) | ✅ | secure transfer, checksum-verified |
| `college_endorsements` | ✅ | ✅ | token link served from internet |
| `scrutiny_records`, `committee_*`, `director_decisions` | ❌ | ✅ | |
| `letters` | certificate + selection letter metadata | ✅ | student-facing docs only |
| `directorates`, `guide_assignments`, `attendance_months`, `clearances` | ❌ | ✅ | |
| `certificates` | public verification subset (view) | ✅ | no internal IDs exposed |
| `feature_flags` | read-only mirror | master | admin edits only on intranet |
| `audit_logs` | channel-local | ✅ master | both log local actions |
| `sync_outbox` / `sync_inbox` | ✅ | ✅ | |

---

## 10. Sync events (cross-boundary contract)

| Event | Direction | Payload (minimum) |
|---|---|---|
| `REFERRAL_ISSUED` | Intranet → Internet | `code_hash`, `student_email`, `expires_at`, `org_type` (no sponsor identity) |
| `REFERRAL_REDEEMED` | Internet → Intranet | `code_hash`, `application_id`, `redeemed_at` |
| `APPLICATION_SUBMITTED` | Internet → Intranet | full form payload (Aadhaar masked; doc file refs) |
| `APPLICATION_UPDATED` | Internet → Intranet | changed fields diff |
| `DOCUMENT_UPLOADED` | Internet → Intranet | `file` ref + `sha256` + doc type |
| `COLLEGE_ENDORSED` | Internet → Intranet | `application_id`, `status`, scan `file` ref |
| `STATUS_CHANGED` | Intranet → Internet | `application_id`, `to_status` (public label only), timestamp |
| `CERTIFICATE_ISSUED` | Intranet → Internet | `serial_no`, `qr_token`, public fields |
| `CERTIFICATE_REVOKED` | Intranet → Internet | `serial_no`, `revoked_at` |

Rules: payload signed (HMAC-SHA256 with rotating key), `idempotency_key` = `event_type:entity_id:version`, retries with backoff, dead-letter after N attempts + Admin alert, checksum logged per batch.

---

## 11. ER overview (primary relationships)

```
users ─1:1─ students ─1:N─ applications ─N:1─ colleges
users ─1:1─ employees ─1:N─ referrals
employees(N:1)─ directorates ─1:N─ directorate_quotas
intake_windows ─1:N─ referrals
intake_windows ─1:N─ applications
referrals ─1:1─ applications
applications ─1:1─ college_endorsements
applications ─1:1─ scrutiny_records
applications ─1:1─ director_decisions
applications ─1:N─ committee_reviews ─N:1─ committee_members ─N:1─ committees
applications ─1:1─ directorate_assignments ─N:1─ directorates
applications ─1:1─ guide_assignments ─N:1─ employees
applications ─1:N─ attendance_months
applications ─1:1─ clearances
applications ─1:1─ certificates
applications ─1:N─ application_status_history
applications ─1:N─ application_documents ─N:1─ files
applications ─1:N─ letters
committees ─1:N─ committee_assignments
```

Key invariants:
- `applications.referral_id` UNIQUE → one application per sponsorship.
- `applications.status = APPROVED` requires `director_decisions.decision = APPROVED`.
- `status ∈ {DIRECTORATE_ASSIGNED, AWAITING_REPORTING, REPORTED, ACTIVE, COMPLETION_PENDING, CERTIFICATE_ISSUED}` requires `directorate_assignments` row.
- `REPORTED` requires `reporting_checklists.pcc_verified = true` and `photo_id_verified = true`.
- `CERTIFICATE_ISSUED` requires `clearances.cleared_at IS NOT NULL` and a certificate row.

---

## 12. Business rules enforced at database/app level

| Rule | Where |
|---|---|
| Indian nationality | CHECK on `students.nationality` |
| UG duration 12–20 weeks; PG 26–52 weeks | CHECK + app validation |
| Start date ≥ submission + 30 days | app validation (server) |
| Synopsis ≤ 150 words | app validation + CHECK on length |
| One application per referral | UNIQUE constraint |
| One live referral per student per window | partial UNIQUE index |
| Referral code single-use | status transition + unique redemption event |
| Seats: 50 UG / 25 PG per window | transactional count under row lock |
| Directorate quota | CHECK `used ≤ allotted` + transactional increment |
| Committee member cannot review own referral | app rule on `committee_reviews` insert |
| Scores/comments never public | column-level permissions + separate DMZ tables |
| Aadhaar full number never stored | schema has only `aadhaar_masked` + encrypted file |
| Rejected applications anonymised after retention period | scheduled job |
| Certificate: serial + QR unique | UNIQUE constraints |

---

## 13. Recommended indexes

```
applications(status)
applications(intake_window_id, degree, status)
applications(college_id)
applications(sponsor_employee_id)
application_status_history(application_id, created_at DESC)
referrals(code_hash) UNIQUE
referrals(student_email, intake_window_id) partial UNIQUE WHERE status IN (...)
committee_reviews(application_id, committee_member_id) UNIQUE
attendance_months(application_id, month) UNIQUE
audit_logs(entity_type, entity_id)
audit_logs(created_at)
sync_outbox(direction, status)
notifications(status)
```

---

## 14. Implementation sequence (build order for the schema)

1. `users`, `roles`(enum), `students`, `employees`, `colleges`, `faculty_coordinators`
2. `intake_windows`, `referrals`, `referral_events`
3. `files`, `applications`, `application_documents`, `application_status_history`
4. `college_endorsements`
5. `scrutiny_records`, `committees`, `committee_members`, `committee_assignments`, `committee_reviews`
6. `director_decisions`, `letters`
7. `directorates`, `directorate_quotas`, `directorate_assignments`, `guide_assignments`
8. `reporting_checklists`, `attendance_months`, `clearances`, `certificates`, `security_pass_requests`
9. `feature_flags`, `system_settings`, `audit_logs`, `notifications`
10. `sync_outbox`, `sync_inbox` + the DMZ subset views

---

## 15. How the internet/intranet process maps to this model

- **Internet DB** is generated from the same migrations but exposes only the ✅ rows of §9.3, via a separate DB role and, ideally, a separate schema (`public` subset) — the staff tables simply do not exist there.
- **Referral redemption** happens entirely in the Internet DB: lookup by `code_hash`, check `status='ACTIVE'` and `expires_at > now()`, bind `student_email`. The full sponsor record stays in the Intranet DB; the DMZ knows only that the code exists and who it belongs to (student email).
- **Application submission** writes `applications` + `files` + `application_documents` in the DMZ, emits `APPLICATION_SUBMITTED` to `sync_outbox`; the intranet worker ingests it into its full model, preserving the same UUIDs so both sides agree.
- **Staff decisions** update the Intranet DB and emit `STATUS_CHANGED`; the DMZ applies only the public label to `applications.status` and appends `application_status_history` — the tracker is therefore accurate without leaking internal reasons.
- **Admin flags** are edited on the Intranet side; a mirror row syncs to the DMZ so the public app can enforce maintenance mode even if the intranet is unreachable.
- **Air-gapped mode:** `sync_outbox` rows are exported as signed JSON bundles (`{events:[…], checksum}`), moved by approved media, imported with `sync_inbox` dedupe — the same code path as online sync, only transport differs.

---

*End of data model.*
