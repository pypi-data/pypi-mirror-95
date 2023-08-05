# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GetCacheResult',
    'AwaitableGetCacheResult',
    'get_cache',
]

@pulumi.output_type
class GetCacheResult:
    """
    Cache details.
    """
    def __init__(__self__, connection_string=None, description=None, id=None, name=None, resource_id=None, type=None):
        if connection_string and not isinstance(connection_string, str):
            raise TypeError("Expected argument 'connection_string' to be a str")
        pulumi.set(__self__, "connection_string", connection_string)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> str:
        """
        Runtime connection string to cache
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Cache description
        """
        return pulumi.get(self, "description")

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
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        Original uri of entity in external system cache points to
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetCacheResult(GetCacheResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCacheResult(
            connection_string=self.connection_string,
            description=self.description,
            id=self.id,
            name=self.name,
            resource_id=self.resource_id,
            type=self.type)


def get_cache(cache_id: Optional[str] = None,
              resource_group_name: Optional[str] = None,
              service_name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCacheResult:
    """
    Use this data source to access information about an existing resource.

    :param str cache_id: Identifier of the Cache entity. Cache identifier (should be either 'default' or valid Azure region identifier).
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['cacheId'] = cache_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:apimanagement:getCache', __args__, opts=opts, typ=GetCacheResult).value

    return AwaitableGetCacheResult(
        connection_string=__ret__.connection_string,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        resource_id=__ret__.resource_id,
        type=__ret__.type)
