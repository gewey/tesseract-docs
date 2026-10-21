#!/usr/bin/env python3
"""Compile the docs module's markdown into website pages.

Markdown stays the source of truth. This produces a sibling .html for every
authored .md so the module is a website, not a pile of text files.

Deliberately dependency-free and conservative: headings, fenced code, tables
(in the site's .param-table style), lists, blockquotes, rules, bold, italic,
inline code, and links. Anything it does not recognise is rendered as text.

Usage:
    python docs_compiler.py
    python docs_compiler.py --check
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent
SKIP = {"AGENTS.md", "README.md"}

HEAD_LOADER = """    <script>
        // Works from tesseract_city/docs/ (deployed) and from 01_Docs (authoring copy).
        (function () {
            var local = document.createElement("script");
            local.src = "../../js/dynamichead.js";
            local.onerror = function () {
                var remote = document.createElement("script");
                remote.src = "https://gewey.github.io/js/dynamichead.js";
                document.head.appendChild(remote);
            };
            document.head.appendChild(local);
        })();
    </script>"""


def _inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    return out


def _cells(row: str):
    s = row.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _is_sep(row: str) -> bool:
    return bool(re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", row)) and "-" in row


def render(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            i = j + 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{_inline(m.group(2).strip())}</h{level}>")
            i += 1
            continue

        if stripped == "---":
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|"):
            j = i
            rows = []
            while j < n and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            if len(rows) >= 2 and _is_sep(rows[1]):
                header = _cells(rows[0])
                out.append('<table class="param-table"><thead><tr>'
                           + "".join(f"<th>{_inline(c)}</th>" for c in header)
                           + "</tr></thead><tbody>")
                for row in rows[2:]:
                    cells = _cells(row)
                    out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells)
                               + "</tr>")
                out.append("</tbody></table>")
            else:
                out.append("<p>" + _inline(" ".join(r.strip() for r in rows)) + "</p>")
            i = j
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ol>")
            continue

        if stripped.startswith(">"):
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "".join(f"<p>{_inline(q)}</p>" for q in quote)
                       + "</blockquote>")
            continue

        if not stripped:
            i += 1
            continue

        para = []
        while i < n:
            cur = lines[i]
            s = cur.strip()
            if not s or s.startswith(("```", "|", ">", "---")) or re.match(r"^(#{1,6}\s|[-*]\s|\d+\.\s)", cur):
                break
            para.append(s)
            i += 1
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
        else:
            i += 1
    return "\n".join(out)


def _title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
    return fallback


def _menu(stems):
    entries = [
        ("index.html", "API Reference"),
        ("api_sdk_lmnop.html", "Surface (AOIT)"),
    ]
    entries += [(f"{stem}.html", stem.replace("_", " ")) for stem in stems]
    return [
        f'<a class="endpoint-btn" href="{href}" style="text-decoration:none;">'
        f'<span class="method-badge get">DOC</span>'
        f'<span>{html.escape(label)}</span></a>'
        for href, label in entries
    ]


def page(title: str, body: str, stems, source: str) -> str:
    return "\n".join([
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        HEAD_LOADER,
        "</head>",
        "<body>",
        '<div class="viewArea">',
        f'<div class="pageHeader"><marquee>⚙️ TESSERACT CITY — '
        f'{html.escape(title.upper())}</marquee></div>',
        '<div class="mainArea">',
        '<div class="pageLeftMenu">',
        '<div class="doc-nav-section">Docs</div>',
        *_menu(stems),
        "</div>",
        '<div class="pageContent">',
        '<div class="doc-stage active">',
        body,
        "</div>",
        "</div>",
        "</div>",
        f'<div class="pageFooter"><span>Compiled from {html.escape(source)} · '
        f'<a href="../../index.html">Homepage</a></span></div>',
        "</div>",
        "</body>",
        "</html>",
        "",
    ])


def compile_all(docs_dir=None, check_only: bool = False):
    docs = Path(docs_dir) if docs_dir else DOCS_DIR
    sources = sorted(p for p in docs.glob("*.md") if p.name not in SKIP)
    stems = [p.stem for p in sources]
    written = []
    for src in sources:
        md = src.read_text(encoding="utf-8")
        target = docs / (src.stem + ".html")
        if not check_only:
            target.write_text(
                page(_title(md, src.stem.replace("_", " ")), render(md), stems, src.name),
                encoding="utf-8",
            )
        written.append(target.name)
    return {"count": len(written), "files": written, "check_only": check_only}


if __name__ == "__main__":
    result = compile_all(check_only="--check" in sys.argv)
    print(result["count"], "page(s):", ", ".join(result["files"]))
