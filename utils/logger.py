import logging


def get_logger(name: str = __name__, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
