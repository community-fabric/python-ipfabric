import logging

from pythonjsonlogger import jsonlogger

from ipfabric import IPFClient

# Get root logger
logger = logging.getLogger(__name__)

# Get ipfabric logger
ipfabricLogger = logging.getLogger('ipfabric')

# Set ipfabric logging level to DEBUG
ipfabricLogger.setLevel(logging.DEBUG)


# Create JSON formatter and replace default handler in only the ipfabric logger
# 1. Create a StreamHandler object
streamHandler = logging.StreamHandler()

# 2. Create a json Formatter
# For a list of log attributes see: https://docs.python.org/3/library/logging.html#logrecord-attributes
formatter = jsonlogger.JsonFormatter('%(levelname)s %(asctime)s %(name)s %(module)s %(message)s')

# 3. Tell the StreamHandler to use the custom json Formatter object
streamHandler.setFormatter(formatter)

# 4. Add the new streamHandler to the ipfabric logger.
ipfabricLogger.addHandler(streamHandler)

"""
If you would like all messages to be in JSON format simply replace ipfabricLogger with the root logger:
logger.addHandler(streamHandler)
"""


if __name__ == '__main__':
    logger.debug('TEST')  # Will not display because only ipfabric logger is set to DEBUG

    ipf = IPFClient()
    """
    {"levelname": "DEBUG", "asctime": "2022-09-14 09:25:55,122", "name": "ipfabric", "module": "api", 
    "message": "Successfully connected to 'demo3.ipfabric.io' IPF version '5.0.2+5' as user 'admin'"}
    """

    logger.warning('Finished')  # Does not display in JSON because only the ipfabric logger is set to user JSON format
    """Finished"""

