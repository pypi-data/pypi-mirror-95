# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GetAuthorizationResult',
    'AwaitableGetAuthorizationResult',
    'get_authorization',
]

@pulumi.output_type
class GetAuthorizationResult:
    """
    ExpressRoute Circuit Authorization
    """
    def __init__(__self__, express_route_authorization_id=None, express_route_authorization_key=None, id=None, name=None, provisioning_state=None, type=None):
        if express_route_authorization_id and not isinstance(express_route_authorization_id, str):
            raise TypeError("Expected argument 'express_route_authorization_id' to be a str")
        pulumi.set(__self__, "express_route_authorization_id", express_route_authorization_id)
        if express_route_authorization_key and not isinstance(express_route_authorization_key, str):
            raise TypeError("Expected argument 'express_route_authorization_key' to be a str")
        pulumi.set(__self__, "express_route_authorization_key", express_route_authorization_key)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="expressRouteAuthorizationId")
    def express_route_authorization_id(self) -> str:
        """
        The ID of the ExpressRoute Circuit Authorization
        """
        return pulumi.get(self, "express_route_authorization_id")

    @property
    @pulumi.getter(name="expressRouteAuthorizationKey")
    def express_route_authorization_key(self) -> str:
        """
        The key of the ExpressRoute Circuit Authorization
        """
        return pulumi.get(self, "express_route_authorization_key")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The state of the  ExpressRoute Circuit Authorization provisioning
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetAuthorizationResult(GetAuthorizationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuthorizationResult(
            express_route_authorization_id=self.express_route_authorization_id,
            express_route_authorization_key=self.express_route_authorization_key,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_authorization(authorization_name: Optional[str] = None,
                      private_cloud_name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAuthorizationResult:
    """
    Use this data source to access information about an existing resource.

    :param str authorization_name: Name of the ExpressRoute Circuit Authorization in the private cloud
    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['authorizationName'] = authorization_name
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:avs:getAuthorization', __args__, opts=opts, typ=GetAuthorizationResult).value

    return AwaitableGetAuthorizationResult(
        express_route_authorization_id=__ret__.express_route_authorization_id,
        express_route_authorization_key=__ret__.express_route_authorization_key,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)
