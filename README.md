# Gabriel de Campos — personal website

A responsive academic website built with Jekyll for GitHub Pages.

**Start editing in `content/`.** Read [EDITING.md](EDITING.md) for a full guide.

| Folder | Purpose |
| --- | --- |
| `content/pages/` | Markdown for Home, Research, Teaching, CV, and other pages |
| `content/_papers/` | One Markdown file per working paper, paper, or policy report |
| `content/settings/` | Profile information and navigation |
| `content/templates/` | Copyable examples for new pages and papers |
| `files/` | CV and paper PDFs |
| `images/` | Portraits and images |
| `assets/css/personal.css` | Website appearance |
| `_layouts/` and `_includes/personal/` | Jekyll presentation templates |
| `_archive/previous-content/` | Previous sources and unused template examples |
| `local/` | Ignored portable runtime and dependencies |

Academic paper files populate Home and Research; policy reports appear only
on Research. Home always includes a Work in progress section. The personal
layout supports desktop and phone screens, with GitHub, email, X, and
LinkedIn icons below the portrait.

Preview from PowerShell:

```powershell
.\scripts\preview.ps1 -Build
.\scripts\preview.ps1
```

Validate generated pages and internal links:

```powershell
python scripts/verify_site.py
```

These commands only build or preview locally. Publishing requires a separate
Git commit and push.

The repository originated from [Academic Pages](https://academicpages.github.io/),
based on Minimal Mistakes. Original template documentation is preserved in
`_archive/previous-content/ACADEMIC_PAGES_README.md`; see `LICENSE` for attribution.
