"""Check the real Jekyll output using only Python's standard library."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import re
import sys


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.paper_links = []
        self.paper_count = 0
        self.paper_groups = {}
        self.current_group = None
        self.h1_count = 0
        self.missing_alt = False
        self.in_paper = False
        self.in_paper_title = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'section' and 'research-group' in attrs.get('class', '').split():
            self.current_group = attrs.get('aria-labelledby')
            self.paper_groups[self.current_group] = 0
        if tag == 'li' and 'paper-entry' in attrs.get('class', '').split():
            self.in_paper = True
            self.paper_count += 1
            if self.current_group:
                self.paper_groups[self.current_group] += 1
        if tag == 'h3' and self.in_paper:
            self.in_paper_title = True
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
            if self.in_paper_title:
                self.paper_links.append(attrs['href'])
        if tag in ('img', 'script') and attrs.get('src'):
            self.links.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') in ('stylesheet', 'icon'):
            self.links.append(attrs['href'])
        if tag == 'img' and 'alt' not in attrs:
            self.missing_alt = True

    def handle_endtag(self, tag):
        if tag == 'h3':
            self.in_paper_title = False
        if tag == 'li':
            self.in_paper = False
        if tag == 'section':
            self.current_group = None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', default='_site')
    parser.add_argument('--baseurl', default='')
    args = parser.parse_args()
    root = Path(args.site).resolve()
    if not (root / 'index.html').is_file():
        parser.error('Build the site first; _site/index.html was not found.')
    errors = []
    pages = {}
    texts = {}
    for path in root.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        pages[path] = Page(text)
        texts[path] = text
        if re.search(r'{[{%]', text):
            errors.append(f'{path.relative_to(root)}: unrendered Liquid')
        if 'Paper Title Number' in text:
            errors.append(f'{path.relative_to(root)}: template paper leaked into site')
        duplicates = [item for item, count in Counter(pages[path].ids).items() if count > 1]
        if duplicates:
            errors.append(f'{path.relative_to(root)}: duplicate IDs {duplicates}')
        if pages[path].missing_alt:
            errors.append(f'{path.relative_to(root)}: image missing alt attribute')

    checked_links = 0
    for path, page in pages.items():
        for href in page.links:
            parsed = urlsplit(href)
            if parsed.scheme in ('mailto', 'tel', 'data'):
                continue
            if parsed.netloc and parsed.netloc != 'gacamposgs.github.io':
                continue
            if parsed.scheme and parsed.scheme not in ('http', 'https'):
                continue
            target_name = unquote(parsed.path)
            if args.baseurl and target_name.startswith(args.baseurl + '/'):
                target_name = target_name[len(args.baseurl):]
            if target_name.startswith('/'):
                target = root / target_name.lstrip('/')
            elif target_name:
                target = path.parent / target_name
            else:
                target = path
            target = target.resolve()
            if target.is_dir():
                target = target / 'index.html'
            if not target.is_file():
                errors.append(f'{path.relative_to(root)}: missing local target {href}')
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(root)}: missing anchor {href}')
            checked_links += 1

    for route in ('index.html', 'publications/index.html', 'teaching/index.html', 'cv/index.html'):
        page = pages.get(root / route)
        if page is None or page.h1_count != 1:
            errors.append(f'{route}: expected one main heading')

    home = pages[root / 'index.html']
    research = pages.get(root / 'publications/index.html')
    detail_pages = set(root.glob('research/*/index.html'))
    if not research or not set(home.paper_links).issubset(research.paper_links):
        errors.append('Homepage paper links must also appear on Research')
    if not research or research.paper_count != len(detail_pages) or not detail_pages:
        errors.append('Every published research item must appear once on Research')
    if 'research-policy' in home.paper_groups:
        errors.append('Policy research must stay off the homepage')
    if 'research-work-in-progress' not in home.paper_groups:
        errors.append('Homepage must keep the Work in progress section visible')
    if research:
        academic_groups = ('research-working-paper', 'research-work-in-progress', 'research-paper')
        for group in academic_groups:
            if home.paper_groups.get(group, 0) != research.paper_groups.get(group, 0):
                errors.append(f'Home and Research disagree on {group}')
        if any(urlsplit(href).path.startswith('/research/') for href in home.paper_links + research.paper_links):
            errors.append('Paper titles must link directly to their source, not a local detail page')
    for excluded in ('_archive', 'content/templates', 'content/settings', 'content/README.md', 'EDITING.md', 'README.md', 'tips_academic_website.pdf', 'files/Provisional_Transcript_Gabriel.pdf', 'scripts', 'local'):
        if (root / excluded).exists():
            errors.append(f'Private/editing-only path published: {excluded}')

    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'PASS: {len(pages)} HTML pages, {checked_links} local links, and {len(detail_pages)} papers checked.')
    print('Homepage filtering, Research entries, internal links, anchors, image alt text, and exclusions pass.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
