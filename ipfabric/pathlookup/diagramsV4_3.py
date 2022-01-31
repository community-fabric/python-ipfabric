from typing import Optional, Union

from ipfabric.pathlookup.graphs import IPFPath


class DiagramV43(IPFPath):
    def __init__(self, client):
        super().__init__(client)

    def unicast(
        self,
        src_ip: str,
        dst_ip: str,
        proto: str = "tcp",
        src_port: Optional[int] = 10000,
        dst_port: Optional[int] = 80,
        sec_drop: Optional[bool] = True,
        grouping: Optional[str] = "siteName",
        flags: Optional[list] = None,
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
        :param grouping: str:  Group by "siteName", "routingDomain", "stpDomain"
        :param flags: list: TCP flags, defaults to None. Must be a list and only allowed values can be
                            subset of ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
        :param snapshot_id: str: Snapshot ID to override class default
        :param overlay: dict: Optional Overlay dictionary
        :return: Union[dict, str]: json contains a dictionary with 'graphResult' and 'pathlookup' primary keys.
                                    If not json then return bytes
        """
        parameters = dict(
            startingPoint=src_ip,
            destinationPoint=dst_ip,
            protocol=proto,
            type="pathLookup",
            securedPath=sec_drop,
            pathLookupType="unicast",
            groupBy=grouping,
            networkMode=self.check_subnets(src_ip, dst_ip),
            l4Options=dict(
                dstPorts=dst_port,
                srcPorts=src_port
            ),
            otherOptions=dict(
                applications=".*",
                tracked=False
            )
        )
        payload = dict(
            parameters=self.check_proto(parameters, flags),
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
        src_port: Optional[int] = 10000,
        grp_port: Optional[int] = 80,
        sec_drop: Optional[bool] = True,
        grouping: Optional[str] = "siteName",
        flags: Optional[list] = None,
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
        :param grouping: str:  Group by "siteName", "routingDomain", "stpDomain"
        :param flags: list: TCP flags, defaults to None. Must be a list and only allowed values can be
                            subset of ['ack', 'fin', 'psh', 'rst', 'syn', 'urg']
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
            type="pathLookup",
            securedPath=sec_drop,
            pathLookupType="multicast",
            groupBy=grouping,
            l4Options=dict(
                dstPorts=grp_port,
                srcPorts=src_port
            ),
            otherOptions=dict(
                applications=".*",
                tracked=False
            )
        )
        if rec_ip and self.check_subnets(rec_ip):
            raise SyntaxError("Multicast Receiver IP must be a single IP not subnet.")
        elif rec_ip:
            parameters["receiver"] = rec_ip

        payload = dict(
            parameters=self.check_proto(parameters, flags),
            snapshot=snapshot_id or self.client.snapshot_id,
        )
        if overlay:
            payload["overlay"] = overlay

        return self._query(payload)

    @staticmethod
    def check_proto(parameters, flags) -> dict:
        """
        Checks parameters and flags
        :param parameters: dict: Data to Post
        :param flags: list: List of optional TCP flags
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
            parameters["l4Options"].pop("srcPorts", None)
            parameters["l4Options"].pop("dstPorts", None)
        return parameters
