import plain_sight.log as log
from logging import Logger, StreamHandler, Handler


_LOGGER_NAME = 'logger_name'


class FakeLogger(Logger):
    def __init__(self, name: str):
        super().__init__(name)
        self.handler = None

    def addHandler(self, hdlr: Handler) -> None:
        self.handler = hdlr


def test_attach_to_console() -> None:
    logger = FakeLogger(_LOGGER_NAME)

    log.attach_to_console(logger)

    assert logger.handler
    assert isinstance(logger.handler, StreamHandler)


def test_get_logger() -> None:
    logger = log.get_logger(_LOGGER_NAME)

    assert isinstance(logger, Logger)
    assert logger.name == _LOGGER_NAME
