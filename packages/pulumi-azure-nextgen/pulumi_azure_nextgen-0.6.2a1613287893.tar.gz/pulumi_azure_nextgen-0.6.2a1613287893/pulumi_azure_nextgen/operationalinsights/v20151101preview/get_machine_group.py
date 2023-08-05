# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'GetMachineGroupResult',
    'AwaitableGetMachineGroupResult',
    'get_machine_group',
]

@pulumi.output_type
class GetMachineGroupResult:
    """
    A user-defined logical grouping of machines.
    """
    def __init__(__self__, count=None, display_name=None, etag=None, group_type=None, id=None, kind=None, machines=None, name=None, type=None):
        if count and not isinstance(count, int):
            raise TypeError("Expected argument 'count' to be a int")
        pulumi.set(__self__, "count", count)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if group_type and not isinstance(group_type, str):
            raise TypeError("Expected argument 'group_type' to be a str")
        pulumi.set(__self__, "group_type", group_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if machines and not isinstance(machines, list):
            raise TypeError("Expected argument 'machines' to be a list")
        pulumi.set(__self__, "machines", machines)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def count(self) -> Optional[int]:
        """
        Count of machines in this group. The value of count may be bigger than the number of machines in case of the group has been truncated due to exceeding the max number of machines a group can handle.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        User defined name for the group
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Resource ETAG.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="groupType")
    def group_type(self) -> Optional[str]:
        """
        Type of the machine group
        """
        return pulumi.get(self, "group_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Additional resource type qualifier.
        Expected value is 'machineGroup'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def machines(self) -> Optional[Sequence['outputs.MachineReferenceWithHintsResponse']]:
        """
        References of the machines in this group. The hints within each reference do not represent the current value of the corresponding fields. They are a snapshot created during the last time the machine group was updated.
        """
        return pulumi.get(self, "machines")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetMachineGroupResult(GetMachineGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMachineGroupResult(
            count=self.count,
            display_name=self.display_name,
            etag=self.etag,
            group_type=self.group_type,
            id=self.id,
            kind=self.kind,
            machines=self.machines,
            name=self.name,
            type=self.type)


def get_machine_group(end_time: Optional[str] = None,
                      machine_group_name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      start_time: Optional[str] = None,
                      workspace_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMachineGroupResult:
    """
    Use this data source to access information about an existing resource.

    :param str end_time: UTC date and time specifying the end time of an interval. When not specified the service uses DateTime.UtcNow
    :param str machine_group_name: Machine Group resource name.
    :param str resource_group_name: Resource group name within the specified subscriptionId.
    :param str start_time: UTC date and time specifying the start time of an interval. When not specified the service uses DateTime.UtcNow - 10m
    :param str workspace_name: OMS workspace containing the resources of interest.
    """
    __args__ = dict()
    __args__['endTime'] = end_time
    __args__['machineGroupName'] = machine_group_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['startTime'] = start_time
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:operationalinsights/v20151101preview:getMachineGroup', __args__, opts=opts, typ=GetMachineGroupResult).value

    return AwaitableGetMachineGroupResult(
        count=__ret__.count,
        display_name=__ret__.display_name,
        etag=__ret__.etag,
        group_type=__ret__.group_type,
        id=__ret__.id,
        kind=__ret__.kind,
        machines=__ret__.machines,
        name=__ret__.name,
        type=__ret__.type)
