# ADA Internship Portal — Project Handoff Document

> **Purpose of this file:** Give any developer / AI model complete context to continue building this project without re-asking questions. Read this fully before writing any code.
>
> **Revision 2 — final model locked:** REFERRAL-ONLY entry (no public/open application path exists), Application Progress Tracker confirmed as module M9 in Phase 1. Earlier drafts discussed a two-category design (referred vs open) — that is **abandoned**. Do not implement any public "Apply" button.

---

## 1. Project Overview

**Aeronautical Development Agency (ADA)** — Bangalore (PB No 1718, Vimanapura Post, Bangalore 560017), the organisation that developed the LCA Tejas — currently runs its student internship / summer-training program **fully on paper**:

1. Student downloads forms, fills them by hand.
2. College Principal/HOD signs a recommendation letter on college letterhead.
3. Student **posts** the whole bundle to ADA's address.
4. Admin & HR Dept manually enters it into a receipt register, scrutinises eligibility, forwards to a Study Committee, and the Director (Admin & HR) gives final approval.

**Goal:** Replace this with a web portal where students apply online. The application is **digitised end-to-end from the existing policy letter ADA/ADM/EST/0267/4/S.Trng: 2025 dated 31 Dec 2025** (with Annexures I–IV, the application format, covering letter, college letter, undertaking, and certificate template — the source images are with the project owner).

### The three non-negotiable business rules (confirmed by the project owner)

| # | Rule | Meaning in the product |
|---|------|------------------------|
| 1 | **REFERRAL-ONLY entry (final, locked)** | No student can apply on their own — ever. There is **no public application form or "Apply" button anywhere**. An ADA employee must first create a *sponsorship/referral* in the portal and give the student a unique referral code. Without a valid code, the application form cannot be opened by anyone. The December intake window governs *when* referred students may submit; it is an announcement, not an open application channel. |
| 2 | **College signature is mandatory** | Hybrid model: student uploads the signed/sealed scanned recommendation letter, **and** the system emails the college official (Principal/HOD/TPO) a secure token link to digitally confirm + upload the letter. Both must be present before the application is "submitted". |
| 3 | **Eligibility & quotas are fixed by ADA policy** | See §4. Hard validations, not suggestions. |
| 4 | **Application Progress Tracker (M9)** | Confirmed feature: every student (and their sponsoring employee) sees a live 10-stage status timeline. Spec in §6 M9. Ships in Phase 1. |

---

## 2. Source Documents (policy → feature mapping)

The owner has scans of the official ADA policy. Every artefact below must exist in the portal. **Do not invent new policy; mirror these documents.**

### 2.1 Policy letter (ADA/ADM/EST/0267/4/S.Trng: 2025, 31 Dec 2025)
- ADA offers training to **UG (BE/B.Tech) and PG (ME/M.Tech) engineering students only**.
- **Advertisement is published on the ADA site in December every year** (this becomes our *Intake Window* — in this portal it announces the window to referred applicants; it is NOT an open application channel, see §1 rule 1).
- Recommendation letter must be addressed to **Director (Admin & HR)**.
- A **Study Committee** constituted by Director (Admin & HR) screens applications and recommends students meeting "acceptability metrics".
- **Director (Admin & HR) has absolute discretion** to accept/reject with or without reasons.
- Clause 8: Project/Technology/Corporate Directors allot a **Guide/Mentor** case-to-case; **each Directorate has a fixed student quota (Appendix 'A')**; guide records the work in their APAR.

### 2.2 Eligibility table (exact numbers — use these as constants)

| Category | Programme | Duration | Seats (at any time during the year) | Notes |
|---|---|---|---|---|
| (a) | Project training after 4th/6th semester, BE/B.Tech | 12–20 weeks (max) | **50 students** | Policy says "Open* with preference to children of ADA employees" — **superseded in this portal:** ALL applicants are employee-referred (§1 rule 1), so the preference note is inherently satisfied |
| (b) | Project work ME/M.Tech (3rd–4th semester) | 6–12 months | **25 students** | Same — all applicants employee-referred |

### 2.3 Annexure-I — Instructions for colleges
- **No industrial training, no paid internship, no stipend.** Apprentices Act 1961 does not apply.
- Letter preferred **1 month in advance** of proposed start date.
- ⚠️ Currently says "**hard copy of recommendation letter & resume is mandatory**; sending soft copy may be avoided" — this directly conflicts with digitisation. **Open policy decision — see §9.**
- Recommendation letter must clearly state: (a) student is bonafide, (b) exact duration with dates, (c) Indian citizen, (d) conduct, (e) resume attached with **project topic + synopsis not exceeding 150 words**.
- If a recommended student is irregular/indisciplined → **institute is blacklisted** (no more students from that institute).
- ADA not obliged to offer employment; not liable for injury compensation.
- **100% attendance** required for certificate.

### 2.4 Annexure-II — Instructions for student trainees
- **Police Clearance Certificate (PCC)** + photo ID mandatory on reporting day; **cannot join without it**. PCC must mention period of stay & address.
- Self-arranged accommodation/food/logistics; no financial assistance.
- Terms & conditions acceptance **countersigned by Principal/HOD** at reporting time.
- Training starts on the notified date; **not reporting = registration cancelled, no rescheduling**.
- Working hours 09:00–17:00.
- No internet/LAN access; no mobiles, laptops, USB dongles, or storage media inside ADA.
- Strict confidentiality; publications cleared per ADA procedure; ADA scientist is **co-guide** on the report.
- On completion: surrender all data → get **clearance from guide** → Admin issues certificate.
- **Certificate is standard template, no duplicates re-issued, no ADA references/recommendations in future.**

### 2.5 Application form fields (the online form must replicate these exactly)

Personal: Name · Passport photo (upload) · DOB · Father's name · **Aadhaar No** (see §7 for PII handling) · Gender · Nationality (must be Indian) · Permanent address · Local address · Contact no + alternative no · Email.

Academic: College name, address & contact · Discipline · Branch code · Degree (UG/PG) · **Semester/Year (two rows: current + completed)** · Average CGPA (scale of 10) or percentage of all completed semesters/years · Achievements / awards / professional memberships.

Project: Topic selected for project work + **synopsis ≤ 150 words** · Area of interest.

**Document checklist (tick + upload each):**
1. Reference/recommendation letter issued by Principal/HOD
2. UG/PG marksheet(s) reflecting CGPA/% for all completed semesters/years
3. Copy of latest Aadhaar card
4. Copy of College ID card

Plus: declaration ("information is correct to the best of my knowledge… candidature may be cancelled") with place, date, e-signature.

### 2.6 Covering letter
Student-authored letter to The Director, ADA: subject "Application for Internship", self-intro (final-year B.E., branch, institute, CGPA, area of interest), place/date, email, mobile. **→ Suggestion implemented as feature: auto-generate this PDF from form data so students never write it.**

### 2.7 College recommendation letter (on college letterhead, signed Principal/HOD/TPO with seal)
Ref No + date · addressed to Director ADA · subject: request for internship opportunity · semester/year, bonafide statement + enrollment no · duration From–To (months) · **Student details table** (name, course, college & ID number, mobile, permanent & residential address, Aadhaar no, email) · **Faculty coordinator table** (name, designation, department, affiliation ID, email) · **College details table** (college name, principal name, university + affiliation no, **AICTE permanent code, DTE code**, email, contact, fax) · no-objection + full-tenure assurance paragraphs · signature block.

**→ Feature: the portal pre-fills this letter as a downloadable PDF using the student's entered data; the college prints on letterhead, signs, seals; student uploads the scan; college official also confirms via the token link.**

### 2.8 Undertaking by student (signed at submission; countersigned by Principal/HOD at reporting)
Clauses (a)–(n): 09:00–17:00 hours, 100% attendance, self-arranged logistics, no stipend (Apprentices Act 1961 N/A), no employment obligation, no compensation liability, conduct + no social-media mentions of ADA, access limited to training areas/library/canteen, no internet/LAN/phones/laptops/USB, confidentiality, no IP infringement, demos only on ADA premises with permission, publications cleared per ADA procedure, violation = termination of individual/group work, co-guide indicated on report, report copy submitted to Technology Director, surrender all data on completion, clearance from guide → certificate, standard template only / no duplicates, no recommendations from ADA officials.

**→ Feature: generated as pre-filled PDF; student e-signs (typed name + checkbox declaration) at submission; the countersigned scan is uploaded at reporting day.**

### 2.9 Annexure-IV — Admin & HR responsibilities (→ the HR admin module's exact workflow)
1. Receiving applications + **entry in receipt register** (auto-generated on submission).
2. Attending policy queries (→ FAQ page reduces this).
3. **Scrutiny of eligibility** + reject letters for non-qualifying applications.
4. **Forwarding to the Study Committee** for selection.
5. Letters/emails to colleges after committee recommendation.
6. Reporting day: document check + briefing; letter to **Security Office for Security Pass**.
7. Letter to Security Office with all documents.
8. Receive **monthly attendance sheets** from departments.
9. **Monthly report** preparation.
10. **Issue of certificates** signed by Dir (Admin & HR) per standard template (Appendix V).

### 2.10 Certificate template (Appendix V — organisational letterhead)
"Certificate: This is to certify that the Student Trainee <name & college ID no>, pursuing <degree> at <college/university/city>, has been given the opportunity to work on the topic <title of work report> at/by AERONAUTICAL DEVELOPMENT AGENCY during <dd/mm/yyyy to dd/mm/yyyy>." Signature of **Guide** + **Director (Admin & HR)**. Place: Bengaluru.

**→ Feature: auto-generated PDF on letterhead with a serial number + QR code linking to a public verification page (name, college, topic, period only — no PII).**

---

## 3. Confirmed Product Decisions (owner-answered — do not relitigate)

1. **REFERRAL-ONLY entry (final):** An ADA employee must sponsor the student (referral code required to even open the application form). There is **no public/open application path, no "Apply" button, no preference-points system, no two-category split** — all applicants arrive via referral only. Referred students submit inside the December intake window (50 UG / 25 PG seats).
2. **College signature:** hybrid — scanned signed letter upload + online college endorsement via expiring token link.
3. **Tech stack:** owner has no preference; decision = **Django 5 + PostgreSQL** (rationale in §8).
4. **Hosting:** undecided; design for portability (Docker, no cloud-lock-in), assume PII-sensitive deployment anywhere (ADA intranet / NIC MeghRaj / commercial cloud).
5. **Application Progress Tracker (M9):** confirmed in scope, spec'd in §6, ships in **Phase 1 MVP**.
6. **Auto-generated PDF documents:** covering letter, pre-filled college recommendation letter, undertaking — all generated from form data (students never author these by hand).

---

## 4. Users, Roles & Permissions

| Role | What they can do |
|---|---|
| **Guest (public)** | View advertisement/intake window ("how to get referred by an ADA employee"), policy documents, instructions, FAQ, download blank templates, verify certificate by QR/serial. **No application form is reachable from the public site.** |
| **Student applicant** | Redeem referral code → fill application (multi-step, auto-save) → upload checklist docs → e-sign declaration → download pre-filled college letter & undertaking PDFs → track live status via the M9 progress tracker → receive notifications. |
| **ADA Employee (sponsor)** | Log in with ADA credentials → create sponsorship (student name/email + relationship: e.g. child/ward or professional referral) → system emails referral code → see status of their sponsored applications only. |
| **College official** | Via emailed token link (no account): review the pre-filled data, upload the signed/sealed letter scan, confirm digitally ("This college endorses…"), or flag a data mismatch. |
| **HR Admin (Admin & HR Dept)** | Receipt register dashboard, eligibility scrutiny (auto-check + manual), reject-letter generator, forward to committee, generate selection letters, reporting-day checklist, security-pass letter PDF, attendance reports, monthly report, initiate certificates. |
| **Study Committee member** | Review applications forwarded by HR, see scoring rubric, comment/score, mark recommended / not recommended. |
| **Director (Admin & HR)** | Final approve/reject (with/without reasons), fix/alter training period, approve certificate issuance. |
| **Technology/Project Director** | View directorate quota (Appendix 'A'), allot Guide/Mentor to an approved trainee, approve project topic. |
| **Guide/Mentor (ADA scientist)** | View their trainees, see topic/synopsis, record mid-term notes (optional), give **end-of-training clearance**. |
| **Department coordinator** | Enter/upload monthly attendance per trainee. |
| **System Admin** | User/role management, intake-window configuration, template management, audit log review. |

---

## 5. Application Lifecycle (state machine — implement exactly)

```
DRAFT
  → SPONSOR_PENDING          (student redeemed code; employee must confirm endorsement)
  → COLLEGE_PENDING          (employee confirmed; student uploads docs; college token sent)
  → SUBMITTED                (all uploads + college confirmation + e-signature complete)
  → UNDER_SCRUTINY           (HR; auto eligibility check + manual review)
  → SCRUTINY_REJECTED        (reject letter auto-generated; terminal)
  → IN_COMMITTEE             (HR forwards; committee members score/comment)
  → COMMITTEE_NOT_RECOMMENDED (terminal, or Director override)
  → COMMITTEE_RECOMMENDED
  → DIRECTOR_DECISION
  → DIRECTOR_REJECTED        (terminal; optional reason)
  → APPROVED                 (selection letter generated & emailed to college + student; period fixed by Director)
  → AWAITING_REPORTING       (PCC reminder, reporting date, no-show countdown)
  → NO_SHOW                  (auto after reporting date passes unreported — registration stands cancelled per Annexure-II)
  → REPORTED                 (originals verified: PCC, photo ID, countersigned undertaking; security-pass letter generated)
  → ACTIVE                   (guide assigned by Technology Director; monthly attendance flowing)
  → TERMINATED               (violation/withdrawal — also flags institute if indiscipline per Annexure-I)
  → COMPLETION_PENDING       (guide clearance submitted + report copy received)
  → CERTIFICATE_ISSUED       (PDF, serial no, QR) → CLOSED
```

Rules:
- Every transition is **audit-logged** (who, when, from→to, reason).
- Terminal rejections auto-generate the templated letter (Annexure-IV duty #3).
- Institute indiscipline flag applies a soft-block to future applications from that college (needs HR confirm to enforce).

---

## 6. Feature Modules (build order = phases in §10)

### M1 — Public site
Home, current advertisement (December intake window with open/close dates and live seat counters: 50 UG / 25 PG) — **informational only: it explains "how to get referred by an ADA employee" instead of offering an apply button**. Policy docs & annexures as downloadable PDFs, student & college instructions, FAQ, contact, certificate verification page (QR/serial lookup).

### M2 — Sponsorship (employee module — the ONLY entry door)
Employee login (ADA credentials), create sponsorship → student receives code by email/SMS. Code is single-use, tied to that student's email, expires with the intake window. The application form is **technically unreachable without a valid code** (enforced in database/backend, not by hiding a link). Employee dashboard lists their sponsored applications + statuses (embeds the M9 tracker, read-only). Employee can withdraw endorsement (application returns to DRAFT/invalid). Anti-abuse controls: relationship declaration recorded, per-employee referral cap configurable, employee excluded from any committee review of their own referral.

### M3 — Student application (requires valid referral code)
Multi-step wizard replicating §2.5 exactly; auto-save; validation: nationality Indian, degree/duration rules from §2.2, start date ≥ 1 month ahead, synopsis ≤ 150 words with live counter, CGPA scale check, duplicate detection (DOB + name + college ID), CAPTCHA + rate limiting. Uploads per checklist. Auto-generated PDFs: covering letter, pre-filled college recommendation letter, undertaking. Declaration e-signature. Acknowledgment + application number (e.g. ADA/TRG/2026/00042).

### M4 — College endorsement
Token link (random, 14-day expiry, re-sendable) → college sees pre-filled data → upload signed letter scan → confirm or flag mismatch. Both scan + confirmation required to move out of COLLEGE_PENDING.

### M5 — HR admin module (mirrors Annexure-IV exactly)
Receipt register (auto-entries, exportable), scrutiny queue with side-by-side document viewer, auto-eligibility verdict + manual override, reject-letter generator, forward-to-committee, decision letters, reporting-day checklist (PCC verified, ID verified, countersigned undertaking uploaded) → security-pass letter PDF, monthly attendance consolidation, **monthly report generator**, certificate initiation.

### M6 — Committee module
Queue of forwarded applications, scoring rubric (suggested weights: CGPA/percentage, relevance of branch to aerospace, quality of synopsis/topic, achievements, completeness & timeliness), member comments, recommend / not-recommend with quorum rule (configurable).

### M7 — Training management
Guide allotment against directorate quotas (Appendix 'A' data maintained by Technology Directors), topic approval, monthly attendance entry, guide clearance form, certificate generation (letterhead template, serial, QR) after Director approval.

### M8 — Cross-cutting
Notifications (email at every state change; SMS optional later), full audit log, admin settings (intake windows, quotas, rubric weights, templates, seat counts).

### M9 — Application Progress Tracker (student-facing, CONFIRMED FEATURE)
Public-visible status timeline for every application, driven by the §5 state machine. Detailed spec:

**Visible to the student (public status page + logged-in dashboard, by application number):**

| # | Stage shown to student | Maps to state machine | Shown as |
|---|---|---|---|
| 1 | Sponsored by ADA employee | SPONSOR_PENDING → endorsed | ✅ complete + sponsor name |
| 2 | Application form submitted | SUBMITTED | ✅ complete + application no |
| 3 | College endorsement received | COLLEGE_PENDING → done | ✅ / ⏳ pending with reminder |
| 4 | Eligibility verification (HR) | UNDER_SCRUTINY | ⏳ / ❌ rejected (polite message + letter download) |
| 5 | Committee review | IN_COMMITTEE | ⏳ "under review by selection committee" (no scores/notes shown) |
| 6 | Final decision (Director) | APPROVED / REJECTED | ✅ approved + reporting date / ❌ rejected |
| 7 | Reporting day | AWAITING_REPORTING | ⏳ countdown + document checklist reminder (PCC, ID, undertaking) |
| 8 | Training in progress | ACTIVE | ⏳ + guide name + current attendance summary |
| 9 | Completion & clearance | COMPLETION_PENDING | ⏳ |
| 10 | Certificate issued | CERTIFICATE_ISSUED | ✅ + download button + QR |

**Rules:**
- Internal-only data (committee member names, scores, notes, HR comments, reject reasons beyond the official letter) is NEVER shown to students — only the outward-facing stage label.
- Every stage change also fires an email notification (M8).
- Rejection states show a dignified message + downloadable official letter, never internal reasoning.
- NO_SHOW state shows: "Reporting date passed — registration stands cancelled as per ADA policy."
- AWAITING_REPORTING shows a live countdown and a document checklist (PCC, photo ID, countersigned undertaking) with per-item checkboxes.
- Also embeds a compact version in the sponsoring employee's dashboard (sponsor sees their students' stages, read-only).
- Reduces HR query load (Annexure-IV duty #2); students self-serve instead of calling.

---

## 7. Security, Privacy & Compliance (critical — Aadhaar involved)

- **Aadhaar:** DPDP Act 2023 + UIDAI restrictions. Recommended: collect Aadhaar only as the **uploaded card scan** (encrypted at rest) and store a **masked number (last 4 digits)** in the database for search — never store the full number in plaintext columns, never in URLs, never in emails/PDFs beyond the official forms. Flag for legal sign-off.
- Consent notice + checkbox at submission; data-retention policy (auto-purge/re-anonymise rejected applications after configurable period, e.g. 24 months).
- **Encryption:** TLS everywhere; PII document store encrypted at rest (SSE or field-level); encrypted DB backups.
- **Auth:** email-OTP or password+OTP for students; ADA-credential login (later: SSO) for staff; mandatory 2FA for Director/HR Admin/System Admin; session timeout.
- **Files:** type/size validation, antivirus scan on upload, virus-scan before staff download, signed short-lived download URLs.
- **RBAC enforced server-side** on every endpoint; object-level permission checks (an employee sees only their sponsorships; a committee member only forwarded applications).
- **Immutable audit log** for every state change and document view/download.
- Rate limiting, CAPTCHA, input sanitisation, security headers, dependency scanning.
- Government hosting compliance checklist if deployed on NIC/MeghRaj: **GIGW guidelines**, accessibility (WCAG), bilingual English/Hindi content readiness.

---

## 8. Recommended Tech Stack (decision + rationale)

| Layer | Choice | Why |
|---|---|---|
| Backend | **Django 5 (Python)** | Built-in admin (huge win for HR module MVP), mature auth/RBAC, excellent PDF libs, secure by default — fits a government record-keeping system. |
| Database | **PostgreSQL** | Relational integrity for the state machine, JSONB for form snapshots, full-text search for the register. |
| Frontend | Django templates + **HTMX/Alpine** for interactivity; (optional) a small React island only for the multi-step student wizard if needed | Keeps one codebase, fast to ship, easy for a small team to maintain. |
| PDF generation | **WeasyPrint** (HTML/CSS → PDF) for all letters/undertaking/certificate on letterhead | Templates = the exact Word formats from policy, trivially maintained. |
| File storage | **S3-compatible (MinIO locally / any S3 later)** with server-side encryption | Portable across hosting choices. |
| Async jobs | **Celery + Redis** (emails, PDF rendering, no-show checks, retention purge) | Keeps requests fast; enables scheduled tasks. |
| Email | SMTP (configurable; later NIC/gov mail relay) | Every workflow step notifies. |
| Deploy | **Docker Compose** (web, db, redis, worker, minio) | Runs identically on ADA intranet, NIC cloud, or any PaaS. |
| Observability | Structured logs, health endpoints, automated encrypted backups | Non-negotiable for a records system. |

---

## 9. Open Policy Questions (get written answers from ADA HR before/while building)

1. **Hard-copy mandate:** Annexure-I currently requires *hard copy* of the recommendation letter + resume. Does ADA officially relax this for portal applications, or does the portal supplement the post? (Suggested: portal-first, with an optional "print & post" fallback slip that HR can still register.)
2. **Referral controls:** maximum referrals per employee per year? Who verifies the declared relationship (child/ward vs professional referral)? Confirm the conflict-of-interest rule (sponsor excluded from reviewing their own referral).
3. **Committee composition & quorum:** how many members, and does a recommendation need unanimous/simple-majority?
4. **Appendix 'A' directorate quotas:** who owns and updates this data, and in what format?
5. **Aadhaar storage:** legal sign-off for storing the card scan digitally, or keep Aadhaar offline-only (collected on reporting day)?
6. **Certificate numbering scheme** and whether reprints (not re-issues) on loss are allowed given the "no duplicate" rule.
7. **Sending domain** for official letters/emails (must look legitimate to colleges).
8. **College token recipients:** only Principal/HOD/TPO emails, or also the faculty coordinator named in the letter?
9. **Intake-window timing for referred students:** confirm that referred students must submit inside the December–January window (owner's current position) or allow year-round referral submissions.

---

## 10. Build Phases & Milestones (compressed schedule — hard stop 10 Feb 2027)

**Project window: 16 Nov 2026 – 10 Feb 2027 (~12.5 weeks).** Lower-priority polish (SMS, bilingual, analytics, plagiarism check, waitlist auto-promotion) is explicitly **out of the 10 Feb commitment** — it lives in the post-project backlog.

| Phase | Dates | Scope | Exit criteria |
|---|---|---|---|
| **P0 — Requirements & policy sign-off** | 16–27 Nov 2026 (2 wks) | Answers to §9; collect final Word/PDF versions of every template; repo/CI/Docker setup; DB schema; auth+RBAC; wireframes | Signed-off configuration sheet + running skeleton |
| **P1 — Foundation & MVP** | 30 Nov 2026 – 08 Jan 2027 (5 wks, incl. Christmas buffer) | M1 public site (no apply button), M2 sponsorship (the only door), M3 application + uploads + auto-PDFs, HR receipt register + scrutiny queue, M9 progress tracker | **MILESTONE 1 (08 Jan):** end-to-end demo — sponsorship → application → register → live status timeline |
| **P2 — Selection workflow** | 11–29 Jan 2027 (3 wks) | M4 college endorsement (token links), M5 rejection-letter generator + forward-to-committee, M6 committee scoring, Director decision, selection letters, no-show countdown + PCC reminders | **MILESTONE 2 (29 Jan):** DRAFT→APPROVED purely in-portal |
| **P3 — Training lifecycle (core path)** | 01–05 Feb 2027 (1 wk) | Condensed: reporting checklist (PCC/ID/undertaking), security-pass letter, NO_SHOW auto-cancellation, directorate quotas + guide allotment, monthly attendance | Reporting → guide → attendance path working |
| **P4 — Certificate, hardening & UAT** | 08–10 Feb 2027 (3 days) | Certificate on letterhead (serial + QR) + public verification page; essential hardening (2FA, audit-log UI, backups); UAT walkthrough with HR office | **MILESTONE 3 (10 Feb):** final management demo & UAT sign-off |

**Post-project backlog (after 10 Feb):** SMS/WhatsApp notifications, bilingual content, analytics dashboards, synopsis plagiarism check, waitlist auto-promotion, chatbot/FAQ assistant, monthly-report auto-builder polish, load testing & DR drills.

---

## 11. Key Suggestions Already Baked Into the Design (owner asked for suggestions)

1. **Auto-generated covering letter & pre-filled college letter** — removes the most error-prone manual step.
2. **Certificate QR verification page** — compensates for the strict "no duplicate certificate" rule without breaking policy.
3. **Live seat counters + auto-close** per intake window (50 UG / 25 PG) so HR never over-commits.
4. **No-show auto-cancellation** (Annexure-II rule 6) with reminder emails for PCC — students constantly miss this; it's the biggest reporting-day failure point.
5. **Institute blacklist flag** (Annexure-I rule 7) enforced softly with HR confirmation.
6. **Committee scoring rubric** for consistent, defensible selections.
7. **Postal fallback:** HR screen can manually register a paper application (backward compatible, satisfies the current hard-copy rule until policy changes).
8. **FAQ page + full Application Progress Tracker (M9 — confirmed in scope)** to cut Annexure-IV duty #2 (query handling) dramatically.
9. **Aadhaar minimisation** (§7) — do not become a DPI-bypass horror story.
10. **Everything audit-logged** — Director-level discretion ("with/without reasons") needs a defensible trail.

---

## 12. Glossary

- **ADA** — Aeronautical Development Agency, Bangalore (LCA Tejas design agency, under DRDO/ADA trust).
- **Intake Window** — the yearly advertisement period (December) during which referred students may submit applications.
- **Sponsorship/Referral** — an ADA employee's endorsement that unlocks a student's application. **The only entry path** (final owner decision — no public applications exist).
- **Referral Code** — single-use, email-bound code issued to the student by the sponsoring employee; required to open the application form.
- **Application Progress Tracker (M9)** — student/sponsor-facing 10-stage status timeline driven by the state machine (§5/§6).
- **PCC** — Police Clearance Certificate, mandatory on reporting day.
- **Scrutiny** — HR's eligibility check against §2.2 rules.
- **Study Committee** — screening body constituted by Director (Admin & HR).
- **Appendix 'A'** — per-Directorate student quota table.
- **GIGW** — Guidelines for Indian Government Websites (compliance target if govt-hosted).

---

*End of handoff. When continuing this project: read §1–§5 first, honour §3 decisions, and treat §2 as the single source of truth for all form fields, rules, and document templates.*
