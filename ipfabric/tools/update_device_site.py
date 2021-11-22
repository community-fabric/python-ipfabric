from ipfabric import IPFClient
import logging
import csv
from tabulate import tabulate
from time import sleep

logger = logging.getLogger()


class UpdateDeviceSite(IPFClient):
    def __init__(self, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.sites = dict()
        self.devices = dict()
        self.changes = list()
        self._get_devices()

    def load_file(self, file):
        with open(file, 'r') as f:
            try:
                csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
            except csv.Error:
                raise csv.Error("File must be a csv with Hostname,Sitename.")
            csvreader = csv.reader(f)
            for row in csvreader:
                hostname = row[0].upper().split('.')[0].strip()
                site = row[1].upper().strip()
                if hostname not in self.devices:
                    logger.warning(f"Could not find device {hostname} in snapshot {self.snapshot_id}.")
                elif site not in self.sites:
                    logger.warning(f"Could not find device {site} in snapshot {self.snapshot_id}.")
                elif self.devices[hostname]["siteKey"] == self.sites[site]:
                    logger.debug(f"Device {hostname} already in site {site} in snapshot {self.snapshot_id}.")
                else:
                    logger.debug(f"Changing device {hostname} to site {site}.")
                    self.changes.append(dict(sn=self.devices[hostname]["sn"], id=self.sites[site]))

    def _get_devices(self):
        devices = self.inventory.devices.all(columns=["sn", "hostname", "siteName", "siteKey"])
        for dev in devices:
            hostname = dev["hostname"].upper().split('.')[0]
            self.devices[hostname] = dict(sn=dev["sn"], siteKey=dev["siteKey"], hostname=dev["hostname"])
            self.sites[dev["siteName"].upper()] = dev["siteKey"]

    def submit_changes(self):
        if not self.changes:
            logger.warning("No changes detected.")
            return
        else:
            logger.warning(f"Submitting {len(self.changes)} device changes.")
        res = self.post('sites/manual-separation', json=dict(sites=self.changes, snapshot=self.snapshot_id))
        res.raise_for_status()
        self._check_snapshot()
        logger.warning("Updates applied.")

    def show_changes(self):
        sn = {self.devices[d]["sn"]: d for d in self.devices}
        sites = {self.sites[s]: s for s in self.sites}
        changes = list()
        for change in self.changes:
            dev = sn[change["sn"]]
            changes.append((dev, sites[self.devices[dev]["siteKey"]], sites[change["id"]]))

        print(tabulate(changes, headers=["Device", "Old Site", "New Site"]))

    def _check_snapshot(self):
        sleep(5)
        res = self.get('snapshots/' + self.snapshot_id)
        res.raise_for_status()
        if res.json()["running"]:
            logger.debug("Snapshot still recalculating, waiting 5 seconds.")
            self._check_snapshot()
