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
    'GetConnectionResult',
    'AwaitableGetConnectionResult',
    'get_connection',
]

@pulumi.output_type
class GetConnectionResult:
    """
    Definition of the connection.
    """
    def __init__(__self__, connection_type=None, creation_time=None, description=None, field_definition_values=None, id=None, last_modified_time=None, name=None, type=None):
        if connection_type and not isinstance(connection_type, dict):
            raise TypeError("Expected argument 'connection_type' to be a dict")
        pulumi.set(__self__, "connection_type", connection_type)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if field_definition_values and not isinstance(field_definition_values, dict):
            raise TypeError("Expected argument 'field_definition_values' to be a dict")
        pulumi.set(__self__, "field_definition_values", field_definition_values)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> Optional['outputs.ConnectionTypeAssociationPropertyResponse']:
        """
        Gets or sets the connectionType of the connection.
        """
        return pulumi.get(self, "connection_type")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Gets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fieldDefinitionValues")
    def field_definition_values(self) -> Mapping[str, str]:
        """
        Gets the field definition values of the connection.
        """
        return pulumi.get(self, "field_definition_values")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> str:
        """
        Gets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetConnectionResult(GetConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectionResult(
            connection_type=self.connection_type,
            creation_time=self.creation_time,
            description=self.description,
            field_definition_values=self.field_definition_values,
            id=self.id,
            last_modified_time=self.last_modified_time,
            name=self.name,
            type=self.type)


def get_connection(automation_account_name: Optional[str] = None,
                   connection_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectionResult:
    """
    Use this data source to access information about an existing resource.

    :param str automation_account_name: The name of the automation account.
    :param str connection_name: The name of connection.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['automationAccountName'] = automation_account_name
    __args__['connectionName'] = connection_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:automation:getConnection', __args__, opts=opts, typ=GetConnectionResult).value

    return AwaitableGetConnectionResult(
        connection_type=__ret__.connection_type,
        creation_time=__ret__.creation_time,
        description=__ret__.description,
        field_definition_values=__ret__.field_definition_values,
        id=__ret__.id,
        last_modified_time=__ret__.last_modified_time,
        name=__ret__.name,
        type=__ret__.type)
