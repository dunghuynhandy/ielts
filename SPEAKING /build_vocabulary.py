#!/usr/bin/env python3
"""Extract vocabulary from all SPEAKING lessons and sources into vocabulary/*.md"""

import os
import re
import glob
import fitz
from collections import defaultdict

BASE = "/Users/ngocdunghuynh/githubs/ielts/SPEAKING "
VOCAB_DIR = os.path.join(BASE, "vocabulary")

LESSONS = [
    ("fighter-lesson-01-wh-questions", "[Fighter 5] LS_Speaking - Lesson 1. Review technique Wh-questions.pdf"),
    ("fighter-lesson-02-review-techniques", "[Fighter 5] LS- Speaking - Lesson 2. Review techniques.pdf"),
    ("fighter-lesson-03-part2-people", "[Fighter 5] LS - Speaking - Lesson 3. Part 2 - Review people monologue.pdf"),
    ("fighter-lesson-04-places", "[Fighter 5] LS- Speaking - Lesson 4. Review places.pdf"),
    ("fighter-lesson-05-part2-things", "[Fighter 5] LS - Speaking - Lesson 5. Part 2 - Review things.pdf"),
    ("fighter-lesson-06-past-events", "[Fighter 5] LS- Speaking - Lesson 6. Review past events and activities.pdf"),
    ("fighter-lesson-07-events-activities", "[Fighter 5] LS - Speaking - Lesson 7. Part 2 - Review events and activities (2).pdf"),
    ("fighter-lesson-08-part3-1", "[Fighter 5] LS- Speaking - Lesson 8. Speaking part 3 (1).pdf"),
    ("fighter-lesson-09-part3-2", "[Fighter 5] LS- Speaking - Lesson 9. Speaking Part 3 (2).pdf"),
    ("fighter-lesson-10-review-part2-3", "[Fighter 5] LS- Speaking - Lesson 10. Review speaking part 2 + 3.pdf"),
]

SOURCES = [
    ("simon-ideas-for-ielts-topics", "extra material /BAND 6.5 TO 9.0 IDEAS FOR IELTS TOPIC - IELTS SIMON (1).pdf"),
]


def extract_text(path: str) -> str:
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)


def parse_vocab_from_fighter(text: str) -> dict:
    """Parse vocabulary and collocation sections from Fighter lesson PDFs."""
    result = {"vocabulary": [], "collocations": [], "phrases": []}

    # Split by section headers
    sections = re.split(
        r"(Topic-based vocabulary|Collocation|USEFUL EXPRESSIONS|Technique|Strategy|Exam focus|LESSON SUMMARY)",
        text,
        flags=re.I,
    )

    current = None
    for part in sections:
        p = part.strip()
        if re.match(r"Topic-based vocabulary", p, re.I):
            current = "vocabulary"
            continue
        if re.match(r"Collocation", p, re.I):
            current = "collocations"
            continue
        if re.match(r"USEFUL EXPRESSIONS", p, re.I):
            current = "phrases"
            continue
        if current in ("vocabulary", "collocations") and len(p) > 20:
            entries = parse_table_entries(p, current)
            result[current].extend(entries)
        elif current == "phrases":
            for line in p.split("\n"):
                line = line.strip()
                if line.startswith("•") or line.startswith("-"):
                    phrase = re.sub(r"^[•\-]\s*", "", line).strip()
                    if len(phrase) > 10:
                        result["phrases"].append({"english": phrase, "vietnamese": "", "cefr": "", "phonetics": ""})

    # Fallback: parse inline vocab patterns from garbled PyMuPDF output
    if not result["vocabulary"] and not result["collocations"]:
        result = parse_inline_vocab(text)

    return result


def parse_table_entries(block: str, kind: str) -> list[dict]:
    entries = []
    lines = [l.strip() for l in block.split("\n") if l.strip()]

    # Structured table (Lesson 8 style)
    i = 0
    while i < len(lines):
        line = lines[i]
        # Skip headers
        if line in ("English", "CEFR level", "Phonetics", "Vietnamese", "NA") or re.match(r"^IELTS", line):
            i += 1
            continue

        # Pattern: word (n/adj/v) on one line, then CEFR, phonetics, vietnamese
        word_m = re.match(r"^([A-Za-z][A-Za-z \-']+?)\s*\((n|v|adj|adv)\)\s*$", line, re.I)
        if word_m:
            word = word_m.group(1).strip()
            pos = word_m.group(2).lower()
            cefr = phonetics = vietnamese = ""
            j = i + 1
            while j < len(lines) and j < i + 6:
                l2 = lines[j]
                if re.match(r"^(NA|A\d|B\d|C\d|C2)$", l2):
                    cefr = l2
                elif l2.startswith("/") and l2.endswith("/"):
                    phonetics = l2
                elif re.search(r"[\u00c0-\u1ef9]", l2) or (len(l2) > 3 and not re.match(r"^[A-Za-z]", l2[:3]) is False and cefr and phonetics):
                    if re.search(r"[\u00c0-\u1ef9a-z]", l2, re.I):
                        vietnamese = (vietnamese + " " + l2).strip() if vietnamese else l2
                elif re.match(r"^[A-Za-z][A-Za-z \-']+\s*\((n|v|adj|adv)\)", l2, re.I):
                    break
                j += 1
            entries.append({
                "english": f"{word} ({pos})",
                "cefr": cefr,
                "phonetics": phonetics,
                "vietnamese": vietnamese,
            })
            i = j
            continue

        # Collocation multi-line entry
        if kind == "collocations" and re.match(r"^[A-Za-z]", line) and not line.startswith("/"):
            english = line
            cefr = phonetics = vietnamese = ""
            j = i + 1
            while j < len(lines) and j < i + 8:
                l2 = lines[j]
                if re.match(r"^(NA|A\d|B\d|C\d|C2)$", l2):
                    cefr = l2
                elif "/" in l2:
                    phonetics = (phonetics + " " + l2).strip() if phonetics else l2
                elif re.search(r"[\u00c0-\u1ef9]", l2):
                    vietnamese = (vietnamese + " " + l2).strip() if vietnamese else l2
                elif re.match(r"^[A-Z][a-z]", l2) and j > i + 1 and (cefr or phonetics):
                    break
                j += 1
            if len(english) > 3:
                entries.append({
                    "english": english,
                    "cefr": cefr,
                    "phonetics": phonetics.strip(),
                    "vietnamese": vietnamese,
                })
            i = max(i + 1, j)
            continue

        i += 1

    return entries


def parse_inline_vocab(text: str) -> dict:
    """Parse compressed single-line vocab from image-heavy PDFs."""
    result = {"vocabulary": [], "collocations": [], "phrases": []}

    # Pattern: word (n)CEFR/phonetic/Vietnamese mashed together
    vocab_block = re.findall(
        r"([A-Za-z][A-Za-z \-']{1,30}?)\s*\((n|v|adj|adv)\)\s*(NA|A\d|B\d|C\d|C2)?\s*(/[^/\n]+/)?([^A-Z/\n]{3,40})",
        text,
    )
    for word, pos, cefr, phon, vi in vocab_block:
        result["vocabulary"].append({
            "english": f"{word.strip()} ({pos})",
            "cefr": cefr or "",
            "phonetics": phon or "",
            "vietnamese": vi.strip(),
        })

    # Collocations: EnglishCEFR/phonetic/Vietnamese pattern
    coll_blocks = re.findall(
        r"([A-Za-z][A-Za-z '\-]{2,50}?)(NA|A\d|B\d|C\d|C2)?(/[\wˈˌəɪʊɔæɛʌɑɜθðʃʒŋʧʤ\s\.,\-]+/)([A-Za-zÀ-ỹ][^\n]{5,60})",
        text,
    )
    for eng, cefr, phon, vi in coll_blocks:
        if len(eng) > 4:
            result["collocations"].append({
                "english": eng.strip(),
                "cefr": cefr or "",
                "phonetics": phon.strip(),
                "vietnamese": vi.strip(),
            })

    # Standalone collocations with leading /
    for m in re.finditer(r"(/[\wˈˌəɪʊɔæɛʌɑɜθðʃʒŋʧʤ\s\.,\-']+/)", text):
        phon = m.group(1)
        # get preceding English phrase (up to 60 chars before)
        start = max(0, m.start() - 80)
        before = text[start:m.start()]
        eng_m = re.search(r"([A-Za-z][A-Za-z '\-]{3,50})$", before)
        if eng_m:
            after = text[m.end():m.end() + 60]
            vi_m = re.search(r"^([A-Za-zÀ-ỹ][^\n/]{4,50})", after)
            result["collocations"].append({
                "english": eng_m.group(1).strip(),
                "cefr": "",
                "phonetics": phon,
                "vietnamese": vi_m.group(1).strip() if vi_m else "",
            })

    # Deduplicate
    for key in result:
        seen = set()
        deduped = []
        for e in result[key]:
            k = e["english"].lower()
            if k not in seen:
                seen.add(k)
                deduped.append(e)
        result[key] = deduped

    return result


def parse_simon_topics(text: str) -> list[dict]:
    """Extract topic idea phrases from Simon book as vocabulary/key phrases."""
    topics = []
    content = text
    topic_pattern = re.compile(r"\n(\d+)\. ([A-Za-z][^\n]+)\n\n\n\n", re.M)
    matches = list(topic_pattern.finditer(content))
    for idx, m in enumerate(matches):
        num = m.group(1)
        name = m.group(2).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        block = content[start:end]
        phrases = []
        for line in block.split("\n"):
            line = line.strip()
            if len(line) > 20 and line[0].isupper() and not line.startswith("Page"):
                phrases.append(line)
        topics.append({"topic": name, "phrases": phrases[:30]})
    return topics


def render_lesson_md(slug: str, title: str, source_file: str, data: dict) -> str:
    lines = [
        f"# {title}",
        "",
        f"> Source: `{source_file}`",
        f"> File: `{slug}.md`",
        "",
    ]

    vocab = data.get("vocabulary", [])
    if vocab:
        lines += ["## Vocabulary", ""]
        lines.append("| English | CEFR | Phonetics | Vietnamese |")
        lines.append("|---------|------|-----------|------------|")
        for e in vocab:
            lines.append(f"| {e['english']} | {e['cefr']} | {e['phonetics']} | {e['vietnamese']} |")
        lines.append("")

    coll = data.get("collocations", [])
    if coll:
        lines += ["## Collocations", ""]
        lines.append("| English | CEFR | Phonetics | Vietnamese |")
        lines.append("|---------|------|-----------|------------|")
        for e in coll:
            lines.append(f"| {e['english']} | {e['cefr']} | {e['phonetics']} | {e['vietnamese']} |")
        lines.append("")

    phrases = data.get("phrases", [])
    if phrases:
        lines += ["## Useful Expressions", ""]
        for e in phrases:
            eng = e["english"] if isinstance(e, dict) else e
            lines.append(f"- {eng}")
        lines.append("")

    if not vocab and not coll and not phrases:
        lines += ["_No vocabulary could be extracted from this file (may be image-based PDF)._", ""]

    return "\n".join(lines)


def render_simon_md(topics: list[dict]) -> str:
    lines = [
        "# IELTS Simon — Ideas for IELTS Topics",
        "",
        "> Source: `BAND 6.5 TO 9.0 IDEAS FOR IELTS TOPIC - IELTS SIMON (1).pdf`",
        "> File: `simon-ideas-for-ielts-topics.md`",
        "",
        "Key phrases and ideas organised by topic (useful for Part 3 discussion).",
        "",
    ]
    for t in topics:
        lines.append(f"## {t['topic']}")
        lines.append("")
        for p in t["phrases"]:
            lines.append(f"- {p}")
        lines.append("")
    return "\n".join(lines)


def render_master_index(files: list[tuple[str, dict]]) -> str:
    lines = [
        "# IELTS Speaking — Vocabulary Index",
        "",
        "All vocabulary extracted from IELTS Fighter lessons and source materials.",
        "",
        "## Files",
        "",
    ]
    for slug, data in files:
        v = len(data.get("vocabulary", []))
        c = len(data.get("collocations", []))
        p = len(data.get("phrases", []))
        lines.append(f"- [{slug}.md]({slug}.md) — {v} vocab, {c} collocations, {p} phrases")
    lines.append("")
    lines.append("## Quick Reference")
    lines.append("")
    lines.append("| # | Lesson | Focus |")
    lines.append("|---|--------|-------|")
    lesson_focus = {
        "fighter-lesson-01-wh-questions": "Part 1 — Wh-questions",
        "fighter-lesson-02-review-techniques": "Part 1 — Technology & Transport",
        "fighter-lesson-03-part2-people": "Part 2 — Describe a person",
        "fighter-lesson-04-places": "Part 2 — Describe a place",
        "fighter-lesson-05-part2-things": "Part 2 — Describe a thing",
        "fighter-lesson-06-past-events": "Part 2 — Past events",
        "fighter-lesson-07-events-activities": "Part 2 — Activities",
        "fighter-lesson-08-part3-1": "Part 3 — Discussion skills",
        "fighter-lesson-09-part3-2": "Part 3 — More practice",
        "fighter-lesson-10-review-part2-3": "Part 2 + 3 Review",
        "simon-ideas-for-ielts-topics": "Simon topic ideas (24 themes)",
    }
    for i, (slug, _) in enumerate(files, 1):
        focus = lesson_focus.get(slug, "")
        lines.append(f"| {i} | [{slug}.md]({slug}.md) | {focus} |")
    return "\n".join(lines)


def main():
    os.makedirs(VOCAB_DIR, exist_ok=True)
    lessons_dir = os.path.join(BASE, "sumary speaking lessons")
    all_files = []

    for slug, filename in LESSONS:
        path = os.path.join(lessons_dir, filename)
        if not os.path.exists(path):
            print(f"SKIP {slug} (not found)")
            continue
        text = extract_text(path)
        data = parse_vocab_from_fighter(text)
        title = filename.replace("[Fighter 5] ", "").replace(".pdf", "")
        md = render_lesson_md(slug, title, filename, data)
        out = os.path.join(VOCAB_DIR, f"{slug}.md")
        with open(out, "w") as f:
            f.write(md)
        all_files.append((slug, data))
        print(f"{slug}: {len(data['vocabulary'])} vocab, {len(data['collocations'])} coll, {len(data['phrases'])} phrases")

    for slug, relpath in SOURCES:
        path = os.path.join(BASE, relpath)
        if not os.path.exists(path):
            continue
        text = extract_text(path)
        topics = parse_simon_topics(text)
        md = render_simon_md(topics)
        out = os.path.join(VOCAB_DIR, f"{slug}.md")
        with open(out, "w") as f:
            f.write(md)
        all_files.append((slug, {"vocabulary": [], "collocations": [], "phrases": [p for t in topics for p in t["phrases"]]}))
        print(f"{slug}: {len(topics)} topics, {sum(len(t['phrases']) for t in topics)} phrases")

    # Master index
    index = render_master_index(all_files)
    with open(os.path.join(VOCAB_DIR, "README.md"), "w") as f:
        f.write(index)

    # Combined all-vocabulary file
    combined = ["# All Vocabulary — Combined", "", "> Merged from all lessons and sources.", ""]
    for slug, data in all_files:
        if slug == "simon-ideas-for-ielts-topics":
            continue
        combined.append(f"## {slug}")
        combined.append("")
        for e in data.get("vocabulary", []):
            combined.append(f"- **{e['english']}** {e['phonetics']} — {e['vietnamese']}")
        for e in data.get("collocations", []):
            combined.append(f"- *{e['english']}* {e['phonetics']} — {e['vietnamese']}")
        combined.append("")
    with open(os.path.join(VOCAB_DIR, "all-vocabulary.md"), "w") as f:
        f.write("\n".join(combined))

    print(f"\nDone — {len(all_files)} files in {VOCAB_DIR}")


if __name__ == "__main__":
    main()
