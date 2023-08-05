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
    'GetEnvironmentResult',
    'AwaitableGetEnvironmentResult',
    'get_environment',
]

@pulumi.output_type
class GetEnvironmentResult:
    """
    An environment, which is essentially an ARM template deployment.
    """
    def __init__(__self__, arm_template_display_name=None, created_by_user=None, deployment_properties=None, id=None, location=None, name=None, provisioning_state=None, resource_group_id=None, tags=None, type=None, unique_identifier=None):
        if arm_template_display_name and not isinstance(arm_template_display_name, str):
            raise TypeError("Expected argument 'arm_template_display_name' to be a str")
        pulumi.set(__self__, "arm_template_display_name", arm_template_display_name)
        if created_by_user and not isinstance(created_by_user, str):
            raise TypeError("Expected argument 'created_by_user' to be a str")
        pulumi.set(__self__, "created_by_user", created_by_user)
        if deployment_properties and not isinstance(deployment_properties, dict):
            raise TypeError("Expected argument 'deployment_properties' to be a dict")
        pulumi.set(__self__, "deployment_properties", deployment_properties)
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
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
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
    @pulumi.getter(name="armTemplateDisplayName")
    def arm_template_display_name(self) -> Optional[str]:
        """
        The display name of the Azure Resource Manager template that produced the environment.
        """
        return pulumi.get(self, "arm_template_display_name")

    @property
    @pulumi.getter(name="createdByUser")
    def created_by_user(self) -> str:
        """
        The creator of the environment.
        """
        return pulumi.get(self, "created_by_user")

    @property
    @pulumi.getter(name="deploymentProperties")
    def deployment_properties(self) -> Optional['outputs.EnvironmentDeploymentPropertiesResponse']:
        """
        The deployment properties of the environment.
        """
        return pulumi.get(self, "deployment_properties")

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
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> str:
        """
        The identifier of the resource group containing the environment's resources.
        """
        return pulumi.get(self, "resource_group_id")

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


class AwaitableGetEnvironmentResult(GetEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEnvironmentResult(
            arm_template_display_name=self.arm_template_display_name,
            created_by_user=self.created_by_user,
            deployment_properties=self.deployment_properties,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            resource_group_id=self.resource_group_id,
            tags=self.tags,
            type=self.type,
            unique_identifier=self.unique_identifier)


def get_environment(expand: Optional[str] = None,
                    lab_name: Optional[str] = None,
                    name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    user_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEnvironmentResult:
    """
    Use this data source to access information about an existing resource.

    :param str expand: Specify the $expand query. Example: 'properties($select=deploymentProperties)'
    :param str lab_name: The name of the lab.
    :param str name: The name of the environment.
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
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devtestlab/latest:getEnvironment', __args__, opts=opts, typ=GetEnvironmentResult).value

    return AwaitableGetEnvironmentResult(
        arm_template_display_name=__ret__.arm_template_display_name,
        created_by_user=__ret__.created_by_user,
        deployment_properties=__ret__.deployment_properties,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        resource_group_id=__ret__.resource_group_id,
        tags=__ret__.tags,
        type=__ret__.type,
        unique_identifier=__ret__.unique_identifier)
