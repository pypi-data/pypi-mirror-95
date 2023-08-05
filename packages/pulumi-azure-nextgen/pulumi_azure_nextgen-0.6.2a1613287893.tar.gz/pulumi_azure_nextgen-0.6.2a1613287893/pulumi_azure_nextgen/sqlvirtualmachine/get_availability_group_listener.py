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
    'GetAvailabilityGroupListenerResult',
    'AwaitableGetAvailabilityGroupListenerResult',
    'get_availability_group_listener',
]

@pulumi.output_type
class GetAvailabilityGroupListenerResult:
    """
    A SQL Server availability group listener.
    """
    def __init__(__self__, availability_group_name=None, create_default_availability_group_if_not_exist=None, id=None, load_balancer_configurations=None, name=None, port=None, provisioning_state=None, type=None):
        if availability_group_name and not isinstance(availability_group_name, str):
            raise TypeError("Expected argument 'availability_group_name' to be a str")
        pulumi.set(__self__, "availability_group_name", availability_group_name)
        if create_default_availability_group_if_not_exist and not isinstance(create_default_availability_group_if_not_exist, bool):
            raise TypeError("Expected argument 'create_default_availability_group_if_not_exist' to be a bool")
        pulumi.set(__self__, "create_default_availability_group_if_not_exist", create_default_availability_group_if_not_exist)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if load_balancer_configurations and not isinstance(load_balancer_configurations, list):
            raise TypeError("Expected argument 'load_balancer_configurations' to be a list")
        pulumi.set(__self__, "load_balancer_configurations", load_balancer_configurations)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="availabilityGroupName")
    def availability_group_name(self) -> Optional[str]:
        """
        Name of the availability group.
        """
        return pulumi.get(self, "availability_group_name")

    @property
    @pulumi.getter(name="createDefaultAvailabilityGroupIfNotExist")
    def create_default_availability_group_if_not_exist(self) -> Optional[bool]:
        """
        Create a default availability group if it does not exist.
        """
        return pulumi.get(self, "create_default_availability_group_if_not_exist")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="loadBalancerConfigurations")
    def load_balancer_configurations(self) -> Optional[Sequence['outputs.LoadBalancerConfigurationResponse']]:
        """
        List of load balancer configurations for an availability group listener.
        """
        return pulumi.get(self, "load_balancer_configurations")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        """
        Listener port.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state to track the async operation status.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetAvailabilityGroupListenerResult(GetAvailabilityGroupListenerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAvailabilityGroupListenerResult(
            availability_group_name=self.availability_group_name,
            create_default_availability_group_if_not_exist=self.create_default_availability_group_if_not_exist,
            id=self.id,
            load_balancer_configurations=self.load_balancer_configurations,
            name=self.name,
            port=self.port,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_availability_group_listener(availability_group_listener_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    sql_virtual_machine_group_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAvailabilityGroupListenerResult:
    """
    Use this data source to access information about an existing resource.

    :param str availability_group_listener_name: Name of the availability group listener.
    :param str resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str sql_virtual_machine_group_name: Name of the SQL virtual machine group.
    """
    __args__ = dict()
    __args__['availabilityGroupListenerName'] = availability_group_listener_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlVirtualMachineGroupName'] = sql_virtual_machine_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:sqlvirtualmachine:getAvailabilityGroupListener', __args__, opts=opts, typ=GetAvailabilityGroupListenerResult).value

    return AwaitableGetAvailabilityGroupListenerResult(
        availability_group_name=__ret__.availability_group_name,
        create_default_availability_group_if_not_exist=__ret__.create_default_availability_group_if_not_exist,
        id=__ret__.id,
        load_balancer_configurations=__ret__.load_balancer_configurations,
        name=__ret__.name,
        port=__ret__.port,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)
