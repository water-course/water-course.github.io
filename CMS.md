# CMS handover — EMSC3025 class summary (2026 Sem 2)

Handover note for picking this work up in a fresh session. It records what was done,
where, and what is still outstanding.

## Background: two separate curriculum objects

There are two distinct things in the ANU CMS, and they must not be confused:

1. **Course record / 2026 course amendment** — the rename from "Remote Sensing of Water
   Resources" to **"Global Water Resources"**, plus new learning outcomes, new assessment
   weightings, prescribed texts, marketing description, etc. Per the curriculum office this
   amendment only takes effect for **2027 delivery** (a course cannot be amended in its own
   delivery year). This record has **not** been edited yet. The field-by-field content for
   it is written up in:
   `~/Library/Mobile Documents/com~apple~CloudDocs/Workspace/2026_course_amendment/CMS_fill_sheet.md`
   and the annotated proposal PDF is in the same folder.

2. **Class summary (2026 Sem 2 delivery)** — the object we actually edited this session.
   - URL: https://cms.anu.edu.au/cms/classes/90518/edit  (class 90518, EMSC3025)
   - Template: "Class Summary", version 014, state: DRAFT
   - It must "generally align with the currently approved/published course information"
     (i.e. the existing Remote Sensing of Water Resources course, not the 2027 amendment).

## What was done to the class summary (all saved as DRAFT; verified after reload)

### Class Overview — "Class Structure and Content" (12-week table)
Filled all 12 weeks from blank. Remote sensing is woven into each relevant topic (no
standalone geodesy block, no lecturer attribution in the table), GRACE folded into the
groundwater intro (wk 6), soil moisture + unsaturated zone combined (wk 5). No standalone
paper-critique week.

1. Introduction; global/regional water cycle; observing water from space
2. Precipitation + satellite precipitation (GPM/TRMM)
3. Evapotranspiration + remote sensing of ET
4. Runoff and streamflow + satellite altimetry (SWOT)
5. Soil moisture and the unsaturated zone + satellite soil moisture (SMAP/SMOS)
6. Groundwater principles + total water storage from GRACE gravity
7. Aquifers
8. Theory of groundwater flow I — Darcy's law, saturated flow
9. Theory of groundwater flow II — wells, pumping, transient flow
10. Geology and hydrogeology
11. Groundwater management and water resources in Australia
12. Water resources in a changing climate — synthesis

The "Assessment and Other Information" column was filled with **indicative** assignment
timing then — see follow-ups — these are placeholders, not final dates.

### Assessment Tasks
Fixed descriptions, reweighted, added a new task. **Written critique dropped in the
2026-07-16 session** (an oral critique is more defensible now that LLMs write reports);
its 15% went to oral (+10) and exam (+5). Final state (total = 100%, 6 tasks):

| # | Task | Weight | Due | Return | LO |
|---|------|--------|-----|--------|----|
| 1 | Computing assignment 1 (precipitation) | 10% | 2026-08-21 | 2026-09-04 | 1,2,3 |
| 2 | Computing assignment 2 (soil moisture) | 15% | 2026-09-25 | 2026-10-09 | 1,2,3 |
| 3 | Computing assignment 3 (groundwater) | 15% | 2026-10-23 | blank | 1,2,3 |
| 4 | Oral critique of a scientific paper | 20% | 2026-10-16 | blank | 4,5 |
| 5 | Final exam | 30% | blank | blank | 1,2,3,5 |
| 6 | Tutorial participation | 10% | blank | blank | 1,2,3,4,5 |

Scheme: computing 40 / oral 20 / participation 10 / exam 30.
(Original class record was: written 10 / computing 40 / oral 10 / exam 40. The intermediate
scheme with a written critique — computing 40 / written 15 / oral 10 / participation 10 /
exam 25 — was superseded in the 2026-07-16 session.)

Due dates are **YYYY-MM-DD** (the publish-validation requires this format — week references
were rejected). Friday of each due week; exam and participation left blank (exam date set
centrally; participation is continuous). Week grid for 2026 Sem 2 confirmed with Sia:
start Mon 27/07, six teaching weeks, **2-week break 7–18 Sep**, six more, ends Fri 30/10 —
W4=17–21 Aug, W6=31 Aug–4 Sep, W7=21–25 Sep, W9=5–9 Oct, W10=12–16 Oct, W11=19–23 Oct.
Oral week (10) taken from the weekly Class Structure table. The weekly-table wk12 cell had
its "Written paper critique due." sentence removed. PARTICIPATION section free-text field
filled. **SELT question** answered YES with a description of the remote-sensing integration.

**The record now passes publish validation ("completed successfully") and is ready to
submit for review** (STATE ▸ → Submit for review). It has NOT been submitted yet — awaiting
Sia. Full write-up + draft email to Caroline in `EMSC3025_class_summary_report.md`.

Participation task is written to be ANU-policy compliant: graded on engagement (attempting
the tutorial problems, contributing in class), **not attendance**; 0/1/2 per tutorial;
best 8 tutorials count.

## Status

- Class summary is **saved as DRAFT** (state unchanged — SAVE only, never re-submitted this
  session). Assessment scheme, due/return weeks, LO links and PARTICIPATION field all done
  and verified after reload (2026-07-16).
- Convener updated to Dr Siavash Ghelichkhan for the Sem 2 delivery (curriculum office
  handled this).

### CMS editing gotchas found this session
- Summary-row deletion is change-tracked: "delete" strikes the row through (red bar) and
  offers **PURGE** to hard-remove it. Task-card deletion is a hard delete (renumbers cards).
- **Textarea (date) edits via scripting don't persist on their own** — a pure native-setter
  `input` event does NOT dirty the Angular form, so SAVE stays disabled and the value is
  lost. Quill (`.ql-editor`) edits DO register. Workaround that worked: make any genuine
  Quill change (setText to a temp value then back — setText to the *same* value no-ops and
  doesn't dirty), which enables SAVE; the textarea DOM values are then serialised on save.
  Set textarea values with a *fresh* DOM query right before saving (Quill edits re-render
  rows and orphan earlier element references — that's why two date fields silently reverted
  the first time).

## Outstanding / follow-ups

- **Due dates are entered as week references.** If the curriculum office insists on
  calendar dates, convert using the week grid above (or leave the exam/participation blank).
- **PGRD version (EMSC6025).** The curriculum office will clone a postgraduate version of
  this class summary once the UGRD one is finalised; it will then need adjusting for the
  PGRD cohort.
- **2027 course amendment.** `CMS_fill_sheet.md` was reconciled to the authoritative class
  summary on 2026-07-16 (indicative-assessment table + rationale now read computing 40 /
  oral 20 / participation 10 / exam 30, written critique removed). The amendment record
  itself in the CMS has **not** been edited (only takes effect for 2027 delivery); when it
  is, use the updated fill sheet.
- **Learning-outcome links** — DONE in the class summary: computing→1,2,3; oral→4,5;
  exam→1,2,3,5; participation→1,2,3,4,5.
- **"PARTICIPATION" free-text field** — DONE (short note describing the Wed 2-hour tutorial
  participation task, engagement-not-attendance, 0/1/2, best 8 count).
- **Course materials still on the old scheme** (not CMS, separate task):
  `slides/00_introduction.qmd` assessment chart still shows assignments 40 / presentation 10
  / written 20 / exam 30, and `misc/paper_critique_guidelines.qd` still has written-critique
  instructions. Update these to the oral-only scheme when convenient.
- **Timetable wording** — the actual Sem 2 timetable is Mon 9–11 lecture (2h), Wed 9–11
  tutorial (2h, participation graded here), Wed 11–12 computer lab (1h). The amendment fill
  sheet workload line still describes "2×1h lecture / 1×2h practical / 1×1h tutorial" — align
  if it matters.

## Reference

- Class summary: https://cms.anu.edu.au/cms/classes/90518/edit
- Curriculum contact: Caroline Chapman, Deputy Manager Curriculum Architecture
  <Caroline.Chapman@anu.edu.au>. Her latest email (thread "Sem 2 class summaries -
  reminder. Due 6 July") contains the concrete follow-up asks above.
- Editing method that worked in the CMS: the content cells are Quill rich-text editors
  (`.ql-editor`); set them via `window.Quill.find(container).setText(text, 'user')`. Date
  fields are textareas (React) — set via the native value setter + input/change events.
  Adding a task: "+ ADD ASSESSMENT TASK" button adds a card; the summary-table "ADD ROW"
  adds a matching summary row (they are independent — do both).
