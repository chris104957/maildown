import pytest
from maildown import utilities, backends, renderer
import boto3
import mock
from botocore.exceptions import ClientError
import builtins
import toml
import configparser


class MockClient(object):
    def __init__(self, *args, **kwargs):
        pass

    def list_verified_email_addresses(self):
        return dict(VerifiedEmailAddresses=["me@email.com"])

    def verify_email_address(self, EmailAddress):
        pass

    def list_configuration_sets(self):
        raise ClientError({"Error": {"Code": 1234}}, "operation_name")


def test_client(monkeypatch):
    monkeypatch.setattr(utilities, "get_config", mock.MagicMock())
    monkeypatch.setattr(boto3, "client", mock.MagicMock())
    utilities.get_config.return_value = dict(access_key=1, secret_key=1)
    backends.AwsBackend().client

    boto3.client.assert_called_with(
        "ses", aws_access_key_id=None, aws_secret_access_key=None, region_name="us-east-1"
    )


def test_verify_address(monkeypatch):
    monkeypatch.setattr(boto3, "client", MockClient)
    backend = backends.AwsBackend()

    assert backend.verify_address("me@email.com") is True
    assert backend.verify_address("me2@email.com") is False


def test_verify_auth(monkeypatch):
    monkeypatch.setattr(boto3, "client", mock.MagicMock())

    assert backends.AwsBackend().verify_auth("access_key", "secret_key") is True
    boto3.client.assert_called_with(
        "ses",
        aws_access_key_id="access_key",
        aws_secret_access_key="secret_key",
        region_name="us-east-1",
    )

    monkeypatch.setattr(boto3, "client", MockClient)
    assert backends.AwsBackend().verify_auth("access_key", "secret_key") is False


def test_get_config(monkeypatch):
    monkeypatch.setattr(builtins, "open", mock.MagicMock())
    monkeypatch.setattr(toml, "loads", mock.MagicMock())

    file_handle = open.return_value.__enter__.return_value

    utilities.get_config()
    file_handle.read.assert_called_with()
    file_handle.read.side_effect = FileNotFoundError()

    assert utilities.get_config() == {}


def test_write_config(monkeypatch):
    monkeypatch.setattr(builtins, "open", mock.MagicMock())
    monkeypatch.setattr(toml, "dumps", mock.MagicMock())
    monkeypatch.setattr(utilities, "get_config", mock.MagicMock())
    utilities.get_config.return_value = {}

    file_handle = open.return_value.__enter__.return_value
    utilities.write_config(test="test")
    toml.dumps.assert_called_with({"test": "test"})


def test_login(monkeypatch):
    monkeypatch.setattr(configparser, "ConfigParser", mock.MagicMock())
    monkeypatch.setattr(backends.AwsBackend, "verify_auth", mock.MagicMock())
    backends.AwsBackend().login(aws_config_file="cred")
    configparser.ConfigParser().read.assert_called_with("cred")


def test_send_message(monkeypatch):
    monkeypatch.setattr(backends.AwsBackend, "client", mock.MagicMock())
    monkeypatch.setattr(builtins, "open", mock.MagicMock())
    monkeypatch.setattr(renderer, "generate_content", mock.MagicMock())
    with pytest.raises(AttributeError):
        backends.AwsBackend().send("test", "test", ["test@test.com"], theme="test")

    backends.AwsBackend().send(
        "test", "test", ["test@test.com"], file_path="test", theme="test"
    )
