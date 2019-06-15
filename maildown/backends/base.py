from typing import Optional, Any
from maildown import utilities, renderer


class BaseConfig(object):
    def __init__(self, backend):
        self.backend = backend

    def __getitem__(self, item):
        config = utilities.get_config()
        backend_config = config.get(self.backend.name, {})
        return backend_config[item]

    def get(self, item, default: Optional[Any] = None):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def __setitem__(self, key, value):
        config = utilities.get_config()
        backend_config = config.get(self.backend.name, {})
        backend_config[key] = value
        config[self.backend.name] = backend_config
        utilities.write_config(**config)


class BaseBackend(object):
    name = "base"
    config = BaseConfig

    def __init__(self):
        self.config = BaseConfig(self)

    def login(self, *args, **kwargs):
        raise NotImplementedError()

    def verify_address(self, email: str) -> bool:
        raise NotImplementedError()

    def send_message(
        self, to: list, sender: str, html: str, content: str, subject: str
    ) -> None:
        raise NotImplementedError()

    def send(
        self,
        sender: str,
        subject: str,
        to: list,
        content: Optional[str] = None,
        file_path: Optional[str] = None,
        context: Optional[dict] = None,
        theme=None,
    ) -> None:

        if not context:
            context = {}

        if file_path:
            with open(file_path) as f:
                content = f.read()

        if content:
            html = renderer.generate_content(content, context=context, theme=theme)

            self.send_message(to, sender, html, content, subject)

        else:
            raise AttributeError(
                "You must provide either the content or filepath attribute"
            )
