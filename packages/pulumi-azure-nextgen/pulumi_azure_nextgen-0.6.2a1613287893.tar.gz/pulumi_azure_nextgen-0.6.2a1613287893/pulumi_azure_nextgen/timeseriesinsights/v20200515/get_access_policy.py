# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetAccessPolicyResult',
    'AwaitableGetAccessPolicyResult',
    'get_access_policy',
]

@pulumi.output_type
class GetAccessPolicyResult:
    """
    An access policy is used to grant users and applications access to the environment. Roles are assigned to service principals in Azure Active Directory. These roles define the actions the principal can perform through the Time Series Insights data plane APIs.
    """
    def __init__(__self__, description=None, id=None, name=None, principal_object_id=None, roles=None, type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if principal_object_id and not isinstance(principal_object_id, str):
            raise TypeError("Expected argument 'principal_object_id' to be a str")
        pulumi.set(__self__, "principal_object_id", principal_object_id)
        if roles and not isinstance(roles, list):
            raise TypeError("Expected argument 'roles' to be a list")
        pulumi.set(__self__, "roles", roles)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An description of the access policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalObjectId")
    def principal_object_id(self) -> Optional[str]:
        """
        The objectId of the principal in Azure Active Directory.
        """
        return pulumi.get(self, "principal_object_id")

    @property
    @pulumi.getter
    def roles(self) -> Optional[Sequence[str]]:
        """
        The list of roles the principal is assigned on the environment.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetAccessPolicyResult(GetAccessPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessPolicyResult(
            description=self.description,
            id=self.id,
            name=self.name,
            principal_object_id=self.principal_object_id,
            roles=self.roles,
            type=self.type)


def get_access_policy(access_policy_name: Optional[str] = None,
                      environment_name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessPolicyResult:
    """
    Use this data source to access information about an existing resource.

    :param str access_policy_name: The name of the Time Series Insights access policy associated with the specified environment.
    :param str environment_name: The name of the Time Series Insights environment associated with the specified resource group.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['accessPolicyName'] = access_policy_name
    __args__['environmentName'] = environment_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:timeseriesinsights/v20200515:getAccessPolicy', __args__, opts=opts, typ=GetAccessPolicyResult).value

    return AwaitableGetAccessPolicyResult(
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        principal_object_id=__ret__.principal_object_id,
        roles=__ret__.roles,
        type=__ret__.type)
