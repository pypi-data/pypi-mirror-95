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
    'GetConfigurationAssignmentResult',
    'AwaitableGetConfigurationAssignmentResult',
    'get_configuration_assignment',
]

@pulumi.output_type
class GetConfigurationAssignmentResult:
    """
    Configuration Assignment
    """
    def __init__(__self__, id=None, location=None, maintenance_configuration_id=None, name=None, resource_id=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maintenance_configuration_id and not isinstance(maintenance_configuration_id, str):
            raise TypeError("Expected argument 'maintenance_configuration_id' to be a str")
        pulumi.set(__self__, "maintenance_configuration_id", maintenance_configuration_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified identifier of the resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Location of the resource
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> Optional[str]:
        """
        The maintenance configuration Id
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The unique resourceId
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")


class AwaitableGetConfigurationAssignmentResult(GetConfigurationAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationAssignmentResult(
            id=self.id,
            location=self.location,
            maintenance_configuration_id=self.maintenance_configuration_id,
            name=self.name,
            resource_id=self.resource_id,
            system_data=self.system_data,
            type=self.type)


def get_configuration_assignment(configuration_assignment_name: Optional[str] = None,
                                 provider_name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 resource_name: Optional[str] = None,
                                 resource_type: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationAssignmentResult:
    """
    Use this data source to access information about an existing resource.

    :param str configuration_assignment_name: Configuration assignment name
    :param str provider_name: Resource provider name
    :param str resource_group_name: Resource group name
    :param str resource_name: Resource identifier
    :param str resource_type: Resource type
    """
    __args__ = dict()
    __args__['configurationAssignmentName'] = configuration_assignment_name
    __args__['providerName'] = provider_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    __args__['resourceType'] = resource_type
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:maintenance/v20210401preview:getConfigurationAssignment', __args__, opts=opts, typ=GetConfigurationAssignmentResult).value

    return AwaitableGetConfigurationAssignmentResult(
        id=__ret__.id,
        location=__ret__.location,
        maintenance_configuration_id=__ret__.maintenance_configuration_id,
        name=__ret__.name,
        resource_id=__ret__.resource_id,
        system_data=__ret__.system_data,
        type=__ret__.type)
