# Notes for agents working on this repository

## Outstanding: the assignment marks do not add up

The assessment scheme is meant to be **40 marks of assignments, 15 + 15 + 10**.
Assignment I has been reworked and is correct at **10**. The other two have not:

| assignment | file | current total | should be |
|---|---|---|---|
| I — Precipitation | `slides/assignments/precipitation.qd` | 10 ✅ | 10 |
| II — Total Water Storage | `slides/assignments/soil_moisture.qd` | **25** ❌ | 15 |
| III — Groundwater | `slides/assignments/groundwater.qd` | **17** ❌ | 15 |

Rebalancing II and III is a separate job that has not been started. If you are
touching either file, raise it rather than silently leaving the totals wrong.

## Where things live

Tutorial notebooks are **generated**, never hand-authored, and three repositories
are involved:

1. `water-course/tutorials` — the source of truth. Percent-format `.py` files plus a
   `Makefile`. Its cell tags drive everything: `# + tags=["empty-cell"]` is the blank
   student skeleton, `# + tags=["solution"]` is the worked answer, `# + [markdown]` is
   prose. Pushing to `main` triggers CI, which runs `make all` and uploads `ready/` as
   an artifact. That build **executes** the solution notebooks, so it needs network
   access to NCI's THREDDS server and to `data.gadopt.org`.
2. `water-course/colab-tutorials` — what students open in Colab. A manually dispatched
   workflow pulls the artifact and commits only the exercise notebooks, filtering out
   `*_solution.ipynb`. **The trigger is manual**, so dispatch "Grab latest tutorials"
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

## Data traps that have already caused bugs

**Read `units` before trusting any Australian Water Outlook file.** AWO publishes a
`processed/deciles/` tree alongside `processed/values/`, using *identical filenames*.
The decile files carry `units: relative` with values in [0, 1] — percentile ranks, not
depths. A decile file was mirrored to `data.gadopt.org` and Tutorial 2 plotted it as
"Rainfall (mm)" for a year. That file has since been deleted from the server.

Monthly rainfall in real millimetres, read over OPeNDAP, no download needed:

```
https://thredds.nci.org.au/thredds/dodsC/iu04/australian-water-outlook/historical/v1/AWRALv7/processed/values/month/rain_day.nc
```

1911-01 to present, 0.05°, variable `rain_day`, monthly **totals**. Its `long_name`
says "Daily Rainfall" even in the monthly file — that attribute is wrong upstream.

**Latitude descends** (−10 to −44). `sel(latitude=slice(-38, -24))` returns an empty
array with no error at all; the correct order is `slice(-24, -38)`. This is the single
most common silent failure with this dataset.

**BoM blocks automated access.** `bom.gov.au` returns HTTP 403 to scripted requests, so
it cannot be used as a data source — only as reading. For ENSO indices use CRU
(`https://crudata.uea.ac.uk/cru/data/soi/soi.dat`) or NOAA PSL.

The basin boundary is `https://data.gadopt.org/water-course/MDB_boundaries.zip`
(north + south shapefiles, EPSG:4283). The old `MDB.latlon` ASCII file has been
retired and deleted from the server.
