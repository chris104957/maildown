from cleo.testers import CommandTester
from maildown.application import application
from maildown import backends
import mock


def test_init(monkeypatch):
    monkeypatch.setattr(backends.AwsBackend, "login", mock.MagicMock())
    command = application.find("init")
    command_tester = CommandTester(command)
    command_tester.execute("access_key=access_key secret_key=secret_key region=region aws_config_file=aws_config_file")

    backends.AwsBackend().login.assert_called_with(
        access_key="access_key",
        secret_key="secret_key",
        region="region",
        aws_config_file="aws_config_file",
    )
    assert "Initiated successfully" in command_tester.io.fetch_output()

    command_tester.execute("--backend=grrr")
    assert 'No backend called grrr' in command_tester.io.fetch_output()


def test_verify(monkeypatch):
    monkeypatch.setattr(backends.AwsBackend, "verify_address", mock.MagicMock())

    command = application.find("verify")
    command_tester = CommandTester(command)
    command_tester.execute("me@email.com")

    backends.AwsBackend().verify_address.assert_called_with("me@email.com")
    assert (
        "This email address has already been verified"
        in command_tester.io.fetch_output()
    )

    backends.AwsBackend().verify_address.return_value = False
    command_tester.execute("me@email.com")
    assert "Email sent to me@email.com" in command_tester.io.fetch_output()

    command_tester.execute("--backend=grrr somebody@email.com")
    assert 'No backend called grrr' in command_tester.io.fetch_output()


def test_send(monkeypatch):
    monkeypatch.setattr(backends.AwsBackend, "send", mock.MagicMock())

    command = application.find("send")
    command_tester = CommandTester(command)
    command_tester.execute("me@email.com test --c test --t test somebody@email.com")

    backends.AwsBackend().send.assert_called_with(
        sender="me@email.com",
        subject="test",
        content="test",
        to=["somebody@email.com"],
        file_path=None,
        theme="test",
        context={},
    )

    assert "Messages added to queue" in command_tester.io.fetch_output()

    command_tester.execute("me@email.com test --c test")

    assert "You must supply at least one recipient" in command_tester.io.fetch_output()

    command_tester.execute("me@email.com test somebody@email.com -e grrr=arg")

    assert (
        "You must provide either the content or file_path argument only"
        in command_tester.io.fetch_output()
    )

    command_tester.execute("--backend=grrr me@email.com test somebody@email.com")
    assert 'No backend called grrr' in command_tester.io.fetch_output()

