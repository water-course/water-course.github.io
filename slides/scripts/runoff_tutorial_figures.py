"""Figures and marked numbers for the runoff tutorial.

Run this from ``slides/scripts``::

    python3 runoff_tutorial_figures.py            # figures + numbers
    python3 runoff_tutorial_figures.py --refetch  # re-pull from WaterNSW first

It writes five PNG files into ``slides/image/`` and prints every number that
appears in ``slides/tutorials/runoff_answers.qd``. If you change the event, the
separation window or the isotope values, re-run this and copy the printed block
into the answer sheet. Nothing in the answer sheet should be a number somebody
typed by hand.

The storm
---------
Goobarragandra River at Lacmalac, AWRC gauge 410057, 665 km^2. A steep forested
catchment in the upper Murrumbidgee, inside the Murray-Darling Basin the rest of
the course uses. The gauge records rainfall as well as stage, so one file gives
the students both sides of a runoff ratio.

The event is 4 to 6 February 2021: flat baseflow, a small precursor rise on
2 February, one sharp peak on 6 February, then a clean recession over 13 days.
Hourly, 505 steps, no gaps and no suspect quality codes.

The isotope values in A1 are illustrative, not measured. There is no isotope
record for this gauge. They are chosen to sit in the range that tracer studies
report for a temperate upland catchment, and the answer sheet says so plainly.
"""

import argparse
import csv
import io
import math
import os
import urllib.request
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

# ---------------------------------------------------------------------------
# The event
# ---------------------------------------------------------------------------

GAUGE = "410057"
GAUGE_NAME = "Goobarragandra River at Lacmalac"
AREA_KM2 = 665.0                      # from CAMELS-AUS v2, same AWRC gauge id

WINDOW = ("20210201", "20210222")     # what the students are given
STORM_RAIN = (datetime(2021, 2, 4), datetime(2021, 2, 7))   # the rain to count
SEPARATION = (datetime(2021, 2, 5), datetime(2021, 2, 19))  # separation limits

# Where the students get the same file.
CSV_URL = ("https://data.gadopt.org/water-course/"
           "goobarragandra_410057_feb2021_hourly.csv")

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "image")

# Illustrative oxygen-18 composition, in per mille relative to VSMOW.
# Pre-event water is the catchment's stored water; the storm rain is lighter,
# which is the usual situation for a cool-season frontal storm.
D_PRE = -6.2
D_RAIN = -11.4
# Stream samples through the event: (timestamp, measured delta-18-O).
D_STREAM = [
    (datetime(2021, 2, 5, 18), -6.4),
    (datetime(2021, 2, 6, 0), -6.9),
    (datetime(2021, 2, 6, 9), -7.6),    # coincides with the discharge peak
    (datetime(2021, 2, 6, 18), -7.2),
    (datetime(2021, 2, 7, 12), -6.7),
]

# Colours, kept consistent across every figure in the sheet.
C_FLOW = "#8a5a2b"
C_RAIN = "#4a90c4"
C_STORM = "#d9a679"
C_BASE = "#3f6f3f"
C_NEW = "#c0504d"
C_OLD = "#9bbfd4"


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load(refetch=False):
    """Return the event as ``(times, discharge_ML_per_day, rainfall_mm)``.

    By default this reads the published CSV, so the figures are built from
    exactly the bytes the students download. ``--refetch`` goes back to the
    WaterNSW API instead, which is how the CSV was made in the first place.
    """
    if refetch:
        from waternsw import trace
        flow = trace(GAUGE, *WINDOW, interval="hour", varto="141.00")
        rain = dict(trace(GAUGE, *WINDOW, interval="hour",
                          varfrom="10.00", varto="10.00", data_type="tot"))
        times = [t for t, _ in flow]
        return (times,
                np.array([v for _, v in flow]),
                np.array([rain.get(t, 0.0) for t in times]))

    text = urllib.request.urlopen(CSV_URL, timeout=60).read().decode()
    rows = list(csv.DictReader(io.StringIO(text)))
    times = [datetime.strptime(r["datetime"], "%Y-%m-%d %H:%M") for r in rows]
    return (times,
            np.array([float(r["discharge_ML_per_day"]) for r in rows]),
            np.array([float(r["rainfall_mm"]) for r in rows]))


def separate(times, flow):
    """Straight-line baseflow separation over ``SEPARATION``.

    The baseflow line runs from the discharge at the start of the window to the
    discharge at its end, and stormflow is whatever sits above it. This is the
    crudest of the standard separations and it is chosen on purpose: it can be
    done with a ruler, so the students can check the code against the figure.

    Returns ``(mask, baseline, stormflow_ML)`` where ``mask`` selects the
    window and ``baseline`` is defined only inside it.
    """
    mask = np.array([SEPARATION[0] <= t <= SEPARATION[1] for t in times])
    inside = flow[mask]
    baseline = np.linspace(inside[0], inside[-1], inside.size)
    # Hourly steps, and discharge is per day, so each step contributes v/24 ML.
    stormflow = float(np.sum(np.maximum(0.0, inside - baseline)) / 24.0)
    return mask, baseline, stormflow


def new_water_fraction(delta_stream):
    """Two-component isotope separation.

    The mass balance is Q_total = Q_new + Q_old with the same balance again on
    the tracer, which rearranges to the fraction of streamflow that is event
    ("new") water::

        f_new = (d_stream - d_pre) / (d_rain - d_pre)

    It assumes both end members are constant through the storm, that soil water
    is not a third distinct component, and that the tracer is conservative.
    """
    return (delta_stream - D_PRE) / (D_RAIN - D_PRE)


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------

def _hydrograph_axes(ax, times, flow, rain, log=False):
    """Draw the shared discharge line and inverted rainfall bars.

    ``log`` puts discharge on a logarithmic axis, which is how a hydrograph is
    normally presented: on a linear axis one large event flattens every normal
    flow onto the x-axis and the recession detail disappears.

    Do NOT use it for the separation figure. Stormflow is the **area** between
    the hydrograph and the baseflow line, and area on a logarithmic axis is not
    proportional to volume. The straight-line separation is also only a straight
    line on linear axes.
    """
    ax.plot(times, flow, color=C_FLOW, lw=1.6, zorder=3)
    ax.set_ylabel("Discharge (ML/day)")
    if log:
        ax.set_yscale("log")
        ax.set_ylim(200, 20000)
        ax.grid(alpha=0.25, lw=0.6, which="both")
    else:
        ax.set_ylim(0, 11000)
        ax.grid(alpha=0.25, lw=0.6)

    top = ax.twinx()
    top.bar(times, rain, width=1 / 26, color=C_RAIN, zorder=2)
    top.set_ylim(30, 0)                     # rainfall hangs from the top
    top.set_ylabel("Rainfall (mm/hour)")
    return top


def figure_hydrograph(times, flow, rain):
    """A2 question figure: the storm, unannotated. The students do the work."""
    fig, ax = plt.subplots(figsize=(9.0, 4.4))
    _hydrograph_axes(ax, times, flow, rain, log=True)
    ax.set_title(f"{GAUGE_NAME} ({GAUGE}), {AREA_KM2:.0f} km$^2$\n"
                 "hourly discharge (logarithmic) and rainfall, February 2021",
                 fontsize=11)
    fig.autofmt_xdate()
    fig.tight_layout()
    path = os.path.join(IMAGE_DIR, "tutorial_runoff_hydrograph.png")
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def figure_separation(times, flow, rain, mask, baseline, stormflow):
    """A2 answer figure: the same storm with the separation drawn on."""
    fig, ax = plt.subplots(figsize=(9.0, 4.4))
    _hydrograph_axes(ax, times, flow, rain)

    window = [t for t, m in zip(times, mask) if m]
    ax.plot(window, baseline, color=C_BASE, lw=1.6, ls="--", zorder=4,
            label="straight-line baseflow separation")
    ax.fill_between(window, baseline, flow[mask],
                    where=flow[mask] > baseline, color=C_STORM, alpha=0.75,
                    zorder=1, label=f"stormflow = {stormflow:,.0f} ML"
                                    f" = {stormflow / AREA_KM2:.1f} mm")

    peak_index = int(np.argmax(flow))
    ax.annotate(f"peak {flow[peak_index]:,.0f} ML/day\n"
                f"{times[peak_index]:%d %b %H:%M}",
                xy=(times[peak_index], flow[peak_index]),
                xytext=(times[peak_index + 60], flow[peak_index] * 0.86),
                arrowprops=dict(arrowstyle="->", lw=1.1), fontsize=9)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.95)
    ax.set_title("Model answer: baseflow separation", fontsize=11)
    fig.autofmt_xdate()
    fig.tight_layout()
    path = os.path.join(IMAGE_DIR, "tutorial_runoff_separation_answer.png")
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def figure_isotopes(times, flow):
    """A1 answer figure: the same peak split into new and old water.

    The sampled fractions are interpolated across the event so that the split
    can be shaded continuously. Outside the sampled period the stream is taken
    to be entirely pre-event water, which is what the first and last samples
    are already close to.
    """
    sample_times = [t for t, _ in D_STREAM]
    fractions = [new_water_fraction(d) for _, d in D_STREAM]

    seconds = np.array([t.timestamp() for t in times])
    sample_seconds = np.array([t.timestamp() for t in sample_times])
    f_new = np.interp(seconds, sample_seconds, fractions, left=0.0, right=0.0)

    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(9.0, 6.0), sharex=True,
        gridspec_kw={"height_ratios": [2.1, 1.0], "hspace": 0.12})

    ax.fill_between(times, 0, flow, color=C_OLD, label="pre-event (old) water")
    ax.fill_between(times, 0, flow * f_new, color=C_NEW,
                    label="event (new) water")
    ax.plot(times, flow, color=C_FLOW, lw=1.4)
    ax.set_ylabel("Discharge (ML/day)")
    ax.set_ylim(0, 11000)
    ax.set_xlim(datetime(2021, 2, 4, 12), datetime(2021, 2, 9))
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.25, lw=0.6)
    ax.set_title("Model answer: two-component isotope separation\n"
                 "at the peak the stream is about "
                 f"{100 * max(fractions):.0f} per cent new water",
                 fontsize=11)

    ax2.plot(sample_times, [100 * f for f in fractions], "o-",
             color=C_NEW, lw=1.4, ms=6)
    for t, d in D_STREAM:
        ax2.annotate(f"{d:.1f}‰", xy=(t, 100 * new_water_fraction(d)),
                     xytext=(0, 8), textcoords="offset points",
                     ha="center", fontsize=8)
    ax2.set_ylabel("New water (%)")
    ax2.set_ylim(0, 40)
    ax2.grid(alpha=0.25, lw=0.6)

    fig.autofmt_xdate()
    fig.tight_layout()
    path = os.path.join(IMAGE_DIR, "tutorial_runoff_isotope_answer.png")
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def figure_swot():
    """A3 question figure: what a swath altimeter sees, and what it does not.

    Left, a cross-section with two water surfaces from two overpasses. The
    interferometer measures both widths and both elevations, so it knows the
    area BETWEEN them. It has never seen the channel below the lower surface.
    Right, the same two surfaces along the reach, which is where the slope in
    Manning's equation comes from.
    """
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.2),
                                  gridspec_kw={"width_ratios": [1.25, 1.0]})

    # --- cross-section -----------------------------------------------------
    bed_x = np.array([-140, -115, -95, -55, 0, 60, 95, 118, 140])
    bed_z = np.array([6.0, 3.4, 1.6, 0.35, 0.0, 0.4, 1.7, 3.5, 6.0])
    fine_x = np.linspace(-140, 140, 400)
    fine_z = np.interp(fine_x, bed_x, bed_z)

    z1, z2 = 2.30, 3.56                    # the two observed water surfaces
    ax.fill_between(fine_x, fine_z, z1, where=fine_z < z1, color="#a8cbe0")
    ax.fill_between(fine_x, np.maximum(fine_z, z1), z2,
                    where=fine_z < z2, facecolor="#f0d4a0", hatch="///",
                    edgecolor="#9a7434", lw=0.5)
    ax.plot(fine_x, fine_z, color="#5b4636", lw=2.0)
    for z, label in ((z1, "pass 1"), (z2, "pass 2")):
        ax.axhline(z, color="#2f5d80", lw=1.2, ls="--", xmax=0.98)
        ax.text(138, z + 0.12, label, ha="right", fontsize=8.5, color="#2f5d80")

    ax.annotate("", xy=(-104, z2 + 0.42), xytext=(107, z2 + 0.42),
                arrowprops=dict(arrowstyle="<->", lw=1.1))
    ax.text(0, z2 + 0.60, "$W_2$ = 210 m  (measured)", ha="center", fontsize=9)
    ax.text(0, (z1 + z2) / 2 - 0.05, r"$\delta A$   measured",
            ha="center", fontsize=9.5)
    ax.text(0, z1 / 2 - 0.15, "$A_0$\nnever observed", ha="center",
            fontsize=9.5, color="#1c3f5b")
    ax.text(-136, 5.4, "cross-section", fontsize=10, style="italic")
    ax.set_ylim(-0.4, 6.6)
    ax.set_xlim(-145, 145)
    ax.set_xlabel("Distance across channel (m)")
    ax.set_ylabel("Height above lowest bed (m)")

    # --- long profile ------------------------------------------------------
    reach = np.array([0.0, 10.0])          # kilometres
    ax2.plot(reach, [85.38, 84.92], color="#2f5d80", lw=1.8, label="pass 2")
    ax2.plot(reach, [84.12, 83.68], color="#2f5d80", lw=1.8, ls="--",
             label="pass 1")
    ax2.annotate("", xy=(7.4, 85.14), xytext=(7.4, 84.06),
                 arrowprops=dict(arrowstyle="<->", lw=1.1))
    ax2.text(7.1, 84.60, "1.26 m", ha="right", fontsize=9)
    ax2.text(5.0, 85.30, r"slope $S$ = 0.46 m / 10 km = $4.6\times10^{-5}$",
             ha="center", fontsize=9)
    ax2.text(0.2, 84.30, "long profile", fontsize=10, style="italic")
    ax2.set_xlabel("Distance along reach (km)")
    ax2.set_ylabel("Water surface elevation (m)")
    ax2.legend(loc="lower right", fontsize=8.5)
    ax2.grid(alpha=0.25, lw=0.6)

    fig.suptitle("What a swath altimeter measures on one reach", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    path = os.path.join(IMAGE_DIR, "tutorial_runoff_swot_section.png")
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def _distance_to_path(grid_x, grid_y, path):
    """Shortest distance from every grid point to a polyline.

    Used to incise valleys along the same lines the channels are later drawn
    on, so that the contours actually bend around the drainage network instead
    of the channels being drawn across an unrelated surface.
    """
    distance = np.full(grid_x.shape, np.inf)
    for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
        segment_x, segment_y = x1 - x0, y1 - y0
        length_squared = segment_x ** 2 + segment_y ** 2
        # Projection of each grid point onto the segment, clamped to its ends.
        t = np.clip(((grid_x - x0) * segment_x + (grid_y - y0) * segment_y)
                    / length_squared, 0.0, 1.0)
        distance = np.minimum(
            distance,
            np.hypot(grid_x - (x0 + t * segment_x),
                     grid_y - (y0 + t * segment_y)))
    return distance


# The drainage network. The valleys are incised along exactly these lines.
MAIN_CHANNEL = np.array([[0.70, 3.92], [2.10, 3.98], [3.50, 4.04],
                         [5.00, 4.06], [6.50, 4.02], [8.00, 3.96],
                         [9.60, 3.90]])
TRIBUTARY = np.array([[3.05, 7.00], [3.35, 6.35], [3.75, 5.70],
                      [4.20, 5.00], [4.75, 4.06]])


def figure_connectivity():
    """A4 question figure: four saturated patches, not all of them connected.

    This is part of a catchment, not a whole one: a valley draining east with
    slopes rising to the north and south, one tributary hollow cut into the
    northern slope, and a bench part way up it. Drawing only a reach avoids
    inventing a divide that the synthetic surface would not really support.

    The surface is built so the contours follow the drainage. Valleys are
    incised along the same polylines the channels are drawn on, and the
    contours come from the surface at a fixed 5 m interval, so the stated
    contour interval is true and the contours V upstream where they should.
    """
    grid_x, grid_y = np.meshgrid(np.linspace(0, 10, 500), np.linspace(0, 8, 400))

    # Side slopes rising away from the valley axis, and a fall to the east.
    elevation = 150.0 + 15.0 * np.abs(grid_y - 4.0) ** 1.35 - 2.6 * grid_x
    # Incise the main valley along the channel.
    elevation -= 14.0 * np.exp(
        -(_distance_to_path(grid_x, grid_y, MAIN_CHANNEL) ** 2) / 0.60)
    # Cut the tributary hollow into the northern slope.
    elevation -= 10.0 * np.exp(
        -(_distance_to_path(grid_x, grid_y, TRIBUTARY) ** 2) / 0.42)
    # A bench on the northern slope: locally flat ground that holds water.
    elevation -= 11.0 * np.exp(-(((grid_x - 6.55) ** 2) / 0.85
                                 + ((grid_y - 6.05) ** 2) / 0.38))

    fig, ax = plt.subplots(figsize=(9.0, 6.0))
    levels = np.arange(np.floor(elevation.min() / 5) * 5, elevation.max() + 5, 5)
    ax.contour(grid_x, grid_y, elevation, levels=levels, colors="#a89880",
               linewidths=0.7)
    index = ax.contour(grid_x, grid_y, elevation, levels=levels[::4],
                       colors="#8a7355", linewidths=1.2)
    ax.clabel(index, fmt="%.0f", fontsize=7.5, inline=True)

    for line, width in ((MAIN_CHANNEL, 2.8), (TRIBUTARY, 1.8)):
        ax.plot(line[:, 0], line[:, 1], color="#2f6f9f", lw=width, zorder=5,
                solid_capstyle="round")
    ax.annotate("to the outlet", xy=(9.55, 3.90), xytext=(-4, 26),
                textcoords="offset points", fontsize=9, ha="right",
                color="#1b4b6b")

    def patch(vertices, label, xy_label):
        ax.add_patch(Polygon(vertices, closed=True, facecolor="#7fb0cd",
                             edgecolor="#2f6f9f", alpha=0.9, lw=1.2, zorder=4))
        ax.annotate(label, xy=xy_label, fontsize=14, fontweight="bold",
                    color="#12384f", zorder=7, ha="center")

    # A: riparian strip, directly beside the channel.
    patch([[5.10, 4.34], [7.30, 4.28], [8.30, 4.22], [8.30, 3.72],
           [7.30, 3.66], [5.10, 3.72]], "A", (6.70, 4.60))
    # B: hollow at the head of the tributary, sitting on the drainage line.
    patch([[2.58, 7.10], [3.38, 7.16], [3.58, 6.63], [3.06, 6.30],
           [2.58, 6.58]], "B", (2.26, 6.83))
    # C: perched patch on the bench, with no drainage line to the channel.
    patch([[5.95, 6.42], [6.95, 6.46], [7.20, 5.85], [6.45, 5.58],
           [5.95, 5.88]], "C", (7.55, 6.20))
    # D: ponded behind the road embankment, on the southern slope.
    patch([[4.10, 2.12], [5.25, 2.18], [5.42, 1.62], [4.55, 1.44],
           [4.05, 1.70]], "D", (3.75, 1.95))
    road = np.array([[1.20, 1.05], [3.20, 1.28], [5.60, 1.44], [8.60, 1.30]])
    ax.plot(road[:, 0], road[:, 1], color="#4a4a4a", lw=2.6, zorder=5)
    ax.plot(road[:, 0], road[:, 1], color="#dcdcdc", lw=0.9, ls=(0, (6, 6)),
            zorder=6)
    ax.annotate("sealed road on an embankment", xy=(8.45, 1.30),
                xytext=(-6, -16), textcoords="offset points",
                fontsize=8.5, ha="right", color="#4a4a4a")
    # The only outlet from D: a single culvert under the embankment.
    ax.plot([4.86, 4.86], [1.52, 1.14], color="#2f6f9f", lw=1.8, zorder=7)
    ax.annotate("culvert", xy=(4.86, 1.12), xytext=(0, -14),
                textcoords="offset points", fontsize=8.5, ha="center",
                color="#2f6f9f")

    ax.set_xlim(0.4, 9.7)
    ax.set_ylim(0.35, 7.75)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_title("Part of a catchment after three days of rain: four saturated "
                 "areas\ncontour interval 5 m (metres), channels in blue",
                 fontsize=11)
    for spine in ax.spines.values():
        spine.set_edgecolor("#8a7355")
    fig.tight_layout()
    path = os.path.join(IMAGE_DIR, "tutorial_runoff_connectivity.png")
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# The marked numbers
# ---------------------------------------------------------------------------

def manning(area, width, slope, roughness):
    """Discharge from Manning's equation for a wide channel.

    For a channel much wider than it is deep the hydraulic radius is very close
    to area divided by width, which is the approximation every satellite
    discharge algorithm makes.
    """
    hydraulic_radius = area / width
    return (1.0 / roughness) * area * hydraulic_radius ** (2.0 / 3.0) * math.sqrt(slope)


def report(times, flow, rain, mask, baseline, stormflow):
    """Print every number that the answer sheet quotes."""
    storm_rain = float(np.sum([r for t, r in zip(times, rain)
                               if STORM_RAIN[0] <= t < STORM_RAIN[1]]))
    peak_index = int(np.argmax(flow))
    peak_flow = float(flow[peak_index])
    inside = flow[mask]
    depth = stormflow / AREA_KM2
    ratio = 100.0 * depth / storm_rain

    rain_peak_time = max(((t, r) for t, r in zip(times, rain)
                          if STORM_RAIN[0] <= t < STORM_RAIN[1]),
                         key=lambda p: p[1])[0]

    print("\n" + "=" * 66)
    print("A2  BASEFLOW SEPARATION AND RUNOFF RATIO")
    print("=" * 66)
    print(f"  storm rainfall, 4-6 Feb        {storm_rain:.1f} mm")
    print(f"  pre-storm baseflow             {inside[0]:.0f} ML/day"
          f"  ({inside[0] / AREA_KM2:.2f} mm/day)")
    print(f"  peak discharge                 {peak_flow:,.0f} ML/day"
          f"  ({peak_flow / AREA_KM2:.1f} mm/day)")
    print(f"  peak time                      {times[peak_index]:%Y-%m-%d %H:%M}")
    print(f"  rise above baseflow            {peak_flow / inside[0]:.0f} times")
    print(f"  heaviest rain hour             {rain_peak_time:%Y-%m-%d %H:%M}")
    print(f"  lag, heaviest rain to peak     "
          f"{(times[peak_index] - rain_peak_time).total_seconds() / 3600:.0f} hours")
    print(f"  flow at end of window          {inside[-1]:.0f} ML/day")
    print(f"  stormflow volume               {stormflow:,.0f} ML")
    print(f"  stormflow depth                {depth:.1f} mm")
    print(f"  runoff ratio                   {ratio:.1f} %")
    print(f"  -> at most {ratio:.0f} % of the catchment could have shed all"
          f" its rain")

    print("\n" + "=" * 66)
    print("A1  ISOTOPE SEPARATION")
    print("=" * 66)
    print(f"  pre-event water  {D_PRE:+.1f} permille"
          f"     storm rain  {D_RAIN:+.1f} permille")
    for t, d in D_STREAM:
        f_new = new_water_fraction(d)
        print(f"  {t:%d %b %H:%M}  delta {d:+.1f}"
              f"   f_new {100 * f_new:5.1f} %   f_old {100 * (1 - f_new):5.1f} %")
    f_peak = new_water_fraction(D_STREAM[2][1])
    print(f"  at the peak: {100 * f_peak:.0f} % new, {100 * (1 - f_peak):.0f} % old")
    print(f"  new water at the peak instant  {f_peak * peak_flow:,.0f} ML/day")
    print(f"  NOTE  A2's {ratio:.0f} % is a fraction of the RAINFALL.")
    print(f"        A1's {100 * f_peak:.0f} % is a fraction of the STREAMFLOW.")

    print("\n" + "=" * 66)
    print("A3  SWOT INVERSION")
    print("=" * 66)
    width, slope = 210.0, 4.6e-5
    delta_area = 0.5 * (185.0 + 210.0) * 1.26
    print(f"  measured   W = {width:.0f} m,  S = {slope:.1e},"
          f"  delta A = {delta_area:.0f} m^2")
    print(f"  unknown    n,  A0")
    print(f"  {'A0 (m^2)':>10}  {'n=0.030':>10}  {'n=0.035':>10}  {'n=0.045':>10}")
    for area_zero in (560.0, 700.0, 840.0):
        row = [manning(area_zero + delta_area, width, slope, n)
               for n in (0.030, 0.035, 0.045)]
        print(f"  {area_zero:>10.0f}  " + "  ".join(f"{q:>10.0f}" for q in row))
    best = manning(700.0 + delta_area, width, slope, 0.035)
    low = manning(560.0 + delta_area, width, slope, 0.045)
    high = manning(840.0 + delta_area, width, slope, 0.030)
    print(f"  central estimate {best:.0f} m^3/s;"
          f"  range {low:.0f} to {high:.0f} m^3/s"
          f"  (a factor of {high / low:.1f})")

    print("\n" + "=" * 66)
    print("F1  RATIONAL METHOD, IN SI")
    print("=" * 66)
    uses = [("residential", 0.25, 0.40), ("roads and roofs", 0.15, 0.90),
            ("parkland on sand", 0.25, 0.15), ("remnant woodland", 0.35, 0.10)]
    area_km2, intensity = 2.4, 78.0
    coefficient = sum(f * c for _, f, c in uses)
    discharge = coefficient * intensity * area_km2 / 3.6
    after = coefficient - 0.35 * 0.10 + 0.35 * 0.90
    discharge_after = after * intensity * area_km2 / 3.6
    for name, fraction, c in uses:
        print(f"  {name:<18} {fraction:>5.2f} x {c:.2f} = {fraction * c:.4f}")
    print(f"  C_basin                        {coefficient:.4f}")
    print(f"  Q = C i A / 3.6                {discharge:.1f} m^3/s")
    print(f"  C after hardstand conversion   {after:.4f}")
    print(f"  Q after                        {discharge_after:.1f} m^3/s"
          f"   ({discharge_after / discharge:.2f} times)")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refetch", action="store_true",
                        help="pull from the WaterNSW API instead of the CSV")
    args = parser.parse_args()

    times, flow, rain = load(refetch=args.refetch)
    mask, baseline, stormflow = separate(times, flow)

    for path in (figure_hydrograph(times, flow, rain),
                 figure_separation(times, flow, rain, mask, baseline, stormflow),
                 figure_isotopes(times, flow),
                 figure_swot(),
                 figure_connectivity()):
        print("wrote", os.path.relpath(path))

    report(times, flow, rain, mask, baseline, stormflow)


if __name__ == "__main__":
    main()
