# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GetWorkloadNetworkDhcpResult',
    'AwaitableGetWorkloadNetworkDhcpResult',
    'get_workload_network_dhcp',
]

@pulumi.output_type
class GetWorkloadNetworkDhcpResult:
    """
    NSX DHCP
    """
    def __init__(__self__, dhcp_type=None, display_name=None, id=None, name=None, provisioning_state=None, revision=None, segments=None, type=None):
        if dhcp_type and not isinstance(dhcp_type, str):
            raise TypeError("Expected argument 'dhcp_type' to be a str")
        pulumi.set(__self__, "dhcp_type", dhcp_type)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
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
        if segments and not isinstance(segments, list):
            raise TypeError("Expected argument 'segments' to be a list")
        pulumi.set(__self__, "segments", segments)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dhcpType")
    def dhcp_type(self) -> str:
        """
        Type of DHCP: SERVER or RELAY.
        """
        return pulumi.get(self, "dhcp_type")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Display name of the DHCP entity.
        """
        return pulumi.get(self, "display_name")

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
    @pulumi.getter
    def segments(self) -> Sequence[str]:
        """
        NSX Segments consuming DHCP.
        """
        return pulumi.get(self, "segments")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWorkloadNetworkDhcpResult(GetWorkloadNetworkDhcpResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkloadNetworkDhcpResult(
            dhcp_type=self.dhcp_type,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            revision=self.revision,
            segments=self.segments,
            type=self.type)


def get_workload_network_dhcp(dhcp_id: Optional[str] = None,
                              private_cloud_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkloadNetworkDhcpResult:
    """
    Use this data source to access information about an existing resource.

    :param str dhcp_id: NSX DHCP identifier. Generally the same as the DHCP display name
    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['dhcpId'] = dhcp_id
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:avs:getWorkloadNetworkDhcp', __args__, opts=opts, typ=GetWorkloadNetworkDhcpResult).value

    return AwaitableGetWorkloadNetworkDhcpResult(
        dhcp_type=__ret__.dhcp_type,
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        revision=__ret__.revision,
        segments=__ret__.segments,
        type=__ret__.type)
