"""All the loggers that I typically use."""
import logging
from typing import Optional

# Strings for formatting with colors
FORMAT_STR = '%(asctime)s - %(name)s - #color%(levelname)s\u001b[0m - %(message)s'
NO_COLOR_STR = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
COLORS = {
    logging.DEBUG: "\u001b[7m",     # Grey
    logging.INFO: "\u001b[34m",     # Blue
    logging.WARNING: "\u001b[172m", # Orange
    logging.ERROR: "\u001b[41m",    # Red
}


class ColorFormatter(logging.Formatter):
    """Class used to color formatters."""
    def __init__(self, use_color: bool = False, *args, colors, **kwargs):
        self.use_color = use_color
        super().__init__(*args, **kwargs)

        if use_color:
            replace_tags = lambda level: (self._style._fmt
                                        .replace("#color", colors.get(level, "")))
        else:
            replace_tags = lambda level: (self._style._fmt)
        levels = set(logging.getLevelNamesMapping().values())
        self._fmts = {level: replace_tags(level) for level in levels}

    def format(self, record):
        self._style._fmt = self._fmts.get(record.levelno)
        return super().format(record)


def get_clean_logger(logger_name: str = 'no_spam', log_filename: Optional[str] = None):
    """Gets a logger with no BS.
    Params:
        logger_name (str): The name displayed in the console + log file.
        log_filename (str): The name of the log file to write to.
    Returns:
        A beautiful logger.
    """
    # create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # add formatter to ch
    ch.setFormatter(ColorFormatter(fmt=FORMAT_STR, colors=COLORS, use_color=True))
    logger.addHandler(ch)

    # add output file
    if log_filename is not None:
        fh = logging.FileHandler(log_filename, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(ColorFormatter(fmt=NO_COLOR_STR, colors=COLORS, use_color=False))
        logger.addHandler(fh)

    return logger
