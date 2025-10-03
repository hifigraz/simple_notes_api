import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)


def getLogger(name: str = __name__):
    logger = logging.getLogger(name)
    return logger
