from logging import Logger


def warn_once(logger: Logger, message: str) -> None:
    if message not in _warned:
        logger.warning(message)
        _warned.append(message)


_warned: list[str] = []
