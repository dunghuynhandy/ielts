#!/usr/bin/env python3
"""Build static HTML site from SPEAKING markdown for GitHub Pages."""

import os
import re
import shutil
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

BASE = os.path.dirname(os.path.abspath(__file__))
SPEAKING = os.path.join(BASE, "SPEAKING ")
DOCS = os.path.join(BASE, "docs")
PERSONAL_SITE = os.path.join(os.path.dirname(BASE), "dunghuynhandy.github.io", "ielts")


def rel(path: str, depth: int = 0) -> str:
    prefix = "../" * depth
    return f"{prefix}{path.lstrip('/')}"

TOPICS = [
    ("01-advertising", "Advertising"),
    ("02-animal-rights", "Animal Rights"),
    ("03-cities", "Cities"),
    ("04-crime", "Crime"),
    ("05-education", "Education"),
    ("06-environment", "Environment"),
    ("07-family", "Family"),
    ("08-gender", "Gender"),
    ("09-genetic-engineering", "Genetic Engineering"),
    ("10-global-issues", "Global Issues"),
    ("11-government-and-society", "Government & Society"),
    ("12-guns-and-weapons", "Guns & Weapons"),
    ("13-health", "Health"),
    ("14-housing-and-architecture", "Housing & Architecture"),
    ("15-language", "Language"),
    ("16-money", "Money"),
    ("17-personality", "Personality"),
    ("18-sport-and-leisure", "Sport & Leisure"),
    ("19-television-internet-phones", "TV, Internet & Phones"),
    ("20-tourism", "Tourism"),
    ("21-traditional-vs-modern", "Traditional vs Modern"),
    ("22-transport", "Transport"),
    ("23-water", "Water"),
    ("24-work", "Work"),
]

BY_SOURCE = [
    ("ngocbach-q1-2024", "NgocBach Q1 2024"),
    ("ngocbach-q1-2022", "NgocBach Q1 2022"),
    ("ngocbach-q3", "NgocBach Q3"),
    ("ngocbach-q2-2022-may-sep", "NgocBach Q2 2022 (May–Sep)"),
]

MD = markdown.Markdown(extensions=[TableExtension(), FencedCodeExtension()])


def fix_links(html: str, depth: int = 0) -> str:
    prefix = "../" * depth

    def repl_md(m):
        href = m.group(1).replace(".md", ".html")
        anchor = m.group(2) or ""
        if href.startswith("examples/") or href.startswith("vocabulary/"):
            return f'href="{rel(href, depth)}{anchor}"'
        if href.startswith("by-source/"):
            return f'href="{rel("examples/" + href, depth)}{anchor}"'
        return f'href="{prefix}{href}{anchor}"'

    html = re.sub(r'href="([^"]+\.md)(#[^"]*)?"', repl_md, html)
    return html


def md_to_html(text: str, depth: int = 0) -> str:
    MD.reset()
    return fix_links(MD.convert(text), depth)


def page(title: str, body: str, active: str = "", depth: int = 0) -> str:
    prefix = "../" * depth
    nav = [
        ("home", "Home", f"{prefix}index.html"),
        ("summary", "Summary", f"{prefix}summary.html"),
        ("examples", "Examples", f"{prefix}examples/index.html"),
        ("vocabulary", "Vocabulary", f"{prefix}vocabulary/index.html"),
    ]
    nav_html = "".join(
        f'<a href="{href}" class="{"active" if key == active else ""}">{label}</a>'
        for key, label, href in nav
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — IELTS Speaking</title>
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
  <header class="site-header">
    <div class="inner">
      <a class="logo" href="{prefix}index.html">IELTS <span>Speaking</span></a>
      <nav>{nav_html}</nav>
    </div>
  </header>
  <main>{body}</main>
  <footer class="site-footer">
    <p>Personal study notes · <a href="https://github.com/dunghuynhandy/ielts">GitHub</a></p>
  </footer>
</body>
</html>"""


def write(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_index():
    topic_cards = "\n".join(
        f'<a class="card" href="examples/{slug}.html"><h3>{name}</h3><p>Part 1 · 2 · 3 questions</p></a>'
        for slug, name in TOPICS
    )
    body = f"""
  <section class="hero">
    <h1>IELTS Speaking Study Hub</h1>
    <p>Lessons, practice questions, and vocabulary from IELTS Fighter, IELTS Simon, and NgocBach — all in one place.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="examples/index.html">Browse Topics</a>
      <a class="btn btn-secondary" href="vocabulary/index.html">Vocabulary</a>
      <a class="btn btn-secondary" href="summary.html">Lesson Summary</a>
    </div>
  </section>
  <h2 class="section-title">24 Speaking Topics</h2>
  <div class="card-grid">{topic_cards}</div>
  <h2 class="section-title">Sources</h2>
  <div class="card-grid">
    <a class="card" href="summary.html"><h3>IELTS Fighter</h3><p>10 speaking lessons — Part 1, 2 & 3 techniques</p></a>
    <a class="card" href="examples/by-source/ngocbach-q1-2024.html"><h3>NgocBach</h3><p>Q1/Q2/Q3 predicted questions 2022–2024</p></a>
    <a class="card" href="vocabulary/22_06_2026.html"><h3>Vocabulary</h3><p>134 words + 120 collocations with CEFR levels</p></a>
  </div>
"""
    write(os.path.join(DOCS, "index.html"), page("Home", body, active="home"))


def build_summary():
    path = os.path.join(SPEAKING, "SUMMARY.md")
    with open(path, encoding="utf-8") as f:
        content = f.read()
    html = md_to_html(content)
    body = f'<div class="breadcrumb"><a href="index.html">Home</a> / Summary</div><div class="content">{html}</div>'
    write(os.path.join(DOCS, "summary.html"), page("Summary", body, active="summary"))


def build_examples_index():
    cards = "\n".join(
        f'<a class="card" href="{slug}.html"><h3>{name}</h3><p>Practice questions</p></a>'
        for slug, name in TOPICS
    )
    source_cards = "\n".join(
        f'<a class="card" href="by-source/{slug}.html"><h3>{name}</h3><p>Full PDF dump</p></a>'
        for slug, name in BY_SOURCE
    )
    readme_path = os.path.join(SPEAKING, "examples", "README.md")
    intro = ""
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            intro = md_to_html(f.read(), depth=1)
    body = f"""
  <div class="breadcrumb"><a href="../index.html">Home</a> / Examples</div>
  <div class="content">{intro}</div>
  <h2 class="section-title">Topics</h2>
  <div class="card-grid">{cards}</div>
  <h2 class="section-title">By Source</h2>
  <div class="card-grid">{source_cards}</div>
"""
    write(os.path.join(DOCS, "examples", "index.html"), page("Examples", body, active="examples", depth=1))


def build_example_pages():
    for slug, name in TOPICS:
        md_path = os.path.join(SPEAKING, "examples", f"{slug}.md")
        if not os.path.exists(md_path):
            continue
        with open(md_path, encoding="utf-8") as f:
            html = md_to_html(f.read(), depth=1)
        body = f"""
  <div class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Examples</a> / {name}</div>
  <div class="content">{html}</div>
"""
        write(os.path.join(DOCS, "examples", f"{slug}.html"), page(name, body, active="examples", depth=1))

    for slug, name in BY_SOURCE:
        md_path = os.path.join(SPEAKING, "examples", "by-source", f"{slug}.md")
        if not os.path.exists(md_path):
            continue
        with open(md_path, encoding="utf-8") as f:
            html = md_to_html(f.read(), depth=2)
        body = f"""
  <div class="breadcrumb"><a href="../../index.html">Home</a> / <a href="../index.html">Examples</a> / {name}</div>
  <div class="content">{html}</div>
"""
        write(os.path.join(DOCS, "examples", "by-source", f"{slug}.html"), page(name, body, active="examples", depth=2))


def build_vocabulary():
    vocab_files = []
    vocab_dir = os.path.join(SPEAKING, "vocabulary")
    if os.path.isdir(vocab_dir):
        for fn in sorted(os.listdir(vocab_dir)):
            if fn.endswith(".md"):
                vocab_files.append(fn)

    cards = "\n".join(
        f'<a class="card" href="{fn.replace(".md", ".html")}"><h3>{fn.replace(".md", "").replace("_", " ")}</h3><p>Vocabulary tables</p></a>'
        for fn in vocab_files
    )
    body = f"""
  <div class="breadcrumb"><a href="../index.html">Home</a> / Vocabulary</div>
  <section class="hero" style="padding-top:0">
    <h1>Vocabulary</h1>
    <p>Words, collocations, and phrases from IELTS Fighter lessons — with CEFR levels, phonetics, and Vietnamese.</p>
  </section>
  <div class="card-grid">{cards}</div>
"""
    write(os.path.join(DOCS, "vocabulary", "index.html"), page("Vocabulary", body, active="vocabulary", depth=1))

    for fn in vocab_files:
        md_path = os.path.join(vocab_dir, fn)
        with open(md_path, encoding="utf-8") as f:
            html = md_to_html(f.read(), depth=1)
        title = fn.replace(".md", "").replace("_", " ")
        body = f"""
  <div class="breadcrumb"><a href="../index.html">Home</a> / <a href="index.html">Vocabulary</a> / {title}</div>
  <div class="content">{html}</div>
"""
        write(os.path.join(DOCS, "vocabulary", fn.replace(".md", ".html")), page(title, body, active="vocabulary", depth=1))


def deploy_personal_site():
    """Copy built site to dunghuynhandy.github.io/ielts/ (already has Pages enabled)."""
    if not os.path.isdir(os.path.dirname(PERSONAL_SITE)):
        print(f"Skip personal deploy — {os.path.dirname(PERSONAL_SITE)} not found")
        return
    if os.path.exists(PERSONAL_SITE):
        shutil.rmtree(PERSONAL_SITE)
    shutil.copytree(DOCS, PERSONAL_SITE)
    print(f"Deployed to {PERSONAL_SITE}")


def main():
    # Keep assets, rebuild HTML
    for item in os.listdir(DOCS):
        p = os.path.join(DOCS, item)
        if item == "assets":
            continue
        if os.path.isfile(p):
            os.remove(p)
        elif os.path.isdir(p):
            shutil.rmtree(p)

    open(os.path.join(DOCS, ".nojekyll"), "w").close()

    build_index()
    build_summary()
    build_examples_index()
    build_example_pages()
    build_vocabulary()

    deploy_personal_site()

    count = sum(len(files) for _, _, files in os.walk(DOCS))
    print(f"Built site in {DOCS} ({count} files)")
    print(f"Live URL: https://dunghuynhandy.github.io/ielts/")


if __name__ == "__main__":
    main()
