import mock
from maildown.application import application
import maildown


def test_app(monkeypatch):
    monkeypatch.setattr(application, 'run', mock.MagicMock())
    maildown.run()
    application.run.assert_called_with()

