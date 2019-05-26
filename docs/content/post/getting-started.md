---
title: "Getting started with Maildown"
description: "From installation to sending your first email"
date: 2010-01-01
draft: false
---

## Introduction

Maildown is a command line interface that lets you send emails using 
Amazon AWS SES with a minimum of fuss.

### Why can't I just use `boto3`?

Maildown makes it easier to add structure and style to your email 
content. It supports **Markdown syntax** out of the box, meaning that 
you can just send Markdown files as emails with no additional effort.

### How much does it cost?

Maildown is open source and therefore completely free. It relies on 
Amazon SES, which *isn't* completely free, but it does let you send up 
to 62,000 free emails per month (*when sent from an EC2 instance*). So for vast majority of people, 
Maildown costs nothing to run.

## Installation and usage

### Pre requisites

In order to use Maildown, you first need to create an AWS free tier 
account [here](https://aws.amazon.com). Once you've signed up, you'll 
also realistically need to [take your AWS SES account out of the sandbox](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html)

### Install with `pip`

You can install maildown as follows:
```bash
pip install maildown
```

### Authenticating Maildown

Maildown stores your credentials locally for convenience. Before you can
use Maildown's features, you should run the `maildown init` command

```bash
maildown init AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY
```

> If you have previously used the `aws cli` and have already run 
`aws configure`, or if you have set the environment variables 
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your environment, 
you can just use `maildown init` with no arguments to store your 
credentials

### Verify email addresses

Amazon only lets you send emails from verified email addresses - In 
other words, you need to verify that you own your email address before 
you can send mails from it. You can either do this from the 
[SES console](https://console.aws.amazon.com/ses/home), or by using 
Maildown:

```bash
$ maildown verify christopherdavies553@gmail.com
Email sent to christopherdavies553@gmail.com. You must click the link in this email to verify ownership before you can send any emails
```

When you use the above command, AWS will send an email to the email 
address you provided. You'll need to click on the link to verify your 
ownership of the account. Once you've done this, you can repeat the 
previous command to check the status

```bash
$ maildown verify christopherdavies553@gmail.com
This email address has already been verified
```

You are now ready to start sending emails!

## Sending emails

You can now send emails with the following command
```bash
maildown send christopherdavies553@gmail.com "my email subject" -f "email.md" recipient1@gmail.com recipient2@gmail.com
```
The above arguments, in order, are:

- The sending email address (which must have been verified)
- The subject line of your email
- A markdown file containing some content to send. Note that you can 
  also use the `-c` flag to pass string content to be sent directly to 
  the email, e.g. `-c "hello"`
- A list of email addresses to send the content to

### Adding context to your emails

It's also possible to add context to your emails. For example, you can
add syntax like this to your Markdown emails:
```markdown
# Hello {{ name  or "there" }}
```

You can then pass the `name` argument to your emails as follows:
```bash
maildown send christopherdavies553@gmail.com "my email subject" -e name=Chris -f "email.md" recipient1@gmail.com 
```
This will be rendered as `Hello Chris` when you send your email. If you 
do not provide this context, it will render as `Hello there`, as you
set the default fallback value to `there` in this instance.

To see the full set of what's possible in your Markdown emails, see
[advanced template syntax](/posts/templates)

## Styling emails

By default, Maildown bakes in its own default style sheet when sending 
emails. This looks something like this (the below email is the content 
of this project's Github readme):

![screenshot](https://raw.githubusercontent.com/chris104957/maildown/master/Screen%20Shot%202019-05-08%20at%2023.26.45.png)

You can apply your own styles by simply using the `--theme` flag when 
sending mails, like this:

```bash
maildown send christopherdavies553@gmail.com "my email subject" -f "email.md" --theme "my-style.css" recipient1@gmail.com recipient2@gmail.com
```
