"""Convert plain recipe Markdown into disposable Hugo content."""

import argparse
import json
from pathlib import Path
import re
import shutil
import tempfile
import unicodedata


def slugify(stem):
    ascii_stem = unicodedata.normalize('NFKD', stem).encode('ascii', 'ignore').decode()
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_stem.lower()).strip('-')
    if not slug:
        raise ValueError(f'Filename has no usable URL characters: {stem!r}')
    return slug


def import_recipes(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if not source.is_dir():
        raise ValueError(f'Recipe directory does not exist: {source}')
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError('Source and generated destination must be separate directories')
    files = sorted(p for p in source.iterdir() if p.is_file() and p.suffix.lower() == '.md')
    if not files:
        raise ValueError(f'No Markdown recipes found in {source}')
    pages, owners = {}, {}
    for path in files:
        slug = slugify(path.stem)
        if slug in owners:
            raise ValueError(f'Duplicate recipe slug {slug!r}: {owners[slug]} and {path.name}')
        owners[slug] = path.name
        text = path.read_text(encoding='utf-8-sig')
        heading = re.match(r'\s*# +([^\n]+)\n?', text)
        if not heading:
            raise ValueError(f'{path.name}: expected a leading # Recipe title heading')
        title = re.sub(r'\s+#+\s*$', '', heading[1]).strip()
        body = text[heading.end():].lstrip('\n')
        metadata = {'title': title, 'slug': slug, 'draft': False}
        pages[f'{slug}.md'] = json.dumps(metadata, ensure_ascii=False) + '\n\n' + body
    pages['_index.md'] = '''---
title: Recipes
description: My recipe collection
cascade:
  params:
    hideMeta: true
    ShowReadingTime: false
    ShowPostNavLinks: false
    ShowBreadCrumbs: true
---
'''
    # Validate the entire input before replacing any previously generated content.
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
        staged = Path(temporary) / 'recipes'
        staged.mkdir()
        for name, content in pages.items():
            (staged / name).write_text(content, encoding='utf-8')
        if destination.exists():
            shutil.rmtree(destination)
        staged.rename(destination)
    return len(files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        print(f'Imported {import_recipes(args.source, args.destination)} recipes')
    except ValueError as error:
        parser.exit(1, f'{error}\n')
