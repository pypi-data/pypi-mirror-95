# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetServerAzureADAdministratorResult',
    'AwaitableGetServerAzureADAdministratorResult',
    'get_server_azure_ad_administrator',
]

@pulumi.output_type
class GetServerAzureADAdministratorResult:
    """
    An server Active Directory Administrator.
    """
    def __init__(__self__, administrator_type=None, id=None, login=None, name=None, sid=None, tenant_id=None, type=None):
        if administrator_type and not isinstance(administrator_type, str):
            raise TypeError("Expected argument 'administrator_type' to be a str")
        pulumi.set(__self__, "administrator_type", administrator_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if login and not isinstance(login, str):
            raise TypeError("Expected argument 'login' to be a str")
        pulumi.set(__self__, "login", login)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if sid and not isinstance(sid, str):
            raise TypeError("Expected argument 'sid' to be a str")
        pulumi.set(__self__, "sid", sid)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="administratorType")
    def administrator_type(self) -> str:
        """
        The type of administrator.
        """
        return pulumi.get(self, "administrator_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def login(self) -> str:
        """
        The server administrator login value.
        """
        return pulumi.get(self, "login")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sid(self) -> str:
        """
        The server administrator Sid (Secure ID).
        """
        return pulumi.get(self, "sid")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The server Active Directory Administrator tenant id.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetServerAzureADAdministratorResult(GetServerAzureADAdministratorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerAzureADAdministratorResult(
            administrator_type=self.administrator_type,
            id=self.id,
            login=self.login,
            name=self.name,
            sid=self.sid,
            tenant_id=self.tenant_id,
            type=self.type)


def get_server_azure_ad_administrator(administrator_name: Optional[str] = None,
                                      resource_group_name: Optional[str] = None,
                                      server_name: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServerAzureADAdministratorResult:
    """
    Use this data source to access information about an existing resource.

    :param str administrator_name: Name of the server administrator resource.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    """
    __args__ = dict()
    __args__['administratorName'] = administrator_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:sql/v20140401:getServerAzureADAdministrator', __args__, opts=opts, typ=GetServerAzureADAdministratorResult).value

    return AwaitableGetServerAzureADAdministratorResult(
        administrator_type=__ret__.administrator_type,
        id=__ret__.id,
        login=__ret__.login,
        name=__ret__.name,
        sid=__ret__.sid,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type)
