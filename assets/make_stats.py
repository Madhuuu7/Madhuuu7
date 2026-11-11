"""Generate the stats card from real numbers. Dev-only, run to refresh it."""
from __future__ import annotations

import pathlib

OUT = pathlib.Path(r"C:\Users\Madhu\projects\profile\assets\stats.svg")

PAPER, ROSE, DUSTY, CREAM, INK = "#F5E6EE", "#E0BAC6", "#C890A6", "#FFFDFB", "#574A50"

FIGURES = [
    ("8", "public projects"),
    ("6", "live consoles"),
    ("183", "commits"),
    # Not "green": a static image cannot know that, and the live badges
    # above it already say so honestly.
    ("15", "CI workflows"),
]

# Aggregated from the GitHub languages API across all eight repositories.
LANGS = [
    ("Python", 61.5, DUSTY),
    ("TypeScript", 14.5, ROSE),
    ("JavaScript", 13.9, "#D9A7B8"),
    ("HTML", 7.6, "#EBD2DC"),
    ("CSS", 1.9, "#C9ADB8"),
    ("Solidity", 0.6, "#B58AA0"),
]

W, H = 1000, 300
BAR_X, BAR_W, BAR_Y, BAR_H = 40, W - 80, 196, 22

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
    f'role="img" aria-label="Eight public projects, six live consoles, 183 commits, '
    f'fifteen CI workflows; 61.5% Python, 14.5% TypeScript">',
    "  <title>The shape of the work</title>",
    f'  <rect width="{W}" height="{H}" rx="14" fill="{CREAM}"/>',
    f'  <rect width="{W}" height="{H}" rx="14" fill="none" stroke="{ROSE}" stroke-width="2"/>',
    f'  <text x="40" y="52" fill="{DUSTY}" font-family="\'Segoe UI\', system-ui, sans-serif" '
    f'font-size="20" font-weight="600">The shape of the work</text>',
    f'  <text x="40" y="76" fill="{INK}" opacity="0.74" font-family="\'Segoe UI\', system-ui, sans-serif" '
    f'font-size="13.5">Counted from the repositories themselves, not from a service that might be down.</text>',
    f'  <line x1="40" y1="94" x2="{W - 40}" y2="94" stroke="{PAPER}" stroke-width="2"/>',
]

# -- the four figures, evenly spaced ---------------------------------------
slot = (W - 80) / len(FIGURES)
for i, (value, label) in enumerate(FIGURES):
    cx = 40 + slot * i + slot / 2
    parts.append(
        f'  <text x="{cx:.0f}" y="142" text-anchor="middle" fill="{DUSTY}" '
        f'font-family="Georgia, serif" font-size="38">{value}</text>'
    )
    parts.append(
        f'  <text x="{cx:.0f}" y="166" text-anchor="middle" fill="{INK}" opacity="0.8" '
        f'font-family="\'Segoe UI\', system-ui, sans-serif" font-size="13">{label}</text>'
    )
    if i:
        x = 40 + slot * i
        parts.append(
            f'  <line x1="{x:.0f}" y1="112" x2="{x:.0f}" y2="170" stroke="{PAPER}" stroke-width="2"/>'
        )

# -- one stacked bar for the languages -------------------------------------
cursor = BAR_X
for name, pct, colour in LANGS:
    width = BAR_W * pct / 100
    parts.append(
        f'  <rect x="{cursor:.1f}" y="{BAR_Y}" width="{width:.1f}" height="{BAR_H}" fill="{colour}"/>'
    )
    cursor += width
parts.append(
    f'  <rect x="{BAR_X}" y="{BAR_Y}" width="{BAR_W}" height="{BAR_H}" rx="4" fill="none" '
    f'stroke="{CREAM}" stroke-width="0"/>'
)

# -- legend -----------------------------------------------------------------
lx = BAR_X
for name, pct, colour in LANGS:
    parts.append(f'  <circle cx="{lx + 6}" cy="{BAR_Y + 52}" r="5.5" fill="{colour}"/>')
    parts.append(
        f'  <text x="{lx + 18}" y="{BAR_Y + 57}" fill="{INK}" opacity="0.85" '
        f'font-family="\'Segoe UI\', system-ui, sans-serif" font-size="13">{name} {pct}%</text>'
    )
    lx += 26 + len(f"{name} {pct}%") * 7.6

parts.append(
    f'  <text x="{W - 40}" y="{H - 18}" text-anchor="end" fill="{INK}" opacity="0.5" '
    f'font-family="\'Segoe UI\', system-ui, sans-serif" font-size="11.5">'
    f'languages by bytes, across all eight repositories</text>'
)
parts.append("</svg>")

OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
