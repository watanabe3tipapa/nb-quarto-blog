# nb-quarto-blog

**A Quarto blog woven by nb.**

nb-quarto-blog is a personal blog that publishes an [nb](https://xwmx.github.io/nb/) notebook as a GitHub repository. Notes are created and edited with nb, committed automatically, and after a push GitHub Actions renders them with [Quarto](https://quarto.org/) and publishes the result to GitHub Pages.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.2.0-blue.svg)](https://github.com/watanabe3tipapa/nb-quarto-blog/releases)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-blue.svg)](https://watanabe3tipapa.github.io/nb-quarto-blog/)
[![GitHub](https://img.shields.io/github/issues/watanabe3tipapa/nb-quarto-blog.svg)](https://github.com/watanabe3tipapa/nb-quarto-blog/issues)

[Japanese](README.md) | [English](README_EN.md)

## Concept

### Why "nb × Quarto"

Running a blog tends to become dual management: writing the content, and publishing it. You write in an editor, build in another screen, and deploy somewhere else — this overhead raises the barrier to posting.

nb-quarto-blog consolidates this flow. **Writing a note equals publishing a post.**

| Activity | nb-quarto-blog counterpart |
|---|---|
| Write a note (post) | `nb add` opens your editor and writes in Markdown |
| Organize posts | CI detects the category and moves posts to `posts/<category>/`, converting to `.qmd` |
| Normalize dates | CI auto-inserts `date:` (Asia/Tokyo) in the front matter |
| Build the site | GitHub Actions runs `quarto render` |
| Publish | Artifacts are auto-deployed to GitHub Pages |

### Automation That Never Loops

This blog is strict about **commits not re-triggering CI**. Commits for organizing, converting, and date insertion are pushed with `[skip ci]`, so automated processing never spawns a new push and loops.

- **nb-first workflow** — the notebook is the repository (git sync)
- **Auto-organizing** — root `.md` files are categorized and moved to `posts/`, converted to `.qmd`
- **CI auto-publish** — a push to `main` completes build and deploy

## Features

- **Note management with nb**: manage notes in one place with `nb add` / `nb edit` / `nb show`
- **Quarto-powered site**: `cosmo` theme, search, TOC, and code copy
- **Automatic category detection**: content keywords route posts into `posts/<category>/`
- **`.md` / `.qmd` support**: conversion scripts generate `.qmd` with front matter
- **Automatic date insertion**: `date:` (JST) is added to front matter when missing
- **`[skip ci]` for safety**: automated commits never cause infinite loops
- **CI auto-publish**: GitHub Actions runs `quarto render` and serves GitHub Pages

## Setup

### Prerequisites

| Tool | Required | Check command |
|---|---|---|
| [Quarto](https://quarto.org/) | Yes (build) | `quarto --version` |
| [nb](https://xwmx.github.io/nb/) | Recommended (posting) | `nb --version` |
| R | Optional (only for `{r}` chunks) | `R --version` |
| Git / GitHub | Yes (publish / sync) | `git --version` |

On macOS install Quarto with `brew install --cask quarto` and nb with `brew install xwmx/taps/nb`.

### 1. Add the notebook

```bash
nb notebooks add https://github.com/watanabe3tipapa/nb-quarto-blog.git
```

### 2. Preview

```bash
quarto preview
```

http://localhost:XXXX opens (the port varies by environment).

### 3. Render

```bash
quarto render
```

Output goes to `docs/`.

### 4. Publish

Pushing to `main` triggers an automatic build and deploy via GitHub Actions.

## Writing and Publishing Flow

```bash
# Add a note (opens your editor)
nb add

# Add with a title and body
nb add "Post body" --title "Post title"

# List / show / edit notes
nb ls
nb show <id>
nb edit <id>

# Sync to GitHub (publish trigger)
nb git push
```

- Root `.md` files are organized and converted into `posts/` by CI.
- Automated commits for conversion and date insertion use `[skip ci]`, avoiding infinite loops.
- You can also place `.qmd` files directly under `posts/<category>/<dir>/index.qmd` and push.

## Directory Layout

| Path | Description |
|---|---|
| [index.qmd](index.qmd) | Homepage (post listing) |
| [about.qmd](about.qmd) | Profile page |
| [_quarto.yml](_quarto.yml) | Site-wide configuration |
| [_metadata.yml](_metadata.yml) | Shared metadata (OG / Twitter cards) |
| [posts/](posts/) | Category-based posts (`.qmd`) |
| [posts/_metadata.yml](posts/_metadata.yml) | Common post settings (e.g. `freeze`) |
| [styles.css](styles.css) | Additional styles |
| [.github/workflows/publish.yml](.github/workflows/publish.yml) | Build & deploy CI |
| [.github/scripts/](.github/scripts/) | Organize / convert / date-insertion scripts |

## How the Automation Works

Pushing `.md` / `.qmd` files to `main` makes CI automatically:

1. Detect the category of root `.md` files and move them to `posts/<category>/<dir>/index.md`
2. Convert `.md` to `.qmd` (committed with `[skip ci]`)
3. Insert `date:` into front matter when missing (committed with `[skip ci]`)
4. Run `quarto render`
5. Deploy to GitHub Pages

## Contributing

Contributions are welcome. If you find a typo or an inaccurate description, please open an [issue](https://github.com/watanabe3tipapa/nb-quarto-blog/issues) to share it first.

1. Fork the repository
2. Create a feature branch (`git checkout -b fix/typo-in-post`)
3. Commit your changes (`git commit -m 'Fix typo in post'`)
4. Push to the branch (`git push origin fix/typo-in-post`)
5. Open a Pull Request

## Contact

GitHub: [https://github.com/watanabe3tipapa/nb-quarto-blog](https://github.com/watanabe3tipapa/nb-quarto-blog)

Published site: [https://watanabe3tipapa.github.io/nb-quarto-blog/](https://watanabe3tipapa.github.io/nb-quarto-blog/)

## License

Distributed under the MIT License — see the [LICENSE](LICENSE) file for details.