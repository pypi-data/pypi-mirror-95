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
    'ListWebAppMetadataSlotResult',
    'AwaitableListWebAppMetadataSlotResult',
    'list_web_app_metadata_slot',
]

@pulumi.output_type
class ListWebAppMetadataSlotResult:
    """
    String dictionary resource.
    """
    def __init__(__self__, id=None, kind=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> Mapping[str, str]:
        """
        Settings.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableListWebAppMetadataSlotResult(ListWebAppMetadataSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppMetadataSlotResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def list_web_app_metadata_slot(name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               slot: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppMetadataSlotResult:
    """
    Use this data source to access information about an existing resource.

    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get the metadata for the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:web/latest:listWebAppMetadataSlot', __args__, opts=opts, typ=ListWebAppMetadataSlotResult).value

    return AwaitableListWebAppMetadataSlotResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)
