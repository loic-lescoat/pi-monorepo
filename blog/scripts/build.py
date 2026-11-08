"""Import recipes and publish a fresh local Hugo build only after success."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from import_recipes import import_recipes


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recipes', type=Path, default=root / 'recipes')
    parser.add_argument('--hugo', default=os.environ.get('HUGO', 'hugo'))
    args = parser.parse_args()
    site = root / 'hugo'
    try:
        count = import_recipes(args.recipes, site / '.generated/recipes')
        print(f'Imported {count} recipes', flush=True)
        with tempfile.TemporaryDirectory(dir=site) as temporary:
            output = Path(temporary) / 'public'
            subprocess.run([args.hugo, '--source', str(site), '--destination', str(output),
                            '--minify', '--panicOnWarning'], check=True)
            public = site / 'public'
            if public.exists():
                shutil.rmtree(public)
            output.rename(public)
        print(f'Built {public}')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Build failed: {error}\n')


if __name__ == '__main__':
    main()
