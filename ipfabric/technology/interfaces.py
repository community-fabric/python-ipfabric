import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Interfaces(BaseModel):
    client: Any

    @property
    def current_rates_data_inbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/load/inbound")

    @property
    def current_rates_data_outbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/load/outbound")

    @property
    def current_rates_data_bidirectional(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/load/bidirectional")

    @property
    def average_rates_data_inbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transfer-rates/inbound")

    @property
    def average_rates_data_outbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transfer-rates/outbound")

    @property
    def average_rates_data_bidirectional(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transfer-rates/bidirectional")

    @property
    def average_rates_data_inbound_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transfer-rates/inbound-device")

    @property
    def average_rates_data_outbound_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transfer-rates/outbound-device")

    @property
    def average_rates_data_bidirectional_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transfer-rates/bidirectional-device")

    @property
    def average_rates_errors_inbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/inbound")

    @property
    def average_rates_errors_outbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/outbound")

    @property
    def average_rates_errors_bidirectional(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/bidirectional")

    @property
    def average_rates_errors_inbound_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/inbound-device")

    @property
    def average_rates_errors_outbound_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/outbound-device")

    @property
    def average_rates_errors_bidirectional_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/bidirectional-device")

    @property
    def average_rates_drops_inbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/drops/inbound")

    @property
    def average_rates_drops_outbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/drops/outbound")

    @property
    def average_rates_drops_bidirectional(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/drops/bidirectional")

    @property
    def average_rates_drops_inbound_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/drops/inbound-device")

    @property
    def average_rates_drops_outbound_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/drops/outbound-device")

    @property
    def average_rates_drops_bidirectional_per_device(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/drops/bidirectional-device")

    @property
    def duplex(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/duplex")

    @property
    def err_disabled(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/errors/disabled")

    @property
    def connectivity_matrix(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/connectivity-matrix")

    @property
    def connectivity_matrix_unmanaged_neighbors_summary(self):
        return models.Table(
            client=self.client, endpoint="tables/interfaces/connectivity-matrix/unmanaged-neighbors/summary"
        )

    @property
    def connectivity_matrix_unmanaged_neighbors_detail(self):
        return models.Table(
            client=self.client, endpoint="tables/interfaces/connectivity-matrix/unmanaged-neighbors/detail"
        )

    @property
    def switchport(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/switchports")

    @property
    def mtu(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/mtu")

    @property
    def storm_control_all(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/storm-control/all")

    @property
    def storm_control_broadcast(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/storm-control/broadcast")

    @property
    def storm_control_unicast(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/storm-control/unicast")

    @property
    def storm_control_multicast(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/storm-control/multicast")

    @property
    def transceivers(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transceivers/inventory")

    @property
    def transceivers_statistics(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transceivers/statistics")

    @property
    def transceivers_triggered_thresholds(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transceivers/statistics")

    @property
    def transceivers_errors(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/transceivers/errors")

    @property
    def point_to_point_over_ethernet(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/pppoe")

    @property
    def point_to_point_over_ethernet_sessions(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/pppoe/sessions")

    @property
    def counters_inbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/counters/inbound")

    @property
    def counters_outbound(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/counters/outbound")

    @property
    def tunnels_ipv4(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/tunnels/ipv4")

    @property
    def tunnels_ipv6(self):
        return models.Table(client=self.client, endpoint="tables/interfaces/tunnels/ipv6")
