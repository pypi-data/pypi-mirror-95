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
    'GetDataControllerResult',
    'AwaitableGetDataControllerResult',
    'get_data_controller',
]

@pulumi.output_type
class GetDataControllerResult:
    """
    Data controller resource
    """
    def __init__(__self__, id=None, location=None, name=None, on_premise_property=None, system_data=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if on_premise_property and not isinstance(on_premise_property, dict):
            raise TypeError("Expected argument 'on_premise_property' to be a dict")
        pulumi.set(__self__, "on_premise_property", on_premise_property)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="onPremiseProperty")
    def on_premise_property(self) -> 'outputs.OnPremisePropertyResponse':
        """
        Properties from the on premise data controller
        """
        return pulumi.get(self, "on_premise_property")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")


class AwaitableGetDataControllerResult(GetDataControllerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataControllerResult(
            id=self.id,
            location=self.location,
            name=self.name,
            on_premise_property=self.on_premise_property,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_data_controller(data_controller_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataControllerResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_group_name: The name of the Azure resource group
    """
    __args__ = dict()
    __args__['dataControllerName'] = data_controller_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:azuredata/v20190724preview:getDataController', __args__, opts=opts, typ=GetDataControllerResult).value

    return AwaitableGetDataControllerResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        on_premise_property=__ret__.on_premise_property,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)
