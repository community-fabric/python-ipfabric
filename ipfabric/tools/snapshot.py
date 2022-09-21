from pathlib import Path

from ipfabric import IPFClient


def upload(ipf: IPFClient, file: str, snapshot_name: str = None):
    snapshot_name = snapshot_name or Path(file).stem
    file = [
        ('file', (snapshot_name, open(file, 'rb'), 'application/x-tar'))
    ]
    resp = ipf.post('snapshots/upload', headers={"Content-Type": "multipart/form-data"}, data=dict(), files=file)
    resp.raise_for_status()
    return resp.json()


def download(snapshot_id: str):
    ...
