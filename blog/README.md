# Build the website

The Hugo/PaperMod site contains the blog and recipe collection. The line-dance
application is served separately by the existing Nginx proxy.

Requirements: Python 3.10+, Make, and Hugo 0.153.0 (matching the Docker image).
With uv installed, install the pinned Hugo executable using
`uv tool install --python 3.12 hugo==0.153.0`.
Initialize the pinned theme with
`git submodule update --init blog/hugo/themes/papermod` from the repository root.

From `blog/`, run:

```sh
make build
```

This reads the tracked `recipes/` directory by default, imports every `.md`
file, then compiles the entire site into `hugo/public/`. All recipe sources
are included in this repository; no external recipe directory is required.
To use another source directory for a local build:

```sh
make build RECIPES_DIR=/path/to/recipes/output
```

Override `HUGO=/path/to/hugo` or `PYTHON=/path/to/python3` if needed.
Run importer checks with `make test`. Preview the built site with
`python3 -m http.server 8000 --directory hugo/public`, then open
`http://localhost:8000/recipes/`.

## Add a recipe

1. Add a UTF-8 Markdown file to `blog/recipes/`, starting with
   `# Recipe title`, followed by the recipe body. No front matter is needed.
2. Run `make build`.

Commit the recipe file along with any website changes to preserve it in Git.

The first heading becomes the page title. The filename determines its URL:
`Chocolate-Mousse.md` becomes `/recipes/chocolate-mousse/`, and
`les_meilleures_crêpes.md` becomes `/recipes/les-meilleures-crepes/`.
Accents are stripped, punctuation/spaces/underscores become hyphens, and names
are lowercased. Renaming a file changes its URL; changing its heading does not.
Duplicate resulting URLs fail the build rather than overwriting recipes.
Different source files with the same title remain separate entries.

The importer never modifies source recipes. It owns `hugo/.generated/recipes/`,
which Hugo mounts as `content/recipes/`. Both generated content and `public/`
are ignored by Git. Successful builds replace the previous output so deleted
or renamed recipes leave no stale pages. An import or Hugo failure preserves
the previous `public/` directory.

The recipe index lists all recipes alphabetically without pagination. Individual
recipes reuse PaperMod with metadata hidden and breadcrumbs back to Recipes.

## Docker build

From the repository root:

```sh
docker compose build nginx
```

The tracked recipes are copied from the regular `blog/` build context.
For a direct Docker build:

```sh
docker build -t loic-website blog
```

The image runs the same importer/build script and includes the generated HTML.
Nginx serves `/recipes/` from its existing static root; no new route is needed.
Rebuild the image after adding recipes. Deploying/restarting production remains
a separate step.
