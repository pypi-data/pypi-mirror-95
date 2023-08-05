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
    'GetServiceFabricResult',
    'AwaitableGetServiceFabricResult',
    'get_service_fabric',
]

@pulumi.output_type
class GetServiceFabricResult:
    """
    A Service Fabric.
    """
    def __init__(__self__, applicable_schedule=None, environment_id=None, external_service_fabric_id=None, id=None, location=None, name=None, provisioning_state=None, tags=None, type=None, unique_identifier=None):
        if applicable_schedule and not isinstance(applicable_schedule, dict):
            raise TypeError("Expected argument 'applicable_schedule' to be a dict")
        pulumi.set(__self__, "applicable_schedule", applicable_schedule)
        if environment_id and not isinstance(environment_id, str):
            raise TypeError("Expected argument 'environment_id' to be a str")
        pulumi.set(__self__, "environment_id", environment_id)
        if external_service_fabric_id and not isinstance(external_service_fabric_id, str):
            raise TypeError("Expected argument 'external_service_fabric_id' to be a str")
        pulumi.set(__self__, "external_service_fabric_id", external_service_fabric_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unique_identifier and not isinstance(unique_identifier, str):
            raise TypeError("Expected argument 'unique_identifier' to be a str")
        pulumi.set(__self__, "unique_identifier", unique_identifier)

    @property
    @pulumi.getter(name="applicableSchedule")
    def applicable_schedule(self) -> 'outputs.ApplicableScheduleResponse':
        """
        The applicable schedule for the virtual machine.
        """
        return pulumi.get(self, "applicable_schedule")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> Optional[str]:
        """
        The resource id of the environment under which the service fabric resource is present
        """
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter(name="externalServiceFabricId")
    def external_service_fabric_id(self) -> Optional[str]:
        """
        The backing service fabric resource's id
        """
        return pulumi.get(self, "external_service_fabric_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

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

    @property
    @pulumi.getter(name="uniqueIdentifier")
    def unique_identifier(self) -> str:
        """
        The unique immutable identifier of a resource (Guid).
        """
        return pulumi.get(self, "unique_identifier")


class AwaitableGetServiceFabricResult(GetServiceFabricResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceFabricResult(
            applicable_schedule=self.applicable_schedule,
            environment_id=self.environment_id,
            external_service_fabric_id=self.external_service_fabric_id,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type,
            unique_identifier=self.unique_identifier)


def get_service_fabric(expand: Optional[str] = None,
                       lab_name: Optional[str] = None,
                       name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       user_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceFabricResult:
    """
    Use this data source to access information about an existing resource.

    :param str expand: Specify the $expand query. Example: 'properties($expand=applicableSchedule)'
    :param str lab_name: The name of the lab.
    :param str name: The name of the service fabric.
    :param str resource_group_name: The name of the resource group.
    :param str user_name: The name of the user profile.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['userName'] = user_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devtestlab:getServiceFabric', __args__, opts=opts, typ=GetServiceFabricResult).value

    return AwaitableGetServiceFabricResult(
        applicable_schedule=__ret__.applicable_schedule,
        environment_id=__ret__.environment_id,
        external_service_fabric_id=__ret__.external_service_fabric_id,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type,
        unique_identifier=__ret__.unique_identifier)
