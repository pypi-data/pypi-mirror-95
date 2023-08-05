# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetWorkloadNetworkPortMirroringResult',
    'AwaitableGetWorkloadNetworkPortMirroringResult',
    'get_workload_network_port_mirroring',
]

@pulumi.output_type
class GetWorkloadNetworkPortMirroringResult:
    """
    NSX Port Mirroring
    """
    def __init__(__self__, destination=None, direction=None, display_name=None, id=None, name=None, provisioning_state=None, revision=None, source=None, status=None, type=None):
        if destination and not isinstance(destination, str):
            raise TypeError("Expected argument 'destination' to be a str")
        pulumi.set(__self__, "destination", destination)
        if direction and not isinstance(direction, str):
            raise TypeError("Expected argument 'direction' to be a str")
        pulumi.set(__self__, "direction", direction)
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
        if source and not isinstance(source, str):
            raise TypeError("Expected argument 'source' to be a str")
        pulumi.set(__self__, "source", source)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def destination(self) -> Optional[str]:
        """
        Destination VM Group.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter
    def direction(self) -> Optional[str]:
        """
        Direction of port mirroring profile.
        """
        return pulumi.get(self, "direction")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Display name of the port mirroring profile.
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
    def source(self) -> Optional[str]:
        """
        Source VM Group.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Port Mirroring Status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWorkloadNetworkPortMirroringResult(GetWorkloadNetworkPortMirroringResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkloadNetworkPortMirroringResult(
            destination=self.destination,
            direction=self.direction,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            revision=self.revision,
            source=self.source,
            status=self.status,
            type=self.type)


def get_workload_network_port_mirroring(port_mirroring_id: Optional[str] = None,
                                        private_cloud_name: Optional[str] = None,
                                        resource_group_name: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkloadNetworkPortMirroringResult:
    """
    Use this data source to access information about an existing resource.

    :param str port_mirroring_id: NSX Port Mirroring identifier. Generally the same as the Port Mirroring display name
    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['portMirroringId'] = port_mirroring_id
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:avs/v20200717preview:getWorkloadNetworkPortMirroring', __args__, opts=opts, typ=GetWorkloadNetworkPortMirroringResult).value

    return AwaitableGetWorkloadNetworkPortMirroringResult(
        destination=__ret__.destination,
        direction=__ret__.direction,
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        revision=__ret__.revision,
        source=__ret__.source,
        status=__ret__.status,
        type=__ret__.type)
