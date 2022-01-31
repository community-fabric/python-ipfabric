import re
from typing import Optional, Union

from ipfabric.pathlookup.graphs import IPFPath
from ipfabric.pathlookup.icmp import ICMP

PORT_REGEX = re.compile(r"^\d*$|^\d*-\d*$")


class DiagramV43(IPFPath):
    CONSTANT_PARAMS = dict(
        type="pathLookup",
        groupBy="siteName",
        otherOptions=dict(applications=".*", tracked=False),
        firstHopAlgorithm=dict(type="automatic"),
        srcRegions=".*",
        dstRegions=".*",
    )

    def __init__(self, client):
        super().__init__(client)

    def unicast(
        self,
        src_ip: str,
        dst_ip: str,
        proto: str = "tcp",
        src_port: Optional[Union[str, int]] = "1024-65535",
        dst_port: Optional[Union[str, int]] = "80,443",
        sec_drop: Optional[bool] = True,
        flags: Optional[list] = None,
        icmp: Optional[ICMP] = None,
        ttl: Optional[int] = 128,
        fragment_offset: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        overlay: dict = None,
    ) -> Union[dict, bytes]:
        """
        Execute an Unicast Path Lookup diagram query for the given set of parameters.

        :param src_ip: str: Source IP address or subnet
        :param dst_ip: str: Destination IP address/subnet
        :param proto: str: Protocol "tcp", "udp", or "icmp"
        :param src_port: int: Source Port for tcp or udp
        :param dst_port: int: Destination Port for tcp or udp
        :param sec_drop: bool: True specifies Security Rules will Drop packets and not Continue
        :param flags: list: TCP flags, defaults to None. Must be a list and only allowed values can be
                            subset of ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
        :param icmp: ICMP: ICMP object
        :param ttl: int: Time to live, default 128
        :param fragment_offset: int: Fragment offset, default 0
        :param snapshot_id: str: Snapshot ID to override class default
        :param overlay: dict: Optional Overlay dictionary
        :return: Union[dict, str]: json contains a dictionary with 'graphResult' and 'pathlookup' primary keys.
                                    If not json then return bytes
        """
        parameters = dict(
            startingPoint=src_ip,
            destinationPoint=dst_ip,
            protocol=proto,
            securedPath=sec_drop,
            pathLookupType="unicast",
            networkMode=self.check_subnets(src_ip, dst_ip),
            l4Options=dict(dstPorts=self.check_ports(dst_port), srcPorts=self.check_ports(src_port)),
            ttl=ttl,
            fragmentOffset=fragment_offset,
            **DiagramV43.CONSTANT_PARAMS,
        )
        payload = dict(
            parameters=self.check_proto(parameters, flags, icmp),
            snapshot=snapshot_id or self.client.snapshot_id,
        )
        if overlay:
            payload["overlay"] = overlay

        return self._query(payload)

    def multicast(
        self,
        src_ip: str,
        grp_ip: str,
        proto: str = "tcp",
        rec_ip: Optional[str] = None,
        src_port: Optional[Union[str, int]] = "1024-65535",
        grp_port: Optional[Union[str, int]] = "80,443",
        sec_drop: Optional[bool] = True,
        flags: Optional[list] = None,
        icmp: Optional[ICMP] = None,
        ttl: Optional[int] = 128,
        fragment_offset: Optional[int] = 0,
        snapshot_id: Optional[str] = None,
        overlay: dict = None,
    ) -> Union[dict, bytes]:
        """
        Execute an Multicast Path Lookup diagram query for the given set of parameters.

        :param src_ip: str: Source IP address
        :param grp_ip: str: Multicast group IP address
        :param proto: str: Protocol "tcp", "udp", or "icmp"
        :param rec_ip: str: Receiver IP address
        :param src_port: int: Source Port for tcp or udp
        :param grp_port: int: Destination Port for tcp or udp
        :param sec_drop: bool: True specifies Security Rules will Drop packets and not Continue
        :param flags: list: TCP flags, defaults to None. Must be a list and only allowed values can be
                            subset of ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
        :param icmp: ICMP: ICMP object
        :param ttl: int: Time to live, default 128
        :param fragment_offset: int: Fragment offset, default 0
        :param snapshot_id: str: Snapshot ID to override class default
        :param overlay: dict: Optional Overlay dictionary
        :return: Union[dict, str]: json contains a dictionary with 'graphResult' and 'pathlookup' primary keys.
                                    If not json then return bytes
        """
        if self.check_subnets(src_ip, grp_ip):
            raise SyntaxError("Multicast does not support subnets, please provide a single IP for Source and Group")

        parameters = dict(
            source=src_ip,
            group=grp_ip,
            protocol=proto,
            securedPath=sec_drop,
            pathLookupType="multicast",
            l4Options=dict(dstPorts=self.check_ports(grp_port), srcPorts=self.check_ports(src_port)),
            ttl=ttl,
            fragmentOffset=fragment_offset,
            **DiagramV43.CONSTANT_PARAMS,
        )
        if rec_ip and self.check_subnets(rec_ip):
            raise SyntaxError("Multicast Receiver IP must be a single IP not subnet.")
        elif rec_ip:
            parameters["receiver"] = rec_ip

        payload = dict(
            parameters=self.check_proto(parameters, flags, icmp),
            snapshot=snapshot_id or self.client.snapshot_id,
        )
        if overlay:
            payload["overlay"] = overlay

        return self._query(payload)

    @staticmethod
    def check_proto(parameters, flags, icmp) -> dict:
        """
        Checks parameters and flags
        :param parameters: dict: Data to Post
        :param flags: list: List of optional TCP flags
        :param icmp: ICMP: ICMP object
        :return: dict: formatted parameters, removing ports if icmp
        """
        if parameters["protocol"] == "tcp" and flags:
            if all(x in ["ack", "fin", "psh", "rst", "syn", "urg"] for x in flags):
                parameters["l4Options"]["flags"] = flags
            else:
                raise SyntaxError("Only accepted TCP flags are ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']")
        elif parameters["protocol"] == "tcp" and not flags:
            parameters["l4Options"]["flags"] = list()
        elif parameters["protocol"] == "icmp":
            if icmp is None:
                raise SyntaxError("Please provide an ICMP type from ipfabric.pathlookup")
            parameters["l4Options"].pop("srcPorts", None)
            parameters["l4Options"].pop("dstPorts", None)
            parameters["l4Options"]["type"] = icmp.type
            parameters["l4Options"]["code"] = icmp.code
        return parameters

    @staticmethod
    def check_ports(ports: str):
        port = ports.replace(" ", "").split(",")
        for p in port:
            if not PORT_REGEX.match(p):
                raise SyntaxError(
                    f"Ports {ports} is not in the valid syntax, "
                    f"examples: ['80', '80,443', '0-1024', '80,8000-8100,8443']"
                )
        return str(",".join(port))
