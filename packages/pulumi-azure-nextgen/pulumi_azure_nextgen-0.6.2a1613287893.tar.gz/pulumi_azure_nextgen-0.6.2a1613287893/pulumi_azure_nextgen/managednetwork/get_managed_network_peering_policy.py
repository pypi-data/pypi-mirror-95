# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetManagedNetworkPeeringPolicyResult',
    'AwaitableGetManagedNetworkPeeringPolicyResult',
    'get_managed_network_peering_policy',
]

@pulumi.output_type
class GetManagedNetworkPeeringPolicyResult:
    """
    The Managed Network Peering Policy resource
    """
    def __init__(__self__, id=None, location=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ManagedNetworkPeeringPolicyPropertiesResponse':
        """
        Gets or sets the properties of a Managed Network Policy
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")


class AwaitableGetManagedNetworkPeeringPolicyResult(GetManagedNetworkPeeringPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedNetworkPeeringPolicyResult(
            id=self.id,
            location=self.location,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_managed_network_peering_policy(managed_network_name: Optional[str] = None,
                                       managed_network_peering_policy_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedNetworkPeeringPolicyResult:
    """
    Use this data source to access information about an existing resource.

    :param str managed_network_name: The name of the Managed Network.
    :param str managed_network_peering_policy_name: The name of the Managed Network Peering Policy.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['managedNetworkName'] = managed_network_name
    __args__['managedNetworkPeeringPolicyName'] = managed_network_peering_policy_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:managednetwork:getManagedNetworkPeeringPolicy', __args__, opts=opts, typ=GetManagedNetworkPeeringPolicyResult).value

    return AwaitableGetManagedNetworkPeeringPolicyResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)
