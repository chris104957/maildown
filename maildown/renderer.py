import os
from typing import Optional
import jinja2
import mistune
import pygments
from pygments import lexers
from pygments.formatters import html
import premailer


class HighlightRenderer(mistune.Renderer):
    """
    This highlight renderer improves the way code blocks are handled
    """

    @staticmethod
    def block_code(code, lang=None):
        if not lang:
            return "\n<pre><code>%s</code></pre>\n" % mistune.escape(code)
        lexer = lexers.get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return pygments.highlight(code, lexer, formatter)


def generate_content(
    md_content: str,
    theme: Optional[str] = None,
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
    if not theme:
        theme = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")

    if not context:
        context = {}

    with open(theme) as f:
        theme = f.read()

    markdown = mistune.Markdown(renderer=HighlightRenderer())

    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.jinja2")
    ) as t:
        template = jinja2.Template(t.read())
    content = premailer.transform(
        template.render(content=markdown(md_content), stylesheet=theme)
    )

    new_template = jinja2.Template(content)
    return new_template.render(context)


#
# with open('test.md') as r:
#     with open('test.html', 'w') as f:
#         f.write(generate_content(r.read(), theme='my-style.css', context=dict(things=['Thing 1', 'Thing 2'])))
