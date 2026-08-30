# Notes for agents working on this repository

## The assignment marks

The assessment scheme is **40 marks of assignments, 10 + 15 + 15**. All three
assignments now match it:

| assignment | file | total | breakdown |
|---|---|---|---|
| I — Precipitation | `slides/assignments/precipitation.qd` | 10 | 2 + 3 + 2 + 3, Q5 bonus |
| II — Total Water Storage | `slides/assignments/soil_moisture.qd` | 15 | 3 + 3 + 2 + 4 + 3 |
| III — Groundwater | `slides/assignments/groundwater.qd` | 15 | 2 + 4 + 4 + 5 |

Assignment I splits differently for the two course codes. EMSC3025 takes
Questions 1-4 for 10 marks and Question 5 as an optional bonus mark. EMSC6025
takes Questions 1-3 for 7 marks, Question 4 for 2 and the required Question 5
for 1. Assignments II and III carry EMSC6025 requirements that are part of the
15 marks and do not add marks.

If you change a mark, change the stated total in the same commit and rebuild the
PDF to confirm the arithmetic still holds.

## Where things live

Computer-lab notebooks are **generated**, never hand-authored, and three repositories
are involved:

1. `water-course/tutorials` — the source of truth. Percent-format `.py` files, one per lab
   (`lab01_python_basics.py`, `lab02_shapefiles_and_masks.py`, `lab03_xarray_gridded_data.py`,
   `lab04_grid_cell_areas.py`, `lab05_rain_gauge_interpolation.py`), plus a `Makefile`. The
   filename number is the student-facing lab number. Its cell tags drive everything: `# + tags=["empty-cell"]` is the blank
   student skeleton, `# + tags=["solution"]` is the worked answer, `# + [markdown]` is
   prose. Pushing to `main` triggers CI, which runs `make all` and uploads `ready/` as
   an artifact. That build **executes** the solution notebooks, so it needs network
   access to NCI's THREDDS server and to `data.gadopt.org`.
2. `water-course/colab-tutorials` — what students open in Colab. A manually dispatched
   workflow pulls the artifact and commits only the exercise notebooks, filtering out
   `*_solution.ipynb` — so the `_solution` suffix is load-bearing and must not be renamed.
   **The trigger is manual**, so dispatch "Grab latest tutorials"
   after pushing to `tutorials`, or students keep seeing the old version.
3. This repository — carries the solution notebooks under `docs/computer-lab/`, which
   is **gitignored** and populated from the same artifact at build time by
   `.github/workflows/build-slides.yml`. `mkdocs-jupyter` renders stored outputs and
   never re-executes, so a notebook without outputs renders as a blank page.

Editing an `.ipynb` in `docs/computer-lab/` therefore accomplishes nothing durable.
Edit the `.py` in the `tutorials` repo instead.

`/admin/` and `/assignment-solutions/` are gitignored. `assignment-solutions/` holds
worked solutions to live assessments and **must stay untracked** — this repository is
public. Build it locally with `make -C assignment-solutions`.

## Rendering trap: paged documents silently delete table rows

Quarkdown's `paged` doctype does not split a table that straddles a page break —
it **drops** the rows that do not fit and leaves the caption orphaned on the next
page. The build reports success. Assignment I shipped for days with only the
`October` row of its two-row month table visible, and a student had to report it.

`slides/definitions.qd` now carries `.quarkdown table { break-inside: avoid; }`,
nested inside the `.pagemargin{bottomright}` block. Both details matter: at top
level Quarkdown's `.css` emits a `<style>` node into the document flow, which then
sits ahead of the first heading and its forced page break, producing an empty
first page; page margins are out of flow, so the rule rides along invisibly. Text
placed inside a `.pagemargin` block is printed verbatim, so keep comments outside
it — an HTML comment in there renders as visible marginalia, markers and all.

When you change anything about paged layout, verify by rendering, not by reading
the `.qd`. Build the PDFs (`make -C slides pdf`), extract the text, and check that
every table cell in the source actually appears in the output.

## Data traps that have already caused bugs

**Read `units` before trusting any Australian Water Outlook file.** AWO publishes a
`processed/deciles/` tree alongside `processed/values/`, using *identical filenames*.
The decile files carry `units: relative` with values in [0, 1] — percentile ranks, not
depths. A decile file was mirrored to `data.gadopt.org` and Lab 2 plotted it as
"Rainfall (mm)" for a year. That file has since been deleted from the server.

Monthly rainfall in real millimetres, read over OPeNDAP, no download needed:

```
https://thredds.nci.org.au/thredds/dodsC/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/month/rain_day.nc
```

1911-01 to present, 0.05°, variable `rain_day`, monthly **totals**. Its `long_name`
says "Daily Rainfall" even in the monthly file — that attribute is wrong upstream.

**Latitude descends** (−10 to −44). `sel(latitude=slice(-38, -24))` returns an empty
array with no error at all; the correct order is `slice(-24, -38)`. This is the single
most common silent failure with this dataset. Lab 3 teaches it explicitly.

**`method="nearest"` applies to every coordinate in the same `.sel`, including time.**
Months in this file are stamped at their *end*, so
`sel(latitude=..., longitude=..., time="2022-10", method="nearest")` parses the string as
2022-10-01, snaps to the 2022-09-30 stamp and silently returns **September**. Do the
nearest-neighbour lookup on the spatial coordinates, then select the time in a separate call.

**BoM blocks automated access.** `bom.gov.au` returns HTTP 403 to scripted requests, so
it cannot be used as a data source — only as reading. For ENSO indices use CRU
(`https://crudata.uea.ac.uk/cru/data/soi/soi.dat`) or NOAA PSL.

The basin boundary is `https://data.gadopt.org/water-course/MDB_boundaries.zip`
(north + south shapefiles, EPSG:4283). The old `MDB.latlon` ASCII file has been
retired and deleted from the server.

**Soil moisture for Assignment II** is the ESA CCI combined v09.1 daily record, cut to a
box around the basin and served as

```
https://data.gadopt.org/water-course/esacci_sm_combined_v09-1_MDB_daily_2003-2023.nc
```

170 MB, 2003-01-01 to 2023-12-31, 0.25 degrees, variables `sm`, `sm_uncertainty` and
`flag`. **The record starts in 2003**, so no groundwater series can begin in 2002 whatever
GRACE offers. Latitude descends here too. It replaces `combined_masked_soil_moisture.nc`,
which was 4.6 GB, was never masked to anything despite the name, and had lost the `units`
attribute off `sm` in subsetting. That file has been deleted from the server, as has the
stale mirror of the CSR mascons. Get the mascons from CSR itself.

**The CSR GRACE file writes its metadata attribute as `Units`, capital U.** `xarray` wants
lowercase `units`, does not find it, and leaves `time` as bare floats -- days since
2002-01-01, per the `time_epoch` attribute -- and `lwe_thickness` unlabelled, in cm. The
grid runs latitude *ascending* and longitude 0 to 360, the opposite of both other datasets
in this course. Anomalies are relative to the mean of 2004.000 to 2009.999, so anything
differenced against them must have that same period removed first.
