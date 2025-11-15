from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from posty.config import Config


class PostyError(RuntimeError):
    pass


class InvalidConfig(PostyError):
    def __init__(self, config_obj: "Config", reason: str) -> None:
        msg = "Invalid config at {}. Reason: {}".format(config_obj.config_path, reason)
        super(self.__class__, self).__init__(msg)


class UnableToImport(PostyError):
    pass


class MalformedInput(PostyError):
    pass


class InvalidObject(PostyError):
    pass
