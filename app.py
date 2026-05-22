import os
from flask import Flask, render_template, abort, send_from_directory, url_for
import markdown
from datetime import datetime

APP_ROOT = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(APP_ROOT, "content")
BLOG_DIR = os.path.join(CONTENT_DIR, "blogs")
DATA_DIR = os.path.join(APP_ROOT, "data")

app = Flask(__name__)


def load_projects():
    import json
    path = os.path.join(DATA_DIR, "projects.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_posts():
    posts = []
    if not os.path.exists(BLOG_DIR):
        return posts
    for fn in sorted(os.listdir(BLOG_DIR), reverse=True):
        if not fn.endswith('.md'):
            continue
        file_path = os.path.join(BLOG_DIR, fn)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # title from first heading
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        title = lines[0].lstrip('# ').strip() if lines and lines[0].startswith('#') else fn.replace('.md', '')
        # excerpt: first paragraph after title
        excerpt = ''
        for line in lines[1:]:
            if line:
                excerpt = line
                break
        # date from filename if prefixed YYYY-MM-DD
        date = None
        try:
            date_part = fn.split('-')[:3]
            date = datetime.strptime('-'.join(date_part), '%Y-%m-%d').date()
        except Exception:
            date = None
        posts.append({
            'slug': fn.replace('.md', ''),
            'title': title,
            'excerpt': excerpt,
            'date': date,
        })
    return posts


def render_markdown_file(slug):
    path = os.path.join(BLOG_DIR, slug + '.md')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    html = markdown.markdown(text, extensions=['fenced_code', 'codehilite', 'toc'])
    # title detection
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0].lstrip('# ').strip() if lines and lines[0].startswith('#') else slug
    return {'title': title, 'content': html}


@app.route('/')
def index():
    projects = load_projects()[:6]
    posts = list_posts()[:3]
    return render_template('index.html', projects=projects, posts=posts)


@app.route('/projects/')
def projects():
    projects = load_projects()
    return render_template('projects.html', projects=projects)


@app.route('/blog/')
def blog_index():
    posts = list_posts()
    return render_template('blogs.html', posts=posts)


@app.route('/blog/<slug>')
def blog_post(slug):
    post = render_markdown_file(slug)
    if not post:
        abort(404)
    return render_template('blog_post.html', post=post)


@app.route('/resume/')
def resume():
    return render_template('resume.html')


if __name__ == '__main__':
    app.run(debug=True)
