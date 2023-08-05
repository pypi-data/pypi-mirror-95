# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GetApiVersionSetResult',
    'AwaitableGetApiVersionSetResult',
    'get_api_version_set',
]

@pulumi.output_type
class GetApiVersionSetResult:
    """
    Api Version Set Contract details.
    """
    def __init__(__self__, description=None, display_name=None, id=None, name=None, type=None, version_header_name=None, version_query_name=None, versioning_scheme=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version_header_name and not isinstance(version_header_name, str):
            raise TypeError("Expected argument 'version_header_name' to be a str")
        pulumi.set(__self__, "version_header_name", version_header_name)
        if version_query_name and not isinstance(version_query_name, str):
            raise TypeError("Expected argument 'version_query_name' to be a str")
        pulumi.set(__self__, "version_query_name", version_query_name)
        if versioning_scheme and not isinstance(versioning_scheme, str):
            raise TypeError("Expected argument 'versioning_scheme' to be a str")
        pulumi.set(__self__, "versioning_scheme", versioning_scheme)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of API Version Set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Name of API Version Set
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
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="versionHeaderName")
    def version_header_name(self) -> Optional[str]:
        """
        Name of HTTP header parameter that indicates the API Version if versioningScheme is set to `header`.
        """
        return pulumi.get(self, "version_header_name")

    @property
    @pulumi.getter(name="versionQueryName")
    def version_query_name(self) -> Optional[str]:
        """
        Name of query parameter that indicates the API Version if versioningScheme is set to `query`.
        """
        return pulumi.get(self, "version_query_name")

    @property
    @pulumi.getter(name="versioningScheme")
    def versioning_scheme(self) -> str:
        """
        An value that determines where the API Version identifer will be located in a HTTP request.
        """
        return pulumi.get(self, "versioning_scheme")


class AwaitableGetApiVersionSetResult(GetApiVersionSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApiVersionSetResult(
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            type=self.type,
            version_header_name=self.version_header_name,
            version_query_name=self.version_query_name,
            versioning_scheme=self.versioning_scheme)


def get_api_version_set(resource_group_name: Optional[str] = None,
                        service_name: Optional[str] = None,
                        version_set_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApiVersionSetResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    :param str version_set_id: Api Version Set identifier. Must be unique in the current API Management service instance.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    __args__['versionSetId'] = version_set_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:apimanagement:getApiVersionSet', __args__, opts=opts, typ=GetApiVersionSetResult).value

    return AwaitableGetApiVersionSetResult(
        description=__ret__.description,
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        type=__ret__.type,
        version_header_name=__ret__.version_header_name,
        version_query_name=__ret__.version_query_name,
        versioning_scheme=__ret__.versioning_scheme)
