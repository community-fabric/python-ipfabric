import logging
from typing import Any

from pydantic import BaseModel

from ipfabric import models

logger = logging.getLogger("python-ipfabric")


class Management(BaseModel):
    client: Any

    @property
    def aaa_servers(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/servers")

    @property
    def aaa_lines(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/lines")

    @property
    def aaa_authentication(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/authentication")

    @property
    def aaa_authorization(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/authorization")

    @property
    def aaa_accounting(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/accounting")

    @property
    def aaa_users(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/users")

    @property
    def aaa_password_strength(self):
        return models.Table(client=self.client, endpoint="tables/security/aaa/password-strength")

    @property
    def telnet_access(self):
        return models.Table(client=self.client, endpoint="tables/security/enabled-telnet")

    @property
    def saved_config_consistency(self):
        return models.Table(client=self.client, endpoint="tables/management/configuration/saved")

    @property
    def ntp_summary(self):
        return models.Table(client=self.client, endpoint="tables/management/ntp/summary")

    @property
    def ntp_sources(self):
        return models.Table(client=self.client, endpoint="tables/management/ntp/sources")

    @property
    def port_mirroring(self):
        return models.Table(client=self.client, endpoint="tables/management/port-mirroring")

    @property
    def logging_summary(self):
        return models.Table(client=self.client, endpoint="tables/management/logging/summary")

    @property
    def logging_remote(self):
        return models.Table(client=self.client, endpoint="tables/management/logging/remote")

    @property
    def logging_local(self):
        return models.Table(client=self.client, endpoint="tables/management/logging/local")

    @property
    def flow_overview(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/overview")

    @property
    def netflow_devices(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/netflow/devices")

    @property
    def netflow_collectors(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/netflow/collectors")

    @property
    def netflow_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/netflow/interfaces")

    @property
    def sflow_devices(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/sflow/devices")

    @property
    def sflow_collectors(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/sflow/collectors")

    @property
    def sflow_sources(self):
        return models.Table(client=self.client, endpoint="tables/management/flow/sflow/sources")

    @property
    def snmp_summary(self):
        return models.Table(client=self.client, endpoint="tables/management/snmp/summary")

    @property
    def snmp_communities(self):
        return models.Table(client=self.client, endpoint="tables/management/snmp/communities")

    @property
    def snmp_trap_hosts(self):
        return models.Table(client=self.client, endpoint="tables/management/snmp/trap-hosts")

    @property
    def snmp_users(self):
        return models.Table(client=self.client, endpoint="tables/management/snmp/users")

    @property
    def ptp_local_clock(self):
        return models.Table(client=self.client, endpoint="tables/management/ptp/local-clock")

    @property
    def ptp_masters(self):
        return models.Table(client=self.client, endpoint="tables/management/ptp/masters")

    @property
    def ptp_interfaces(self):
        return models.Table(client=self.client, endpoint="tables/management/ptp/interfaces")

    @property
    def license_summary(self):
        return models.Table(client=self.client, endpoint="tables/management/licenses/summary")

    @property
    def licenses(self):
        return models.Table(client=self.client, endpoint="tables/management/licenses")

    @property
    def licenses_detail(self):
        return models.Table(client=self.client, endpoint="tables/management/licenses/detail")

    @property
    def cisco_smart_licenses_authorization(self):
        return models.Table(
            client=self.client, endpoint="tables/management/licenses/cisco-smart-licenses/authorization"
        )

    @property
    def cisco_smart_licenses_registration(self):
        return models.Table(client=self.client, endpoint="tables/management/licenses/cisco-smart-licenses/registration")

    @property
    def cisco_smart_licenses_reservations(self):
        return models.Table(client=self.client, endpoint="tables/management/licenses/cisco-smart-licenses/reservations")

    @property
    def dns_resolver_settings(self):
        return models.Table(client=self.client, endpoint="tables/management/dns/settings")

    @property
    def dns_resolver_servers(self):
        return models.Table(client=self.client, endpoint="tables/management/dns/servers")
