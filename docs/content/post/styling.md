---
title: "Styling emails in Maildown"
description: "Learn how to change the default styles in your emails"
draft: false
---

## Styling emails in Maildown

By default, Maildown applies its own style sheet to all emails it sends.
These style sheets get baked into the HTML at the moment the email is 
rendered. For example, this:

```css
h1, h2, h3, h4, h5, h6 {
 font-weight: bold;
}

h1 {
 color: #000000;
 font-size: 28pt;
}
```

Becomes this in the rendered email:

```html
<h1 style="font-weight:bold; color:#000; font-size:28pt">Hello</h1>
```

Styles need to be converted to inline markup like this due to the way
email works. You can see the whole default style sheet that gets
applied by Maildown [here](https://github.com/chris104957/maildown/blob/master/maildown/style.css)

## Applying your own style sheets

It is possible to specify your own style sheets in Maildown. Simply
write your css to a file, like this:

`my-style.css`

```css
h1 {
    color: pink
}
```

You can then call it like this:

```bash
maildown send me@email.com "subject" -f "email.md" -t my-style.css somebody@email.com
```
This would produce a result like this:

![pink](/bacon-style.png)

If you don't like the default style sheet, but don't want to make your
own, then there are plenty of good style sheets designed specifically 
for markdown out there - like [this](https://github.com/jasonm23/markdown-css-themes)

For example, theme 8 from the above repository looks like this when
applied to our email:

![pink](/bacon-style-2.png)

 