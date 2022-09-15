import logging
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger

from ipfabric import IPFClient

# Get root logger
logger = logging.getLogger(__name__)

# Get ipfabric logger
ipfabricLogger = logging.getLogger('ipfabric')

# Add a stream handler for ipfabric logger
ipfabricLogger.addHandler(logging.StreamHandler())

# Create regular log file with a custom format and set to WARN:
fileHandler = logging.FileHandler(filename='ipfabric.log', mode='w')
fileHandler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(module)s - %(message)s"))
fileHandler.setLevel(logging.WARNING)
ipfabricLogger.addHandler(fileHandler)

# Example JSON logger:
formatter = jsonlogger.JsonFormatter('%(levelname)s %(asctime)s %(name)s %(module)s %(message)s')

# To create a rotating log file with DEBUG level and JSON formatting.
rotatingFileHandler = RotatingFileHandler(filename='rotating_ipfabric.log', backupCount=3, maxBytes=2000)
rotatingFileHandler.setLevel(logging.DEBUG)
rotatingFileHandler.setFormatter(formatter)
ipfabricLogger.addHandler(rotatingFileHandler)


"""
If you would like all messages to logged to a file simply replace ipfabricLogger with the root logger:
logger.addHandler(fileHandler)
logger.addHandler(rotatingFileHandler)
"""


if __name__ == '__main__':
    logger.debug('TEST')  # Will not display because only ipfabric logger is set to DEBUG

    ipf = IPFClient()

    logger.warning('Finished - root')  # Sends to Console
    """Finished - root"""

    ipfabricLogger.warning('Finished - ipfabric')
    """Finished - ipfabric"""

    """
    ipfabric.log:
    WARNING - 2022-09-14 10:53:38,765 - ipfabric - logging_file_example - Finished - ipfabric
    """

    """
    rotating_ipfabric.log:
    {"levelname": "WARNING", "asctime": "2022-09-14 10:51:09,101", "name": "ipfabric", "module": "logging_file_example", "message": "Finished - ipfabric"}
    {"levelname": "WARNING", "asctime": "2022-09-14 10:53:38,765", "name": "ipfabric", "module": "logging_file_example", "message": "Finished - ipfabric"}
    """
