# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from ._enums import *

__all__ = [
    'IoTSpacesPropertiesArgs',
    'IoTSpacesSkuInfoArgs',
    'StorageContainerPropertiesArgs',
]

@pulumi.input_type
class IoTSpacesPropertiesArgs:
    def __init__(__self__, *,
                 storage_container: Optional[pulumi.Input['StorageContainerPropertiesArgs']] = None):
        """
        The properties of an IoTSpaces instance.
        :param pulumi.Input['StorageContainerPropertiesArgs'] storage_container: The properties of the designated storage container.
        """
        if storage_container is not None:
            pulumi.set(__self__, "storage_container", storage_container)

    @property
    @pulumi.getter(name="storageContainer")
    def storage_container(self) -> Optional[pulumi.Input['StorageContainerPropertiesArgs']]:
        """
        The properties of the designated storage container.
        """
        return pulumi.get(self, "storage_container")

    @storage_container.setter
    def storage_container(self, value: Optional[pulumi.Input['StorageContainerPropertiesArgs']]):
        pulumi.set(self, "storage_container", value)


@pulumi.input_type
class IoTSpacesSkuInfoArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'IoTSpacesSku']]):
        """
        Information about the SKU of the IoTSpaces instance.
        :param pulumi.Input[Union[str, 'IoTSpacesSku']] name: The name of the SKU.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'IoTSpacesSku']]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'IoTSpacesSku']]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class StorageContainerPropertiesArgs:
    def __init__(__self__, *,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None):
        """
        The properties of the Azure Storage Container for file archive.
        :param pulumi.Input[str] connection_string: The connection string of the storage account.
        :param pulumi.Input[str] container_name: The name of storage container in the storage account.
        :param pulumi.Input[str] resource_group: The name of the resource group of the storage account.
        :param pulumi.Input[str] subscription_id: The subscription identifier of the storage account.
        """
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)
        if container_name is not None:
            pulumi.set(__self__, "container_name", container_name)
        if resource_group is not None:
            pulumi.set(__self__, "resource_group", resource_group)
        if subscription_id is not None:
            pulumi.set(__self__, "subscription_id", subscription_id)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        The connection string of the storage account.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_string", value)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of storage container in the storage account.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group of the storage account.
        """
        return pulumi.get(self, "resource_group")

    @resource_group.setter
    def resource_group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group", value)

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> Optional[pulumi.Input[str]]:
        """
        The subscription identifier of the storage account.
        """
        return pulumi.get(self, "subscription_id")

    @subscription_id.setter
    def subscription_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_id", value)


