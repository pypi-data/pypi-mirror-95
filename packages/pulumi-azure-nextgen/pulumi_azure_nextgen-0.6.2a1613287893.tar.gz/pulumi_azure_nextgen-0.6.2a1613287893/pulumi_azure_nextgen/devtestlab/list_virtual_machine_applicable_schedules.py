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
    'ListVirtualMachineApplicableSchedulesResult',
    'AwaitableListVirtualMachineApplicableSchedulesResult',
    'list_virtual_machine_applicable_schedules',
]

@pulumi.output_type
class ListVirtualMachineApplicableSchedulesResult:
    """
    Schedules applicable to a virtual machine. The schedules may have been defined on a VM or on lab level.
    """
    def __init__(__self__, id=None, lab_vms_shutdown=None, lab_vms_startup=None, location=None, name=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lab_vms_shutdown and not isinstance(lab_vms_shutdown, dict):
            raise TypeError("Expected argument 'lab_vms_shutdown' to be a dict")
        pulumi.set(__self__, "lab_vms_shutdown", lab_vms_shutdown)
        if lab_vms_startup and not isinstance(lab_vms_startup, dict):
            raise TypeError("Expected argument 'lab_vms_startup' to be a dict")
        pulumi.set(__self__, "lab_vms_startup", lab_vms_startup)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="labVmsShutdown")
    def lab_vms_shutdown(self) -> Optional['outputs.ScheduleResponse']:
        """
        The auto-shutdown schedule, if one has been set at the lab or lab resource level.
        """
        return pulumi.get(self, "lab_vms_shutdown")

    @property
    @pulumi.getter(name="labVmsStartup")
    def lab_vms_startup(self) -> Optional['outputs.ScheduleResponse']:
        """
        The auto-startup schedule, if one has been set at the lab or lab resource level.
        """
        return pulumi.get(self, "lab_vms_startup")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableListVirtualMachineApplicableSchedulesResult(ListVirtualMachineApplicableSchedulesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListVirtualMachineApplicableSchedulesResult(
            id=self.id,
            lab_vms_shutdown=self.lab_vms_shutdown,
            lab_vms_startup=self.lab_vms_startup,
            location=self.location,
            name=self.name,
            tags=self.tags,
            type=self.type)


def list_virtual_machine_applicable_schedules(lab_name: Optional[str] = None,
                                              name: Optional[str] = None,
                                              resource_group_name: Optional[str] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListVirtualMachineApplicableSchedulesResult:
    """
    Use this data source to access information about an existing resource.

    :param str lab_name: The name of the lab.
    :param str name: The name of the virtual machine.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devtestlab:listVirtualMachineApplicableSchedules', __args__, opts=opts, typ=ListVirtualMachineApplicableSchedulesResult).value

    return AwaitableListVirtualMachineApplicableSchedulesResult(
        id=__ret__.id,
        lab_vms_shutdown=__ret__.lab_vms_shutdown,
        lab_vms_startup=__ret__.lab_vms_startup,
        location=__ret__.location,
        name=__ret__.name,
        tags=__ret__.tags,
        type=__ret__.type)
