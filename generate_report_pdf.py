"""Generate the ADA Internship Portal process-flow & timeline PDF (mirrors the docx content)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)

ACCENT = colors.HexColor("#1F4E79")
HDR_BG = colors.HexColor("#DCE6F1")
BAR = colors.HexColor("#2E75B6")

S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=19, leading=24, alignment=TA_CENTER, textColor=ACCENT),
    "subtitle": ParagraphStyle("subtitle", fontName="Helvetica-Bold", fontSize=14, leading=18, alignment=TA_CENTER),
    "small_center": ParagraphStyle("small_center", fontName="Helvetica", fontSize=9, leading=12, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=ACCENT, spaceBefore=14, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=ACCENT, spaceBefore=10, spaceAfter=4),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.5, leading=13, leftIndent=14, bulletIndent=4, spaceAfter=2),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8, leading=10),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=8, leading=10),
    "tiny": ParagraphStyle("tiny", fontName="Helvetica", fontSize=7.5, leading=9, alignment=TA_CENTER),
}


def P(text, style="body"):
    return Paragraph(text, S[style])


def bullets(items, style="body"):
    return [Paragraph(t, S[style], bulletText="\u2022") for t in items]


def make_table(headers, rows, widths, font=8):
    st = S["cell"] if font == 8 else ParagraphStyle("c2", parent=S["cell"], fontSize=font, leading=font + 2)
    data = [[Paragraph(h, S["cellb"]) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(v), st) for v in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HDR_BG),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def gantt(items, week_labels, name_w=185, col_w=25.5):
    data = [[Paragraph("<b>Build component</b>", S["cellb"])] + [Paragraph(w.replace("\n", "<br/>"), S["tiny"]) for w in week_labels]]
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HDR_BG),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]
    for r, (name, weeks) in enumerate(items, start=1):
        row = [Paragraph(name, S["cell"])]
        for i in range(1, len(week_labels) + 1):
            row.append(Paragraph("", S["cell"]))
            if i in weeks:
                style.append(("BACKGROUND", (i, r), (i, r), BAR))
        data.append(row)
    t = Table(data, colWidths=[name_w] + [col_w] * len(week_labels), repeatRows=1)
    t.setStyle(TableStyle(style))
    return t


doc = SimpleDocTemplate("ADA_Internship_Portal_Process_Flow_and_Timeline.pdf",
                        pagesize=A4, topMargin=1.5 * cm, bottomMargin=1.5 * cm,
                        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                        title="ADA Internship Portal - Detailed Process Flow & Project Timeline")
E = []

# ---------------- TITLE ----------------
E += [Spacer(1, 160)]
E.append(P("AERONAUTICAL DEVELOPMENT AGENCY (ADA)", "title"))
E.append(Spacer(1, 8))
E.append(P("Internship / Project-Work Training Portal", "subtitle"))
E.append(Spacer(1, 4))
E.append(P("Detailed Process Flow &amp; Project Timeline", "subtitle"))
E.append(Spacer(1, 30))
E.append(P("Reference policy: ADA/ADM/EST/0267/4/S.Trng: 2025 dated 31 Dec 2025 (with Annexures I-IV)", "small_center"))
E.append(P("Prepared: 16 November 2026 &nbsp;|&nbsp; Project window: 16 November 2026 - 10 February 2027", "small_center"))
E.append(PageBreak())

# ---------------- 1. OVERVIEW ----------------
E.append(P("1. Project Overview", "h1"))
E.append(P("ADA currently runs its student internship / summer-training programme entirely on paper: the student "
           "fills forms by hand, the college signs a recommendation letter on letterhead, the bundle is posted to "
           "ADA (PB No 1718, Vimanapura Post, Bangalore 560017), and Admin &amp; HR manually registers, scrutinises "
           "and routes it through the Study Committee and Director (Admin &amp; HR)."))
E.append(P("This project replaces that with a secure web portal that digitises the entire journey end-to-end, "
           "mirroring the official policy documents exactly."))
E.append(P("Non-negotiable business rules", "h2"))
E += bullets([
    "<b>Referral-only entry:</b> An ADA employee must sponsor the student first and issue a referral code. No public "
    "application exists - the form cannot even be opened without a valid code.",
    "<b>College signature (hybrid):</b> The student uploads the signed/sealed college letter AND the college confirms "
    "online via a secure expiring link. Both are required before submission.",
    "<b>Fixed eligibility &amp; quotas:</b> 50 seats for BE/B.Tech (12-20 weeks, after 4th/6th semester) and 25 seats "
    "for ME/M.Tech (6-12 months), Indian citizens only, applied inside the December intake window.",
    "<b>Application Progress Tracker:</b> Every student and their sponsoring employee see a live 10-stage status "
    "timeline at all times.",
])

# ---------------- 2. ACTORS ----------------
E.append(P("2. Actors in the Process", "h1"))
E.append(make_table(
    ["Actor", "Role in the process"],
    [
        ["ADA Employee (Sponsor)", "Sponsors a student, generates referral code, endorses the application, tracks progress"],
        ["Student Applicant", "Redeems code, fills application, uploads documents, e-signs, tracks status"],
        ["College (Principal/HOD/TPO)", "Signs &amp; seals recommendation letter; confirms endorsement via secure link"],
        ["Admin &amp; HR Dept", "Receipt register, eligibility scrutiny, rejection letters, forwards to committee, letters, security pass, monthly reports, certificates"],
        ["Study Committee", "Screens and scores applications, recommends candidates"],
        ["Director (Admin &amp; HR)", "Final approve/reject, fixes training period, approves certificates"],
        ["Technology/Project Director", "Allots Guide/Mentor against directorate quotas"],
        ["Guide/Mentor (Scientist)", "Mentors trainee, gives end-of-training clearance"],
        ["Department Coordinator", "Enters monthly attendance of trainees"],
        ["System", "Auto-validates eligibility, auto-generates all letters/certificates, sends notifications, maintains audit log"],
    ],
    [115, 395]))
E.append(PageBreak())

# ---------------- 3. PROCESS FLOW ----------------
E.append(P("3. Detailed Process Flow (Stage by Stage)", "h1"))
E.append(P("The flow below is the complete to-be process. Each stage lists who acts, what they do, what the system "
           "does automatically, and the output/notification produced."))
stages = [
    ("Stage 0 - Intake Window Announcement (every December)", "ADA (public site)",
     "Publishes the annual advertisement: window open/close dates, seat counters (50 UG / 25 PG), eligibility rules, "
     "and instructions on how to get referred by an ADA employee. Informational only - no public apply button exists.",
     "Window opens; seat counters go live; referral-code requests become possible.",
     "Public advertisement page + downloadable policy documents"),
    ("Stage 1 - Employee Sponsorship", "ADA Employee",
     "Logs in with ADA credentials; clicks 'Sponsor a Student'; enters student's name, email and relationship "
     "(child/ward/professional referral); confirms endorsement.",
     "Generates unique single-use referral code (email-bound, expires with window); emails it to student; records "
     "sponsor + relationship; enforces per-employee referral cap.",
     "Referral code emailed to student; sponsorship recorded"),
    ("Stage 2 - Student Application", "Student",
     "Redeems code (form unreachable without it); fills multi-step form: personal details, photo, Aadhaar, college, "
     "branch, degree UG/PG, semester/year, CGPA/%, achievements, project topic + synopsis (max 150 words), area of "
     "interest; uploads marksheets, Aadhaar copy, college ID; e-signs declaration.",
     "Auto-validates: Indian nationality, duration 12-20 wks (UG) / 6-12 months (PG), start date at least 1 month "
     "ahead, CGPA scale, duplicate detection (DOB+name+college ID), CAPTCHA/rate-limit; auto-saves; auto-generates 3 "
     "PDFs: covering letter, pre-filled college recommendation letter, undertaking; issues application number "
     "(e.g. ADA/TRG/2026/00042).",
     "Draft application + 3 auto-generated PDFs + acknowledgment email"),
    ("Stage 3 - College Endorsement (hybrid)", "Student + College",
     "Student prints the pre-filled letter, obtains Principal/HOD signature &amp; official seal on college letterhead, "
     "uploads the scan. College official receives secure token link (14-day expiry), reviews the data, uploads the "
     "signed letter and clicks 'confirm endorsement' (or flags a data mismatch).",
     "Tracks both conditions; blocks progression until scan + online confirmation both exist; sends expiry reminders.",
     "Application moves to SUBMITTED; status updated to student, sponsor and college"),
    ("Stage 4 - Receipt &amp; Acknowledgment", "System",
     "-",
     "Creates entry in digital receipt register (date, application no, student, college); triggers notification to HR.",
     "Receipt-register entry (exportable); submission acknowledgment"),
    ("Stage 5 - Eligibility Scrutiny (HR)", "Admin &amp; HR",
     "Reviews application + documents side-by-side; verifies auto eligibility verdict; manual override with reason if "
     "needed; rejects ineligible applications.",
     "Auto eligibility pre-verdict; on rejection auto-generates official rejection letter; on pass enables 'forward "
     "to committee'.",
     "Eligible: committee queue; Ineligible: rejection letter emailed"),
    ("Stage 6 - Committee Selection", "Study Committee",
     "Members review forwarded applications; score on fixed rubric (CGPA, branch relevance, synopsis quality, "
     "achievements); comment; mark Recommended / Not Recommended.",
     "Ranking, quorum enforcement (configurable); scores hidden from students; conflict-of-interest exclusion (a "
     "sponsor never reviews their own referral).",
     "Recommended list sent to Director"),
    ("Stage 7 - Director Decision", "Director (Admin &amp; HR)",
     "Approves or rejects (full discretion per policy, with/without reasons); fixes the training period.",
     "On approval: auto-generates selection letter, emails student + college, sets reporting date; starts no-show "
     "countdown with PCC reminders. On rejection: optional-reason letter.",
     "Selection letter; reporting date; reminder schedule"),
    ("Stage 8 - Reporting Day (in person at ADA)", "Student + Admin &amp; HR",
     "Student reports on the notified date with Police Clearance Certificate, photo ID, undertaking countersigned by "
     "Principal/HOD; HR verifies originals and briefs the student.",
     "Reporting checklist in portal; auto-generates letter to Security Office for security pass; marks trainee as "
     "REPORTED; if date passes unreported, auto-cancels (NO_SHOW) per policy.",
     "Security-pass letter; trainee activated / registration auto-cancelled"),
    ("Stage 9 - Training Period", "Technology Director, Guide, Dept Coordinator",
     "Technology Director allots Guide/Mentor within directorate quota; guide mentors trainee; department "
     "coordinator records monthly attendance; guide may note progress.",
     "Quota enforcement (Appendix 'A'); topic approval record; monthly attendance consolidation; attendance "
     "shortfall alerts (100% required for certificate).",
     "Attendance records; monthly report data"),
    ("Stage 10 - Completion &amp; Certificate", "Guide, HR, Director",
     "Student submits project report copy and surrenders all data/materials; guide gives clearance; HR initiates "
     "certificate; Director approves.",
     "Auto-generates certificate on ADA letterhead (standard template) with serial number + QR; QR links to public "
     "verification page (name, college, topic, period only).",
     "Training certificate (PDF) + permanent verification record"),
]
for title, actor, human, system, output in stages:
    block = [P(title, "h2"), P("<b>Actor:</b> " + actor, "body"),
             P("\u2022 <b>Human actions:</b> " + human, "bullet"),
             P("\u2022 <b>System automation:</b> " + system, "bullet"),
             P("\u2022 <b>Output:</b> " + output, "bullet")]
    E.append(KeepTogether(block))
E.append(PageBreak())

# ---------------- 4. LIFECYCLE ----------------
E.append(P("4. Application Lifecycle (Status States)", "h1"))
E.append(P("Every application moves through a controlled state machine; every transition is audit-logged (who, when, "
           "from - to, reason). Terminal states: SCRUTINY_REJECTED, COMMITTEE_NOT_RECOMMENDED, DIRECTOR_REJECTED, "
           "NO_SHOW, TERMINATED and CLOSED."))
E.append(make_table(
    ["#", "State", "Meaning"],
    [
        ["1", "DRAFT", "Code redeemed; form being filled"],
        ["2", "SPONSOR_PENDING", "Awaiting employee endorsement confirmation"],
        ["3", "COLLEGE_PENDING", "Awaiting college scan upload + online confirmation"],
        ["4", "SUBMITTED", "Complete; entered in receipt register"],
        ["5", "UNDER_SCRUTINY", "HR eligibility verification"],
        ["6", "SCRUTINY_REJECTED", "Not eligible - rejection letter issued"],
        ["7", "IN_COMMITTEE", "Scoring &amp; recommendation"],
        ["8", "COMMITTEE_RECOMMENDED / NOT_RECOMMENDED", "Committee outcome"],
        ["9", "DIRECTOR_DECISION / APPROVED / DIRECTOR_REJECTED", "Final decision; selection letter"],
        ["10", "AWAITING_REPORTING", "Countdown + PCC reminders"],
        ["11", "NO_SHOW", "Date passed unreported - auto-cancelled"],
        ["12", "REPORTED", "Originals verified; security-pass letter issued"],
        ["13", "ACTIVE", "Guide assigned; attendance flowing"],
        ["14", "TERMINATED", "Violation / withdrawal (may flag institute)"],
        ["15", "COMPLETION_PENDING", "Guide clearance + report copy received"],
        ["16", "CERTIFICATE_ISSUED / CLOSED", "Certificate PDF with serial + QR"],
    ],
    [24, 160, 326]))
E.append(PageBreak())

# ---------------- 5. TIMELINE ----------------
E.append(P("5. Build-Process Timeline (16 Nov 2026 - 10 Feb 2027)", "h1"))
E.append(P("Total duration: ~12.5 working weeks, ending 10 February 2027. The schedule is compressed: the training "
           "lifecycle and hardening/UAT are condensed into the final weeks, and lower-priority polish (bilingual "
           "content, SMS, analytics dashboards) is moved to a post-project backlog."))

E.append(P("5.1 How the Build Proceeds (construction order)", "h2"))
E.append(P("The system is built layer by layer - nothing is built before what it depends on:"))
E += bullets([
    "<b>Layer 1 (W1-W2) FOUNDATION:</b> environment, database schema, authentication and role-based access - the "
    "skeleton every other component stands on.",
    "<b>Layer 2 (W3-W6) APPLICANT PATH:</b> public site, sponsorship/referral door, application wizard, document "
    "uploads, auto-generated PDF letters. After this layer, a student's application exists in the system.",
    "<b>Layer 3 (W7-W10) OFFICE PATH:</b> HR receipt register &amp; scrutiny, college endorsement, committee scoring, "
    "Director decision, selection/rejection letters. After this layer, an application can travel from submission to "
    "approval entirely in the portal.",
    "<b>Layer 4 (W11) TRAINING PATH:</b> reporting-day verification, security-pass letter, guide allotment, "
    "attendance. After this layer, an approved student can physically join and train.",
    "<b>Layer 5 (W12) FINALISATION:</b> certificate + QR verification, security hardening, UAT with HR office, "
    "management demo. After this layer, the system is handed over.",
])
E.append(P("Running through every layer: the notification/email engine, the audit log, and the progress tracker - "
           "the tracker is wired to each module as that module is built, so the status timeline grows with the system.",
           "body"))

E.append(P("5.2 Build-Process Gantt Chart (component x week)", "h2"))
E.append(P("Shaded cells = weeks in which that component is under construction. Demos at the end of W7 (MVP), W10 "
           "(selection flow) and W12 (final, 10 Feb). Holiday buffer: 24-27 Dec.", "body"))
wl = ["W1<br/>16 Nov", "W2<br/>23 Nov", "W3<br/>30 Nov", "W4<br/>07 Dec", "W5<br/>14 Dec", "W6<br/>21 Dec",
      "W7<br/>04 Jan", "W8<br/>11 Jan", "W9<br/>18 Jan", "W10<br/>25 Jan", "W11<br/>01 Feb", "W12<br/>08 Feb"]
E.append(gantt([
    ("Infra: repo, CI, Docker environment", [1, 2]),
    ("Database schema &amp; data models", [1, 2]),
    ("Authentication &amp; roles (RBAC)", [2]),
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
], wl))
E.append(Spacer(1, 6))

E.append(P("5.3 Weekly Build Progression (what is built, what is testable)", "h2"))
E.append(make_table(
    ["Wk", "Dates", "Work planned", "Deliverable of the week"],
    [
        ["W1", "16-20 Nov", "Requirements workshops with HR; collect final Word/PDF of every template; get answers to open policy questions (hard-copy rule, referral caps, Aadhaar, email domain)", "Signed-off requirements &amp; configuration sheet"],
        ["W2", "23-27 Nov", "Repository setup, CI, Docker environment; database schema design; auth + roles; UI wireframes approved", "Running skeleton with login/RBAC; approved wireframes"],
        ["W3", "30 Nov-04 Dec", "M1 public site: advertisement page (window dates, seat counters), policy downloads, FAQ, contact - informational only, no apply button", "Public site live in staging"],
        ["W4", "07-11 Dec", "M2 sponsorship: employee login, sponsorship creation, single-use referral codes, referral email; anti-abuse controls", "Employee can sponsor and student receives code"],
        ["W5", "14-18 Dec", "M3 student application wizard (part 1): multi-step form, auto-save, all fields, validations (eligibility rules, 150-word synopsis, duplicates, CAPTCHA)", "Form fully functional with validations"],
        ["W6", "21-23 + 28-31 Dec", "M3 (part 2): document uploads per checklist; auto-generated PDFs - covering letter, pre-filled college letter, undertaking; e-signature; application number", "Complete application package + 3 PDFs"],
        ["-", "24-27 Dec", "Holiday buffer (Christmas week)", "-"],
        ["W7", "04-08 Jan", "M5 (part 1): HR receipt register (auto-entries, exportable); scrutiny queue with document viewer + auto eligibility verdict; M9 progress tracker (10-stage student + sponsor timeline)", "MILESTONE 1 - MVP demo: sponsorship - application - register - live tracker"],
        ["W8", "11-15 Jan", "M4 college endorsement: secure token links (14-day expiry, resend), scan upload, online confirmation / mismatch flag; expiry reminders", "College endorsement working end-to-end"],
        ["W9", "18-22 Jan", "M6 committee module: scoring rubric, comments, recommend/not-recommend, quorum; M5 (part 2): rejection-letter generator, forward-to-committee", "Committee review cycle working"],
        ["W10", "25-29 Jan", "Director decision screen (approve/reject with reason); selection-letter generation + emails; period fixing; no-show countdown + PCC reminder scheduling", "MILESTONE 2 - DRAFT to APPROVED purely in-portal"],
        ["W11", "01-05 Feb", "Condensed training lifecycle core: reporting-day checklist (PCC, ID, countersigned undertaking); security-pass letter; NO_SHOW auto-cancellation; directorate quotas + guide allotment; monthly attendance entry", "Reporting - guide - attendance path working"],
        ["W12", "08-10 Feb", "Certificate generation on letterhead (serial + QR) + public verification page; essential hardening (2FA, audit-log UI, backups); UAT walkthrough with HR office; final management demonstration", "MILESTONE 3 - Final demo &amp; UAT sign-off (10 Feb 2027)"],
    ],
    [26, 62, 296, 126]))

E.append(P("5.4 Milestones (management check-points)", "h2"))
E.append(make_table(
    ["Milestone", "Date", "What management will see"],
    [
        ["M1 - MVP Demo", "08 Jan 2027", "Live demo: employee sponsors, student applies with code, auto-PDFs, application in HR register, student/sponsor see live status timeline"],
        ["M2 - Selection Demo", "29 Jan 2027", "Live demo: college endorses online, committee scores, Director approves, selection letter auto-emailed"],
        ["M3 - Final Demo &amp; UAT Sign-off", "10 Feb 2027", "Live demo: reporting, security pass, guide allotment, attendance, certificate with QR verification; UAT complete"],
    ],
    [105, 65, 340]))
E.append(P("Post-project backlog (not part of the 10 Feb commitment): SMS/WhatsApp notifications, bilingual content, "
           "analytics dashboards, synopsis plagiarism check, waitlist auto-promotion, chatbot/FAQ assistant.", "body"))

# ---------------- 6. DELIVERABLES ----------------
E.append(P("6. Final Deliverables", "h1"))
E += bullets([
    "Web portal (all modules M1-M9): public site, sponsorship, application wizard, college endorsement, HR admin, "
    "committee, training management, notifications/audit, progress tracker",
    "All official documents auto-generated as PDFs: covering letter, college recommendation letter (pre-filled), "
    "undertaking, selection/rejection letters, security-pass letter, monthly report, certificate with QR",
    "Admin configuration: intake windows, seat quotas, scoring rubric weights, templates, referral caps",
    "Documentation: user manual (student/employee/HR), admin guide, deployment guide (Docker)",
    "Security pack: RBAC matrix, audit log, backup/restore procedure, Aadhaar data-handling note",
])

# ---------------- 7. ASSUMPTIONS ----------------
E.append(P("7. Assumptions &amp; Dependencies", "h1"))
E += bullets([
    "ADA HR provides final versions of all templates and answers to open policy questions during Phase 0 (esp. the "
    "hard-copy mandate conflict in Annexure-I).",
    "An official email domain/relay for sending letters to students and colleges is available by Phase 2.",
    "Employee list (for sponsor login) can be imported or created manually at launch.",
    "Directorate quota data (Appendix 'A') is provided by the Technology Directors before Phase 3.",
    "Hosting decision (ADA intranet / NIC / cloud) is confirmed by Phase 4; the build is Docker-portable meanwhile.",
    "Aadhaar handling (encrypted scan + masked digits) receives legal sign-off during Phase 0-1.",
])

# ---------------- 8. RISKS ----------------
E.append(P("8. Risks &amp; Mitigation", "h1"))
E.append(make_table(
    ["Risk", "Impact", "Mitigation"],
    [
        ["Compressed schedule (hard stop 10 Feb 2027)", "High", "MVP-first ordering; lower-priority polish moved to post-project backlog; holiday buffer included; weekly milestone tracking"],
        ["Hard-copy mandate (Annexure-I) conflicts with digital-only flow", "High", "Get policy relaxation signed off in P0; until then keep HR 'manual registration' fallback for postal applications"],
        ["Aadhaar storage legal clearance delayed", "High", "Design supports offline-only Aadhaar (collected on reporting day) as fallback"],
        ["Holiday-season slowdown (late Dec / early Jan)", "Medium", "Buffer already included in W6-W7; light workload scheduled for holidays"],
        ["College officials slow to use endorsement links", "Medium", "14-day expiry + reminders + mismatch-flag path; scan upload alone can gate submission if policy permits"],
        ["Email deliverability to colleges", "Low", "Official sending domain confirmed in P0; reminders include portal link fallback"],
    ],
    [150, 45, 315]))

E.append(Spacer(1, 14))
E.append(P("- End of document -", "small_center"))

doc.build(E)
print("Saved ADA_Internship_Portal_Process_Flow_and_Timeline.pdf")
