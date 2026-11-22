# no artifacts

Source for [noartifacts.com](https://noartifacts.com), a one-page site in the spirit of [nohello.net](https://nohello.net).

The point: don't forward the thing your AI made. Send what you think.

## Languages

English at `/`, plus Español, Português, Français, Deutsch, Italiano, Русский, 日本語, 中文, 한국어, हिन्दी, العربية and עברית at `/<code>/`.
The root page sends visitors to their browser's language. Picking a language from the list on the page overrides that.

## Editing

All copy lives in `strings.py`, one block per language. The pages are generated from it:

```bash
python3 build.py
```

This writes `index.html` and `<code>/index.html`. Commit the generated files: the site has no build step on deploy.

## Deploying

Static files on Cloudflare Pages (project `noartifacts`), deployed from the repo root:

```bash
npx wrangler pages deploy . --project-name noartifacts --branch main
```

`www.noartifacts.com` redirects to the apex with a Cloudflare redirect rule.

## Files

- `index.html`, `<code>/index.html`: generated pages
- `strings.py`, `build.py`: copy and generator
- `404.html`: not-found page
- `og.png`: 1200×630 link preview image
- `img/`: chat avatars (generated portraits of people who don't exist)

## Translations

Fixes from native speakers are welcome. Edit `strings.py`, run `python3 build.py`, and open a pull request.
