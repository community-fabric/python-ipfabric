from loguru import logger
import sys


def set_logger(console_debug: bool = False):
    logger.level("DEBUG", color="<green>")
    logger.level("INFO", color="<white>")
    logger.level("WARNING", color="<yellow>")
    logger.level("ERROR", color="<red>")
    fmt = (
        "<green>{time:YYYY-MM-DDHH:mm:ss.SSS}</green>|"
        "<level>{level:<8}</level>|"
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>|"
        "<level>{message}</level>"
    )
    # three log files
    # 1 for latest iteration
    # 2 for full day log
    # 3 for weekly log
    logger.add("ipfabric_1.log", level="DEBUG", format=fmt, rotation="5 MB")
    logger.add("ipfabric_2.log", level="DEBUG", format=fmt, rotation="12:00")
    logger.add("ipfabric_3.log", level="DEBUG", format=fmt, rotation="7 days")

    # loguru default loghandler logs to stderr,but sets default level to debug
    # we only want debug logs to the console when we explicitly set it

    # remove default console logger
    logger.remove(0)
    # add a console logger only if console_debug is True
    if console_debug:
        logger.add(sys.stderr, level="DEBUG", format=fmt, colorize=True)
    else:
        logger.add(sys.stderr, level="INFO", format=fmt, colorize=True)
