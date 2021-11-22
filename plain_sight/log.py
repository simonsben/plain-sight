from logging import getLogger, Logger, StreamHandler, Formatter, Handler
from sys import stdout
from os import environ


_FORMATTER = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

emergency_logger = getLogger('EMERGENCY')
emergency_logger.setLevel('ERROR')


def attach_to_console(logger: Logger) -> None:
    handler = StreamHandler(stdout)
    handler.setFormatter(_FORMATTER)

    logger.addHandler(handler)


attach_to_console(emergency_logger)


def get_logger(name: str) -> Logger:
    log_level = environ.get('log_level', 'ERROR')
    emergency_logger.info('Setting %s log level to %s.', name, log_level)

    logger = getLogger(name)
    logger.setLevel(log_level)

    attach_to_console(logger)

    return logger

