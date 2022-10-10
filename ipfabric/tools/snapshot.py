from __future__ import annotations

from typing import TYPE_CHECKING

"""
Conditional import for typing, allowing the use of the download function in a snapsnot object.
If we did not utlize a Conditional Import here, you would receive a circular import error when trying to import
the IPF client. Example with non conditional import:
>>> from ipfabric import IPFClient
Traceback (most recent call last):
  File "python-ipfabric/ipfabric/models.py", line 8, in <module>
    from ipfabric.tools.snapshot import download
  File "python-ipfabric/ipfabric/tools/__init__.py", line 4, in <module>
    from .snapshot import upload, download
  File "python-ipfabric/ipfabric/tools/snapshot.py", line 4, in <module>
    from ipfabric import IPFClient
ImportError: cannot import name 'IPFClient' from partially initialized module 'ipfabric' 
(most likely due to a circular import) (python-ipfabric/ipfabric/__init__.py)
>>> 
"""
if TYPE_CHECKING:
    from ipfabric import IPFClient
from pathlib import Path
import time
import logging

logger = logging.getLogger("python-ipfabric")


def find_job_id(ipf, snapshot_id):
    ipf_filter = {
        "snapshot": [
            "eq",
            f"{snapshot_id}"
        ],
        "name": [
            "eq",
            "snapshotDownload"
        ],
        "status": [
            "eq",
            'done'
        ],
        "downloadFile": [
            "empty",
            "false"
        ]
    }
    jobs = ipf.fetch_all("tables/jobs", filters=ipf_filter, snapshot=False)
    job_id = None
    if len(jobs) > 1:
        logger.warning("multiple snapshots downloaded recently with the same snapshot_id, using most recent job_id")
        job_ids = sorted([int(job['id']) for job in jobs])
        job_id = job_ids[-1]
    elif len(jobs) == 0:
        logger.warning(f"No download job found for snap-snap {snapshot_id}")
        logger.debug(f"snapshot_id:{snapshot_id}\nfilter:{ipf_filter}\njobs: {jobs}")
        return job_id
    return job_id


def upload(ipf: IPFClient, file: str):
    # as of time of development, httpx does not support file uploads via form data
    # urllib3 supports pools to stream data faster
    try:
        import urllib3
    except ModuleNotFoundError as err:
        logger.warning("urllib3 is not installed,"
                       "please install via pip using:"
                       "pip install urllib3")
        return None
    http = urllib3.PoolManager() if ipf.verify else urllib3.PoolManager(cert_reqs='CERT_NONE')
    with open(file, 'rb') as fp:
        file = {'file': (Path(file).name, fp.read(), 'application/x-tar')}
    resp = http.request("POST", f"{ipf.base_url}" + "/snapshots/upload", fields=file, headers={'X-API-Token': ipf.auth.api_key})
    if resp.status != 200:
        logger.warning(f"Error uploading snapshot, {resp.data}")
    return resp.data.decode()


# def upload(ipf: IPFClient, file: str):  #TODO Update with new HTTPX Client
#     file = {'file': (Path(file).name, open(file, 'rb'), 'application/x-tar')}
#     resp = ipf.request('POST', 'snapshots/upload', files=file, headers={"Content-Type": "multipart/form-data"})
#     resp.raise_for_status()
#     return resp.json()


def download(ipf: IPFClient, snapshot_id: str, path: str = None):
    if not snapshot_id:
        snapshot_id = ipf.snapshot_id
    # start download job
    ipf.get(f"/snapshots/{snapshot_id}/download")
    # waiting for download job to process
    time.sleep(5)
    if not isinstance(path, Path):
        path = Path(f"{path}")
        if not path:
            ss_name = ipf.snapshots[snapshot_id].dict()['name']
            file_name = f"{snapshot_id}.tar"
            if not bool(ss_name):
                file_name = f"{ss_name}_{snapshot_id}.tar"
            path = Path(f"{file_name}")
    if path and not path.name.endswith('.tar'):
        path = Path(f"{path.name}.tar")
    job_id = find_job_id(ipf, snapshot_id)
    file = ipf.get(f"jobs/{job_id}/download")
    with open(path, "wb") as fp:
        fp.write(file.read())
    return path
