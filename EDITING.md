# How to edit this website

Start in **`content/`**. Everything you normally write or update is collected there.

## Change a page

- `content/pages/home.md`: homepage biography.
- `content/pages/research.md`: Research page settings and optional introduction.
- `content/pages/teaching.md`: teaching experience.
- `content/pages/cv.md`: education and the CV download page.

The lines between the two `---` markers are the page settings. Text below those
markers is ordinary Markdown: `## Heading`, `**bold**`, and `[label](url)` all work.
Keep each existing `permalink` to preserve public URLs.

## Add a working paper, publication, or policy report

1. Copy `content/templates/paper.md` into `content/_papers/`.
2. Rename it, for example `2026-my-new-paper.md`.
3. Replace the sample settings and delete the template instructions from the body.
4. Write the abstract or details below the second `---` marker.

Example:

```yaml
---
title: "Title of my paper"
category: working-paper
year: 2026
coauthors: "First Coauthor and Second Coauthor"
paper_url: /files/my-paper.pdf
summary: "A short, optional description."
---
```

Working papers, work in progress, and published papers appear automatically on
**Home** and **Research**. Policy reports appear only on **Research**. Each title links
directly to `paper_url`, which can be the publisher's page, report page, or PDF.
No HTML edits are needed. Existing `/research/…/` pages remain available for old
links, but research lists no longer send visitors through them.

Choose one category:

| Category | Section on the website |
| --- | --- |
| `working-paper` | Working papers |
| `paper` | Published papers |
| `policy` | Policy research |
| `work-in-progress` | Work in progress |

Items are sorted by year, newest first, within each section. Empty sections are
hidden, except **Work in progress** on the homepage, which stays visible without
placeholder text. Published papers will appear when you add your first item
with `category: paper`. Include `year` as a number and set `paper_url` to its destination.
An item without `paper_url` has a plain title, useful for work in progress.
Optional fields can be removed entirely: `coauthors`, `venue`, `summary`,
`title_note`, `paper_label`, and `coverage`. A `title_note` such as `Master's Thesis`
appears as a plain bracketed label after the title. The title is the only paper
link in research lists; links below entries are reserved for media coverage.
`paper_label` only controls the source link on legacy detail pages.

For press coverage, add:

```yaml
coverage:
  - label: Nexo
    url: https://example.com/article
```

Use `published: false` in a paper's settings to keep a draft off the public site.
Use a unique filename for every paper. Keep filenames after publication so
existing links continue to work. Put PDFs in `files/` and reference them as
`/files/filename.pdf`. External PDF/report URLs also work.

## Change your photo or contact links

Edit **`content/settings/profile.yml`**. This controls your name, affiliation,
location, research interests, portrait, email, GitHub, X/Twitter, LinkedIn, and
CV PDF. Use full profile URLs for `github`, `x`, and `linkedin`. Leave a social
field empty to hide its icon. The icon buttons sit in one row below your photo.

Put a new image in `images/` and update `photo`. Put a new CV in `files/` and
update `cv`. Your biography still lives in `content/pages/home.md`.

## Add a new page

1. Copy `content/templates/page.md` into `content/pages/`.
2. Choose a filename, page title, and unique `permalink`, for example `/projects/`.
3. Delete the template instructions and write the page in Markdown.
4. To add it to the menu, edit `content/settings/navigation.yml`:

```yaml
  - title: Projects
    url: /projects/
```

New pages automatically use the personal site design.

## Preview locally on Windows

From PowerShell in this repository:

```powershell
.\scripts\preview.ps1 -Build
.\scripts\preview.ps1
```

The second command runs a local preview at `http://127.0.0.1:4000`. Press Ctrl+C
to stop it. These commands do not commit, push, or publish anything.

The script uses the portable Ruby runtime in `local/runtime/` if present, or
Ruby on your PATH. This checkout has a portable runtime for local testing.
After a fresh clone, install Ruby with Devkit and Bundler, then run:

```powershell
bundle config set --local path local/gems
bundle install
```

`local/`, `.bundle/`, `Gemfile.lock`, and `_site/` are ignored by Git. `_site/`
contains generated output; always edit `content/`, not `_site/`.

To check internal links and generated pages after building:

```powershell
python scripts/verify_site.py
```

## Files for design changes

Normal content edits need no changes here:

- `assets/css/personal.css`: spacing, fonts, colors, and phone layout.
- `_layouts/home.html`: homepage arrangement.
- `_layouts/personal.html`: common document shell.
- `_includes/personal/`: shared header, portrait, and research rendering.
- `_config.yml`: Jekyll build settings, domain, and search metadata.

The portrait and biography sit side by side on desktop and stack below 700px.
The phone portrait is approximately 260–340px tall. Contact and social icons
appear beneath the photo. Colors follow the visitor's light/dark preference.

## Previous template content

`_archive/previous-content/` preserves all previous page and collection sources,
including unused Academic Pages examples and the original template README.
It is excluded from the published site, preventing example papers and duplicate
Research URLs from appearing. Existing Home, Research, Teaching, CV, About,
Resume, and Sitemap URLs remain available.
