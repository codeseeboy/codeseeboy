"""Build the profile README and the images it uses.

Edit the data in the first half of this file, then run

    python scripts/build_assets.py

It rewrites README.md and every SVG in assets/, once for GitHub's light theme
and once for the dark one. Only the standard library is used.

Monospace text is laid out on a fixed character grid (CW below) and stretched
to it with textLength, so columns line up whichever monospace font the
viewer's system has.
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

PORTFOLIO = "https://ezz-shashiii.vercel.app"
GITHUB = "https://github.com/codeseeboy"
EMAIL = "shashi2005.pvt@gmail.com"

PROFILE = {
    "host": "shashikant@codeseeboy: ~",
    "banner": ("SHASHIKANT", "RAJPUT"),
    "tagline": (
        "AI engineer. I build LLM apps, retrieval that cites its source,",
        "vision models that count real things, and the APIs around them.",
    ),
    "status": (
        ("role", "Intern AI Engineer @ ADDLYFT"),
        ("study", "B.Tech AI & ML, final year"),
        ("base", "Mumbai, India"),
        ("next", "Open to full-time AI roles from mid-2027"),
    ),
}

# (file slug, label, link)
LINKS = (
    ("portfolio", "portfolio", PORTFOLIO),
    ("resume", "résumé", f"{PORTFOLIO}/resume"),
    ("linkedin", "linkedin", "https://www.linkedin.com/in/shashikant-rajput"),
    ("email", EMAIL, f"mailto:{EMAIL}"),
)

PROJECTS = (
    {
        "slug": "non8",
        "path": "non8",
        "kind": "case study",
        "href": f"{PORTFOLIO}/work/non8",
        "title": "NON8",
        "tags": "agents · rag · offline",
        "desc": "Offline AI workbench for sensitive documents. A LangGraph agent "
                "answers from private files on local models and cites every source.",
        "metric": "simple queries 60–80 s → 0.8 s on a 12 GB GPU",
        "stack": ("langgraph", "ollama", "faiss", "fastapi", "react"),
    },
    {
        "slug": "clausewise",
        "path": "clausewise",
        "kind": "repo",
        "href": f"{GITHUB}/clausewise",
        "title": "Clausewise",
        "tags": "retrieval · evaluation",
        "desc": "Policy search that answers only from the clause it found. "
                "Benchmarks vector, hybrid and reranked retrieval on one corpus.",
        "metric": "NDCG@5  vector 0.878 · hybrid 0.794 · rerank 0.928",
        "stack": ("qdrant", "bm25", "bge-reranker", "ollama", "docker"),
    },
    {
        "slug": "urbanfix",
        "path": "urban-fix-ai",
        "kind": "repo",
        "href": f"{GITHUB}/urban-fix-ai",
        "title": "UrbanFix AI",
        "tags": "computer vision · capstone",
        "desc": "Civic-issue reporting app. Reads a citizen's photo, scores "
                "urgency and routes the issue to the right department.",
        "metric": "v1 SigLIP + YOLOv8 · v2 Gemini on Vertex AI",
        "stack": ("expo", "node.js", "supabase", "kafka", "spark"),
    },
    {
        "slug": "trustlayer",
        "path": "Trust-layer-AI",
        "kind": "repo",
        "href": f"{GITHUB}/Trust-layer-AI",
        "title": "TrustLayer AI",
        "tags": "llm verification · hackathon",
        "desc": "Splits an AI answer into claims, checks each one against "
                "Wikipedia and web search, and scores how far to trust it.",
        "metric": "top national finalist, GFG ByteQuest",
        "stack": ("next.js", "express", "gemini", "groq", "openrouter"),
    },
    {
        "slug": "countx",
        "path": "countX",
        "kind": "repo",
        "href": f"{GITHUB}/countX",
        "title": "CountX",
        "tags": "computer vision · retail",
        "desc": "Shelf counting for a US convenience-store client. Detects "
                "12 drink SKUs and prices the count from a price book.",
        "metric": "YOLOv8n · image, video and live camera",
        "stack": ("yolov8", "opencv", "easyocr", "gradio"),
    },
    {
        "slug": "llm-gateway",
        "path": "llm-backend",
        "kind": "repo",
        "href": f"{GITHUB}/llm-backend",
        "title": "LLM Gateway",
        "tags": "llm infrastructure",
        "desc": "One API in front of nine LLM providers. Tries them in order "
                "and falls back when one is rate-limited or down.",
        "metric": "text, images, PDFs and office files in one call",
        "stack": ("fastapi", "gemini", "groq", "openrouter", "mistral"),
    },
)

MORE = (
    {
        "slug": "gridlock",
        "path": "game-theory-capstone",
        "href": f"{GITHUB}/game-theory-capstone",
        "title": "Gridlock",
        "desc": "Traffic strategy game on an equilibrium engine: Nash flow, Braess, VCG tolls.",
    },
    {
        "slug": "addx",
        "path": "addX",
        "href": f"{GITHUB}/addX",
        "title": "AddX",
        "desc": "Expo app that turns a store promotion into an audio ad.",
    },
    {
        "slug": "bottles",
        "path": "beverage-bottle-detection-model",
        "href": f"{GITHUB}/beverage-bottle-detection-model",
        "title": "Bottle detection",
        "desc": "YOLOv8 trained on 73 beverage-bottle classes.",
    },
)

# Newest first. "work" and "edu" are drawn as two branches of one git graph.
CAREER = (
    {
        "lane": "work", "dates": "Aug 2026 → now",
        "role": "Intern AI Engineer", "org": "ADDLYFT", "head": True,
        "detail": "Voice and video generation for in-store retail ads. Built the voice-ad "
                  "service (Gemini, ElevenLabs, FFmpeg) in Python, then rebuilt it in NestJS. "
                  "Benchmarked video models and cut per-shot generation from 697 s to 116 s.",
    },
    {
        "lane": "work", "dates": "Apr → May 2026",
        "role": "Software Consultant", "org": "Indian Navy",
        "detail": "Built StockFlow, an inventory and order-tracking web app.",
    },
    {
        "lane": "work", "dates": "Feb → Aug 2026",
        "role": "AI Developer (freelance)", "org": "CStoreExpert",
        "detail": "Retail computer vision and audio ads for a US convenience-store client: "
                  "YOLOv8 shelf counting, an LLM gateway over nine providers, and the AddX app.",
    },
    {
        "lane": "edu", "dates": "2024 → 2027",
        "role": "B.Tech, AI & ML", "org": "St. John College of Engineering and Management",
        "detail": "University of Mumbai · final year",
    },
    {
        "lane": "work", "dates": "Feb → Aug 2024",
        "role": "Web Development Intern (backend)", "org": "Tenet Concepts / Worko",
        "detail": "Serverless TypeScript API on AWS Lambda and DynamoDB: payments, WhatsApp "
                  "Cloud API, SQS and EventBridge schedules. Top committer on the API.",
    },
    {
        "lane": "edu", "dates": "2022 → 2024",
        "role": "Diploma, Computer Engineering", "org": "Government Polytechnic Mumbai",
        "detail": "",
    },
)

STACK = (
    ("languages", ("python", "typescript", "javascript", "sql")),
    ("llm", ("langgraph", "rag", "ollama", "gemini", "vertex-ai")),
    ("retrieval", ("hybrid-search", "reranking", "faiss", "qdrant")),
    ("vision", ("yolov8", "opencv", "siglip", "pytorch")),
    ("backend", ("fastapi", "nodejs", "express", "nestjs", "postgresql", "prisma", "supabase")),
    ("cloud", ("aws-lambda", "dynamodb", "sqs", "eventbridge", "docker", "github-actions")),
)

WINS = (
    ("1st place", "BIS national competition, 2026"),
    ("finalist", "Top national finalist, GFG ByteQuest, with TrustLayer AI"),
    ("top 10", "Hackanova 4.0  ·  Vibe Coding Vol. 1"),
    ("lead", "Technical Head, ASCAI  ·  Tech Team Lead, GDG on Campus"),
    ("trainer", "Computer vision at Wiserli, 80+ students"),
)

NEXT = "Full-time AI engineering roles from mid-2027: LLM apps, retrieval, vision."

# ---------------------------------------------------------------------------
# Design
# ---------------------------------------------------------------------------

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = ("'JetBrains Mono', 'Cascadia Code', 'SF Mono', SFMono-Regular, ui-monospace, "
        "Menlo, Consolas, 'Liberation Mono', monospace")
CW = 0.6  # monospace advance, as a share of the font size
BAR = 38  # window title bar height
LIGHTS = ("#ff5f57", "#febc2e", "#28c840")

THEMES = {
    "dark": {
        "body": "#0b0f14", "bar": "#151a21", "line": "#2b323c", "chip": "#121820",
        "text": "#e6edf3", "text2": "#c4ccd5", "muted": "#8b949e", "dim": "#636c76",
        "accent": "#ff6b5e", "green": "#56d364", "blue": "#79c0ff", "purple": "#d2a8ff",
        "yellow": "#e3b341", "string": "#a5d6ff",
        "shadow": "#2d333b", "shadow2": "#5c1f1b",
    },
    "light": {
        "body": "#f6f8fa", "bar": "#eaeef2", "line": "#d0d7de", "chip": "#ffffff",
        "text": "#1f2328", "text2": "#3b434b", "muted": "#59636e", "dim": "#8c959f",
        "accent": "#d1242f", "green": "#1a7f37", "blue": "#0969da", "purple": "#8250df",
        "yellow": "#9a6700", "string": "#0a3069",
        "shadow": "#d0d7de", "shadow2": "#f5c2bd",
    },
}

# 5x7 pixel letters for the name banner.
PIXELS = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "....#", "....#", "....#", "....#", "#...#", ".###."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".###.", "#...#", "#....", ".###.", "....#", "#...#", ".###."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
}

CSS = (
    "<style>"
    f".m{{font-family:{MONO}}}.s{{font-family:{SANS}}}"
    ".k{animation:on .01s both}"
    ".f{animation:up .45s ease-out both}"
    ".b{animation:on .01s both,blink 1.1s steps(1) infinite}"
    ".p{animation:pulse 2.4s ease-in-out infinite}"
    "@keyframes on{from{opacity:0}to{opacity:1}}"
    "@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}"
    "@keyframes blink{50%{opacity:0}}"
    "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    "</style>"
)

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def mw(s: str, size: float) -> float:
    """Width of a monospace string on the character grid."""
    return len(s) * CW * size


def delay(d: float, *more: float) -> str:
    return "animation-delay:" + ",".join(f"{x:.2f}s" for x in (d, *more))


def text(x, y, s, size, fill, *, font="m", weight=None, anchor=None, fit=False,
         cls=None, style=None, raw=False) -> str:
    a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'class="{font}{" " + cls if cls else ""}"',
         f'font-size="{size:g}"', f'fill="{fill}"']
    if weight:
        a.append(f'font-weight="{weight}"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    if fit:
        n = len(re.sub(r"<[^>]+>", "", s)) if raw else len(s)
        a.append(f'textLength="{n * CW * size:.1f}" lengthAdjust="spacing"')
    if style:
        a.append(f'style="{style}"')
    return f'<text {" ".join(a)}>{s if raw else esc(s)}</text>'


def span(s: str, fill: str, weight: str | None = None) -> str:
    w = f' font-weight="{weight}"' if weight else ""
    return f'<tspan fill="{fill}"{w}>{esc(s)}</tspan>'


def plain(spans: str) -> str:
    return re.sub(r"<[^>]+>", "", spans)


def fade(body: str, at: float) -> str:
    return f'<g class="f" style="{delay(at)}">{body}</g>'


def chevron(x, y, size, color, at=None) -> str:
    h = size * 0.56
    top = y - size * 0.68
    w = h * 0.55
    anim = f' class="k" style="{delay(at)}"' if at is not None else ""
    return (f'<path{anim} d="M{x:.1f} {top:.1f}L{x + w:.1f} {top + h / 2:.1f}L{x:.1f} {top + h:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{size * 0.14:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def arrow(x, y, color, size=7) -> str:
    """A small north-east arrow whose bottom-left corner sits at (x, y)."""
    return (f'<path d="M{x:.1f} {y:.1f}L{x + size:.1f} {y - size:.1f}'
            f'M{x + size * 0.25:.1f} {y - size:.1f}H{x + size:.1f}V{y - size * 0.75:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')


def typed(x, y, s, size, fill, start, step):
    out = [
        text(x + i * CW * size, y, ch, size, fill, cls="k", style=delay(start + i * step))
        for i, ch in enumerate(s) if ch != " "
    ]
    return "".join(out), start + len(s) * step


def prompt(x, y, cmd, size, th, *, start=None, step=0.06, comment=None):
    """A shell prompt line. With `start`, the command is typed out one key at a time."""
    cx = x + 2 * CW * size
    if start is None:
        out, end = chevron(x, y, size, th["accent"]) + text(cx, y, cmd, size, th["text"], fit=True), 0.0
    else:
        keys, end = typed(cx, y, cmd, size, th["text"], start, step)
        out = chevron(x, y, size, th["accent"], at=start - 0.15) + keys
    if comment:
        out += text(cx + mw(cmd + "  ", size), y, comment, size, th["dim"], fit=True)
    return out, end


def cursor(x, y, size, th, at=0.0) -> str:
    return (f'<rect class="b" style="{delay(at, at)}" x="{x:.1f}" y="{y - size * 0.82:.1f}" '
            f'width="{CW * size:.1f}" height="{size * 1.02:.1f}" fill="{th["text2"]}"/>')


def window(W, H, th, title="", right="", lights=True, bar=BAR, tab=None) -> list[str]:
    r = 10
    o = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="{r}" fill="{th["body"]}"/>',
        f'<path d="M.5 {bar}V{r + .5}A{r} {r} 0 0 1 {r + .5} .5H{W - r - .5}A{r} {r} 0 0 1 {W - .5} {r + .5}V{bar}Z" '
        f'fill="{th["bar"]}"/>',
        f'<path d="M.5 {bar}H{W - .5}" stroke="{th["line"]}"/>',
    ]
    if lights:
        o += [f'<circle cx="{20 + i * 18}" cy="{bar / 2}" r="5.5" fill="{c}"/>' for i, c in enumerate(LIGHTS)]
    if tab:
        tx, tw = 80, mw(tab, 12.5) + 44
        o += [
            f'<path d="M{tx} {bar + .5}V{14}A6 6 0 0 1 {tx + 6} 8H{tx + tw - 6}A6 6 0 0 1 {tx + tw} 14V{bar + .5}Z" '
            f'fill="{th["body"]}" stroke="{th["line"]}"/>',
            f'<path d="M{tx + 1} {bar + .5}H{tx + tw - 1}" stroke="{th["body"]}" stroke-width="2"/>',
            f'<path d="M{tx + 6} 8.5H{tx + tw - 6}" stroke="{th["accent"]}" stroke-width="2"/>',
            f'<rect x="{tx + 14}" y="{bar / 2 - 1.5}" width="9" height="9" rx="2" fill="{th["accent"]}" opacity=".85"/>',
            text(tx + 30, bar / 2 + 8, tab, 12.5, th["text"], fit=True),
        ]
    if title:
        o.append(text(W / 2, bar / 2 + 4.5, title, 12.5, th["muted"], anchor="middle", fit=True))
    if right:
        o.append(text(W - 18, bar / 2 + 4.5, right, 11.5, th["dim"], anchor="end", fit=True))
    return o


def frame(W, H, th) -> str:
    return f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{th["line"]}"/>'


def svg(W, H, label, body) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{esc(label)}"><title>{esc(label)}</title>{CSS}{body}</svg>\n'
    )


def check(ok: bool, what: str) -> None:
    if not ok:
        raise ValueError(what)


# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------


def banner(x, y, words, cell, th, start, step=0.035):
    """The name in pixel letters, each letter dropping in after the last."""
    out, col, n = [], 0, 0
    for wi, word in enumerate(words):
        fg = th["text"] if wi == 0 else th["accent"]
        sh = th["shadow"] if wi == 0 else th["shadow2"]
        for ch in word:
            back, front = [], []
            for ry, row in enumerate(PIXELS[ch]):
                for rx, bit in enumerate(row):
                    if bit == "#":
                        px, py = x + (col + rx) * cell, y + ry * cell
                        back.append(f'<rect x="{px + 2:g}" y="{py + 2:g}" width="{cell - 1}" height="{cell - 1}" rx="1.2"/>')
                        front.append(f'<rect x="{px:g}" y="{py:g}" width="{cell - 1}" height="{cell - 1}" rx="1.2"/>')
            out.append(fade(f'<g fill="{sh}">{"".join(back)}</g><g fill="{fg}">{"".join(front)}</g>', start + n * step))
            col, n = col + 6, n + 1
        col += 3
    return "".join(out), (col - 4) * cell, start + n * step


def header(th) -> str:
    W, H, X, S = 880, 404, 32, 14
    o = window(W, H, th, PROFILE["host"], "zsh")
    p, t = prompt(X, 80, "whoami", S, th, start=0.35, step=0.07)
    o.append(p)
    b, width, t = banner(X + 1, 102, PROFILE["banner"], 7, th, start=t + 0.15)
    check(width <= W - 2 * X, f"banner too wide ({width}px)")
    o.append(b)
    t += 0.2
    for i, line in enumerate(PROFILE["tagline"]):
        check(mw(line, 13.5) <= W - 2 * X, "tagline line too wide")
        o.append(fade(text(X, 190 + i * 22, line, 13.5, th["text2"], fit=True), t + i * 0.1))
    p, t = prompt(X, 252, "cat status.txt", S, th, start=t + 0.5, step=0.045)
    o.append(p)
    vx = X + 16 + mw("study   ", 13.5)
    for i, (k, v) in enumerate(PROFILE["status"]):
        y = 280 + i * 23
        row = text(X + 16, y, k, 13.5, th["dim"], fit=True) + text(vx, y, v, 13.5, th["text"], fit=True)
        if k == "next":
            row += f'<circle class="p" cx="{vx + mw(v, 13.5) + 14:.1f}" cy="{y - 4.5}" r="4" fill="{th["green"]}"/>'
        o.append(fade(row, t + 0.15 + i * 0.1))
    t += 0.15 + len(PROFILE["status"]) * 0.1 + 0.25
    o += [chevron(X, 384, S, th["accent"], at=t), cursor(X + 2 * CW * S, 384, S, th, at=t), frame(W, H, th)]
    return svg(W, H, header_alt(), "".join(o))


def header_alt() -> str:
    return ("Shashikant Rajput. " + " ".join(PROFILE["tagline"]) + " "
            + " ".join(f"{k}: {v}." for k, v in PROFILE["status"]))


def link_badge(label, th) -> str:
    S, H = 13, 36
    W = round(14 + 2 * CW * S + mw(label, S) + 12 + 8 + 14)
    o = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="{th["body"]}" stroke="{th["line"]}"/>',
        chevron(14, 23, S, th["accent"]),
        text(14 + 2 * CW * S, 23, label, S, th["text"], fit=True),
        arrow(W - 14 - 8, 22, th["muted"], 8),
    ]
    return svg(W, H, label, "".join(o))


def section(cmd, comment, th) -> str:
    W, H, S = 880, 40, 14
    p, _ = prompt(6, 26, cmd, S, th, comment=comment)
    return svg(W, H, f"{cmd} {comment}", p)


def metric_spans(metric, th) -> str:
    parts = re.split(r"((?<![\w@])\d[\d.]*(?:–\d[\d.]*)?(?: ?(?:s|GB)\b)?|→)", metric)
    out = []
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2:
            out.append(span(part, th["accent"] if part == "→" else th["green"], "600"))
        else:
            out.append(span(part, th["text"]))
    return "".join(out)


def card(c, th) -> str:
    W, H, X, bar = 460, 272, 24, 36
    o = window(W, H, th, lights=False, bar=bar)
    o.append(text(X, 23, span("~/", th["dim"]) + span(c["path"], th["muted"]), 12, th["muted"], raw=True, fit=True))
    o.append(text(W - X - 14, 23, c["kind"], 12, th["text2"], anchor="end", fit=True))
    o.append(arrow(W - X - 7, 21, th["text2"]))
    o.append(text(X, 80, c["title"], 23, th["text"], font="s", weight="700"))
    o.append(text(X, 103, c["tags"], 12, th["accent"], fit=True))
    lines = wrap(c["desc"], 52)
    check(len(lines) <= 3, f"{c['slug']}: description runs to {len(lines)} lines")
    for i, line in enumerate(lines):
        o.append(text(X, 134 + i * 22, line, 15, th["text2"], font="s"))
    check(mw(c["metric"], 13) + 16 <= W - 2 * X, f"{c['slug']}: metric too wide")
    o.append(f'<path d="M{X} 201.5l7 4.5-7 4.5z" fill="{th["accent"]}"/>')
    o.append(text(X + 16, 210, metric_spans(c["metric"], th), 13, th["text"], raw=True, fit=True))
    x = X
    for item in c["stack"]:
        w = mw(item, 11.5) + 16
        o.append(f'<rect x="{x:.1f}" y="226.5" width="{w:.1f}" height="24" rx="6" fill="{th["chip"]}" stroke="{th["line"]}"/>')
        o.append(text(x + 8, 242.5, item, 11.5, th["text2"], fit=True))
        x += w + 6
    check(x - 6 <= W - X, f"{c['slug']}: stack chips too wide")
    o.append(frame(W, H, th))
    alt = f'{c["title"]} ({c["tags"]}): {c["desc"]} {c["metric"]}. Stack: {", ".join(c["stack"])}.'
    return svg(W, H, alt, "".join(o))


def more_card(c, th) -> str:
    W, H, X, bar = 292, 112, 16, 30
    o = window(W, H, th, lights=False, bar=bar)
    check(mw("~/" + c["path"], 11) <= W - 2 * X - 16, f"{c['slug']}: path too wide")
    o.append(text(X, 19.5, span("~/", th["dim"]) + span(c["path"], th["muted"]), 11, th["muted"], raw=True, fit=True))
    o.append(arrow(W - X - 7, 18.5, th["text2"]))
    o.append(text(X, 60, c["title"], 16, th["text"], font="s", weight="700"))
    lines = wrap(c["desc"], 42)
    check(len(lines) <= 2, f"{c['slug']}: description runs to {len(lines)} lines")
    for i, line in enumerate(lines):
        o.append(text(X, 82 + i * 18, line, 13, th["muted"], font="s"))
    o.append(frame(W, H, th))
    return svg(W, H, f'{c["title"]}: {c["desc"]}', "".join(o))


def career(th) -> str:
    W, X = 880, 32
    lanes = {"work": 46, "edu": 70}
    colors = {"work": th["accent"], "edu": th["purple"]}
    DX, CX = 98, 236
    o_body = []
    p, _ = prompt(X, 78, "git log --graph --all", 14, th)
    o_body.append(p)

    y = 122
    rows = []
    for r in CAREER:
        lines = wrap(r["detail"], 84) if r["detail"] else []
        rows.append((r, y, lines))
        y += 22 + 20 * len(lines) + 18
    H = y + 4

    def node_y(row_y):
        return row_y - 5

    lines_svg = []
    work = [node_y(ry) for r, ry, _ in rows if r["lane"] == "work"]
    edu = [node_y(ry) for r, ry, _ in rows if r["lane"] == "edu"]
    lw, le = lanes["work"], lanes["edu"]
    lines_svg.append(f'<path d="M{lw} {work[0]}V{work[-1]}" stroke="{colors["work"]}" stroke-width="2"/>')
    lines_svg.append(f'<path d="M{le} {work[0]}V{edu[0]}" stroke="{colors["edu"]}" stroke-width="2" stroke-dasharray="3 4" opacity=".8"/>')
    lines_svg.append(f'<path d="M{le} {edu[0]}V{edu[-1]}" stroke="{colors["edu"]}" stroke-width="2"/>')
    # Work branched off while the diploma was still running.
    y1, y2 = edu[-1], work[-1]
    lines_svg.append(
        f'<path d="M{le} {y1}C{le} {y1 - 18} {lw} {y2 + 18} {lw} {y2}" fill="none" stroke="{colors["work"]}" stroke-width="2"/>'
    )

    first_edu = next(r for r in CAREER if r["lane"] == "edu")
    nodes, content = [], []
    for r, ry, lines in rows:
        lx, color, ny = lanes[r["lane"]], colors[r["lane"]], node_y(ry)
        if r.get("head"):
            nodes.append(f'<circle class="p" cx="{lx}" cy="{ny}" r="10" fill="{th["green"]}" opacity=".18"/>')
            nodes.append(f'<circle cx="{lx}" cy="{ny}" r="5.5" fill="{th["green"]}" stroke="{th["body"]}" stroke-width="2"/>')
        else:
            nodes.append(f'<circle cx="{lx}" cy="{ny}" r="5" fill="{th["body"]}" stroke="{color}" stroke-width="2.2"/>')
        content.append(text(DX, ry, r["dates"], 12.5, th["yellow"], fit=True))
        content.append(text(
            CX, ry,
            span(r["role"], th["text"], "600") + span("  ·  ", th["dim"]) + span(r["org"], th["text2"]),
            15, th["text"], font="s", raw=True,
        ))
        if r.get("head"):
            deco = span("(", th["yellow"]) + span("HEAD", th["blue"], "700") + span(" → ", th["blue"]) \
                + span("work", th["green"], "700") + span(")", th["yellow"])
        elif r is first_edu:
            deco = span("(", th["yellow"]) + span("edu", th["purple"], "700") + span(")", th["yellow"])
        else:
            deco = ""
        if deco:
            content.append(text(W - X, ry, deco, 12, th["text"], anchor="end", raw=True, fit=True))
        for i, line in enumerate(lines):
            content.append(text(CX, ry + 22 + i * 20, line, 13.5, th["muted"], font="s"))

    o = window(W, H, th, "~/career — git", "zsh") + o_body + lines_svg + nodes + content + [frame(W, H, th)]
    alt = "Career, as a git log. " + " ".join(
        f'{r["dates"]}: {r["role"]}, {r["org"]}. {r["detail"]}'.strip() for r in CAREER
    )
    return svg(W, H, alt, "".join(o))


def stack(th) -> str:
    W, S, LH = 880, 14, 25
    top = 74
    code = [[("# what I build with", th["dim"])]]
    keyw = max(len(k) for k, _ in STACK) + 2
    for key, items in STACK:
        toks = [(key, th["accent"]), (":" + " " * (keyw - len(key) - 1), th["muted"]), ("[", th["muted"])]
        for i, item in enumerate(items):
            toks.append((item, th["string"]))
            if i < len(items) - 1:
                toks.append((", ", th["muted"]))
        toks.append(("]", th["muted"]))
        code.append(toks)
    H = top + (len(code) - 1) * LH + 24 + 26
    o = window(W, H, th, right="YAML", tab="stack.yaml")
    gx, cx = 46, 66
    for n, toks in enumerate(code):
        y = top + n * LH
        o.append(text(gx, y, str(n + 1), 12.5, th["dim"], anchor="end"))
        col = 0
        for s, fill in toks:
            if s.strip():
                lead = len(s) - len(s.lstrip())
                o.append(text(cx + (col + lead) * CW * S, y, s.strip(), S, fill, fit=True))
            col += len(s)
        check(cx + col * CW * S <= W - 20, f"stack line {n + 1} too wide")
    # Status bar.
    sb = H - 26
    o += [
        f'<path d="M.5 {sb}H{W - .5}V{H - 10.5}A10 10 0 0 1 {W - 10.5} {H - .5}H10.5A10 10 0 0 1 .5 {H - 10.5}Z" fill="{th["bar"]}"/>',
        f'<path d="M.5 {sb}H{W - .5}" stroke="{th["line"]}"/>',
        f'<g fill="none" stroke="{th["muted"]}" stroke-width="1.4">'
        f'<circle cx="20" cy="{sb + 8}" r="2.2"/><circle cx="20" cy="{sb + 19}" r="2.2"/>'
        f'<circle cx="28" cy="{sb + 10}" r="2.2"/><path d="M20 {sb + 10.2}V{sb + 16.8}M28 {sb + 12.2}C28 {sb + 15} 20 {sb + 14} 20 {sb + 16.5}"/></g>',
        text(38, sb + 17.5, "main", 11.5, th["muted"], fit=True),
        text(W - 18, sb + 17.5, "UTF-8   LF   Ln 7, Col 1", 11.5, th["dim"], anchor="end", fit=True),
        frame(W, H, th),
    ]
    alt = "Toolbox, as stack.yaml. " + " ".join(f"{k}: {', '.join(v)}." for k, v in STACK)
    return svg(W, H, alt, "".join(o))


def footer(th) -> str:
    W, X, S = 880, 32, 14
    H = 354
    o = window(W, H, th, PROFILE["host"], "zsh")
    p, _ = prompt(X, 78, "cat wins.log", S, th)
    o.append(p)
    vx = X + 16 + mw("1st place   ", 13.5)
    for i, (k, v) in enumerate(WINS):
        y = 106 + i * 23
        o.append(text(X + 16, y, k, 13.5, th["yellow"], fit=True))
        o.append(text(vx, y, v, 13.5, th["text2"], fit=True))
    p, _ = prompt(X, 242, "echo $NEXT", S, th)
    o.append(p)
    check(mw(NEXT, 13.5) <= W - 2 * X - 16, "NEXT too wide")
    o.append(text(X + 16, 270, NEXT, 13.5, th["text"], fit=True))
    o.append(text(X + 16, 294, "mail", 13.5, th["dim"], fit=True))
    o.append(text(X + 16 + mw("mail  ", 13.5), 294, "→ " + EMAIL, 13.5, th["accent"], fit=True))
    o += [chevron(X, 332, S, th["accent"]), cursor(X + 2 * CW * S, 332, S, th), frame(W, H, th)]
    alt = ("Recognition. " + " ".join(f"{k}: {v}." for k, v in WINS) + f" Next: {NEXT} Email {EMAIL}.")
    return svg(W, H, alt, "".join(o))


# ---------------------------------------------------------------------------
# README
# ---------------------------------------------------------------------------


def picture(name, alt, size) -> str:
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<img src="assets/{name}-light.svg" {size} alt="{esc(alt)}"></picture>')


def linked(href, body) -> str:
    return f'<a href="{href}">{body}</a>'


def readme() -> str:
    blocks = [
        picture("header", header_alt(), 'width="100%"'),
        "<p>\n" + "\n".join(
            linked(href, picture(f"link-{slug}", label, 'height="34"')) for slug, label, href in LINKS
        ) + "\n</p>",
        picture("section-projects", "ls ~/projects", 'width="100%"'),
    ]
    for i in range(0, len(PROJECTS), 2):
        pair = PROJECTS[i:i + 2]
        blocks.append("<p>\n" + "\n".join(
            linked(c["href"], picture(f"card-{c['slug']}",
                   f'{c["title"]}: {c["desc"]} {c["metric"]}.', 'width="49%"'))
            for c in pair
        ) + "\n</p>")
    blocks.append("<p>\n" + "\n".join(
        linked(c["href"], picture(f"more-{c['slug']}", f'{c["title"]}: {c["desc"]}', 'width="32.4%"'))
        for c in MORE
    ) + "\n</p>")
    blocks.append(picture("career", "Experience and education: " + "; ".join(
        f'{r["role"]}, {r["org"]} ({r["dates"].replace("→", "to")})' for r in CAREER), 'width="100%"'))
    blocks.append(picture("stack", "Toolbox: " + "; ".join(
        f"{k}: {', '.join(v)}" for k, v in STACK), 'width="100%"'))
    blocks.append(linked(f"mailto:{EMAIL}", picture("footer", "Recognition: " + "; ".join(
        f"{k}, {v}" for k, v in WINS) + f". {NEXT} Email: {EMAIL}", 'width="100%"')))
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    files: dict[str, str] = {}
    for name, th in THEMES.items():
        files[f"header-{name}.svg"] = header(th)
        files[f"section-projects-{name}.svg"] = section("ls ~/projects", "# selected work", th)
        for slug, label, _ in LINKS:
            files[f"link-{slug}-{name}.svg"] = link_badge(label, th)
        for c in PROJECTS:
            files[f"card-{c['slug']}-{name}.svg"] = card(c, th)
        for c in MORE:
            files[f"more-{c['slug']}-{name}.svg"] = more_card(c, th)
        files[f"career-{name}.svg"] = career(th)
        files[f"stack-{name}.svg"] = stack(th)
        files[f"footer-{name}.svg"] = footer(th)
    for old in ASSETS.glob("*.svg"):
        if old.name not in files:
            old.unlink()
    for fname, body in files.items():
        (ASSETS / fname).write_text(body, encoding="utf-8")
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    print(f"wrote README.md and {len(files)} images to {ASSETS}")


if __name__ == "__main__":
    main()
