import logging
import os
from logging.handlers import RotatingFileHandler

import dotenv
from pythonjsonlogger import jsonlogger

from ipfabric import IPFClient
from ipfabric.snapshot_models import snapshot_upload

logger = logging.getLogger("python-ipfabric")
formatter = jsonlogger.JsonFormatter('%(levelname)s %(asctime)s %(name)s %(module)s %(message)s')

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

rotatingFileHandler = RotatingFileHandler(filename='rotating_ipfabric.log', backupCount=3, maxBytes=20 * 10000000)
rotatingFileHandler.setLevel(logging.DEBUG)
rotatingFileHandler.setFormatter(formatter)

logger.addHandler(rotatingFileHandler)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    dotenv.load_dotenv(dotenv.find_dotenv())
    SNAP_ID_NOT_TO_DOWNLOAD = ["$last", "$lastLocked", "$prev"]

    ipf_download = IPFClient(base_url=os.getenv("IPF_URL_DOWNLOAD"), token=os.getenv("IPF_TOKEN_DOWNLOAD"))
    ipf_upload = IPFClient(base_url=os.getenv("IPF_URL_UPLOAD"), token=os.getenv("IPF_TOKEN_UPLOAD"))
    snapshots = [snap for snap in ipf_download.snapshots.values() if snap.snapshot_id not in SNAP_ID_NOT_TO_DOWNLOAD]

    for snapshot in snapshots:
        logger.info(f"name: {snapshot.name}, id: {snapshot.snapshot_id}")
        download_path = snapshot.download(ipf_download, retry=5, timeout=5)  # 5 x 5 = 25 seconds
        upload_snap_id = snapshot_upload(ipf_upload, download_path)
        logger.info(
            f"uploaded snapshot {snapshot.name} to {os.getenv('IPF_URL_UPLOAD')} new snap_id = {upload_snap_id}")
