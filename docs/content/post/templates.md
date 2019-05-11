---
title: "Advanced template syntax"
description: "See the full set of functionality available in your emails"
draft: false
---

# Advanced template syntax

## Introduction

When generating your emails, Maildown actually renders the content 
twice - First, it inserts your markdown email content into a basic
HTML template along with the selected (or default) css style sheet.
The rendered template then has the css file *baked* into it - that's to
say, the style sheet is removed totally, and instead every single
HTML element is styled individually. This needs to happen as emails do
not support styling in the same way as browser rendered web sites do.

This rendered content then becomes a template itself - at this stage,
anything passed to the email as the `context` parameter gets inserted
into the template, producing the final email. This allows you to easily
iterate through some data and send emails, like this:

```python
from maildown import utilities as md
people = [{'name': 'Chris'}, {'name': 'Steve'}]
content = '# Hello, {{ name }}'
for context in people:
    md.send_message(..., content=content, context=context)
    
# Hello, Chris
# Hello, Steve
```

Maildown uses `jinja2` to render emails. What this means is that 
Maildown supports both Markdown and Jinja2 syntax in emails - you can
use Jinja2 to handle placeholders, conditional sections, and iteration
- there are a few examples of this below

## Examples

### Conditionally including sections in your emails

Email template:
```markdown
# Everyone can see this message

{% if include %}
    This is only visible if the `include` variable has been passed in 
    the context
{% endif %}
```

### Simple placeholder insertion with default values

```markdown
# Hello {{ name  or "there" }}
```

### Iterating through a list of items 
 
 ```markdown
 ## Things
Here are some things:
{% for thing in things %}

- {{ thing }}

{% endfor %}
 ```

### Applying filters

```markdown
{% filter upper %}
    Everything here will become very shouty
{% endfilter %}
```



 
 