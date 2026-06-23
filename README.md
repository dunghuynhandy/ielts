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

**One-time setup** (required — without this you get a 404):

1. Push this repo to GitHub
2. Open **Settings → Pages** on the repo:
   https://github.com/dunghuynhandy/ielts/settings/pages
3. Under **Build and deployment → Source**, select **GitHub Actions** (not "Deploy from branch")
4. Push any commit — the workflow in `.github/workflows/deploy-pages.yml` will deploy automatically
5. Wait 1–2 minutes, then open: **https://dunghuynhandy.github.io/ielts/**

> **Alternative:** You can also choose **Deploy from a branch** → branch `master` → folder `/docs` instead of GitHub Actions.

## Sources

- IELTS Fighter — 10 speaking lessons (Part 1, 2, 3)
- IELTS Simon — Ideas for IELTS Topics
- NgocBach — Predicted questions Q1/Q2/Q3 2022–2024
