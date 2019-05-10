---
title: "Working with Python"
description: "Implementing Maildown in your Python projects"
date: 2009-01-01
draft: false
---

# Working with Python

Maildown is designed to be used as a CLI tool. However, it is built 
entirely in Python, and its possible to easily integrate it with your 
Python projects too. 

## Setting credentials

When you first install Maildown, as explained in the 
[Getting started guide](/post/getting-started/), you'll need to run
the `maildown init` command. This stores your AWS credentials to your
local environment. Assuming you run the command in the same Python
environment as your project, this will also set your configuration
for the Python library too. Alternatively, you can use the Python
library to store your AWS credentials as follows:

```python
from maildown import utilities as md

md.login('aws_access_key','aws_secret_key')
```

## Verifying email addresses

You can ask Maildown to send a verification email to a new email 
address as follows:

```python
from maildown import utilities as md

md.verify_address("me@email.com")
```

The above command sends an email to `me@email.com`. As with the CLI,
clicking on the email in this link verifies your ownership of that
address, and allows you to send emails from it.

## Sending emails

As in the CLI equivalent, the `send_message` method allows you to supply
either a file path, or string content as the email body 

```python
from maildown import utilities as md

md.send_message(
    sender='me@email.com', 
    subject='Hello', 
    to=['somebody@example.com', 'somebody.else@example.com'],
    file_path='my-email.md'
)

```

## Sending emails with context

The Python library offers one big advantage over the CLI - the ability
to add context to an email.

Maildown actually renders emails twice - it has a simple HTML template
into which the supplied markdown content and style sheet is inserted,
and is then rendered a second time. At this second stage, user supplied
variables can be passed to your emails.

Maildown templates support [Jinja2](http://jinja.pocoo.org/docs/2.10/)
syntax. For example, you can insert Jinja syntax into your markdown
files like this:

```markdown
# Hello {{ name  or "there" }}
```

Then, by passing a context when using `send_message`:

```python
from maildown import utilities as md

md.send_message(
    sender='me@email.com', 
    subject='Hello', 
    to=['somebody@example.com', 'somebody.else@example.com'],
    file_path='my-email.md',
    context=dict(name='Chris')
)
```

You get an email that looks like this:
```
Hello Chris
```

If you did *not* provide a context, you'd get a message that simply said
`Hello there` instead.

It's also possible to combine Markdown with Jinja to conditionally
include content:

```markdown
{% if things %}
## Things
Here are some things:
{% for thing in things %}

- {{ thing }}

{% endfor %}
{% endif %}

```

If you send the above mail with this context:
```python
context=dict(things=['Thing 1', 'Thing 2', 'Thing 3'])
```

Then it renders as this:
```
## Things
Here are some things:
- Thing 1
- Thing 2
- Thing 3
```

If you do *not* provide the `things` in the email context, then due to
the `if` statement, this section would not be displayed at all