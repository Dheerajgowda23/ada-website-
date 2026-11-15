"""Generate the ADA Internship Portal process-flow & timeline Word document."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ACCENT = RGBColor(0x1F, 0x4E, 0x79)  # dark blue

doc = Document()

# ---------- base styles ----------
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)
for h, size in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5)):
    s = doc.styles[h]
    s.font.name = "Calibri"
    s.font.size = Pt(size)
    s.font.color.rgb = ACCENT
    s.font.bold = True


def para(text, bold=False, size=None, align=None, color=None, space_after=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    if size:
        r.font.size = Pt(size)
    if color:
        r.font.color.rgb = color
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    return p


def bullet(text, bold_prefix=None, level=0):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(2)
    return p


def numbered(text, bold_prefix=None):
    p = doc.add_paragraph(style="List Number")
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
    p.add_run(text)
    p.paragraph_format.space_after = Pt(2)
    return p


def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        r = hdr[i].paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "DCE6F1")
        hdr[i]._tc.get_or_add_tcPr().append(shd)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            r = cells[i].paragraphs[0].add_run(str(val))
            r.font.size = Pt(9.5)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return t


def gantt(items, week_labels, name_w=1.55, col_w=0.44):
    t = doc.add_table(rows=1, cols=len(week_labels) + 1)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    hdr[0].text = ""
    r = hdr[0].paragraphs[0].add_run("Build component")
    r.bold = True
    r.font.size = Pt(8.5)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "DCE6F1")
    hdr[0]._tc.get_or_add_tcPr().append(shd)
    for i, wl in enumerate(week_labels):
        c = hdr[i + 1]
        c.text = ""
        r = c.paragraphs[0].add_run(wl)
        r.bold = True
        r.font.size = Pt(7)
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), "DCE6F1")
        c._tc.get_or_add_tcPr().append(shd)
    for name, weeks in items:
        cells = t.add_row().cells
        cells[0].text = ""
        r = cells[0].paragraphs[0].add_run(name)
        r.font.size = Pt(8.5)
        for i in range(len(week_labels)):
            c = cells[i + 1]
            c.text = ""
            if (i + 1) in weeks:
                shd = OxmlElement("w:shd")
                shd.set(qn("w:fill"), "2E75B6")
                c._tc.get_or_add_tcPr().append(shd)
    for i, w in enumerate([name_w] + [col_w] * len(week_labels)):
        for row in t.rows:
            row.cells[i].width = Inches(w)
    doc.add_paragraph()
    return t


# ================= TITLE PAGE =================
for _ in range(6):
    doc.add_paragraph()
para("AERONAUTICAL DEVELOPMENT AGENCY (ADA)", bold=True, size=20, align=WD_ALIGN_PARAGRAPH.CENTER, color=ACCENT)
para("Internship / Project-Work Training Portal", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Detailed Process Flow & Project Timeline", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_paragraph()
para("Reference policy: ADA/ADM/EST/0267/4/S.Trng: 2025 dated 31 Dec 2025 (with Annexures I–IV)", size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
para("Prepared: 16 November 2026   |   Project window: 16 November 2026 – 10 February 2027", size=10, align=WD_ALIGN_PARAGRAPH.CENTER)
doc.add_page_break()

# ================= 1. OVERVIEW =================
doc.add_heading("1. Project Overview", level=1)
para("ADA currently runs its student internship / summer-training programme entirely on paper: the student "
     "fills forms by hand, the college signs a recommendation letter on letterhead, the bundle is posted to "
     "ADA (PB No 1718, Vimanapura Post, Bangalore 560017), and Admin & HR manually registers, scrutinises "
     "and routes it through the Study Committee and Director (Admin & HR).")
para("This project replaces that with a secure web portal that digitises the entire journey end-to-end, "
     "mirroring the official policy documents exactly.")
doc.add_heading("Non-negotiable business rules", level=2)
bullet("An ADA employee must sponsor the student first and issue a referral code. No public application exists — the "
       "form cannot even be opened without a valid code. (Referral-only entry.)", bold_prefix="Referral-only entry: ")
bullet("The student uploads the signed/sealed college letter AND the college confirms online via a secure expiring "
       "link. Both are required before submission.", bold_prefix="College signature (hybrid): ")
bullet("50 seats for BE/B.Tech (12–20 weeks, after 4th/6th semester) and 25 seats for ME/M.Tech (6–12 months), "
       "Indian citizens only, applied inside the December intake window.", bold_prefix="Fixed eligibility & quotas: ")
bullet("Every student and their sponsoring employee see a live 10-stage status timeline at all times.",
       bold_prefix="Application Progress Tracker: ")

# ================= 2. ACTORS =================
doc.add_heading("2. Actors in the Process", level=1)
table(
    ["Actor", "Role in the process"],
    [
        ["ADA Employee (Sponsor)", "Sponsors a student, generates referral code, endorses the application, tracks progress"],
        ["Student Applicant", "Redeems code, fills application, uploads documents, e-signs, tracks status"],
        ["College (Principal/HOD/TPO)", "Signs & seals recommendation letter; confirms endorsement via secure link"],
        ["Admin & HR Dept", "Receipt register, eligibility scrutiny, rejection letters, forwards to committee, letters, security pass, monthly reports, certificates"],
        ["Study Committee", "Screens and scores applications, recommends candidates"],
        ["Director (Admin & HR)", "Final approve/reject, fixes training period, approves certificates"],
        ["Technology/Project Director", "Allots Guide/Mentor against directorate quotas"],
        ["Guide/Mentor (Scientist)", "Mentors trainee, gives end-of-training clearance"],
        ["Department Coordinator", "Enters monthly attendance of trainees"],
        ["System", "Auto-validates eligibility, auto-generates all letters/certificates, sends notifications, maintains audit log"],
    ],
    widths=[1.9, 4.9],
)

# ================= 3. DETAILED PROCESS FLOW =================
doc.add_heading("3. Detailed Process Flow (Stage by Stage)", level=1)
para("The flow below is the complete to-be process. Each stage lists who acts, what they do, what the system does "
     "automatically, and the output/notification produced.")

stages = [
    ("Stage 0 — Intake Window Announcement (every December)",
     "ADA (public site)",
     ["Publishes the annual advertisement: window open/close dates, seat counters (50 UG / 25 PG), eligibility rules, "
      "and instructions on how to get referred by an ADA employee. Informational only — no public apply button exists."],
     ["Window opens; seat counters go live; referral-code requests become possible."],
     "Public advertisement page + downloadable policy documents"),
    ("Stage 1 — Employee Sponsorship",
     "ADA Employee",
     ["Logs in with ADA credentials; clicks 'Sponsor a Student'; enters student's name, email and relationship "
      "(child/ward/professional referral); confirms endorsement."],
     ["Generates unique single-use referral code (email-bound, expires with window); emails it to student; records "
      "sponsor + relationship on the future application; enforces per-employee referral cap."],
     "Referral code emailed to student; sponsorship recorded"),
    ("Stage 2 — Student Application",
     "Student",
     ["Redeems code (form unreachable without it); fills multi-step form: personal details, photo, Aadhaar, college, "
      "branch, degree UG/PG, semester/year, CGPA/%, achievements, project topic + synopsis (max 150 words), "
      "area of interest; uploads marksheets, Aadhaar copy, college ID; e-signs declaration."],
     ["Auto-validates: Indian nationality, duration 12–20 wks (UG) / 6–12 months (PG), start date ≥ 1 month ahead, "
      "CGPA scale, duplicate detection (DOB+name+college ID), CAPTCHA/rate-limit; auto-saves progress; "
      "auto-generates 3 PDFs: covering letter, pre-filled college recommendation letter, undertaking; "
      "issues application number (e.g. ADA/TRG/2026/00042)."],
     "Draft application + 3 auto-generated PDFs + acknowledgment email"),
    ("Stage 3 — College Endorsement (hybrid)",
     "Student + College",
     ["Student prints the pre-filled letter, obtains Principal/HOD signature & official seal on college letterhead, "
      "uploads the scan. College official receives secure token link (14-day expiry), reviews the data, uploads the "
      "signed letter and clicks 'confirm endorsement' (or flags a data mismatch)."],
     ["Tracks both conditions; blocks progression until scan + online confirmation both exist; sends expiry reminders."],
     "Application moves to SUBMITTED; status updated to student, sponsor and college"),
    ("Stage 4 — Receipt & Acknowledgment",
     "System",
     ["—"],
     ["Creates entry in digital receipt register (date, application no, student, college); triggers notification to HR."],
     "Receipt-register entry (exportable); submission acknowledgment"),
    ("Stage 5 — Eligibility Scrutiny (HR)",
     "Admin & HR",
     ["Reviews application + documents side-by-side; verifies auto eligibility verdict; manual override with reason "
      "if needed; rejects ineligible applications."],
     ["Auto eligibility pre-verdict; on rejection auto-generates official rejection letter; on pass enables "
      "'forward to committee'."],
     "Eligible → committee queue; Ineligible → rejection letter emailed"),
    ("Stage 6 — Committee Selection",
     "Study Committee",
     ["Members review forwarded applications; score on fixed rubric (CGPA, branch relevance, synopsis quality, "
      "achievements); comment; mark Recommended / Not Recommended."],
     ["Ranking, quorum enforcement (configurable); scores hidden from students; conflict-of-interest exclusion "
      "(a sponsor never reviews their own referral)."],
     "Recommended list sent to Director"),
    ("Stage 7 — Director Decision",
     "Director (Admin & HR)",
     ["Approves or rejects (full discretion per policy, with/without reasons); fixes the training period."],
     ["On approval: auto-generates selection letter, emails student + college, sets reporting date; starts no-show "
      "countdown with PCC reminders. On rejection: optional-reason letter."],
     "Selection letter; reporting date; reminder schedule"),
    ("Stage 8 — Reporting Day (in person at ADA)",
     "Student + Admin & HR",
     ["Student reports on the notified date with Police Clearance Certificate, photo ID, undertaking countersigned "
      "by Principal/HOD; HR verifies originals and briefs the student."],
     ["Reporting checklist in portal; auto-generates letter to Security Office for security pass; marks trainee "
      "as REPORTED; if date passes unreported → auto-cancels (NO_SHOW) per policy."],
     "Security-pass letter; trainee activated / registration auto-cancelled"),
    ("Stage 9 — Training Period",
     "Technology Director, Guide, Dept Coordinator",
     ["Technology Director allots Guide/Mentor within directorate quota; guide mentors trainee; department "
      "coordinator records monthly attendance; guide may note progress."],
     ["Quota enforcement (Appendix 'A'); topic approval record; monthly attendance consolidation; attendance "
      "shortfall alerts (100% required for certificate)."],
     "Attendance records; monthly report data"),
    ("Stage 10 — Completion & Certificate",
     "Guide, HR, Director",
     ["Student submits project report copy and surrenders all data/materials; guide gives clearance; HR initiates "
      "certificate; Director approves."],
     ["Auto-generates certificate on ADA letterhead (standard template) with serial number + QR; QR links to public "
      "verification page (name, college, topic, period only)."],
     "Training certificate (PDF) + permanent verification record"),
]
for title, actor, human, system, output in stages:
    doc.add_heading(title, level=2)
    para("Actor: " + actor, bold=True, size=10)
    bullet("Human actions: " + " ".join(human), bold_prefix=None)
    bullet("System automation: " + " ".join(system))
    bullet("Output: " + output)

doc.add_page_break()

# ================= 4. LIFECYCLE =================
doc.add_heading("4. Application Lifecycle (Status States)", level=1)
para("Every application moves through a controlled state machine; every transition is audit-logged (who, when, "
     "from → to, reason). Terminal states are SCRUTINY_REJECTED, COMMITTEE_NOT_RECOMMENDED, DIRECTOR_REJECTED, "
     "NO_SHOW, TERMINATED and CLOSED.")
table(
    ["#", "State", "Meaning"],
    [
        ["1", "DRAFT", "Code redeemed; form being filled"],
        ["2", "SPONSOR_PENDING", "Awaiting employee endorsement confirmation"],
        ["3", "COLLEGE_PENDING", "Awaiting college scan upload + online confirmation"],
        ["4", "SUBMITTED", "Complete; entered in receipt register"],
        ["5", "UNDER_SCRUTINY", "HR eligibility verification"],
        ["6", "SCRUTINY_REJECTED", "Not eligible — rejection letter issued"],
        ["7", "IN_COMMITTEE", "Scoring & recommendation"],
        ["8", "COMMITTEE_RECOMMENDED / NOT_RECOMMENDED", "Committee outcome"],
        ["9", "DIRECTOR_DECISION → APPROVED / DIRECTOR_REJECTED", "Final decision; selection letter"],
        ["10", "AWAITING_REPORTING", "Countdown + PCC reminders"],
        ["11", "NO_SHOW", "Date passed unreported — auto-cancelled"],
        ["12", "REPORTED", "Originals verified; security-pass letter issued"],
        ["13", "ACTIVE", "Guide assigned; attendance flowing"],
        ["14", "TERMINATED", "Violation / withdrawal (may flag institute)"],
        ["15", "COMPLETION_PENDING", "Guide clearance + report copy received"],
        ["16", "CERTIFICATE_ISSUED → CLOSED", "Certificate PDF with serial + QR"],
    ],
    widths=[0.4, 2.5, 3.9],
)

# ================= 5. TIMELINE =================
doc.add_page_break()
doc.add_heading("5. Project Timeline (16 Nov 2026 – 10 Feb 2027)", level=1)
para("Total duration: ~12.5 working weeks, ending 10 February 2027. The schedule is compressed: the training "
     "lifecycle and hardening/UAT are condensed into the final weeks, and lower-priority polish (bilingual "
     "content, SMS, analytics dashboards) is moved to a post-project backlog.")

doc.add_heading("5.1 How the Build Proceeds (construction order)", level=2)
para("The system is built layer by layer — nothing is built before what it depends on. The construction sequence "
     "is: foundation → the applicant's path → the office's path → the training path → finalisation.")
numbered("FOUNDATION (W1–W2): environment, database schema, authentication and role-based access — the skeleton every other component stands on.", bold_prefix="Layer 1 — ")
numbered("APPLICANT PATH (W3–W6): public site → sponsorship/referral door → application wizard → document uploads → auto-generated PDF letters. After this layer, a student's application exists in the system.", bold_prefix="Layer 2 — ")
numbered("OFFICE PATH (W7–W10): HR receipt register & scrutiny → college endorsement → committee scoring → Director decision → selection/rejection letters. After this layer, an application can travel from submission to approval entirely in the portal.", bold_prefix="Layer 3 — ")
numbered("TRAINING PATH (W11): reporting-day verification → security-pass letter → guide allotment → attendance. After this layer, an approved student can physically join and train.", bold_prefix="Layer 4 — ")
numbered("FINALISATION (W12): certificate + QR verification → security hardening → UAT with HR office → management demo. After this layer, the system is handed over.", bold_prefix="Layer 5 — ")
para("Running through every layer: the notification/email engine, the audit log, and the progress tracker — the "
     "tracker is wired to each module as that module is built, so the status timeline grows with the system.", size=9.5)

doc.add_heading("5.2 Build-Process Gantt Chart (component × week)", level=2)
para("Shaded cells = weeks in which that component is under construction. Milestone weeks end with a demo.", size=9.5)
gantt(
    [
        ("Infra: repo, CI, Docker environment", [1, 2]),
        ("Database schema & data models", [1, 2]),
        ("Authentication & roles (RBAC)", [2]),
        ("Public site M1 (advert, FAQ, policy docs)", [3]),
        ("Email/notification engine", [4, 5, 6, 7, 8, 9, 10]),
        ("Sponsorship module M2 (referral codes)", [4]),
        ("Application wizard M3 (form + validations)", [5, 6]),
        ("Document uploads (checklist)", [6]),
        ("PDF engine (covering letter, college letter, undertaking)", [6]),
        ("HR receipt register + scrutiny queue M5", [7]),
        ("Progress tracker M9 (student + sponsor)", [7]),
        ("College endorsement M4 (token links)", [8]),
        ("Committee module M6 (scoring rubric)", [9]),
        ("Rejection-letter generator M5b", [9]),
        ("Director decision + selection letters", [10]),
        ("No-show countdown + PCC reminders", [10]),
        ("Reporting checklist + security-pass letter", [11]),
        ("Guide allotment (quotas) + attendance", [11]),
        ("Certificate + QR verification page", [12]),
        ("Hardening: 2FA, audit-log UI, backups", [12]),
        ("UAT walkthrough + final demo", [12]),
    ],
    ["W1\n16 Nov", "W2\n23 Nov", "W3\n30 Nov", "W4\n07 Dec", "W5\n14 Dec", "W6\n21 Dec",
     "W7\n04 Jan", "W8\n11 Jan", "W9\n18 Jan", "W10\n25 Jan", "W11\n01 Feb", "W12\n08 Feb"],
    name_w=1.9, col_w=0.40,
)
para("★ Demos at the end of W7 (MVP), W10 (selection flow) and W12 (final, 10 Feb). Holiday buffer: 24–27 Dec.", size=9.5)

doc.add_heading("5.3 Weekly Build Progression (what is built, what is testable)", level=2)
table(
    ["Wk", "Dates", "Work planned", "Deliverable of the week"],
    [
        ["W1", "16–20 Nov", "Requirements workshops with HR; collect final Word/PDF of every template (application, letters, undertaking, certificate); get answers to open policy questions (hard-copy rule, referral caps, Aadhaar, email domain)", "Signed-off requirements & configuration sheet"],
        ["W2", "23–27 Nov", "Repository setup, CI, Docker environment; database schema design; auth + roles (employee, student, HR, committee, Director…); UI wireframes approved", "Running skeleton with login/RBAC; approved wireframes"],
        ["W3", "30 Nov–04 Dec", "M1 public site: advertisement page (window dates, seat counters), policy downloads, FAQ, contact — informational only, no apply button", "Public site live in staging"],
        ["W4", "07–11 Dec", "M2 sponsorship: employee login, sponsorship creation, single-use referral codes, referral email; anti-abuse controls (relationship declaration, caps)", "Employee can sponsor and student receives code"],
        ["W5", "14–18 Dec", "M3 student application wizard (part 1): multi-step form, auto-save, all §2.5 fields, validations (eligibility rules, 150-word synopsis, duplicates, CAPTCHA)", "Form fully functional with validations"],
        ["W6", "21–23 Dec + 28–31 Dec", "M3 (part 2): document uploads per checklist; auto-generated PDFs — covering letter, pre-filled college recommendation letter, undertaking; e-signature declaration; application number", "Complete application package + 3 PDFs"],
        ["—", "24–27 Dec", "Holiday buffer (Christmas week)", "—"],
        ["W7", "04–08 Jan", "M5 (part 1): HR receipt register (auto-entries, exportable); scrutiny queue with document viewer + auto eligibility verdict; M9 progress tracker (10-stage student + sponsor timeline)", "MILESTONE 1 — MVP demo: sponsorship → application → register → live tracker"],
        ["W8", "11–15 Jan", "M4 college endorsement: secure token links (14-day expiry, resend), scan upload, online confirmation / mismatch flag; expiry reminders", "College endorsement working end-to-end"],
        ["W9", "18–22 Jan", "M6 committee module: scoring rubric, comments, recommend/not-recommend, quorum; M5 (part 2): rejection-letter generator, forward-to-committee", "Committee review cycle working"],
        ["W10", "25–29 Jan", "Director decision screen (approve/reject with reason); selection-letter generation + emails; period fixing; no-show countdown + PCC reminder scheduling", "MILESTONE 2 — DRAFT → APPROVED purely in-portal"],
        ["W11", "01–05 Feb", "Condensed training lifecycle core: reporting-day checklist (PCC, ID, countersigned undertaking); security-pass letter; NO_SHOW auto-cancellation; directorate quotas + guide allotment; monthly attendance entry", "Reporting → guide → attendance path working"],
        ["W12", "08–10 Feb", "Certificate generation on letterhead (serial + QR) + public verification page; essential hardening (2FA for staff, audit-log UI, backups); UAT walkthrough with HR office; final management demonstration", "MILESTONE 3 — Final demo & UAT sign-off (10 Feb 2027)"],
    ],
    widths=[0.5, 1.2, 3.6, 1.7],
)

doc.add_heading("5.4 Milestones (management check-points)", level=2)
table(
    ["Milestone", "Date", "What management will see"],
    [
        ["M1 — MVP Demo", "08 Jan 2027", "Live demo: employee sponsors → student applies with code → auto-PDFs → application in HR register → student/sponsor see live status timeline"],
        ["M2 — Selection Demo", "29 Jan 2027", "Live demo: college endorses online → committee scores → Director approves → selection letter auto-emailed"],
        ["M3 — Final Demo & UAT Sign-off", "10 Feb 2027", "Live demo: reporting → security pass → guide allotment → attendance → certificate with QR verification; UAT complete"],
    ],
    widths=[1.7, 1.1, 4.0],
)
para("Post-project backlog (not part of the 10 Feb commitment): SMS/WhatsApp notifications, bilingual content, "
     "analytics dashboards, synopsis plagiarism check, waitlist auto-promotion, chatbot/FAQ assistant.", size=9)

# ================= 6. DELIVERABLES =================
doc.add_heading("6. Final Deliverables", level=1)
numbered("Web portal (all modules M1–M9): public site, sponsorship, application wizard, college endorsement, HR admin, committee, training management, notifications/audit, progress tracker")
numbered("All official documents auto-generated as PDFs: covering letter, college recommendation letter (pre-filled), undertaking, selection/rejection letters, security-pass letter, monthly report, certificate with QR")
numbered("Admin configuration: intake windows, seat quotas, scoring rubric weights, templates, referral caps")
numbered("Documentation: user manual (student/employee/HR), admin guide, deployment guide (Docker)")
numbered("Security pack: RBAC matrix, audit log, backup/restore procedure, Aadhaar data-handling note")

# ================= 7. ASSUMPTIONS & DEPENDENCIES =================
doc.add_heading("7. Assumptions & Dependencies", level=1)
bullet("ADA HR provides final versions of all templates and answers to open policy questions during Phase 0 (esp. the hard-copy mandate conflict in Annexure-I).")
bullet("An official email domain/relay for sending letters to students and colleges is available by Phase 2.")
bullet("Employee list (for sponsor login) can be imported or created manually at launch.")
bullet("Directorate quota data (Appendix 'A') is provided by the Technology Directors before Phase 3.")
bullet("Hosting decision (ADA intranet / NIC / cloud) is confirmed by Phase 4; the build is Docker-portable meanwhile.")
bullet("Aadhaar handling (encrypted scan + masked digits) receives legal sign-off during Phase 0–1.")

# ================= 8. RISKS =================
doc.add_heading("8. Risks & Mitigation", level=1)
table(
    ["Risk", "Impact", "Mitigation"],
    [
        ["Compressed schedule (hard stop 10 Feb 2027)", "High", "MVP-first ordering; lower-priority polish (SMS, bilingual, analytics) moved to post-project backlog; holiday buffer already included; weekly milestone tracking"],
        ["Hard-copy mandate (Annexure-I) conflicts with digital-only flow", "High", "Get policy relaxation signed off in P0; until then keep HR 'manual registration' fallback for postal applications"],
        ["Aadhaar storage legal clearance delayed", "High", "Design supports offline-only Aadhaar (collected on reporting day) as fallback"],
        ["Holiday-season slowdown (late Dec / early Jan)", "Medium", "Buffer already included in W6–W7; light workload scheduled for holidays"],
        ["College officials slow to use endorsement links", "Medium", "14-day expiry + reminders + mismatch-flag path; scan upload alone can gate submission if policy permits"],
        ["Email deliverability to colleges", "Low", "Official sending domain confirmed in P0; reminders include portal link fallback"],
    ],
    widths=[2.4, 0.8, 3.6],
)

para("", align=WD_ALIGN_PARAGRAPH.CENTER, size=9)
para("— End of document —", align=WD_ALIGN_PARAGRAPH.CENTER, size=9)

doc.save("ADA_Internship_Portal_Process_Flow_and_Timeline.docx")
print("Saved ADA_Internship_Portal_Process_Flow_and_Timeline.docx")
