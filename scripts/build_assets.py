"""Render the SVG assets used by the profile README.

Edit the data below, then run:

    python scripts/build_assets.py

Every asset is written twice, for GitHub's light and dark themes.
Only the standard library is used.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
SERIF = "'Playfair Display', Georgia, 'Times New Roman', serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "light": {
        "bg": "#ffffff", "line": "#d3d2d2", "soft": "#ebebeb", "text": "#0a0a0a",
        "text2": "#2b2b2b", "muted": "#6b6b6b", "label": "#8c8c8c", "accent": "#d40d0d",
        "dot": "#d6d6d6", "chip": "#f6f6f6", "live": "#1a7f37",
    },
    "dark": {
        "bg": "#0d1117", "line": "#30363d", "soft": "#21262d", "text": "#f0f3f6",
        "text2": "#d1d7e0", "muted": "#9198a1", "label": "#7d8590", "accent": "#ff5a52",
        "dot": "#262c34", "chip": "#151b23", "live": "#3fb950",
    },
}

HEADER = {
    "label_left": "GITHUB.COM/CODESEEBOY",
    "label_right": "MUMBAI, INDIA",
    "kicker": "AI ENGINEER",
    "name": "Shashikant Rajput",
    "lede": [
        "I build LLM applications, retrieval pipelines and",
        "computer-vision models, and the backends they run on.",
    ],
    "status": "Intern AI Engineer at ADDLYFT  /  B.Tech AI & ML, final year  /  Open to roles from mid-2027",
    # The small agent graph on the right: one node per step.
    "graph": ["query", "retrieve", "rerank", "reason", "answer + citations"],
}

# Cards for "Selected work". `corner` is the label shown top-right.
CARDS = [
    {
        "slug": "non8",
        "tag": "AGENTS · RAG · OFFLINE",
        "title": "NON8",
        "corner": "CASE STUDY ↗",
        "desc": "Offline AI workbench for sensitive documents. A LangGraph agent "
                "answers from private files on local models and cites every source.",
        "metric": "Simple queries 60–80 s → 0.8 s on a 12 GB GPU",
        "stack": "LangGraph · Ollama · FAISS · FastAPI · React",
    },
    {
        "slug": "clausewise",
        "tag": "RETRIEVAL · EVALUATION",
        "title": "Clausewise",
        "corner": "REPO ↗",
        "desc": "Policy search that answers only from the clause it found. "
                "Benchmarks vector, hybrid and reranked retrieval on one corpus.",
        "metric": "NDCG@5  vector 0.878 · hybrid 0.794 · rerank 0.928",
        "stack": "Qdrant · BM25 · bge-reranker · Ollama · Docker",
    },
    {
        "slug": "urbanfix",
        "tag": "COMPUTER VISION · CAPSTONE",
        "title": "UrbanFix AI",
        "corner": "REPO ↗",
        "desc": "Civic-issue reporting app. Reads a citizen's photo, scores "
                "urgency and routes the issue to the right department.",
        "metric": "v1 SigLIP + YOLOv8 · v2 Gemini on Vertex AI",
        "stack": "Expo · Node.js · Supabase · Kafka · Spark",
    },
    {
        "slug": "trustlayer",
        "tag": "LLM VERIFICATION · HACKATHON",
        "title": "TrustLayer AI",
        "corner": "REPO ↗",
        "desc": "Splits an AI answer into claims, checks each one against "
                "Wikipedia and web search, and scores how far to trust it.",
        "metric": "Top national finalist, GFG ByteQuest",
        "stack": "Next.js · Express · Gemini → Groq → OpenRouter",
    },
    {
        "slug": "countx",
        "tag": "COMPUTER VISION · RETAIL",
        "title": "CountX",
        "corner": "REPO ↗",
        "desc": "Shelf counting for a US convenience-store client. Detects "
                "12 drink SKUs and prices the count from a price book.",
        "metric": "YOLOv8n · image, video and live camera",
        "stack": "YOLOv8 · OpenCV · EasyOCR · Gradio",
    },
    {
        "slug": "llm-gateway",
        "tag": "LLM INFRASTRUCTURE",
        "title": "LLM Gateway",
        "corner": "REPO ↗",
        "desc": "One API in front of nine LLM providers. Tries them in order "
                "and falls back when one is rate-limited or down.",
        "metric": "Text, images, PDFs and office files in one call",
        "stack": "FastAPI · Gemini · Groq · OpenRouter · Mistral",
    },
]

STACK = [
    ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "SQL"]),
    ("LLM + RETRIEVAL", ["LangGraph", "RAG", "Hybrid search", "Reranking", "Ollama", "FAISS", "Qdrant", "Gemini / Vertex AI"]),
    ("VISION", ["YOLOv8", "OpenCV", "SigLIP", "PyTorch"]),
    ("BACKEND", ["FastAPI", "Node.js", "Express", "NestJS", "PostgreSQL", "Prisma", "Supabase"]),
    ("CLOUD", ["AWS Lambda", "DynamoDB", "SQS", "EventBridge", "Docker", "GitHub Actions"]),
]


def style() -> str:
    return f"""<style>
  .sans {{ font-family: {SANS}; }}
  .serif {{ font-family: {SERIF}; }}
  .mono {{ font-family: {MONO}; }}
  .live {{ animation: pulse 2.4s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }}
  @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{ .live, .travel {{ animation: none; display: none; }} }}
</style>"""


def corners(x: float, y: float, w: float, h: float, color: str, size: float = 14) -> str:
    """Registration marks on the four corners of a frame."""
    r, b = x + w, y + h
    paths = [
        f"M{x} {y + size}V{y}H{x + size}",
        f"M{r - size} {y}H{r}V{y + size}",
        f"M{r} {b - size}V{b}H{r - size}",
        f"M{x + size} {b}H{x}V{b - size}",
    ]
    return "".join(
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"/>' for d in paths
    )


def text(x, y, s, cls, size, fill, weight=400, anchor="start", spacing=0) -> str:
    extra = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{extra}>{escape(s)}</text>'
    )


def svg(w: int, h: int, title: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>{style()}{body}</svg>\n"
    )


def header(t: dict) -> str:
    W, H, pad = 1200, 380, 20
    fx, fy, fw, fh = pad, pad, W - 2 * pad, H - 2 * pad
    left = fx + 44
    parts = [
        f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
        # Dot grid behind the graph, faded towards the text.
        '<defs>'
        f'<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.3" fill="{t["dot"]}"/></pattern>'
        '<radialGradient id="fade" cx="0.78" cy="0.5" r="0.42">'
        '<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>'
        '</defs>',
        f'<rect x="{fx}" y="{fy + 48}" width="{fw}" height="{fh - 104}" fill="url(#dots)" mask="url(#m)"/>',
        f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="{t["line"]}"/>',
        corners(fx, fy, fw, fh, t["text"]),
        # Top label row.
        text(left, fy + 31, HEADER["label_left"], "mono", 13, t["label"], spacing=2),
        text(fx + fw - 44, fy + 31, HEADER["label_right"], "mono", 13, t["label"], anchor="end", spacing=2),
        f'<line x1="{fx}" y1="{fy + 48}" x2="{fx + fw}" y2="{fy + 48}" stroke="{t["soft"]}"/>',
        # Name block.
        text(left, 128, HEADER["kicker"], "mono", 15, t["accent"], 600, spacing=4),
        text(left - 3, 204, HEADER["name"], "serif", 74, t["text"], 700),
        text(left, 252, HEADER["lede"][0], "sans", 23, t["text2"]),
        text(left, 284, HEADER["lede"][1], "sans", 23, t["text2"]),
        # Status row.
        f'<line x1="{fx}" y1="{fy + fh - 52}" x2="{fx + fw}" y2="{fy + fh - 52}" stroke="{t["soft"]}"/>',
        f'<circle class="live" cx="{left + 5}" cy="{fy + fh - 31}" r="5" fill="{t["live"]}"/>',
        text(left + 22, fy + fh - 26, HEADER["status"], "mono", 14, t["muted"]),
    ]
    parts.append(graph(t, x=860, y=96))
    return svg(W, H, "Shashikant Rajput, AI engineer", "".join(parts))


def graph(t: dict, x: int, y: int) -> str:
    """A small agent graph: a vertical chain of steps with a dot travelling down it."""
    nodes = HEADER["graph"]
    nw, nh, gap = 196, 30, 13
    cx = x + nw / 2
    out = []
    for i, label in enumerate(nodes):
        ny = y + i * (nh + gap)
        last = i == len(nodes) - 1
        stroke = t["accent"] if last else t["line"]
        out.append(f'<rect x="{x}" y="{ny}" width="{nw}" height="{nh}" fill="{t["bg"]}" stroke="{stroke}"/>')
        out.append(text(x + 12, ny + 20, f"{i + 1:02d}", "mono", 11, t["label"]))
        out.append(text(x + 40, ny + 20, label, "mono", 13, t["text"] if last else t["text2"]))
        if not last:
            out.append(f'<line x1="{cx}" y1="{ny + nh}" x2="{cx}" y2="{ny + nh + gap}" stroke="{t["line"]}"/>')
    # Side loop: "reason" calls tools and comes back.
    ry = y + 3 * (nh + gap) + nh / 2
    tx = x + nw + 34
    out.append(f'<path d="M{x + nw} {ry - 6}H{tx}" stroke="{t["line"]}" fill="none"/>')
    out.append(f'<path d="M{tx} {ry + 6}H{x + nw}" stroke="{t["line"]}" fill="none" stroke-dasharray="3 3"/>')
    out.append(f'<rect x="{tx}" y="{ry - 15}" width="62" height="30" fill="{t["bg"]}" stroke="{t["line"]}"/>')
    out.append(text(tx + 31, ry + 4, "tools", "mono", 12, t["muted"], anchor="middle"))
    # Travelling dot.
    top, bottom = y + nh / 2, y + (len(nodes) - 1) * (nh + gap) + nh / 2
    out.append(
        f'<circle class="travel" r="3.5" fill="{t["accent"]}">'
        f'<animateMotion dur="3.6s" repeatCount="indefinite" '
        f'path="M{x - 14} {top}V{bottom}"/></circle>'
    )
    out.append(f'<line x1="{x - 14}" y1="{top}" x2="{x - 14}" y2="{bottom}" stroke="{t["soft"]}"/>')
    return "".join(out)


def card(c: dict, index: int, t: dict) -> str:
    W, H = 540, 272
    px = 28
    lines = wrap(c["desc"], 52)
    if len(lines) > 3:
        raise ValueError(f"{c['slug']}: description too long ({len(lines)} lines)")
    corner_color = t["text"]
    parts = [
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="{t["bg"]}" stroke="{t["line"]}"/>',
        corners(1, 1, W - 2, H - 2, t["text"], 12),
        text(px, 34, f"{index:02d}", "mono", 12.5, t["accent"], 600, spacing=1.5),
        text(px + 30, 34, c["tag"], "mono", 12.5, t["label"], spacing=1.5),
        text(W - px, 34, c["corner"], "mono", 12.5, corner_color, 600, anchor="end", spacing=1.5),
        f'<line x1="1" y1="52" x2="{W - 1}" y2="52" stroke="{t["soft"]}"/>',
        text(px - 1, 98, c["title"], "serif", 32, t["text"], 700),
    ]
    for i, line in enumerate(lines):
        parts.append(text(px, 132 + i * 24, line, "sans", 17, t["text2"]))
    parts += [
        f'<line x1="1" y1="{H - 74}" x2="{W - 1}" y2="{H - 74}" stroke="{t["soft"]}"/>',
        text(px, H - 44, c["metric"], "mono", 14, t["text"], 600),
        text(px, H - 20, c["stack"], "mono", 13, t["muted"]),
    ]
    alt = f'{c["title"]}: {c["desc"]} {c["metric"]}. {c["stack"]}.'
    return svg(W, H, alt, "".join(parts))


def stack(t: dict) -> str:
    W, pad, row_h = 1200, 20, 50
    char_w, chip_h = 8.4, 30
    # Label row (48) + top gap (22) + rows + bottom gap (24), inside the frame.
    H = 2 * pad + 48 + 22 + row_h * (len(STACK) - 1) + chip_h + 24
    fx, fy, fw, fh = pad, pad, W - 2 * pad, H - 2 * pad
    parts = [
        f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>',
        f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="{t["line"]}"/>',
        corners(fx, fy, fw, fh, t["text"]),
        text(fx + 44, fy + 31, "TOOLBOX", "mono", 13, t["label"], spacing=2),
        f'<line x1="{fx}" y1="{fy + 48}" x2="{fx + fw}" y2="{fy + 48}" stroke="{t["soft"]}"/>',
    ]
    y = fy + 48 + 22
    for label, items in STACK:
        parts.append(text(fx + 44, y + 20, label, "mono", 13, t["accent"], 600, spacing=1.5))
        x = fx + 260
        for item in items:
            w = len(item) * char_w + 26
            parts.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{chip_h}" fill="{t["chip"]}" stroke="{t["line"]}"/>')
            parts.append(text(x + 13, y + 20, item, "mono", 14, t["text2"]))
            x += w + 10
        if x > fx + fw - 30:
            raise ValueError(f"{label}: row too wide ({x:.0f}px)")
        y += row_h
    alt = "Toolbox. " + " ".join(f"{label.title().replace('Llm', 'LLM')}: {', '.join(items)}." for label, items in STACK)
    return svg(W, H, alt, "".join(parts))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"stack-{name}.svg").write_text(stack(t), encoding="utf-8")
        for i, c in enumerate(CARDS, start=1):
            (OUT / f"card-{c['slug']}-{name}.svg").write_text(card(c, i, t), encoding="utf-8")
    print(f"wrote {len(list(OUT.glob('*.svg')))} files to {OUT}")


if __name__ == "__main__":
    main()
