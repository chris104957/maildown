[![Netlify Status](https://api.netlify.com/api/v1/badges/9d67273a-a51d-417b-bbad-291c237e5d8a/deploy-status)](https://app.netlify.com/sites/adoring-newton-752f36/deploys)
![MIT license](https://img.shields.io/github/license/chris104957/maildown.svg)
[![Coverage Status](https://coveralls.io/repos/github/chris104957/maildown/badge.svg?branch=master)](https://coveralls.io/github/chris104957/maildown?branch=master)
[![Build Status](https://travis-ci.org/chris104957/maildown.svg?branch=master)](https://travis-ci.org/chris104957/maildown)
[![GitSpo Mentions](https://gitspo.com/badges/mentions/chris104957/maildown?style=flat-square)](https://gitspo.com/mentions/chris104957/maildown)

# Maildown

A super simple CLI for sending emails

## Introduction

Maildown is a command line interface that lets you send emails with a minimum of fuss. It currently supports the AWS SES (default)
and Sendgrid as email backends. Support for more email providers will be added in the future

### Why can't I just use `boto3`/the SendGrid API?

Maildown makes it easier to add structure and style to your email content. It supports **Markdown syntax** out of the box, meaning that you can just send Markdown files as emails with no additional effort.

### How much does it cost?

Maildown is open source and therefore completely free. However, it relies on third party services (e.g. AWS, SendGrid) to actually send your emails - these services aren't free,
alhough they do have free limits depending on the number of emails you need to send

## Installation and usage

### Pre requisites

In order to use Maildown, you first need to create an account with one of the supported backend email providers:

- **[AWS](https://aws.amazon.com)**

   For AWS, you'll also realistically need to [take your AWS SES account out of the sandbox](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html)
   
- **[SendGrid](https://sendgrid.com/)**


### Install with `pip`

You can install maildown as follows:
```bash
pip install maildown
```

### Authenticating Maildown

Maildown stores your credentials locally for convenience. Before you can use Maildown's features, you should run the `maildown init` command. By default, 
`maildown` uses the AWS backend:

```bash
maildown init access_key=AWS_ACCESS_KEY_ID secret_key=AWS_SECRET_ACCESS_KEY
```

To use the SendGrid API, you'll need to pass the `--backend=sendgrid` option with all commands:
```bash
maildown init api_key=SENDGRID_API_KEY --backend=sendgrid
```

> If you have previously used the `aws cli` and have already run `aws configure`, or if you have set the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your environment, you can just use `maildown init` with no arguments to store your credentials

### Verify email addresses

Amazon only lets you send emails from verified email addresses - In other words, you need to verify that you own your email address before you can send mails from it. You can either do this from the [SES console](https://console.aws.amazon.com/ses/home), or by using Maildown:

```bash
$ maildown verify christopherdavies553@gmail.com
Email sent to christopherdavies553@gmail.com. You must click the link in this email to verify ownership before you can send any emails
```

When you use the above command, AWS will send an email to the email address you provided. You'll need to click on the link to verify your ownership of the account. Once you've done this, you can repeat the previous command to check the status

```bash
$ maildown verify christopherdavies553@gmail.com
This email address has already been verified
```

You are now ready to start sending emails!

.. note:
    This command is AWS-specific - The SendGrid backend does not implement this feature

## Sending emails

You can now send emails with the following command
```bash
maildown send christopherdavies553@gmail.com "my email subject" -f "email.md" recipient1@gmail.com recipient2@gmail.com
```
The above arguments, in order, are:
- The sending email address (which must have been verified)
- The subject line of your email
- A markdown file containing some content to send. Note that you can also use the `-c` flag to pass string content to be sent directly to the email, e.g. `-c "hello"`
- A list of email addresses to send the content to

## Styling emails

By default, Maildown bakes in its own default style sheet when sending emails. This looks something like this (the below email is the content of this readme):

![screenshot](https://raw.githubusercontent.com/chris104957/maildown/master/Screen%20Shot%202019-05-08%20at%2023.26.45.png)

You can apply your own styles by simply using the `--theme` flag when sending mails, like this:

```bash
maildown send christopherdavies553@gmail.com "my email subject" -f "email.md" --theme "my-style.css" recipient1@gmail.com recipient2@gmail.com
```

