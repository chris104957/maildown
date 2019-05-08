import os
import toml
from typing import Optional, Dict, Union, SupportsFloat
import configparser
import boto3
from botocore.exceptions import ClientError
from maildown.renderer import generate_content


def get_client() -> boto3.client:
    config = get_config()

    return boto3.client(
        "ses",
        aws_access_key_id=config.get("access_key"),
        aws_secret_access_key=config.get("secret_key"),
        region_name=config.get("region", "us-east-1"),
    )


def verify_address(email: str) -> bool:
    client = get_client()
    addresses = client.list_verified_email_addresses().get("VerifiedEmailAddresses")

    if email in addresses:
        return True

    client.verify_email_address(EmailAddress=email)
    return False


def verify_auth(
    access_key: str, secret_key: str, region_name: str = "us-east-1"
) -> bool:
    """
    Checks that the given credentials work by executing a simple boto3 command
    """
    client = boto3.client(
        "ses",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region_name,
    )
    try:
        client.list_configuration_sets()
        return True
    except ClientError:
        return False


def get_config() -> dict:
    """
    Returns the existing configuration from the local
    """
    try:
        with open(os.path.join(os.path.expanduser("~"), "maildown.toml")) as f:
            return toml.loads(f.read())
    except FileNotFoundError:
        pass
    return {}


def write_config(**config: Dict[str, Union[str, SupportsFloat, bool]]) -> None:
    """
    Updates the existing local config with the given additional arguments
    """
    existing = get_config()
    for key, val in config.items():
        existing[key] = val
    with open(os.path.expanduser("~/maildown.toml"), "w") as f:
        f.write(toml.dumps(config))


def login(
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region_name: str = "us-east-1",
    aws_config_file: str = os.path.expanduser("~/.aws/credentials"),
) -> None:
    """
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

    TODO: replace all exceptions raised in this method with Maildown ones
    """

    if not any([access_key, secret_key]):
        access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not any([access_key, secret_key]):
        config = configparser.ConfigParser()
        config.read(aws_config_file)
        try:
            access_key = config["default"].get("aws_access_key_id")
            secret_key = config["default"].get("aws_secret_access_key")

        except KeyError:
            raise KeyError(
                f"Cannot find expected keys in config file stored at {aws_config_file}"
            )

    if not all([access_key, secret_key]):
        raise AttributeError(
            "No credentials supplied - you must either provide the `access_key`, and `secret_key` "
            "values, set the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, or run "
            "`aws configure` and try again"
        )

    if not verify_auth(access_key, secret_key, region_name):
        raise AttributeError("The supplied credentials are not valid")

    config = get_config()
    config["access_key"] = access_key
    config["secret_key"] = secret_key
    config["region_name"] = region_name
    write_config(**config)


def send_message(
    sender: str,
    subject: str,
    to: list,
    content: Optional[str] = None,
    file_path: Optional[str] = None,
    context: Optional[dict] = None,
    theme=None,
):
    if not context:
        context = {}

    if all([content, file_path]) or not any([content, file_path]):
        raise AttributeError(
            "You must provide either the content or filepath attribute"
        )

    if file_path:
        with open(file_path) as f:
            content = f.read()

    kwargs = dict(md_content=content, context=context)

    if theme:
        kwargs["theme"] = theme

    message = generate_content(**kwargs)

    client = get_client()
    return client.send_email(
        Source=sender,
        Destination=dict(ToAddresses=to),
        Message=dict(
            Body=dict(
                Html=dict(Charset="utf-8", Data=message),
                Text=dict(Charset="utf-8", Data=content),
            ),
            Subject=dict(Charset="utf-8", Data=subject),
        ),
    )
