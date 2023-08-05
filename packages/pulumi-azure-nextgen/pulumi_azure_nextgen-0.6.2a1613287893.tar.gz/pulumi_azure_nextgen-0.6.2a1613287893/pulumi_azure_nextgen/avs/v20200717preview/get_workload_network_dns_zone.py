# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetWorkloadNetworkDnsZoneResult',
    'AwaitableGetWorkloadNetworkDnsZoneResult',
    'get_workload_network_dns_zone',
]

@pulumi.output_type
class GetWorkloadNetworkDnsZoneResult:
    """
    NSX DNS Zone
    """
    def __init__(__self__, display_name=None, dns_server_ips=None, dns_services=None, domain=None, id=None, name=None, provisioning_state=None, revision=None, source_ip=None, type=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if dns_server_ips and not isinstance(dns_server_ips, list):
            raise TypeError("Expected argument 'dns_server_ips' to be a list")
        pulumi.set(__self__, "dns_server_ips", dns_server_ips)
        if dns_services and not isinstance(dns_services, float):
            raise TypeError("Expected argument 'dns_services' to be a float")
        pulumi.set(__self__, "dns_services", dns_services)
        if domain and not isinstance(domain, list):
            raise TypeError("Expected argument 'domain' to be a list")
        pulumi.set(__self__, "domain", domain)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if revision and not isinstance(revision, float):
            raise TypeError("Expected argument 'revision' to be a float")
        pulumi.set(__self__, "revision", revision)
        if source_ip and not isinstance(source_ip, str):
            raise TypeError("Expected argument 'source_ip' to be a str")
        pulumi.set(__self__, "source_ip", source_ip)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Display name of the DNS Zone.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="dnsServerIps")
    def dns_server_ips(self) -> Optional[Sequence[str]]:
        """
        DNS Server IP array of the DNS Zone.
        """
        return pulumi.get(self, "dns_server_ips")

    @property
    @pulumi.getter(name="dnsServices")
    def dns_services(self) -> Optional[float]:
        """
        Number of DNS Services using the DNS zone.
        """
        return pulumi.get(self, "dns_services")

    @property
    @pulumi.getter
    def domain(self) -> Optional[Sequence[str]]:
        """
        Domain names of the DNS Zone.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def revision(self) -> Optional[float]:
        """
        NSX revision number.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter(name="sourceIp")
    def source_ip(self) -> Optional[str]:
        """
        Source IP of the DNS Zone.
        """
        return pulumi.get(self, "source_ip")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWorkloadNetworkDnsZoneResult(GetWorkloadNetworkDnsZoneResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkloadNetworkDnsZoneResult(
            display_name=self.display_name,
            dns_server_ips=self.dns_server_ips,
            dns_services=self.dns_services,
            domain=self.domain,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            revision=self.revision,
            source_ip=self.source_ip,
            type=self.type)


def get_workload_network_dns_zone(dns_zone_id: Optional[str] = None,
                                  private_cloud_name: Optional[str] = None,
                                  resource_group_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkloadNetworkDnsZoneResult:
    """
    Use this data source to access information about an existing resource.

    :param str dns_zone_id: NSX DNS Zone identifier. Generally the same as the DNS Zone's display name
    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['dnsZoneId'] = dns_zone_id
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:avs/v20200717preview:getWorkloadNetworkDnsZone', __args__, opts=opts, typ=GetWorkloadNetworkDnsZoneResult).value

    return AwaitableGetWorkloadNetworkDnsZoneResult(
        display_name=__ret__.display_name,
        dns_server_ips=__ret__.dns_server_ips,
        dns_services=__ret__.dns_services,
        domain=__ret__.domain,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        revision=__ret__.revision,
        source_ip=__ret__.source_ip,
        type=__ret__.type)
