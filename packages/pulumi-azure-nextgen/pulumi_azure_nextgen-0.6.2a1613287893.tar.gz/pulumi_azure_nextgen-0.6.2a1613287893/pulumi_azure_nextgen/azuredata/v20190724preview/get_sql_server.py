# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetSqlServerResult',
    'AwaitableGetSqlServerResult',
    'get_sql_server',
]

@pulumi.output_type
class GetSqlServerResult:
    """
    A SQL server.
    """
    def __init__(__self__, cores=None, edition=None, id=None, name=None, property_bag=None, registration_id=None, type=None, version=None):
        if cores and not isinstance(cores, int):
            raise TypeError("Expected argument 'cores' to be a int")
        pulumi.set(__self__, "cores", cores)
        if edition and not isinstance(edition, str):
            raise TypeError("Expected argument 'edition' to be a str")
        pulumi.set(__self__, "edition", edition)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if property_bag and not isinstance(property_bag, str):
            raise TypeError("Expected argument 'property_bag' to be a str")
        pulumi.set(__self__, "property_bag", property_bag)
        if registration_id and not isinstance(registration_id, str):
            raise TypeError("Expected argument 'registration_id' to be a str")
        pulumi.set(__self__, "registration_id", registration_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def cores(self) -> Optional[int]:
        """
        Cores of the Sql Server.
        """
        return pulumi.get(self, "cores")

    @property
    @pulumi.getter
    def edition(self) -> Optional[str]:
        """
        Sql Server Edition.
        """
        return pulumi.get(self, "edition")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="propertyBag")
    def property_bag(self) -> Optional[str]:
        """
        Sql Server Json Property Bag.
        """
        return pulumi.get(self, "property_bag")

    @property
    @pulumi.getter(name="registrationID")
    def registration_id(self) -> Optional[str]:
        """
        ID for Parent Sql Server Registration.
        """
        return pulumi.get(self, "registration_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Version of the Sql Server.
        """
        return pulumi.get(self, "version")


class AwaitableGetSqlServerResult(GetSqlServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlServerResult(
            cores=self.cores,
            edition=self.edition,
            id=self.id,
            name=self.name,
            property_bag=self.property_bag,
            registration_id=self.registration_id,
            type=self.type,
            version=self.version)


def get_sql_server(expand: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   sql_server_name: Optional[str] = None,
                   sql_server_registration_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlServerResult:
    """
    Use this data source to access information about an existing resource.

    :param str expand: The child resources to include in the response.
    :param str resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str sql_server_name: Name of the SQL Server.
    :param str sql_server_registration_name: Name of the SQL Server registration.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlServerName'] = sql_server_name
    __args__['sqlServerRegistrationName'] = sql_server_registration_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:azuredata/v20190724preview:getSqlServer', __args__, opts=opts, typ=GetSqlServerResult).value

    return AwaitableGetSqlServerResult(
        cores=__ret__.cores,
        edition=__ret__.edition,
        id=__ret__.id,
        name=__ret__.name,
        property_bag=__ret__.property_bag,
        registration_id=__ret__.registration_id,
        type=__ret__.type,
        version=__ret__.version)
