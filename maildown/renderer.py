import os
from typing import Optional
from jinja2 import Template
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from premailer import transform


class HighlightRenderer(mistune.Renderer):
    """
    This highlight renderer improves the way code blocks are handled
    """

    def block_code(self, code, lang=None):
        if not lang:
            return "\n<pre><code>%s</code></pre>\n" % mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


def generate_content(
    md_content: str,
    theme: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css"),
    context: Optional[dict] = None,
):
    """
    Generates the content of an email to be sent. This method actually renders two templates:
    1. The extremely simple local template, which writes the stylesheet, header and user-provided md_content to the
    message
    2.  The result of 1. is also treated as a jinja template, and rendered using the arguments provided in the context
    parameter

    Apart from rendering the template, this method also does two other things:
    1. Applies an additional highlight renderer with better support for code blocks
    2. Uses premailer.transform to bake the css into the HTML
    """
    if not context:
        context = {}

    with open(theme) as f:
        theme = f.read()

    markdown = mistune.Markdown(renderer=HighlightRenderer())

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.jinja2"),) as t:
        template = Template(t.read())
    content = transform(template.render(content=markdown(md_content), stylesheet=theme))

    t = Template(content)
    return t.render(context)
