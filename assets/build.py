"""Draw every panel on the profile.

One generator, so the palette, the type scale and the spacing cannot drift
between pieces, and so a number that changes is a one-line edit followed by
`python assets/build.py` rather than a careful search through five files.

Everything here is a static SVG committed to the repository. The profile does
not depend on a third-party card service: while this was being written, the
one most profiles use was answering DEPLOYMENT_PAUSED, which leaves broken
images in the middle of the page it was supposed to decorate.
"""

from __future__ import annotations

import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# -- palette ---------------------------------------------------------------
PAPER = "#F5E6EE"   # blossom, the page tint
CREAM = "#FFFDFB"   # cards
ROSE = "#E0BAC6"    # borders, second accent
DUSTY = "#C890A6"   # titles, the figure colour
INK = "#574A50"     # text
HAIR = "#F0DEE6"    # the faintest rule

SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
SANS = "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', sans-serif"

W = 1000


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def wrap(text: str, width: int) -> list[str]:
    """Greedy wrap. SVG text does not flow, so the lines are decided here."""
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def blossom(cx: float, cy: float, r: float, fill: str, opacity: float = 1.0) -> str:
    """Five petals and a pale centre, drawn small."""
    petals = []
    for dx, dy in ((0, -1.22), (1.16, -0.38), (0.72, 0.99), (-0.72, 0.99), (-1.16, -0.38)):
        petals.append(f'<circle cx="{cx + dx * r:.2f}" cy="{cy + dy * r:.2f}" r="{r:.2f}"/>')
    return (
        f'<g fill="{fill}" opacity="{opacity}">' + "".join(petals)
        + f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r * 0.42:.2f}" fill="{CREAM}"/></g>'
    )


def svg(width: int, height: int, body: str, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{esc(label)}">\n'
        f"  <title>{esc(label)}</title>\n{body}\n</svg>\n"
    )


def card(width: int, height: int, radius: int = 12) -> str:
    return (
        f'  <rect width="{width}" height="{height}" rx="{radius}" fill="{CREAM}"/>\n'
        f'  <rect width="{width}" height="{height}" rx="{radius}" fill="none" '
        f'stroke="{ROSE}" stroke-width="2"/>'
    )


def write(name: str, content: str) -> None:
    path = HERE / name
    path.write_text(content, encoding="utf-8")
    print(f"  {name:<24} {path.stat().st_size:>6,}B")


# -- 1. the hero -----------------------------------------------------------


def hero() -> str:
    h = 250
    body = [
        '  <defs>',
        f'    <linearGradient id="sky" x1="0" y1="0" x2="0.85" y2="1">'
        f'<stop offset="0" stop-color="{PAPER}"/><stop offset="0.5" stop-color="{CREAM}"/>'
        f'<stop offset="1" stop-color="{PAPER}"/></linearGradient>',
        f'    <linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{ROSE}"/><stop offset="1" stop-color="{DUSTY}"/></linearGradient>',
        '  </defs>',
        f'  <rect width="{W}" height="{h}" rx="14" fill="url(#sky)"/>',
        f'  <rect width="{W}" height="{h}" rx="14" fill="none" stroke="{ROSE}" stroke-width="2"/>',
        # two branches, one high left, one low right
        f'  <path d="M -10 58 C 120 30, 232 82, 344 52" fill="none" stroke="{ROSE}" '
        f'stroke-width="2.4" stroke-linecap="round" opacity="0.8"/>',
        f'  <path d="M 1010 196 C 890 220, 796 170, 700 198" fill="none" stroke="{ROSE}" '
        f'stroke-width="2.4" stroke-linecap="round" opacity="0.8"/>',
        blossom(72, 44, 5.4, DUSTY, 0.95),
        blossom(164, 58, 4.2, DUSTY, 0.8),
        blossom(254, 68, 4.8, DUSTY, 0.65),
        blossom(330, 46, 3.6, ROSE, 0.6),
        blossom(900, 190, 5.2, DUSTY, 0.9),
        blossom(812, 204, 4.0, DUSTY, 0.7),
        blossom(728, 186, 4.6, ROSE, 0.6),
        blossom(120, 168, 3.2, ROSE, 0.5),
        blossom(946, 62, 3.4, ROSE, 0.5),
        # the eyebrow
        f'  <text x="{W/2}" y="56" text-anchor="middle" fill="{INK}" opacity="0.62" '
        f'font-family="{SANS}" font-size="12.5" letter-spacing="3.2">'
        f'BENGALURU, INDIA &#183; COMPUTER SCIENCE &#183; 2027</text>',
        # the name
        f'  <text x="{W/2}" y="122" text-anchor="middle" fill="{INK}" '
        f'font-family="{SERIF}" font-size="56" letter-spacing="1.2">Madhura M R</text>',
        f'  <rect x="{W/2 - 94}" y="140" width="188" height="3" rx="1.5" fill="url(#ribbon)"/>',
        # the role line
        f'  <text x="{W/2}" y="174" text-anchor="middle" fill="{DUSTY}" '
        f'font-family="{SANS}" font-size="17.5" font-weight="600" letter-spacing="0.4">'
        f'Backend &#183; Applied ML &#183; Systems that measure themselves</text>',
        f'  <text x="{W/2}" y="200" text-anchor="middle" fill="{INK}" opacity="0.78" '
        f'font-family="{SANS}" font-size="14">'
        f'Six public systems, each with a console you can open. Growing one commit at a time.</text>',
        # the availability pill
        # The pill is sized around the text rather than guessed at: 33
        # characters at 11.5px with 1.1 of tracking is about 250px, and the
        # blossom needs its own 24px to the left of that or it prints on
        # top of the first letter.
        f'  <rect x="{W/2 - 158}" y="214" width="316" height="26" rx="13" fill="{PAPER}" '
        f'stroke="{ROSE}" stroke-width="1.5"/>',
        blossom(W / 2 - 138, 227, 3.6, DUSTY),
        f'  <text x="{W/2 + 16}" y="231" text-anchor="middle" fill="{DUSTY}" '
        f'font-family="{SANS}" font-size="11.5" letter-spacing="1.1">'
        f'OPEN TO SOFTWARE &#38; ML INTERNSHIPS</text>',
    ]
    return svg(W, h, "\n".join(body), "Madhura M R — backend, applied ML, systems that measure themselves")


# -- 2. section bars -------------------------------------------------------


def section(number: str, title: str, subtitle: str) -> str:
    h = 52
    body = [
        card(W, h, 10),
        blossom(30, h / 2, 5.0, DUSTY),
        f'  <text x="48" y="{h/2 + 5}" fill="{DUSTY}" font-family="{SANS}" '
        f'font-size="13" font-weight="600" letter-spacing="1.4">{number}</text>',
        f'  <text x="78" y="{h/2 + 6}" fill="{INK}" font-family="{SANS}" '
        f'font-size="17.5" font-weight="600">{esc(title)}</text>',
        f'  <text x="{W - 24}" y="{h/2 + 5}" text-anchor="end" fill="{INK}" opacity="0.6" '
        f'font-family="{SANS}" font-size="13">{esc(subtitle)}</text>',
    ]
    return svg(W, h, "\n".join(body), f"{number} {title} — {subtitle}")


# -- 3. about: a statement, and a whoami table -----------------------------


ABOUT_POINTS = [
    ("Measure, do not assert", "every claim in these repositories has a run behind it"),
    ("Test the failure", "the crash, the dead dependency, the judge that cannot rule"),
    ("State the limits", "each README says what the project cannot do, next to what it can"),
]

WHOAMI = [
    ("role", "Computer science undergraduate, 2027"),
    ("focus", "Backend services, applied ML, distributed systems"),
    ("languages", "Python, TypeScript, SQL, a little Solidity"),
    ("ml", "scikit-learn, pandas, NumPy, conformal prediction"),
    ("backend", "FastAPI, asyncio, Postgres, MongoDB, Docker"),
    ("frontend", "React, Vite, hand-written SVG when a chart has to be honest"),
    ("ci", "GitHub Actions on every push, benchmarks included"),
    ("proof", "6 live consoles, 183 commits, 15 workflows"),
]


def about() -> str:
    h = 332
    gap, left_w = 20, 452
    right_x = left_w + gap
    right_w = W - right_x
    body = [f'  <rect width="{W}" height="{h}" fill="none"/>']

    # left card
    body.append(f'  <g><rect width="{left_w}" height="{h}" rx="12" fill="{CREAM}"/>'
                f'<rect width="{left_w}" height="{h}" rx="12" fill="none" stroke="{ROSE}" stroke-width="2"/></g>')
    body.append(f'  <text x="26" y="40" fill="{DUSTY}" font-family="{SANS}" font-size="11.5" '
                f'letter-spacing="2.4">WHAT I OPTIMISE FOR</text>')
    for i, line in enumerate(wrap("I build systems that check their own claims.", 26)):
        body.append(f'  <text x="26" y="{82 + i * 30}" fill="{INK}" font-family="{SERIF}" '
                    f'font-size="25">{esc(line)}</text>')
    y = 162
    for title, detail in ABOUT_POINTS:
        body.append(blossom(33, y - 4, 4.4, DUSTY, 0.9))
        body.append(f'  <text x="48" y="{y}" fill="{INK}" font-family="{SANS}" font-size="14" '
                    f'font-weight="600">{esc(title)}</text>')
        for j, line in enumerate(wrap(detail, 48)):
            body.append(f'  <text x="48" y="{y + 18 + j * 16}" fill="{INK}" opacity="0.72" '
                        f'font-family="{SANS}" font-size="12.5">{esc(line)}</text>')
        y += 50

    # right card: whoami
    body.append(f'  <g transform="translate({right_x} 0)">')
    body.append(f'    <rect width="{right_w}" height="{h}" rx="12" fill="{CREAM}"/>'
                f'<rect width="{right_w}" height="{h}" rx="12" fill="none" stroke="{ROSE}" stroke-width="2"/>')
    body.append(f'    <text x="24" y="36" fill="{DUSTY}" font-family="{SANS}" font-size="12.5">'
                f'madhura@github ~ $ whoami</text>')
    body.append(f'    <line x1="24" y1="50" x2="{right_w - 24}" y2="50" stroke="{HAIR}" stroke-width="2"/>')
    ty = 76
    for key, value in WHOAMI:
        body.append(f'    <text x="24" y="{ty}" fill="{DUSTY}" font-family="{SANS}" '
                    f'font-size="12.5" font-weight="600">{key}</text>')
        for j, line in enumerate(wrap(value, 44)):
            body.append(f'    <text x="116" y="{ty + j * 15}" fill="{INK}" opacity="0.85" '
                        f'font-family="{SANS}" font-size="12.5">{esc(line)}</text>')
        ty += 15 * max(1, len(wrap(value, 44))) + 12
    body.append("  </g>")
    return svg(W, h, "\n".join(body), "About — I build systems that check their own claims")


# -- 4. project cards ------------------------------------------------------

PROJECTS = [
    {
        "file": "card-gridcast.svg", "eyebrow": "01 · FORECASTING", "name": "gridcast",
        "line": "Day-ahead load forecasts for the Delhi grid, in 96 settlement blocks.",
        "figure": "5.07%", "caption": "MAPE across 32,391 out-of-sample blocks, 51% better than seasonal naive",
        "tags": ["Python", "scikit-learn", "FastAPI", "Postgres"],
    },
    {
        "file": "card-relay.svg", "eyebrow": "02 · LLM INFRASTRUCTURE", "name": "relay",
        "line": "A gateway that routes on live latency, errors and queue depth.",
        "figure": "−71.8%", "caption": "p95 latency, 4,640 ms to 1,308 ms, replayed over 4,000 requests in CI",
        "tags": ["Python", "asyncio", "FastAPI", "React"],
    },
    {
        "file": "card-revenant.svg", "eyebrow": "03 · DURABLE EXECUTION", "name": "revenant",
        "line": "An agent runtime where a crash is a cursor position in a log.",
        "figure": "140/140", "caption": "journal boundaries killed and recovered, zero duplicate effects",
        "tags": ["Python", "MongoDB", "FastAPI", "React"],
    },
    {
        "file": "card-transitlab.svg", "eyebrow": "04 · ALGORITHMS", "name": "transitlab",
        "line": "RAPTOR from scratch, then ported so it routes in your browser tab.",
        "figure": "37 ms", "caption": "a query in the browser, against 1,373 ms for the same algorithm in Python",
        "tags": ["TypeScript", "Python", "GTFS", "Vite"],
    },
    {
        "file": "card-verdict.svg", "eyebrow": "05 · STATISTICS", "name": "verdict",
        "line": "A regression gate that calibrates its judge before trusting it.",
        "figure": "46.7%", "caption": "false alarms from re-testing every case, against 5.9% for one look",
        "tags": ["Python", "NumPy", "FastAPI"],
    },
    {
        "file": "card-nanofaas.svg", "eyebrow": "06 · PLATFORMS", "name": "nanofaas",
        "line": "Scale-to-zero functions that measure their own cold-start tax.",
        "figure": "1,028×", "caption": "a cold start against a 1.64 ms warm call, 75% of it interpreter boot",
        "tags": ["Python", "Docker", "FastAPI"],
    },
]


def project_card(spec: dict) -> str:
    w, h = 490, 214
    body = [
        f'  <rect width="{w}" height="{h}" rx="12" fill="{CREAM}"/>',
        f'  <rect width="{w}" height="{h}" rx="12" fill="none" stroke="{ROSE}" stroke-width="2"/>',
        f'  <rect x="0" y="0" width="{w}" height="4" rx="2" fill="{DUSTY}" opacity="0.55"/>',
        f'  <text x="24" y="34" fill="{ROSE}" font-family="{SANS}" font-size="10.5" '
        f'letter-spacing="2">{esc(spec["eyebrow"])}</text>',
        f'  <text x="24" y="62" fill="{INK}" font-family="{SERIF}" font-size="26">{esc(spec["name"])}</text>',
        blossom(w - 28, 30, 5.0, ROSE, 0.75),
    ]
    for i, line in enumerate(wrap(spec["line"], 52)):
        body.append(f'  <text x="24" y="{86 + i * 17}" fill="{INK}" opacity="0.76" '
                    f'font-family="{SANS}" font-size="12.5">{esc(line)}</text>')
    body.append(f'  <line x1="24" y1="122" x2="{w - 24}" y2="122" stroke="{HAIR}" stroke-width="2"/>')
    body.append(f'  <text x="24" y="156" fill="{DUSTY}" font-family="{SERIF}" '
                f'font-size="30">{esc(spec["figure"])}</text>')
    for i, line in enumerate(wrap(spec["caption"], 42)):
        body.append(f'  <text x="150" y="{144 + i * 15}" fill="{INK}" opacity="0.72" '
                    f'font-family="{SANS}" font-size="11.5">{esc(line)}</text>')
    x = 24
    for tag in spec["tags"]:
        tw = 13 + len(tag) * 6.4
        body.append(f'  <rect x="{x:.0f}" y="178" width="{tw:.0f}" height="20" rx="10" '
                    f'fill="{PAPER}" stroke="{ROSE}" stroke-width="1"/>')
        body.append(f'  <text x="{x + tw/2:.0f}" y="192" text-anchor="middle" fill="{INK}" '
                    f'opacity="0.8" font-family="{SANS}" font-size="10.5">{esc(tag)}</text>')
        x += tw + 7
    return svg(w, h, "\n".join(body),
               f'{spec["name"]} — {spec["figure"]}, {spec["caption"]}')


# -- 5. how I build --------------------------------------------------------

HABITS = [
    ("The benchmark is a test",
     "relay replays 4,000 requests on every push, revenant re-runs all 140 crash "
     "scenarios, nanofaas records a session against a real Docker daemon. A number "
     "cannot quietly go stale."),
    ("A published console is a recording",
     "Pages runs no Python and no containers, so each page replays responses captured "
     "from the real service and names the date and host they came from."),
    ("The failure path is tested",
     "a platform reported healthy while its data plane is down, an effect that escaped "
     "before the log recorded it: those are the cases with tests."),
    ("The README states the limits",
     "no VM isolation, no egress control, a ledger paused because its free database "
     "expired. A claim is worth more with its limits beside it."),
]


def habits() -> str:
    h = 258
    col_w, gap = 476, 24
    body = [card(W, h)]
    body.append(f'  <text x="26" y="40" fill="{DUSTY}" font-family="{SANS}" font-size="12" '
                f'letter-spacing="2.4">madhura@github ~ $ cat how-i-build.md</text>')
    body.append(f'  <line x1="26" y1="54" x2="{W - 26}" y2="54" stroke="{HAIR}" stroke-width="2"/>')
    for i, (title, detail) in enumerate(HABITS):
        cx = 26 + (col_w + gap) * (i % 2)
        cy = 86 + (i // 2) * 92
        body.append(f'  <rect x="{cx}" y="{cy - 16}" width="3" height="18" rx="1.5" fill="{DUSTY}"/>')
        body.append(f'  <text x="{cx + 14}" y="{cy}" fill="{INK}" font-family="{SANS}" '
                    f'font-size="14.5" font-weight="600">{esc(title)}</text>')
        for j, line in enumerate(wrap(detail, 62)):
            body.append(f'  <text x="{cx + 14}" y="{cy + 20 + j * 16}" fill="{INK}" opacity="0.74" '
                        f'font-family="{SANS}" font-size="12.5">{esc(line)}</text>')
    return svg(W, h, "\n".join(body), "How I build — four habits that repeat across the six projects")


# -- 6. the counted card ---------------------------------------------------

FIGURES = [("8", "public projects"), ("6", "live consoles"),
           ("183", "commits"), ("15", "CI workflows")]
LANGS = [("Python", 61.5, DUSTY), ("TypeScript", 14.5, ROSE), ("JavaScript", 13.9, "#D9A7B8"),
         ("HTML", 7.6, "#EBD2DC"), ("CSS", 1.9, "#C9ADB8"), ("Solidity", 0.6, "#B58AA0")]


def counted() -> str:
    h = 250
    bar_x, bar_w, bar_y, bar_h = 40, W - 80, 148, 22
    body = [card(W, h)]
    body.append(f'  <text x="40" y="42" fill="{DUSTY}" font-family="{SANS}" font-size="12" '
                f'letter-spacing="2.4">madhura@github ~ $ ./count.sh</text>')
    body.append(f'  <line x1="40" y1="56" x2="{W - 40}" y2="56" stroke="{HAIR}" stroke-width="2"/>')
    slot = (W - 80) / len(FIGURES)
    for i, (value, label) in enumerate(FIGURES):
        cx = 40 + slot * i + slot / 2
        body.append(f'  <text x="{cx:.0f}" y="100" text-anchor="middle" fill="{DUSTY}" '
                    f'font-family="{SERIF}" font-size="34">{value}</text>')
        body.append(f'  <text x="{cx:.0f}" y="122" text-anchor="middle" fill="{INK}" opacity="0.78" '
                    f'font-family="{SANS}" font-size="12.5">{label}</text>')
        if i:
            x = 40 + slot * i
            body.append(f'  <line x1="{x:.0f}" y1="74" x2="{x:.0f}" y2="126" stroke="{HAIR}" stroke-width="2"/>')
    cursor = bar_x
    for name, pct, colour in LANGS:
        width = bar_w * pct / 100
        body.append(f'  <rect x="{cursor:.1f}" y="{bar_y}" width="{width:.1f}" height="{bar_h}" fill="{colour}"/>')
        cursor += width
    lx = bar_x
    for name, pct, colour in LANGS:
        body.append(f'  <circle cx="{lx + 6}" cy="{bar_y + 48}" r="5.5" fill="{colour}"/>')
        body.append(f'  <text x="{lx + 18}" y="{bar_y + 53}" fill="{INK}" opacity="0.85" '
                    f'font-family="{SANS}" font-size="12.5">{name} {pct}%</text>')
        lx += 26 + len(f"{name} {pct}%") * 7.6
    body.append(f'  <text x="{W - 40}" y="{h - 16}" text-anchor="end" fill="{INK}" opacity="0.5" '
                f'font-family="{SANS}" font-size="11.5">counted from the repositories, '
                f'not from a service that might be down</text>')
    return svg(W, h, "\n".join(body),
               "8 public projects, 6 live consoles, 183 commits, 15 CI workflows; 61.5% Python")


# -- 7. footer -------------------------------------------------------------


def footer() -> str:
    h = 120
    body = [
        '  <defs>',
        f'    <linearGradient id="dusk" x1="0" y1="1" x2="0.8" y2="0">'
        f'<stop offset="0" stop-color="{PAPER}"/><stop offset="0.55" stop-color="{CREAM}"/>'
        f'<stop offset="1" stop-color="{PAPER}"/></linearGradient>',
        '  </defs>',
        f'  <rect width="{W}" height="{h}" rx="14" fill="url(#dusk)"/>',
        f'  <rect width="{W}" height="{h}" rx="14" fill="none" stroke="{ROSE}" stroke-width="2"/>',
        f'  <path d="M -10 96 C 150 76, 300 108, 460 88" fill="none" stroke="{ROSE}" '
        f'stroke-width="2.2" stroke-linecap="round" opacity="0.65"/>',
        f'  <path d="M 1010 96 C 850 76, 700 108, 540 88" fill="none" stroke="{ROSE}" '
        f'stroke-width="2.2" stroke-linecap="round" opacity="0.65"/>',
        blossom(96, 86, 4.0, DUSTY, 0.85),
        blossom(208, 96, 3.2, DUSTY, 0.6),
        blossom(904, 86, 4.0, DUSTY, 0.85),
        blossom(792, 96, 3.2, DUSTY, 0.6),
        f'  <text x="{W/2}" y="54" text-anchor="middle" fill="{INK}" font-family="{SERIF}" '
        f'font-size="21">Thanks for visiting my little garden</text>',
        f'  <text x="{W/2}" y="80" text-anchor="middle" fill="{DUSTY}" font-family="{SANS}" '
        f'font-size="13">open a console, then read what it says it cannot show you</text>',
    ]
    return svg(W, h, "\n".join(body), "Thanks for visiting my little garden")


SECTIONS = [
    ("section-about.svg", "01", "About", "Who I am, and what I optimise for."),
    ("section-work.svg", "02", "The work", "Six systems, each with a number behind it."),
    ("section-build.svg", "03", "How I build", "The habits that repeat across all six."),
    ("section-counted.svg", "04", "Counted", "Measured from the repositories themselves."),
    ("section-contact.svg", "05", "Contact", "Happy to talk about any of it."),
]


def main() -> None:
    print("drawing the profile:")
    write("hero.svg", hero())
    for name, number, title, subtitle in SECTIONS:
        write(name, section(number, title, subtitle))
    write("about.svg", about())
    for spec in PROJECTS:
        write(spec["file"], project_card(spec))
    write("how-i-build.svg", habits())
    write("counted.svg", counted())
    write("footer.svg", footer())


if __name__ == "__main__":
    main()
