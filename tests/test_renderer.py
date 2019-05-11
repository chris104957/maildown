import mock
from maildown import renderer
import mistune
import pygments
from pygments import lexers
from pygments.formatters import html
import premailer
import jinja2


def test_highlight_renderer(monkeypatch):
    monkeypatch.setattr(mistune, 'escape', mock.MagicMock())
    monkeypatch.setattr(lexers, 'get_lexer_by_name', mock.MagicMock())
    monkeypatch.setattr(html, 'HtmlFormatter', mock.MagicMock())
    monkeypatch.setattr(pygments, 'highlight', mock.MagicMock())

    lexers.get_lexer_by_name.return_value = True
    html.HtmlFormatter.return_value = {}

    r = renderer.HighlightRenderer()
    r.block_code('code')

    mistune.escape.assert_called_with('code')

    r.block_code('code', 'python')
    lexers.get_lexer_by_name.assert_called_with('python', stripall=True)
    pygments.highlight.assert_called_with('code', True, {})


def test_generate_content(monkeypatch):
    monkeypatch.setattr(mistune, 'Markdown', mock.MagicMock())
    monkeypatch.setattr(premailer, 'transform', mock.MagicMock())
    monkeypatch.setattr(renderer, 'HighlightRenderer', mock.MagicMock())
    monkeypatch.setattr(jinja2, 'Template', mock.MagicMock())

    renderer.HighlightRenderer.return_value = 1
    premailer.transform.return_value = ''
    jinja2.Template.render.return_value = ''
    renderer.generate_content('')
    mistune.Markdown.assert_called_with(renderer=1)
