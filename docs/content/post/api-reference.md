---
title: "API reference"
description: "Python method documentation"
draft: false
---

# maildown.utilities

## get_client
```python
get_client() -> <function client at 0x10632d158>
```

Returns an authenticated boto3.ses client

## verify_address
```python
verify_address(email: str) -> bool
```

Asks Amazon to send an email to a given email address to verify the user's ownership of that address.

Email addresses must be verified by Amazon before you can send emails from them with SES

### Parameters:

- `email`: The email address to be verified

## verify_auth
```python
verify_auth(access_key: str, secret_key: str, region_name: str = 'us-east-1') -> bool
```

Checks that the given credentials are valid by performing a simple call on the SES API

### Parameters:

- `access_key`: AWS access key
- `secret_key`: AWS secret key
- `region_name`: The AWS region name. Defaults to `us-east-1`


## get_config
```python
get_config() -> dict
```

Returns the existing configuration from the local environment

## write_config
```python
write_config(**config: Dict[str, Union[str, SupportsFloat, bool]]) -> None
```

Updates the existing local config with the given additional arguments

### Parameters:

- `config`: the new configuration items to add to the configuration


## login
```python
login(access_key: Union[str, NoneType] = None, secret_key: Union[str, NoneType] = None, region_name: str = 'us-east-1', aws_config_file: str = '/Users/christopherdavies/.aws/credentials') -> None
```

Checks your AWS credentials are valid, and stores them locally if so for future re use.

If you provide the access key/secret key arguments directly to this function, then these credentials will be taken
in the first instance.

If these arguments are NOT supplied, then this method will first check to see if the AWS_ACCESS_KEY_ID and
AWS_SECRET_ACCESS_KEY environmental variables have been set.

If not, this method will attempt to read the file kept at `aws_config_file`, which is the default location of
the Amazon CLI config file.

If this method cannot find credentials via any one of these methods, or if the credentials it does find are invalid,
then an Exception is raised.

However, if valid credentials can be found, these are stored locally

### Parameters:

- `access_key`: AWS access key
- `secret_key`: AWS secret key
- `region_name`: The AWS region name. Defaults to `us-east-1`
- `aws_config_file`: The location of the credentials file created by `aws configure`


## send_message
```python
send_message(sender: str, subject: str, to: list, content: Union[str, NoneType] = None, file_path: Union[str, NoneType] = None, context: Union[dict, NoneType] = None, theme=None)
```

Sends an email to a given list of recipients

### Parameters:

- `sender`: the email address to send the message from. Must have been verified by SES
- `subject`: The subject line of the email
- `to`: A list of email addresses to send the email to
- `content`: The content of the email to send. Either this parameter, or `file_path`, must be supplied
- `file_path`: A local file path to a file to be send as the email body
- `context`: Additional context to be sent to the email - can be inserted using Jinja2 template syntax
- `theme`: A local file path to a css style sheet. If not supplied, the default style is used

