from pathlib import Path
import time
import logging
from ipfabric import IPFClient

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
    resp = ipf.post('snapshots/upload', headers={"Content-Type": "multipart/form-data"}, data=dict(), files=file)
    resp.raise_for_status()
    return resp.json()


def download(ipf: IPFClient, snapshot_id: str, path: str):
    if not snapshot_id:
        snapshot_id = ipf.snapshot_id
    # start download job
    ipf.get(f"/snapshots/{snapshot_id}/download")
    # waiting for download job to process
    time.sleep(5)
    if not isinstance(path, Path):
        path = Path(f"{path}")
    if path and not path.name.endswith('.tar'):
        path = Path(f"{path.name}.tar")
    if not path:
        ss_name = ipf.snapshots[snapshot_id].dict()['name']
        file_name = f"{snapshot_id}.tar"
        if not bool(ss_name):
            file_name = f"{ss_name}_{snapshot_id}.tar"
        path = Path(f"{file_name}")
    job_id = find_job_id(ipf, snapshot_id)
    file = ipf.get(f"jobs/{job_id}/download")
    with open(path, "wb") as fp:
        fp.write(file.read())
    return True
