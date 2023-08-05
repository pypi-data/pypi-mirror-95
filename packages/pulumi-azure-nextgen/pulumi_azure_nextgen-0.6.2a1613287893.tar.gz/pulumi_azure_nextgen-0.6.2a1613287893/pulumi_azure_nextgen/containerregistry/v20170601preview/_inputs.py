# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = [
    'SkuArgs',
    'StorageAccountPropertiesArgs',
]

@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'SkuName']]):
        """
        The SKU of a container registry.
        :param pulumi.Input[Union[str, 'SkuName']] name: The SKU name of the container registry. Required for registry creation.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        The SKU name of the container registry. Required for registry creation.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class StorageAccountPropertiesArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str]):
        """
        The properties of a storage account for a container registry. Only applicable to Basic SKU.
        :param pulumi.Input[str] id: The resource ID of the storage account.
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        The resource ID of the storage account.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)


