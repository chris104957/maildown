from typing import Optional
import os
import configparser
from maildown.backends.base import BaseBackend
import boto3
from botocore.exceptions import ClientError


class AwsBackend(BaseBackend):
    name = "aws"

    def login(  # type: ignore
        self,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        region_name: str = "us-east-1",
        aws_config_file: str = os.path.expanduser("~/.aws/credentials"),
    ) -> None:
        """
        Retrieves, checks and stores AWS credentials to the maildown config file. Credentials are either
        taken from the direct parameters, the environmental variables or the .aws/credentials file
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
        elif access_key and secret_key:
            if not self.verify_auth(access_key, secret_key, region_name):
                raise AttributeError("The supplied credentials are not valid")

            self.config["access_key"] = access_key  # type: ignore
            self.config["secret_key"] = secret_key  # type: ignore
            self.config["region_name"] = region_name  # type: ignore

    def send_message(
        self, to: list, sender: str, html: str, content: str, subject: str
    ):
        return self.client.send_email(
            Source=sender,
            Destination=dict(ToAddresses=to),
            Message=dict(
                Body=dict(
                    Html=dict(Charset="utf-8", Data=html),
                    Text=dict(Charset="utf-8", Data=content),
                ),
                Subject=dict(Charset="utf-8", Data=subject),
            ),
        )

    @property
    def client(self) -> boto3.client:
        """
        Returns an authenticated boto3.ses client
        """
        return boto3.client(
            "ses",
            aws_access_key_id=self.config.get("access_key"),  # type: ignore
            aws_secret_access_key=self.config.get("secret_key"),  # type: ignore
            region_name=self.config.get("region", "us-east-1"),  # type: ignore
        )

    def verify_address(self, email: str) -> bool:
        """
        Asks Amazon to send an email to a given email address to verify the user's ownership of that address.

        Email addresses must be verified by Amazon before you can send emails from them with SES

        ### Parameters:

        - `email`: The email address to be verified
        """
        addresses = self.client.list_verified_email_addresses().get(
            "VerifiedEmailAddresses"
        )

        if email in addresses:
            return True

        self.client.verify_email_address(EmailAddress=email)
        return False

    @staticmethod
    def verify_auth(
        access_key: str, secret_key: str, region_name: str = "us-east-1"
    ) -> bool:
        """
        Checks that the given credentials are valid by performing a simple call on the SES API

        ### Parameters:

        - `access_key`: AWS access key
        - `secret_key`: AWS secret key
        - `region_name`: The AWS region name. Defaults to `us-east-1`

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
