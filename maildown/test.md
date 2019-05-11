# Hello {{ name or "there" }}

{% if things %}
## Things
Here are some things:
{% for thing in things %}

- {{ thing }}

{% endfor %}
{% endif %}
