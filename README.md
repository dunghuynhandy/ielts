# IELTS Speaking — Personal Study Site

IELTS Speaking materials: lessons, practice questions, and vocabulary.

**Live site:** [https://dunghuynhandy.github.io/ielts/](https://dunghuynhandy.github.io/ielts/)

## Contents

| Folder | Description |
|--------|-------------|
| `SPEAKING /` | Source markdown (lessons, examples, vocabulary) |
| `docs/` | Generated static website (GitHub Pages) |

## Build the website

```bash
pip3 install markdown
python3 build_site.py
```

This regenerates all HTML in `docs/` from the markdown files.

## Enable GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**
4. Choose branch **master** and folder **/docs**
5. Save — your site will be live at `https://dunghuynhandy.github.io/ielts/` within a few minutes

## Sources

- IELTS Fighter — 10 speaking lessons (Part 1, 2, 3)
- IELTS Simon — Ideas for IELTS Topics
- NgocBach — Predicted questions Q1/Q2/Q3 2022–2024
