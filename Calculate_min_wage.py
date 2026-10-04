"""
Minimum Wage vs. Inflation, 1938-2036
Author: Patrick Durbin

Plots the actual U.S. federal minimum wage against two inflation-adjusted
(COLA) lines, with a 10-year projection:
  - Average of all 23 federal minimum wage raises since 1938, adjusted to
    today's dollars and carried through time with CPI
  - The first minimum wage (25 cents, Oct 1938) adjusted every year for CPI
  - The actual federal minimum wage (step line)

Data sources:
  - CPI-U annual averages, U.S. Bureau of Labor Statistics (1982-84 = 100),
    retrieved via FRED (series CPIAUCNS). 2026 uses the August 2026 value.
  - Federal minimum wage history, U.S. Department of Labor.

Requires: Python 3, matplotlib, numpy
    pip install matplotlib numpy
Run:
    python minimum_wage_chart.py
Output:
    minimum_wage_vs_inflation.png
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
OUTPUT_FILE = "minimum_wage_vs_inflation.png"
TODAY = 2026                 # last year of real data
PROJECT_TO = 2036            # end of projection
INFLATION = 0.03             # assumed yearly inflation for the projection
AUTHOR = "Patrick Durbin"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
# CPI-U annual averages (BLS). 2026 = August 2026.
CPI = {
    1938: 14.1, 1939: 13.9, 1940: 14.0, 1941: 14.7, 1942: 16.3, 1943: 17.3,
    1944: 17.6, 1945: 18.0, 1946: 19.5, 1947: 22.3, 1948: 24.1, 1949: 23.8,
    1950: 24.1, 1951: 26.0, 1952: 26.5, 1953: 26.7, 1954: 26.9, 1955: 26.8,
    1956: 27.2, 1957: 28.1, 1958: 28.9, 1959: 29.1, 1960: 29.6, 1961: 29.9,
    1962: 30.2, 1963: 30.6, 1964: 31.0, 1965: 31.5, 1966: 32.4, 1967: 33.4,
    1968: 34.8, 1969: 36.7, 1970: 38.8, 1971: 40.5, 1972: 41.8, 1973: 44.4,
    1974: 49.3, 1975: 53.8, 1976: 56.9, 1977: 60.6, 1978: 65.2, 1979: 72.6,
    1980: 82.4, 1981: 90.9, 1982: 96.5, 1983: 99.6, 1984: 103.9, 1985: 107.6,
    1986: 109.6, 1987: 113.6, 1988: 118.3, 1989: 124.0, 1990: 130.7,
    1991: 136.2, 1992: 140.3, 1993: 144.5, 1994: 148.2, 1995: 152.4,
    1996: 156.9, 1997: 160.5, 1998: 163.0, 1999: 166.6, 2000: 172.2,
    2001: 177.1, 2002: 179.9, 2003: 184.0, 2004: 188.9, 2005: 195.3,
    2006: 201.6, 2007: 207.342, 2008: 215.303, 2009: 214.537, 2010: 218.056,
    2011: 224.939, 2012: 229.594, 2013: 232.957, 2014: 236.736,
    2015: 237.017, 2016: 240.007, 2017: 245.120, 2018: 251.107,
    2019: 255.657, 2020: 258.811, 2021: 270.970, 2022: 292.655,
    2023: 304.702, 2024: 313.689, 2025: 321.943, 2026: 334.980,
}

# Every federal minimum wage raise: (year it took effect, $ per hour)
RAISES = [
    (1938, 0.25), (1939, 0.30), (1945, 0.40), (1950, 0.75), (1956, 1.00),
    (1961, 1.15), (1963, 1.25), (1967, 1.40), (1968, 1.60), (1974, 2.00),
    (1975, 2.10), (1976, 2.30), (1978, 2.65), (1979, 2.90), (1980, 3.10),
    (1981, 3.35), (1990, 3.80), (1991, 4.25), (1996, 4.75), (1997, 5.15),
    (2007, 5.85), (2008, 6.55), (2009, 7.25),
]


def min_wage(year):
    """Federal minimum wage in effect at the end of a given year."""
    rate = 0.0
    for start, wage in RAISES:
        if year >= start:
            rate = wage
    return rate


def in_todays_dollars(wage, year):
    """Convert a wage from a past year into TODAY's dollars."""
    return wage * CPI[TODAY] / CPI[year]


# ---------------------------------------------------------------------------
# Build the series
# ---------------------------------------------------------------------------
years = sorted(CPI)
actual = [min_wage(y) for y in years]

# Line 1: first minimum wage (25 cents in 1938) adjusted each year
first_wage_cola = [0.25 * CPI[y] / CPI[1938] for y in years]

# Line 2: average of every raise, converted to today's dollars, then carried
# back through time with CPI so the line shows that same buying power each year
avg_today = sum(in_todays_dollars(w, y) for y, w in RAISES) / len(RAISES)
average_cola = [avg_today * CPI[y] / CPI[TODAY] for y in years]

# Projection years and values
proj_years = list(range(TODAY, PROJECT_TO + 1))
proj_avg = [average_cola[-1] * (1 + INFLATION) ** (y - TODAY) for y in proj_years]
proj_first = [first_wage_cola[-1] * (1 + INFLATION) ** (y - TODAY) for y in proj_years]
actual_now = actual[-1]

# 1968 peak in today's dollars (for the annotation)
peak_1968_today = in_todays_dollars(1.60, 1968)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
SURFACE = "#fcfcfb"
TEXT_1 = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e6e5e1"
PROJ_BG = "#efeeea"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
GREEN = "#1baf7a"
DASH = (0, (4, 3))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 15})
fig, ax = plt.subplots(figsize=(10.8, 13.5), dpi=100)   # 1080 x 1350 px
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
fig.subplots_adjust(left=0.10, right=0.85, top=0.76, bottom=0.13)

# Projection band
ax.axvspan(TODAY, PROJECT_TO + 0.6, color=PROJ_BG, lw=0)
ax.text((TODAY + PROJECT_TO) / 2 + 0.3, 19.3,
        f"PROJECTION\n{INFLATION:.0%} inflation/yr",
        ha="center", fontsize=12, color=TEXT_2, fontweight="bold", linespacing=1.3)

# Lines
ax.plot(years, average_cola, color=BLUE, lw=3)
ax.plot(proj_years, proj_avg, color=BLUE, lw=3, ls=DASH)
ax.plot(years, first_wage_cola, color=GREEN, lw=3)
ax.plot(proj_years, proj_first, color=GREEN, lw=3, ls=DASH)
ax.step(years, actual, where="post", color=ORANGE, lw=3)
ax.plot([TODAY, PROJECT_TO], [actual_now, actual_now], color=ORANGE, lw=3, ls=DASH)

# Axes
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.grid(axis="y", color=GRID, lw=1)
ax.set_axisbelow(True)
ax.tick_params(colors=TEXT_2, length=0, labelsize=14)
ax.set_xlim(1936, PROJECT_TO + 0.6)
ax.set_ylim(0, 20.5)
ax.set_yticks(range(0, 21, 4))
ax.set_yticklabels([f"${v}" for v in range(0, 21, 4)])
ax.set_xticks([1938, 1950, 1970, 1990, 2010, TODAY, PROJECT_TO])

# Dots at today and at the end of the projection
for value, color in ((average_cola[-1], BLUE), (first_wage_cola[-1], GREEN), (actual_now, ORANGE)):
    ax.scatter([TODAY], [value], s=60, color=color, zorder=5, edgecolor=SURFACE, linewidth=2)
for value, color in ((proj_avg[-1], BLUE), (proj_first[-1], GREEN), (actual_now, ORANGE)):
    ax.scatter([PROJECT_TO], [value], s=80, color=color, zorder=5, edgecolor=SURFACE, linewidth=2)


def label(x, value, caption, dx, dy, ha):
    """Bold dollar value with a small caption under it."""
    ax.annotate(f"${value:.2f}", (x, value), xytext=(dx, dy), textcoords="offset points",
                ha=ha, va="center", fontsize=16 if x == TODAY else 18,
                fontweight="bold", color=TEXT_1, annotation_clip=False)
    ax.annotate(caption, (x, value), xytext=(dx, dy - (18 if x == TODAY else 21)),
                textcoords="offset points", ha=ha, va="center",
                fontsize=11.5 if x == TODAY else 12, color=TEXT_2, annotation_clip=False)


# Labels where the projection starts (today)
label(TODAY, average_cola[-1], "average today", -12, 26, "right")
label(TODAY, actual_now, "actual today", -12, -18, "right")
label(TODAY, first_wage_cola[-1], "1938 base today", 8, -30, "left")

# Labels at the end of the projection
label(PROJECT_TO, proj_avg[-1], "average", 10, 0, "left")
label(PROJECT_TO, proj_first[-1], "1938 base", 10, 22, "left")
label(PROJECT_TO, actual_now, "if never raised", 10, -16, "left")

# Historical notes
ax.annotate("First minimum wage:\n25¢ in Oct 1938", (1938, 0.25), xytext=(2, 30),
            textcoords="offset points", fontsize=13, color=TEXT_2)
ax.annotate(f"1968 peak: $1.60\n(worth ~${peak_1968_today:.2f} today)", (1968, 1.60),
            xytext=(-70, 70), textcoords="offset points", fontsize=13, color=TEXT_2,
            arrowprops=dict(arrowstyle="-", color=TEXT_2, lw=1))

# Title, subtitle, legend
fig.text(0.06, 0.955, f"Minimum Wage vs. Inflation, 1938–{PROJECT_TO}",
         fontsize=29, fontweight="bold", color=TEXT_1)
fig.text(0.06, 0.92, "What the minimum wage would be if it rose with prices every year",
         fontsize=16, color=TEXT_2)
legend_items = [
    (BLUE, f"Average of all {len(RAISES)} raises since 1938, with COLA"),
    (GREEN, "With COLA from the first one, 1938 (25¢)"),
    (ORANGE, "Actual federal minimum wage"),
]
for i, (color, text) in enumerate(legend_items):
    y = 0.875 - i * 0.03
    fig.add_artist(plt.Line2D([0.06, 0.095], [y + 0.006, y + 0.006], color=color, lw=3,
                              transform=fig.transFigure))
    fig.text(0.105, y, text, fontsize=15, color=TEXT_1)
fig.text(0.06, 0.79,
         "Blue = each raise adjusted to today's dollars, then averaged. Dashed = projection.",
         fontsize=12.5, color=TEXT_2, style="italic")

# Footer: method, sources, author
fig.text(0.06, 0.035,
         "Dollars per hour. COLA = starting wage × (CPI that year ÷ CPI in start year). "
         f"{TODAY} uses Aug CPI.\n"
         "Sources: U.S. Bureau of Labor Statistics CPI-U (via FRED); "
         "U.S. Dept. of Labor minimum wage history.\n"
         f"Chart and Python code by {AUTHOR}",
         fontsize=11.5, color=TEXT_2, linespacing=1.5)

fig.savefig(OUTPUT_FILE, facecolor=SURFACE)
print(f"Saved {OUTPUT_FILE}")
print(f"Average of all raises in {TODAY} dollars: ${avg_today:.2f}")
