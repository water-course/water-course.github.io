#!/usr/bin/env python3
"""Render every figure used in the precipitation lecture onto its own page.

The output PDF exists for one purpose: to be uploaded to NotebookLM as a source
so that Video Overviews draw the course's real figures instead of inventing
watercolour substitutes. NotebookLM runs a "visual crop" pass over image-bearing
sources and lifts charts and diagrams out of them, so the figures need to sit
alone on a white page with plenty of margin rather than two-up inside a coloured
container the way they appear on the slides.

Each page carries a stable identifier (FIG-P01 ...) printed under the figure.
The markdown notes in slides/notes/precipitation/ cite those identifiers, which
is what lets a segment prompt say "use FIG-P07 here" and be understood.

Usage:
    python3 make_figure_pack.py

Writes slides/notes/precipitation/Precipitation-Figures.pdf.
"""

import io
import re
from pathlib import Path

import fitz
from PIL import Image

HERE = Path(__file__).resolve().parent
SLIDES = HERE.parent
IMAGES = SLIDES / "image"
OUT = SLIDES / "notes" / "precipitation" / "Precipitation-Figures.pdf"

# A4 portrait, in PDF points. The figures are placed at native resolution and
# merely scaled by the placement rectangle, so page size sets layout, not quality.
PAGE_W, PAGE_H = 595, 842
MARGIN = 43
CAPTION_H = 200
MAX_EDGE = 2000

# (id, filename, headline, caption). Ordered as the figures appear in the
# lecture, so the pack reads as a companion to the deck. The caption is written
# for the video model, not for a student: it says what the figure shows and what
# point it is being used to make, because that is what decides whether the crop
# lands on the right slide.
FIGURES = [
    ("FIG-P01", "internet_NOAprecipitation.gif",
     "Global precipitation, animated",
     "NOAA animation of precipitation moving across the globe. Opening image of the "
     "lecture, used to establish that rainfall is a field in constant motion, not a "
     "set of static totals. Source: scijinks.gov."),
    ("FIG-P02", "internet_rainsleethail.webp",
     "Rain, sleet, hail and snow",
     "The four forms precipitation takes, shown side by side with the vertical "
     "temperature profile that produces each. Use whenever the segment needs to make "
     "the point that 'precipitation' covers all phases, not just rain."),
    ("FIG-P03", "davie_ed3_fig_2-1.png",
     "Saturation vapour pressure against temperature",
     "Davie & Quinn 3rd ed., Fig. 2.1. Saturation vapour pressure rises steeply and "
     "non-linearly with temperature; the solid curve is over water, the dotted curve "
     "over ice and lies BELOW it. This single figure carries three separate teaching "
     "points: the Clausius-Clapeyron relation, the dew point, and the ice-water gap "
     "that drives the Bergeron process. The gap between the two curves is the detail "
     "that matters."),
    ("FIG-P04", "internet_Adiabatic_lapse_rate.png",
     "Adiabatic and environmental lapse rates",
     "A parcel of air rising and cooling, with the dry adiabatic lapse rate (about "
     "9.8 C/km), the saturated adiabatic lapse rate (about 4-6 C/km, shallower "
     "because condensation releases latent heat) and the environmental lapse rate "
     "(about 6 C/km) drawn as separate lines on a temperature-height plot."),
    ("FIG-P05", "internet_meteorology_uplift.jpg",
     "Four lifting mechanisms",
     "Four labelled panels: (a) convective, warm air rising from a heated surface; "
     "(b) orographic, air cooling adiabatically to dew point as it climbs a range, "
     "with a rain shadow marked on the lee side where descending air warms; "
     "(c) frontal, warm air riding up over a cold air mass along a front; and "
     "(d) convergent, air converging at the surface and forced upward. Note the "
     "figure has FOUR panels; the slide text lists only three."),
    ("FIG-P06", "internet_cloud_seeding.webp",
     "Cloud seeding",
     "An aircraft dispersing seeding agent into a cloud. Illustrates the practical "
     "consequence of condensation nuclei being the limiting factor: supply artificial "
     "nuclei (silver iodide, or more recently potassium chloride) and you may "
     "precipitate a cloud that would otherwise stay supersaturated."),
    ("FIG-P07", "davie_ed3_fig_2-2.png",
     "Cloud droplet against raindrop, to scale",
     "Davie & Quinn 3rd ed., Fig. 2.2. Circles drawn at relative scale and annotated "
     "with RADIUS, number concentration and terminal velocity: condensation nucleus "
     "1 um, 10^12 per m3, 10^-7 m/s; typical cloud drop 10 um, 10^9 per m3, 10^-3 m/s; "
     "large cloud drop 50 um, 10^6 per m3, 0.27 m/s; conventional cloud-drop / raindrop "
     "borderline at 100 um, 0.7 m/s; typical raindrop 1000 um, 10^3 per m3, 6.5 m/s. "
     "The whole growth problem in one image, and the terminal velocity column is the "
     "part that matters: a cloud drop falls a thousand times slower than a raindrop."),
    ("FIG-P08", "internet_collisionmodel2.jpg",
     "Collision, coalescence and breakup",
     "Four stacked panels A to D. A: a large cloud droplet among small ones, with "
     "updraught arrows. B: it has swept up others and become a raindrop. C: the large "
     "drop breaks apart due to instability. D: the fragments become new collector "
     "drops and the cycle repeats. The breakup step in panel C is why raindrops have "
     "an upper size limit and is not mentioned on the slide."),
    ("FIG-P09", "davie_3rd_fig_2-3.png",
     "Cloud types by height and form",
     "Davie & Quinn 3rd ed., Fig. 2.3. The standard cloud classification arranged by "
     "altitude, from cirrus at the top through altostratus to stratus and cumulonimbus. "
     "Provides the vocabulary for talking about which clouds rain and why."),
    ("FIG-P10", "internet_hail.jpg",
     "Hailstones",
     "Hailstones photographed in the hand for scale, showing the concentric layering "
     "visible in cross-section. Alternating clear and opaque bands record repeated "
     "circulation through the updraught of a cumulonimbus."),
    ("FIG-P11", "davie_fig_2-4.png",
     "Annual precipitation across the USA, 1996",
     "National Atmospheric Deposition Program map. Wet in the Pacific Northwest "
     "(Oregon, Washington) from north Pacific cyclonic systems, wet in Florida and the "
     "southeast from the warm Caribbean, dry through the interior. Used to argue that "
     "topography alone does not explain the pattern; dynamic controls do the rest."),
    ("FIG-P12", "davie_fig_2-5-a.png",
     "South Island of New Zealand, relief",
     "Davie & Quinn Fig. 2.5a. The South Island with land above 1500 m shaded, showing "
     "the Southern Alps running the length of the island across the path of the "
     "prevailing westerlies. The setup for the rain shadow."),
    ("FIG-P13", "davie_fig_2-5-b.png",
     "Rainfall transect across the Southern Alps",
     "Davie & Quinn Fig. 2.5b. Rainfall plotted along a west-to-east transect: very "
     "high on the west coast, peaking near the divide, then collapsing on the eastern "
     "side. The rain shadow effect as a number rather than an idea. Pair with FIG-P12."),
    ("FIG-P14", "internet_mareeba_earth.png",
     "Mareeba elevation profile",
     "Google Earth terrain view with an elevation profile for moist air arriving from "
     "the east over the Queensland coastal range and descending towards Mareeba. The "
     "Australian instance of the same mechanism as the Southern Alps."),
    ("FIG-P15", "internet_storm_tracks.webp",
     "Global tropical storm tracks",
     "Composite map of tropical cyclone tracks. Roughly 80 tropical storms form "
     "annually, about two thirds reaching category 1 or above, and nearly 90 per cent "
     "form within 20 degrees of the equator. The clearest single image of a dynamic "
     "control on precipitation."),
    ("FIG-P16", "internet_precipitation_measurement.jpg",
     "Measuring rainfall looks easy",
     "A rain gauge in the field. Used ironically: the image opens the measurement "
     "section precisely because the apparatus looks trivial and the error budget is not."),
    ("FIG-P17", "davie_fig_2-6-a.png",
     "Fourteenth-century Korean rain gauge",
     "Davie & Quinn Fig. 2.6a. Photograph of a cylindrical bronze gauge standing on a "
     "carved stone pedestal, the characters for 'measure rain' cut into the stone. A "
     "standardised national rain gauge network, six centuries ago."),
    ("FIG-P18", "davie_fig_2-6-b.png",
     "Modern raised rain gauge",
     "Davie & Quinn Fig. 2.6b. Photograph of a small cylindrical gauge on a post above "
     "long grass, clear of surrounding vegetation. Raising the gauge is a trade: it "
     "solves splash and creates a wind turbulence problem."),
    ("FIG-P19", "internet_tippingbucketrain.webp",
     "Tipping bucket rain gauge",
     "Cutaway of a tipping bucket gauge showing the funnel narrowing to a small "
     "orifice above a see-saw of two small buckets. The funnel is not incidental: it "
     "shades the collected water and restricts air exchange, which is how evaporation "
     "loss is controlled. Each tip is a fixed depth, 0.2 mm in Australian practice."),
    ("FIG-P20", "internet_tippingbucketrain_metal.webp",
     "Steep-sided metal tipping bucket",
     "A tipping bucket with steep, non-stick metal funnel walls. The design response to "
     "wetting loss, where water clings to the funnel and never reaches the mechanism."),
    ("FIG-P21", "davie_fig_2-7.png",
     "Ground-level gauge in a non-splash grid",
     "Davie & Quinn Fig. 2.7. Field photograph of a gauge set flush with the ground in "
     "the centre of a square slatted anti-splash grid, in rough grass. The closest "
     "thing to an ideal gauge, and unusable anywhere it snows because it buries."),
    ("FIG-P22", "davie_fig_2-8.png",
     "Airflow over a raised gauge",
     "Davie & Quinn Fig. 2.8. Line diagram: horizontal streamlines approaching a "
     "cylindrical gauge, deflecting up and over the orifice, with small arrows showing "
     "flow lifting off the rim. The mechanism of under-catch, drawn plainly. THE SLIDE "
     "CAPTION FOR THIS FIGURE IS WRONG: it describes a two-panel figure with baffles, "
     "which is FIG-P23."),
    ("FIG-P23", "davie_fig_2-9.png",
     "Slatted wind shield around a gauge",
     "Davie & Quinn Fig. 2.9. Photograph of a gauge encircled by a ring of angled metal "
     "slats (an Alter-type shield) in a grassy field. The standard fix for wind "
     "under-catch, which reaches roughly 20 per cent at 20 km/h and roughly 40 per cent "
     "at 90 km/h, and worsens as drop size falls. THE SLIDE CAPTION FOR THIS FIGURE IS "
     "WRONG: it calls this turbulent flow over an elevated gauge, which is FIG-P22."),
    ("FIG-P24", "internet_BoMRainGauge.jpg",
     "Bureau of Meteorology standard gauge",
     "The Australian standard 203 mm manual gauge, mounted 0.3 m above ground, read into "
     "a graduated cylinder. Read at 9 am daily, in very many cases by volunteers."),
    ("FIG-P25", "internet_snow_gauge.png",
     "Shielded snow gauge",
     "Photograph of a gauge raised on a pedestal inside a ring of white angled slats, "
     "the shield opening upward like a flower. Colour photograph, blue instrument. "
     "Shows the wind shielding a snow gauge needs; the heated rim and the drainage "
     "path described on the slide are internal and not visible here."),
    ("FIG-P26", "davie_fig_4-12.png",
     "Snow pillow",
     "Davie & Quinn Fig. 4.12. Cutaway diagram: layers of snow drawn as a curved "
     "stack, with a flat fluid-filled bladder labelled 'snow pillow' lying beneath "
     "them and a 'pressure gauge' attached at one side. It weighs the snow above it, "
     "so it measures stored water mass rather than depth, which is what matters for "
     "forecasting delayed melt runoff."),
    ("FIG-P27", "davie_fig_2-13.png",
     "Thiessen polygons over a catchment",
     "Davie & Quinn Fig. 2.13. Gauges within and around a catchment boundary, with "
     "perpendicular bisectors dividing the area into polygons, one per gauge. Each "
     "polygon is the region closer to its gauge than to any other. Areal rainfall is "
     "the area-weighted sum of the gauge readings."),
    ("FIG-P28", "davie_3rd_fig_2-14.png",
     "Hypsometric and isohyetal estimation",
     "Davie & Quinn 3rd ed., Fig. 2.14. The same catchment outline as FIG-P27, but "
     "divided by curved contour lines into four elevation bands labelled a1 to a4, "
     "with six gauges r1 to r6 scattered across them and two bands shaded. Unsampled "
     "points are assumed to share the rainfall of sampled points at the same altitude. "
     "The identical figure serves the isohyetal method if the contours are read as "
     "lines of equal rainfall instead of equal elevation."),
    ("FIG-P29", "internet_googlemaps_sierraNevada.png",
     "Sierra Nevada west-east transect",
     "Google Earth terrain transect from the Pacific coast across the Sierra Nevada "
     "crest to Bishop in the Owens Valley. This is the tutorial figure: students mark "
     "the zone of maximum orographic precipitation on the western flank and the rain "
     "shadow in the Owens Valley, then apply lapse rates along it."),
]

TITLE_PAGE = (
    "Precipitation — Figure Pack",
    "EMSC3025/6025 · Water in the Landscape",
    "Every figure used in the Precipitation lecture and tutorial, one per page, at "
    "native resolution. Cite figures by the identifier printed beneath each one "
    "(FIG-P01 to FIG-P29); the section notes refer to them by that identifier and "
    "nothing else.",
)



def prepare_figure(filename):
    """Load a figure, flatten transparency onto white, return it as PNG bytes.

    Returned at NATIVE resolution and never resampled. Scaling is left to the PDF
    placement rectangle, so the embedded image object a consumer extracts is the
    original figure rather than a resized copy of it.
    """
    src = Image.open(IMAGES / filename)
    # Animated GIF/WebP: take the first frame. Nothing downstream can use motion.
    if getattr(src, "n_frames", 1) > 1:
        src.seek(0)
    # Several figures carry an alpha channel. A plain convert("RGB") turns every
    # transparent pixel black, which frames the figure in a heavy black border and
    # gives the crop pass an edge to latch onto that is not the figure. Composite
    # onto white instead.
    src = src.convert("RGBA")
    flat = Image.new("RGBA", src.size, (255, 255, 255, 255))
    src = Image.alpha_composite(flat, src).convert("RGB")

    # Cap the long edge. The placement box is about 500 pt, so 2000 px is still
    # ~290 dpi -- well beyond what any consumer needs -- while keeping the pack small
    # enough to upload. The first build shipped everything at native size and came to
    # 28 MB, which took over two minutes to push to NotebookLM.
    if max(src.width, src.height) > MAX_EDGE:
        s = MAX_EDGE / max(src.width, src.height)
        src = src.resize((round(src.width * s), round(src.height * s)),
                         Image.LANCZOS)

    buf = io.BytesIO()
    src.save(buf, format="PNG", optimize=True)
    # Line art and charts compress to almost nothing as PNG and must stay lossless,
    # because their content is thin black strokes and small annotations. Photographs
    # do not, and a photograph left as PNG dominates the pack: the section 7 pack came
    # to 2.8 MB largely because one gauge photograph stored as PNG was 1 MB on its own,
    # and that pack was the only one whose video generation failed, twice. The
    # threshold is deliberately low, so anything photographic falls through to JPEG.
    if buf.tell() > 300_000:
        buf = io.BytesIO()
        src.save(buf, format="JPEG", quality=85, optimize=True)
    return buf.getvalue(), src.width, src.height


def add_figure_page(doc, fig_id, filename, headline, caption):
    """One figure per page: a single embedded image object, plus real text.

    The first version of this script drew each page with Pillow and saved the
    result as a full-page raster. That produced a PDF whose every page was one
    1654x2339 image with no text layer at all, and it failed its only purpose:
    NotebookLM's visual-crop pass extracts embedded image objects, and a page-sized
    object crops to the whole page, caption and all. The FIG-Pxx identifiers were
    not machine-readable either, so the notes' "use FIG-P03" instruction had nothing
    to bind to. Verified by generating segment 01 from the raster pack: across 9m18s
    of video, not one figure was lifted.

    So the figure goes in as its own image XObject at native resolution, and every
    piece of text goes in as text.
    """
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    png, w, h = prepare_figure(filename)

    box_w = PAGE_W - 2 * MARGIN
    box_h = PAGE_H - CAPTION_H - 2 * MARGIN
    scale = min(box_w / w, box_h / h, 2.0)
    dw, dh = w * scale, h * scale
    x = (PAGE_W - dw) / 2
    y = MARGIN + (box_h - dh) / 2
    page.insert_image(fitz.Rect(x, y, x + dw, y + dh), stream=png)

    ty = PAGE_H - CAPTION_H
    page.draw_line(fitz.Point(MARGIN, ty), fitz.Point(PAGE_W - MARGIN, ty),
                   color=(0.6, 0.6, 0.6), width=2)

    ty += 22
    page.insert_text(fitz.Point(MARGIN, ty), fig_id, fontname="hebo",
                     fontsize=13, color=(0.69, 0.23, 0.18))
    # Shrink the headline until it fits beside the identifier rather than running
    # off the page edge, which silently truncated the longer titles.
    head_x, size = MARGIN + 62, 14
    while (fitz.get_text_length(headline, fontname="hebo", fontsize=size)
           > PAGE_W - MARGIN - head_x and size > 8):
        size -= 1
    page.insert_text(fitz.Point(head_x, ty), headline, fontname="hebo",
                     fontsize=size, color=(0, 0, 0))

    # insert_textbox silently drops the whole string if it does not fit, so give it
    # generous room and check the return value rather than trusting it. The first
    # vector build left a 34 pt box here and every caption vanished.
    ty += 18
    box = fitz.Rect(MARGIN, ty, PAGE_W - MARGIN, PAGE_H - 26)
    if page.insert_textbox(box, caption, fontname="helv", fontsize=9.5,
                           color=(0.13, 0.13, 0.13), lineheight=1.35) < 0:
        raise SystemExit(f"caption does not fit on {fig_id}; enlarge CAPTION_H")

    page.insert_text(fitz.Point(MARGIN, PAGE_H - 14),
                     f"source file: {filename}", fontname="helv",
                     fontsize=7, color=(0.47, 0.47, 0.47))


def add_title_page(doc):
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    title, subtitle, blurb = TITLE_PAGE
    page.insert_text(fitz.Point(MARGIN, 120), title, fontname="hebo", fontsize=22)
    page.insert_text(fitz.Point(MARGIN, 142), subtitle, fontname="helv", fontsize=12, color=(0.33, 0.33, 0.33))
    page.insert_textbox(fitz.Rect(MARGIN, 165, PAGE_W - MARGIN, 250), blurb, fontname="helv", fontsize=10, lineheight=1.4)
    y = 265
    for fig_id, _filename, headline, _caption in FIGURES:
        page.insert_text(fitz.Point(MARGIN, y), fig_id,
                         fontname="hebo", fontsize=9, color=(0.69, 0.23, 0.18))
        page.insert_text(fitz.Point(MARGIN + 52, y), headline, fontname="helv", fontsize=9)
        y += 13


def build(path, entries, title_page=True):
    doc = fitz.open()
    if title_page:
        add_title_page(doc)
    for fig_id, filename, headline, caption in entries:
        add_figure_page(doc, fig_id, filename, headline, caption)
    doc.save(path, deflate=True)
    return doc


# Video generation fails outright on a pack of nine figures. Section 7 was the only
# section over five, and it was the only one whose video would not generate: three
# attempts, all "generation_failed ... no media produced". The note alone, with no
# pack, generated fine on the first try, which is what pinned the cause on the pack
# rather than on the note or the prompt. Shrinking the pack's bytes did not help
# (2.8 MB -> 1.05 MB, identical failure), so the limit is on figure count, not size.
#
# Every pack that did generate had five figures or fewer, so cap at five. For a
# section over the cap, list the figures to KEEP here in priority order rather than
# letting it truncate by identifier, which for section 7 would drop exactly the
# turbulence pair the section is built around.
PACK_LIMIT = 5
PACK_PRIORITY = {
    # The four errors and the fix, which is the sequence the note's Visual direction
    # walks through. Dropped: FIG-P16 (scene-setting photo), FIG-P17 (Korean gauge),
    # FIG-P18 (raised gauge), FIG-P24 (BoM gauge) -- all context rather than mechanism.
    "07": ["FIG-P19", "FIG-P20", "FIG-P21", "FIG-P22", "FIG-P23"],
}


def build_per_section_packs():
    """One small pack per section, containing only that section's figures.

    The full 29-figure pack defeats the whole point of scoping a video to a single
    section. Its captions describe every figure in the module, so a video scoped to
    "note 01 + full pack" reads the pack and produces a survey of the entire lecture:
    the first attempt came back with five chapters covering rain shadows, gauge
    under-catch and the history of the rain gauge, none of which are in section 1.

    Scoping only works if every source in scope is about that section. So each
    section gets a pack holding just the figures its note cites. Sections 10 to 13
    cite none, and correctly get no pack at all.
    """
    by_id = {f[0]: f for f in FIGURES}
    made = []
    for note in sorted(OUT.parent.glob("[0-1][0-9]-*.md")):
        num = note.name[:2]
        if num == "14":
            continue
        ids = sorted(set(re.findall(r"FIG-P\d{2}", note.read_text())))
        if not ids:
            print(f"  {num}: no figures, no pack")
            continue
        if len(ids) > PACK_LIMIT:
            keep = PACK_PRIORITY.get(num, ids[:PACK_LIMIT])
            # Never let a cap pass silently -- a pack that quietly lost four figures
            # would look identical to one that never had them.
            dropped = [i for i in ids if i not in keep]
            print(f"  {num}: {len(ids)} figures exceeds PACK_LIMIT={PACK_LIMIT}; "
                  f"DROPPING {' '.join(dropped)}")
            ids = keep
        path = OUT.parent / f"Figures-{num}.pdf"
        build(path, [by_id[i] for i in ids], title_page=False)
        made.append(path)
        print(f"  {num}: {len(ids)} figures -> {path.name}  "
              f"({path.stat().st_size // 1024} kB)  {' '.join(ids)}")
    return made


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    missing = [f for _, f, _, _ in FIGURES if not (IMAGES / f).exists()]
    if missing:
        raise SystemExit(f"missing figures: {missing}")

    build(OUT, FIGURES)
    print(f"full pack: {OUT.name}")
    print("per-section packs:")
    build_per_section_packs()

    # The whole point of the rebuild, so assert it rather than trusting it. A figure
    # page must place its image in a rectangle strictly inside the page (not a
    # full-page flatten), and must carry a real text layer. Compare PLACEMENT
    # rectangles in points, never pixel dimensions against page points -- a 1258x1408
    # px figure dropped into a 400x450 pt box is exactly what we want.
    check = fitz.open(OUT)
    bad = []
    for i, p in enumerate(check):
        if i == 0:
            continue
        rects = [r for xref in {im[0] for im in p.get_images(full=True)}
                 for r in p.get_image_rects(xref)]
        if not rects:
            bad.append((i + 1, "no image object"))
        elif any(r.height > PAGE_H - CAPTION_H for r in rects):
            bad.append((i + 1, "image spans the caption area"))
        elif not p.get_text().strip():
            bad.append((i + 1, "no text layer"))
    if bad:
        raise SystemExit(f"figure pages built wrong: {bad}")
    chars = sum(len(p.get_text().strip()) for p in check)
    print(f"\nwrote {OUT} ({len(check)} pages, "
          f"{sum(len(p.get_images()) for p in check)} embedded image objects, "
          f"{chars} chars of extractable text)")


if __name__ == "__main__":
    main()
