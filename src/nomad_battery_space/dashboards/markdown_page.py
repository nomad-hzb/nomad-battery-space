"""Shared helper: a FastAPI app that shows a remote markdown file in NOMAD style."""

import re
import time
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from markdown_it import MarkdownIt

STATIC_DIR = Path(__file__).parent / 'static'
HEDGEDOC_HOSTS = ('notes.desy.de',)

_PAGE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <base target="_blank">
  <link rel="stylesheet" href="{base}/static/style.css">
  <script src="{base}/static/nomad-theme.js"></script>
</head>
<body>
  <main class="markdown">
{content}
  </main>
  <footer>Source: <a href="{source}" rel="noopener">{source}</a></footer>
</body>
</html>
"""

_FRONT_MATTER = re.compile(r'\A---\s*\n.*?\n---\s*\n', re.DOTALL)


def raw_url(source_url: str) -> str:
    """Derive the URL that returns the raw markdown for a human-facing URL."""
    url = urlparse(source_url)
    if url.netloc == 'github.com' and '/blob/' in url.path:
        # github.com/<org>/<repo>/blob/<ref>/<path> -> raw.githubusercontent.com/...
        return f'https://raw.githubusercontent.com{url.path.replace("/blob/", "/", 1)}'
    if url.netloc in HEDGEDOC_HOSTS:
        return source_url.rstrip('/') + '/download'
    return source_url


def _create_renderer() -> MarkdownIt:
    md = MarkdownIt('commonmark').enable(['table', 'strikethrough'])

    # Never emit raw HTML from the markdown: the dashboard runs same-origin
    # with NOMAD, so scripts in the source could act on the user's session.
    def drop(self, tokens, idx, options, env):
        return ''

    md.add_render_rule('html_block', drop)
    md.add_render_rule('html_inline', drop)

    # Make images clickable to open them in full size.
    def image(self, tokens, idx, options, env):
        src = escape(tokens[idx].attrGet('src') or '')
        return f'<a href="{src}" rel="noopener">{self.image(tokens, idx, options, env)}</a>'

    md.add_render_rule('image', image)
    return md


def create_markdown_app(source_url: str, cache_seconds: int = 600) -> FastAPI:
    """Return a FastAPI app rendering the markdown behind `source_url`."""
    fetch_url = raw_url(source_url)
    md = _create_renderer()
    cache: dict = {'html': None, 'fetched_at': 0.0}

    async def render() -> str:
        """Fetch and render, cached; serve the stale copy if the source fails."""
        now = time.time()
        if cache['html'] is not None and now - cache['fetched_at'] < cache_seconds:
            return cache['html']
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                response = await client.get(fetch_url)
                response.raise_for_status()
            cache['html'] = md.render(_FRONT_MATTER.sub('', response.text))
            cache['fetched_at'] = now
        except httpx.HTTPError as e:
            if cache['html'] is None:
                return f'<p class="error">Could not load {escape(fetch_url)}: {escape(str(e))}</p>'
        return cache['html']

    app = FastAPI()
    app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')

    @app.get('/', response_class=HTMLResponse)
    async def index(request: Request):
        # root_path is where NOMAD mounted this app, e.g. .../dashboards/<id>
        base = request.scope.get('root_path', '').rstrip('/')
        return _PAGE.format(base=base, content=await render(), source=escape(source_url))

    return app
