# Edit your website here

| What you want to change | File or folder |
| --- | --- |
| Your homepage biography | `pages/home.md` |
| Research page settings or optional introduction | `pages/research.md` |
| Teaching information | `pages/teaching.md` |
| CV page and education | `pages/cv.md` |
| Add or update a paper or report | `_papers/` — one Markdown file per item |
| Name, photo, affiliation, interests, email, GitHub, X, LinkedIn, PDF CV path | `settings/profile.yml` |
| Menu items and their order | `settings/navigation.yml` |
| Starting point for a new page or paper | `templates/` |

Working papers, work in progress, and published papers appear automatically on
**Home** and **Research**. Policy research appears only on **Research**. The
homepage keeps the Work in progress heading visible even when it is empty.
Paper titles link directly to `paper_url`; do not duplicate the research lists.

See `../EDITING.md` for examples and local preview instructions.

The other files in `settings/` are retained template data. For normal edits,
you only need `profile.yml` and `navigation.yml`.
