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
import httpx
from urllib.parse import urljoin

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
    file = {'file': (Path(file).name, open(file, 'rb'), 'application/x-tar')}
    resp = httpx.request('POST', urljoin(str(ipf.base_url), 'snapshots/upload'), files=file, auth=ipf.auth,
                         verify=ipf.verify)
    resp.raise_for_status()
    return resp.json()


def download(ipf: IPFClient, snapshot_id: str = None, path: str = None, timeout: int = 60):
    if not snapshot_id:
        snapshot_id = ipf.snapshot_id
    else:
        snapshot_id = ipf.snapshots[snapshot_id].snapshot_id  # This checks if snapshot exists

    if not path:
        path = Path(f"{snapshot_id}.tar")
    elif not isinstance(path, Path):
        path = Path(f"{path}")
    if path.name.endswith('.tar'):
        path = Path(f"{path.name}.tar")

    # start download job
    resp = ipf.get(f"/snapshots/{snapshot_id}/download")
    resp.raise_for_status()
    # waiting for download job to process
    time.sleep(timeout)  # TODO Loop until timeout to check
    job_id = find_job_id(ipf, snapshot_id)
    file = ipf.get(f"jobs/{job_id}/download")
    with open(path, "wb") as fp:
        fp.write(file.read())
    return path
