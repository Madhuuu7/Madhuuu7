"""Draw every panel on the profile.

One generator, so the palette, the type scale and the spacing cannot drift
between pieces, and so a number that changes is a one-line edit followed by
`python assets/build.py` rather than a careful search through five files.

Everything here is a static SVG committed to the repository. The profile does
not depend on a third-party card service: while this was being written, the
one most profiles use was answering DEPLOYMENT_PAUSED, which leaves broken
images in the middle of the page it was supposed to decorate.

Some panels move. GitHub serves a README image as a sandboxed SVG: no script
runs, but CSS keyframes and SMIL do, so the petals, the typed line and the
proof run are animation written into the file itself. Every animated element
is drawn in its finished state first and only then animated, so a reader who
has asked for reduced motion -- or a renderer that ignores the animation --
sees the complete panel rather than an empty one.
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


def petal(x: float, delay: float, duration: float, drift: float, size: float,
          fill: str) -> str:
    """One falling petal: a teardrop that drifts sideways as it turns."""
    return (
        f'  <g class="petal" style="animation-delay:{delay}s;animation-duration:{duration}s;'
        f'--drift:{drift}px">'
        f'<path transform="translate({x} -14) scale({size})" '
        f'd="M0 0 C 5 -7, 12 -2, 8 6 C 6 10, 1 9, 0 0 Z" fill="{fill}"/></g>'
    )


TYPED = "Hey there, I'm Madhura. Growing one commit at a time."


def hero() -> str:
    h = 262
    # The typed line is real text under a clip that opens in steps, one
    # character at a time. Georgia is not monospaced, so the clip is a hair
    # ahead or behind a letter mid-way -- which reads as typing, not as a bug.
    type_w = 460
    type_x = W / 2 - type_w / 2
    steps = len(TYPED)
    style = f'''  <style>
    .petal {{ opacity: 0; animation-name: fall; animation-timing-function: linear;
              animation-iteration-count: infinite; }}
    @keyframes fall {{
      0%   {{ opacity: 0; transform: translate(0, 0) rotate(0deg); }}
      8%   {{ opacity: .85; }}
      85%  {{ opacity: .7; }}
      100% {{ opacity: 0; transform: translate(var(--drift), {h + 30}px) rotate(300deg); }}
    }}
    .reveal {{ transform-origin: {type_x}px 0; animation: type 11s steps({steps}, end) infinite; }}
    @keyframes type {{
      0%, 4%    {{ transform: scaleX(0); }}
      38%, 94%  {{ transform: scaleX(1); }}
      100%      {{ transform: scaleX(0); }}
    }}
    .caret {{ animation: blink 1s steps(1, end) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .rule {{ transform-origin: {W / 2}px 0; animation: draw 11s ease-out infinite; }}
    @keyframes draw {{ 0% {{ transform: scaleX(0); }} 9%, 100% {{ transform: scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .petal, .reveal, .caret, .rule {{ animation: none; }}
    }}
  </style>'''
    body = [
        '  <defs>',
        f'    <linearGradient id="sky" x1="0" y1="0" x2="0.85" y2="1">'
        f'<stop offset="0" stop-color="{PAPER}"/><stop offset="0.5" stop-color="{CREAM}"/>'
        f'<stop offset="1" stop-color="{PAPER}"/></linearGradient>',
        f'    <linearGradient id="ribbon" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{ROSE}"/><stop offset="1" stop-color="{DUSTY}"/></linearGradient>',
        f'    <clipPath id="frame"><rect width="{W}" height="{h}" rx="14"/></clipPath>',
        f'    <clipPath id="typing"><rect class="reveal" x="{type_x}" y="212" '
        f'width="{type_w}" height="34"/></clipPath>',
        '  </defs>',
        style,
        f'  <rect width="{W}" height="{h}" rx="14" fill="url(#sky)"/>',
        # two branches, one high left, one low right
        f'  <path d="M -10 58 C 120 30, 232 82, 344 52" fill="none" stroke="{ROSE}" '
        f'stroke-width="2.4" stroke-linecap="round" opacity="0.8"/>',
        f'  <path d="M 1012 226 C 964 246, 920 214, 876 236" fill="none" stroke="{ROSE}" '
        f'stroke-width="2.4" stroke-linecap="round" opacity="0.8"/>',
        blossom(72, 44, 5.4, DUSTY, 0.95),
        blossom(164, 58, 4.2, DUSTY, 0.8),
        blossom(254, 68, 4.8, DUSTY, 0.65),
        blossom(330, 46, 3.6, ROSE, 0.6),
        blossom(986, 230, 5.2, DUSTY, 0.9),
        blossom(936, 236, 4.0, DUSTY, 0.7),
        blossom(886, 230, 4.6, ROSE, 0.6),
        blossom(62, 226, 3.2, ROSE, 0.5),
        blossom(946, 62, 3.4, ROSE, 0.5),
        # the petals the branches let go of, kept inside the frame
        '  <g clip-path="url(#frame)">',
        petal(90, 0.0, 13, 150, 1.0, DUSTY),
        petal(210, 4.5, 16, 110, 0.8, ROSE),
        petal(300, 9.0, 12, 190, 1.1, DUSTY),
        petal(430, 2.2, 17, -60, 0.7, ROSE),
        petal(560, 7.4, 14, 120, 0.9, DUSTY),
        petal(680, 11.5, 15, -90, 1.0, ROSE),
        petal(780, 1.2, 18, 80, 0.75, DUSTY),
        petal(880, 6.1, 13, -140, 1.05, ROSE),
        petal(960, 10.2, 16, -200, 0.85, DUSTY),
        '  </g>',
        f'  <rect width="{W}" height="{h}" rx="14" fill="none" stroke="{ROSE}" stroke-width="2"/>',
        # the eyebrow
        f'  <text x="{W/2}" y="56" text-anchor="middle" fill="{INK}" opacity="0.62" '
        f'font-family="{SANS}" font-size="12.5" letter-spacing="3.2">'
        f'BENGALURU, INDIA &#183; COMPUTER SCIENCE &#183; 2027</text>',
        # the name
        f'  <text x="{W/2}" y="122" text-anchor="middle" fill="{INK}" '
        f'font-family="{SERIF}" font-size="56" letter-spacing="1.2">Madhura M R</text>',
        f'  <rect class="rule" x="{W/2 - 94}" y="140" width="188" height="3" rx="1.5" fill="url(#ribbon)"/>',
        # the role line
        f'  <text x="{W/2}" y="174" text-anchor="middle" fill="{DUSTY}" '
        f'font-family="{SANS}" font-size="17.5" font-weight="600" letter-spacing="0.4">'
        f'Full-Stack Developer &#183; Applied ML &#183; Distributed Systems</text>',
        f'  <text x="{W/2}" y="200" text-anchor="middle" fill="{INK}" opacity="0.78" '
        f'font-family="{SANS}" font-size="14">'
        f'Building real-world apps with clean, maintainable code &#8212; seven of them live, '
        f'each one you can open.</text>',
        # the typed line, which used to be an image from somebody else's server
        f'  <text x="{W/2}" y="236" text-anchor="middle" fill="{DUSTY}" clip-path="url(#typing)" '
        f'font-family="{SERIF}" font-size="18" font-style="italic">'
        f'{esc(TYPED)}</text>',
    ]
    return svg(W, h, "\n".join(body),
               "Madhura M R — full-stack developer, applied ML, distributed systems")


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
    ("focus", "End-to-end web apps: API, data model, UI, and the CI that ships them"),
    ("languages", "Python, TypeScript, SQL, a little Solidity"),
    ("ml", "scikit-learn, pandas, conformal prediction"),
    ("backend", "FastAPI, asyncio, Postgres, MongoDB, Docker"),
    ("frontend", "React, Vite, hand-written SVG charts"),
    ("testing", "pytest, vitest, Playwright, on every push"),
    ("full stack", "Next.js, Prisma, offline-first sync"),
    ("proof", "7 live, 232 commits, 16 workflows"),
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
    y = 158
    for title, detail in ABOUT_POINTS:
        body.append(blossom(33, y - 4, 4.4, DUSTY, 0.9))
        body.append(f'  <text x="48" y="{y}" fill="{INK}" font-family="{SANS}" font-size="14" '
                    f'font-weight="600">{esc(title)}</text>')
        for j, line in enumerate(wrap(detail, 48)):
            body.append(f'  <text x="48" y="{y + 18 + j * 16}" fill="{INK}" opacity="0.72" '
                        f'font-family="{SANS}" font-size="12.5">{esc(line)}</text>')
        y += 55

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


# -- 4b. the newest one, drawn wide ----------------------------------------

CLAIMKIT = {
    "eyebrow": "07 · FULL STACK · THE NEWEST",
    "name": "ClaimKit",
    "line": "A family puts one health-insurance claim together, from phones in a "
            "hospital corridor with no signal.",
    "figure": "266",
    "caption": "tests against a real Postgres. Two phones edit offline, and both end up "
               "with the same claim.",
    "tags": ["TypeScript", "Next.js", "Postgres", "Prisma", "Playwright"],
}


def claimkit_card() -> str:
    """ClaimKit, with the thing it does drawn beside it.

    Two phones each make an edit with no signal, the edits wait, and then both
    reach the log and come back to the other phone. The dots are SMIL motion
    along the same paths the lines are drawn on, so the picture cannot show a
    route the diagram does not have.
    """
    w, h = W, 214
    spec = CLAIMKIT
    body = [
        f'  <rect width="{w}" height="{h}" rx="12" fill="{CREAM}"/>',
        f'  <rect width="{w}" height="{h}" rx="12" fill="none" stroke="{ROSE}" stroke-width="2"/>',
        f'  <rect x="0" y="0" width="{w}" height="4" rx="2" fill="{DUSTY}" opacity="0.55"/>',
        f'  <text x="24" y="34" fill="{DUSTY}" font-family="{SANS}" font-size="10.5" '
        f'letter-spacing="2">{esc(spec["eyebrow"])}</text>',
        f'  <text x="24" y="62" fill="{INK}" font-family="{SERIF}" font-size="26">{esc(spec["name"])}</text>',
    ]
    for i, line in enumerate(wrap(spec["line"], 62)):
        body.append(f'  <text x="24" y="{86 + i * 17}" fill="{INK}" opacity="0.76" '
                    f'font-family="{SANS}" font-size="12.5">{esc(line)}</text>')
    body.append(f'  <line x1="24" y1="122" x2="520" y2="122" stroke="{HAIR}" stroke-width="2"/>')
    body.append(f'  <text x="24" y="156" fill="{DUSTY}" font-family="{SERIF}" '
                f'font-size="30">{esc(spec["figure"])}</text>')
    for i, line in enumerate(wrap(spec["caption"], 58)):
        body.append(f'  <text x="96" y="{144 + i * 15}" fill="{INK}" opacity="0.72" '
                    f'font-family="{SANS}" font-size="11.5">{esc(line)}</text>')
    x = 24
    for tag in spec["tags"]:
        tw = 13 + len(tag) * 6.4
        body.append(f'  <rect x="{x:.0f}" y="178" width="{tw:.0f}" height="20" rx="10" '
                    f'fill="{PAPER}" stroke="{ROSE}" stroke-width="1"/>')
        body.append(f'  <text x="{x + tw/2:.0f}" y="192" text-anchor="middle" fill="{INK}" '
                    f'opacity="0.8" font-family="{SANS}" font-size="10.5">{esc(tag)}</text>')
        x += tw + 7

    # the diagram: phone, log, phone
    ax, bx, ly = 604, 908, 44           # phone A, phone B, top of the log
    lx = (ax + bx) / 2 + 18             # the log's centre line
    up_a = f"M {ax + 36} 118 C {ax + 90} 118, {lx - 70} 78, {lx - 34} 78"
    up_b = f"M {bx} 118 C {bx - 54} 118, {lx + 70} 78, {lx + 34} 78"

    def phone(px: float, who: str) -> str:
        return (
            f'  <g><rect x="{px}" y="72" width="36" height="92" rx="7" fill="{PAPER}" '
            f'stroke="{ROSE}" stroke-width="2"/>'
            f'<rect x="{px + 7}" y="84" width="22" height="3" rx="1.5" fill="{ROSE}"/>'
            f'<rect x="{px + 7}" y="93" width="16" height="3" rx="1.5" fill="{ROSE}" opacity=".7"/>'
            f'<rect x="{px + 7}" y="102" width="20" height="3" rx="1.5" fill="{ROSE}" opacity=".5"/>'
            f'<circle cx="{px + 18}" cy="152" r="3" fill="{ROSE}"/>'
            f'<text x="{px + 18}" y="184" text-anchor="middle" fill="{INK}" opacity=".7" '
            f'font-family="{SANS}" font-size="10.5">{who}</text></g>'
        )

    body.append(phone(ax, "phone A"))
    body.append(phone(bx, "phone B"))
    for k in range(3):
        body.append(f'  <rect x="{lx - 34}" y="{ly + 22 + k * 14}" width="68" height="10" rx="3" '
                    f'fill="{PAPER}" stroke="{ROSE}" stroke-width="1.5"/>')
    body.append(f'  <text x="{lx}" y="{ly + 10}" text-anchor="middle" fill="{INK}" opacity=".7" '
                f'font-family="{SANS}" font-size="10.5">one ordered log</text>')
    for d in (up_a, up_b):
        body.append(f'  <path d="{d}" fill="none" stroke="{ROSE}" stroke-width="1.6" '
                    f'stroke-dasharray="3 5" stroke-linecap="round"/>')

    def dot(path: str, begin: str, back: bool, colour: str) -> str:
        points = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if back else ""
        return (
            f'  <circle r="4.2" fill="{colour}" opacity="0">'
            f'<animateMotion dur="2.2s" begin="{begin}" repeatCount="indefinite" '
            f'path="{path}"{points}/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" '
            f'dur="2.2s" begin="{begin}" repeatCount="indefinite"/></circle>'
        )

    body.append(dot(up_a, "0s", False, DUSTY))       # A's edit goes up
    body.append(dot(up_b, "0.5s", False, "#A9718A"))  # B's edit goes up
    body.append(dot(up_b, "1.1s", True, DUSTY))      # A's edit arrives at B
    body.append(dot(up_a, "1.6s", True, "#A9718A"))   # B's edit arrives at A
    body.append(f'  <text x="{lx}" y="{h - 22}" text-anchor="middle" fill="{DUSTY}" '
                f'font-family="{SANS}" font-size="11.5" font-weight="600">'
                f'edited offline &#8594; queued &#8594; converged</text>')
    return svg(w, h, "\n".join(body),
               "ClaimKit — 266 tests; two phones edit offline and converge on one claim")


# -- 4c. the proof run -----------------------------------------------------

# Each row is a claim, what was done to it, and what came back. Every figure
# here is one a test in that repository produces; none of them is typed in
# from memory, and a row whose test stops passing should come off this list.
PROOFS = [
    ("revenant", "killed at every one of its journal boundaries", "140 / 140 recovered"),
    ("relay", "replayed a 4,000-request trace through four policies", "p95 down 71.8%"),
    ("gridcast", "scored on 32,391 blocks it never trained on", "5.07% MAPE"),
    ("transitlab", "raced against the Python engine it was ported from", "37x faster"),
    ("verdict", "re-tested every case, against looking once", "46.7% vs 5.9% false alarms"),
    ("nanofaas", "timed a cold start against a warm call", "1,028x apart"),
    ("claimkit", "two phones, no signal, the same field", "conflict shown, nothing lost"),
]


def proof_run() -> str:
    """A terminal that runs the claims, one line at a time, and starts over.

    The rows are plain text in their final positions; the animation only
    fades each one in on a stagger. With motion reduced the whole run is
    simply there, which is the version a screenshot would want anyway.
    """
    row_h, top = 30, 92
    h = top + len(PROOFS) * row_h + 58
    cycle = 16.0
    rules = []
    for i in range(len(PROOFS) + 1):
        start = 4 + i * 9          # percent of the cycle at which row i appears
        rules.append(
            f"    .r{i} {{ animation: r{i} {cycle}s linear infinite; }}\n"
            f"    @keyframes r{i} {{ 0%, {start}% {{ opacity: 0; }} "
            f"{start + 3}%, 94% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}"
        )
    style = (
        "  <style>\n" + "\n".join(rules) + "\n"
        "    .cur { animation: cur 1s steps(1, end) infinite; }\n"
        "    @keyframes cur { 50% { opacity: 0; } }\n"
        "    @media (prefers-reduced-motion: reduce) { [class] { animation: none; } }\n"
        "  </style>"
    )
    body = [card(W, h), style]
    # three window dots, because it is a terminal and should look like one
    for k, tone in enumerate((ROSE, "#EBD2DC", DUSTY)):
        body.append(f'  <circle cx="{34 + k * 16}" cy="30" r="5" fill="{tone}"/>')
    body.append(f'  <text x="96" y="35" fill="{DUSTY}" font-family="{SANS}" font-size="12.5" '
                f'letter-spacing="1.2">madhura@github ~ $ ./prove.sh</text>')
    body.append(f'  <rect class="cur" x="322" y="23" width="8" height="15" fill="{DUSTY}" opacity=".7"/>')
    body.append(f'  <line x1="26" y1="52" x2="{W - 26}" y2="52" stroke="{HAIR}" stroke-width="2"/>')
    body.append(f'  <text x="40" y="76" fill="{INK}" opacity=".55" font-family="{SANS}" '
                f'font-size="11" letter-spacing="1.6">CLAIM</text>')
    body.append(f'  <text x="168" y="76" fill="{INK}" opacity=".55" font-family="{SANS}" '
                f'font-size="11" letter-spacing="1.6">WHAT WAS DONE TO IT</text>')
    body.append(f'  <text x="{W - 40}" y="76" text-anchor="end" fill="{INK}" opacity=".55" '
                f'font-family="{SANS}" font-size="11" letter-spacing="1.6">WHAT CAME BACK</text>')
    for i, (name, did, got) in enumerate(PROOFS):
        y = top + i * row_h + 18
        body.append(f'  <g class="r{i}">')
        if i:
            body.append(f'    <line x1="40" y1="{y - 20}" x2="{W - 40}" y2="{y - 20}" '
                        f'stroke="{HAIR}" stroke-width="1.5"/>')
        body.append(f'    <path d="M {40} {y - 5} l 4 4 l 8 -9" fill="none" stroke="{DUSTY}" '
                    f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        body.append(f'    <text x="62" y="{y}" fill="{INK}" font-family="{SERIF}" '
                    f'font-size="16">{esc(name)}</text>')
        body.append(f'    <text x="168" y="{y}" fill="{INK}" opacity=".76" font-family="{SANS}" '
                    f'font-size="13">{esc(did)}</text>')
        body.append(f'    <text x="{W - 40}" y="{y}" text-anchor="end" fill="{DUSTY}" '
                    f'font-family="{SANS}" font-size="13.5" font-weight="600">{esc(got)}</text>')
        body.append('  </g>')
    fy = top + len(PROOFS) * row_h + 30
    last = len(PROOFS)
    body.append(f'  <g class="r{last}">'
                f'<text x="40" y="{fy}" fill="{INK}" opacity=".78" font-family="{SANS}" '
                f'font-size="13">{len(PROOFS)} claims, {len(PROOFS)} checked. '
                f'Each one is a test that runs in CI, not a sentence in a README.</text></g>')
    return svg(W, h, "\n".join(body),
               "The proof run: seven claims, what was done to each, and what came back")


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
    return svg(W, h, "\n".join(body), "How I build — four habits that repeat across the projects")


# -- 6. the counted card ---------------------------------------------------

FIGURES = [("9", "public projects"), ("7", "live, open to click"),
           ("232", "commits"), ("16", "CI workflows")]
LANGS = [("Python", 50.4, DUSTY), ("TypeScript", 26.7, ROSE), ("JavaScript", 11.1, "#D9A7B8"),
         ("HTML", 9.3, "#EBD2DC"), ("CSS", 2.1, "#C9ADB8"), ("Solidity", 0.4, "#B58AA0")]


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
               "9 public projects, 7 live, 232 commits, 16 CI workflows; 50.4% Python")


# -- 7. the contribution year ---------------------------------------------

# The calendar is a committed snapshot rather than a live call, for the same
# reason every other panel here is a committed file: the page has to draw
# itself with no network and no service in the middle. Refresh it with
#
#   gh api graphql -f login=Madhuuu7 -f query='query($login:String!){
#     user(login:$login){contributionsCollection{contributionCalendar{
#     totalContributions weeks{firstDay contributionDays{
#     date contributionCount weekday}}}}}}' > assets/contributions.json
#
# and run this script again.

# five steps, palest to deepest; index 0 is a day with nothing in it
LEVELS = [HAIR, "#F3D6E0", ROSE, DUSTY, "#A9718A"]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _calendar() -> dict:
    import json
    raw = json.loads((HERE / "contributions.json").read_text(encoding="utf-8"))
    return raw["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def _level(count: int, busiest: int) -> int:
    """Which of the five tones a day gets.

    The thresholds are a share of the busiest day rather than fixed counts,
    so a quiet year does not render as a blank sheet and a loud one does not
    saturate to a single tone.
    """
    if count <= 0:
        return 0
    for i, share in enumerate((0.10, 0.30, 0.60), start=1):
        if count <= max(1, round(busiest * share)):
            return i
    return 4


def contributions() -> str:
    cal = _calendar()
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    busiest = max((d["contributionCount"] for d in days), default=0)
    active = sum(1 for d in days if d["contributionCount"])

    left, top = 74, 86          # the weekday gutter, and the month strip
    cell, gap = 13.0, 3.6
    step = cell + gap
    h = int(top + 7 * step + 76)

    body = [card(W, h)]
    body.append(f'  <text x="40" y="42" fill="{DUSTY}" font-family="{SANS}" font-size="12" '
                f'letter-spacing="2.4">madhura@github ~ $ ./year.sh</text>')
    body.append(f'  <line x1="40" y1="56" x2="{W - 40}" y2="56" stroke="{HAIR}" stroke-width="2"/>')

    # month labels, written once where a month first appears
    seen = set()
    for wi, week in enumerate(weeks):
        month = int(week["firstDay"][5:7])
        if month in seen:
            continue
        seen.add(month)
        x = left + wi * step
        if x > W - 90:
            continue
        body.append(f'  <text x="{x:.1f}" y="{top - 10}" fill="{INK}" opacity="0.55" '
                    f'font-family="{SANS}" font-size="11">{MONTHS[month - 1]}</text>')

    # Monday, Wednesday, Friday, the way the calendar on the site labels them
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = top + row * step + cell - 2
        body.append(f'  <text x="{left - 10}" y="{y:.1f}" text-anchor="end" fill="{INK}" '
                    f'opacity="0.55" font-family="{SANS}" font-size="11">{name}</text>')

    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            x = left + wi * step
            y = top + day["weekday"] * step
            tone = LEVELS[_level(day["contributionCount"], busiest)]
            body.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" '
                        f'rx="3" fill="{tone}"/>')

    legend_y = top + 7 * step + 26
    body.append(f'  <text x="{W - 40}" y="{legend_y + 10:.1f}" text-anchor="end" fill="{INK}" '
                f'opacity="0.6" font-family="{SANS}" font-size="11.5">more</text>')
    lx = W - 92
    for tone in reversed(LEVELS):
        body.append(f'  <rect x="{lx:.1f}" y="{legend_y:.1f}" width="{cell}" height="{cell}" '
                    f'rx="3" fill="{tone}"/>')
        lx -= step
    body.append(f'  <text x="{lx + cell - 4:.1f}" y="{legend_y + 10:.1f}" text-anchor="end" '
                f'fill="{INK}" opacity="0.6" font-family="{SANS}" font-size="11.5">less</text>')

    total = cal["totalContributions"]
    body.append(f'  <text x="40" y="{legend_y + 10:.1f}" fill="{INK}" opacity="0.78" '
                f'font-family="{SANS}" font-size="13">'
                f'{total} contributions in the last year, across {active} days '
                f'&#8212; {busiest} on the busiest one</text>')
    body.append(f'  <text x="40" y="{legend_y + 34:.1f}" fill="{INK}" opacity="0.5" '
                f'font-family="{SANS}" font-size="11.5">'
                f'a snapshot from the GitHub API, committed like every other panel here'
                f'</text>')
    return svg(W, h, "\n".join(body),
               f"{total} contributions in the last year, across {active} days")


# -- 8. footer -------------------------------------------------------------


# The dino, one character per pixel. Drawn as a bitmap so it stays a dino at
# any size and its outline is something a person can read and correct.
DINO = [
    "........XXXXXXX.",
    ".......XXXXXXXXX",
    ".......XX.XXXXXX",
    ".......XXXXXXXXX",
    ".......XXXXX....",
    ".......XXXXXXXX.",
    "X.....XXXXX.....",
    "X....XXXXXXXX...",
    "XX..XXXXXXXX.X..",
    "XXXXXXXXXXXX....",
    "XXXXXXXXXXXX....",
    ".XXXXXXXXXX.....",
    "..XXXXXXXX......",
    "...XXXXXX.......",
]
# Two pairs of legs. Showing one and then the other is the whole run cycle.
LEGS_A = [
    "...XX..XX.......",
    "...X....XX......",
    "...XX...........",
]
LEGS_B = [
    "...XX..XX.......",
    "...XX...X.......",
    "........XX......",
]


def _pixels(rows: list[str], px: float, top: int = 0) -> str:
    """Runs of filled cells become one rect each, so the file stays small."""
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] != "X":
                c += 1
                continue
            start = c
            while c < len(row) and row[c] == "X":
                c += 1
            out.append(f'<rect x="{start * px:.1f}" y="{(top + r) * px:.1f}" '
                       f'width="{(c - start) * px:.1f}" height="{px + 0.4:.1f}"/>')
    return "".join(out)


def footer() -> str:
    h = 178
    ground = 150                    # where the branches run, and the dino's feet
    px = 3.0
    dino_w = 16 * px
    dino_h = (len(DINO) + len(LEGS_A)) * px
    base_x = 40                     # where it stands when nothing is moving
    travel_from, travel_to = -100, 980
    span = travel_to - travel_from
    lap = 14                        # seconds to cross the garden

    # The blossoms it has to clear. Each jump is timed from where the flower
    # actually is, so moving a blossom moves the jump with it.
    flowers = [96, 208, 792, 904]
    frames = ["0% { transform: translateY(0); }"]
    for fx in flowers:
        t = (fx - (base_x + dino_w / 2) - travel_from) / span * 100
        frames.append(f"{t - 3.4:.1f}% {{ transform: translateY(0); "
                      f"animation-timing-function: cubic-bezier(.2,.7,.4,1); }}")
        frames.append(f"{t:.1f}% {{ transform: translateY(-38px); "
                      f"animation-timing-function: cubic-bezier(.6,0,.8,.3); }}")
        frames.append(f"{t + 3.4:.1f}% {{ transform: translateY(0); }}")
    frames.append("100% { transform: translateY(0); }")

    style = (
        "  <style>\n"
        f"    .run {{ animation: run {lap}s linear infinite; }}\n"
        f"    @keyframes run {{ from {{ transform: translateX({travel_from}px); }} "
        f"to {{ transform: translateX({travel_to}px); }} }}\n"
        f"    .hop {{ animation: hop {lap}s linear infinite; }}\n"
        "    @keyframes hop { " + " ".join(frames) + " }\n"
        "    .la { animation: step .28s steps(1, end) infinite; }\n"
        "    .lb { opacity: 0; animation: step .28s steps(1, end) -.14s infinite; }\n"
        "    @keyframes step { 0% { opacity: 1; } 50%, 100% { opacity: 0; } }\n"
        "    @media (prefers-reduced-motion: reduce) {\n"
        "      .run, .hop, .la, .lb { animation: none; }\n"
        "    }\n"
        "  </style>"
    )

    dino_top = ground - dino_h - 1
    body = [
        '  <defs>',
        f'    <linearGradient id="dusk" x1="0" y1="1" x2="0.8" y2="0">'
        f'<stop offset="0" stop-color="{PAPER}"/><stop offset="0.55" stop-color="{CREAM}"/>'
        f'<stop offset="1" stop-color="{PAPER}"/></linearGradient>',
        f'    <clipPath id="garden"><rect width="{W}" height="{h}" rx="14"/></clipPath>',
        '  </defs>',
        style,
        f'  <rect width="{W}" height="{h}" rx="14" fill="url(#dusk)"/>',
        f'  <path d="M -10 {ground + 4} C 150 {ground - 16}, 300 {ground + 16}, 460 {ground - 4}" '
        f'fill="none" stroke="{ROSE}" stroke-width="2.2" stroke-linecap="round" opacity="0.65"/>',
        f'  <path d="M 1010 {ground + 4} C 850 {ground - 16}, 700 {ground + 16}, 540 {ground - 4}" '
        f'fill="none" stroke="{ROSE}" stroke-width="2.2" stroke-linecap="round" opacity="0.65"/>',
        blossom(96, ground - 6, 4.0, DUSTY, 0.85),
        blossom(208, ground + 4, 3.2, DUSTY, 0.6),
        blossom(904, ground - 6, 4.0, DUSTY, 0.85),
        blossom(792, ground + 4, 3.2, DUSTY, 0.6),
        f'  <text x="{W/2}" y="54" text-anchor="middle" fill="{INK}" font-family="{SERIF}" '
        f'font-size="21">Thanks for visiting my little garden</text>',
        f'  <text x="{W/2}" y="80" text-anchor="middle" fill="{DUSTY}" font-family="{SANS}" '
        f'font-size="13">open a console, then read what it says it cannot show you</text>',
        # the dino: across the garden, over every blossom, and round again
        '  <g clip-path="url(#garden)">',
        '    <g class="run">',
        '      <g class="hop">',
        f'        <g transform="translate({base_x} {dino_top:.1f})" fill="{DUSTY}">',
        '          ' + _pixels(DINO, px),
        f'          <rect x="{9 * px:.1f}" y="{2 * px:.1f}" width="{px:.1f}" height="{px:.1f}" '
        f'fill="{CREAM}"/>',
        '          <g class="la">' + _pixels(LEGS_A, px, len(DINO)) + '</g>',
        '          <g class="lb">' + _pixels(LEGS_B, px, len(DINO)) + '</g>',
        '        </g>',
        '      </g>',
        '    </g>',
        '  </g>',
        f'  <rect width="{W}" height="{h}" rx="14" fill="none" stroke="{ROSE}" stroke-width="2"/>',
    ]
    return svg(W, h, "\n".join(body),
               "Thanks for visiting my little garden. A small dino runs across it, "
               "hopping over the blossoms.")


SECTIONS = [
    ("section-about.svg", "01", "About", "Who I am, and what I optimise for."),
    ("section-work.svg", "02", "The work", "Seven systems, each with a number behind it."),
    ("section-build.svg", "03", "How I build", "The habits that repeat across all of them."),
    ("section-counted.svg", "04", "Counted", "Measured from the repositories themselves."),
    ("section-contact.svg", "05", "Contact", "Happy to talk about any of it."),
]


def main() -> None:
    print("drawing the profile:")
    write("hero.svg", hero())
    for name, number, title, subtitle in SECTIONS:
        write(name, section(number, title, subtitle))
    write("about.svg", about())
    write("proof-run.svg", proof_run())
    write("card-claimkit.svg", claimkit_card())
    for spec in PROJECTS:
        write(spec["file"], project_card(spec))
    write("how-i-build.svg", habits())
    write("counted.svg", counted())
    write("contributions.svg", contributions())
    write("footer.svg", footer())


if __name__ == "__main__":
    main()
