from ipfabric import IPFClient
from ipfabric.tools.snapshot import download, upload

import os
import logging
from logging.handlers import RotatingFileHandler
import dotenv
from pythonjsonlogger import jsonlogger


logger = logging.getLogger("python-ipfabric")
formatter = jsonlogger.JsonFormatter('%(levelname)s %(asctime)s %(name)s %(module)s %(message)s')

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

rotatingFileHandler = RotatingFileHandler(filename='rotating_ipfabric.log', backupCount=3, maxBytes=20*10000000)
rotatingFileHandler.setLevel(logging.DEBUG)
rotatingFileHandler.setFormatter(formatter)

logger.addHandler(rotatingFileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    dotenv.load_dotenv(dotenv.find_dotenv())
    SNAP_ID_NOT_TO_DOWNLOAD=["$last","$lastLocked","$prev"]

    ipf_download = IPFClient(base_url=os.getenv("IPF_URL_DOWNLOAD"), token=os.getenv("IPF_TOKEN_DOWNLOAD"))
    ipf_upload = IPFClient(base_url=os.getenv("IPF_URL_UPLOAD"), token=os.getenv("IPF_TOKEN_UPLOAD"))
    snap_ids = [snapshot_id for snapshot_id in ipf_download.snapshots if snapshot_id not in SNAP_ID_NOT_TO_DOWNLOAD]

    for id in snap_ids:
        snap_dict = ipf_download.snapshots[id].dict()
        logger.info(f"name: {snap_dict['name']}, id: {snap_dict['snapshot_id']}, count:{snap_dict['count']}")
        download_path = download(ipf_download, snapshot_id=snap_dict['snapshot_id'])
        upload_snap_id = upload(ipf_upload, download_path)
        logger.info(f"uploaded snapshot {snap_dict['name']} to {os.getenv('IPF_URL_UPLOAD')} new snap_id = {upload_snap_id}")
