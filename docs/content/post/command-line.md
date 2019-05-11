---
title: "Command line reference"
description: "A list of commands and parameters"
draft: false
---

# Command line reference

## `maildown init`

> Configures Maildown for use

```bash
USAGE
  console init [<access-key>] [<secret-key>] [<region>] [<aws-config-file>]

ARGUMENTS
  <access-key>           Your AWS Access Key ID
  <secret-key>           Your AWS Secret key
  <region>               AWS region to use (defaults to "us-east-1")
  <aws-config-file>      Path to your AWS config file (defaults to ~/.aws/credentials

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

```

## `maildown verify`

> Verifies your ownership of an email address. Must be done prior to sending any messages

```bash
USAGE
  console verify <email-address>

ARGUMENTS
  <email-address>        The email address that you want to verify

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

```

## `maildown send`

>  Send an email to a list of recipients

```bash
USAGE
  console send [-c [<...>]] [-f [<...>]] [-t] <sender> <subject> [<recipients1>] ... [<recipientsN>]

ARGUMENTS
  <sender>               The source email address (you must have verified ownership)
  <subject>              The subject line of the email
  <recipients>           A list of email addresses to send the mail to

OPTIONS
  -c (--content)         The content of the email to send
  -f (--file-path)       A path to a file containing content to send
  -t (--theme)           A path to a css file to be applied to the email
  -e (--variable)        Context variables to pass to the email, e.g. `-e name=Chris` (multiple values allowed)


GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

```

