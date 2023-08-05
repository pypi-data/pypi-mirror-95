# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ListTenantAccessSecretsResult',
    'AwaitableListTenantAccessSecretsResult',
    'list_tenant_access_secrets',
]

@pulumi.output_type
class ListTenantAccessSecretsResult:
    """
    Tenant access information contract of the API Management service.
    """
    def __init__(__self__, enabled=None, id=None, primary_key=None, secondary_key=None):
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Determines whether direct access is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> Optional[str]:
        """
        Primary access key. This property will not be filled on 'GET' operations! Use '/listSecrets' POST request to get the value.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> Optional[str]:
        """
        Secondary access key. This property will not be filled on 'GET' operations! Use '/listSecrets' POST request to get the value.
        """
        return pulumi.get(self, "secondary_key")


class AwaitableListTenantAccessSecretsResult(ListTenantAccessSecretsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListTenantAccessSecretsResult(
            enabled=self.enabled,
            id=self.id,
            primary_key=self.primary_key,
            secondary_key=self.secondary_key)


def list_tenant_access_secrets(access_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               service_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListTenantAccessSecretsResult:
    """
    Use this data source to access information about an existing resource.

    :param str access_name: The identifier of the Access configuration.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['accessName'] = access_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:apimanagement/latest:listTenantAccessSecrets', __args__, opts=opts, typ=ListTenantAccessSecretsResult).value

    return AwaitableListTenantAccessSecretsResult(
        enabled=__ret__.enabled,
        id=__ret__.id,
        primary_key=__ret__.primary_key,
        secondary_key=__ret__.secondary_key)
