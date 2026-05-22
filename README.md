# Minimal Flask Static Portfolio

This project is a simple, lightweight personal portfolio built with Flask and Frozen-Flask (static export). It uses Tailwind (CDN) for styling and Markdown files for blog posts.

Quick start

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run locally:

```powershell
flask run
```

4. Open the site in your browser:

```text
http://127.0.0.1:5000
```

5. Generate static site into `build/`:

```powershell
python freeze.py
```

Deployment

- **GitHub Pages**: push this repo to GitHub, then enable Pages from the `gh-pages` branch. The included workflow automatically builds `build/` and deploys it on every push to `main`.
- **Vercel**: connect the GitHub repo and use the static `build/` directory as your published output, or deploy directly from the repository and let the site run as a static app.

GitHub Actions

A workflow file is included at `.github/workflows/deploy.yml`. It installs Python, builds the static site with `python freeze.py`, and publishes the generated `build/` folder to the `gh-pages` branch.

Notes

- To add a blog post: create a Markdown file in `content/blogs/` named like `YYYY-MM-DD-your-slug.md` and include a top-level `# Title` heading. The site will pick it up on the next build.
- Edit `data/projects.json` to update the projects grid.
