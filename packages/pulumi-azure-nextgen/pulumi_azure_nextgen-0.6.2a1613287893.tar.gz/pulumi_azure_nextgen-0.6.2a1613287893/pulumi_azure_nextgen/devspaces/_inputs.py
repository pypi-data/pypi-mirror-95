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
    'SkuArgs',
]

@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'SkuName']],
                 tier: Optional[pulumi.Input[Union[str, 'SkuTier']]] = None):
        """
        Model representing SKU for Azure Dev Spaces Controller.
        :param pulumi.Input[Union[str, 'SkuName']] name: The name of the SKU for Azure Dev Spaces Controller.
        :param pulumi.Input[Union[str, 'SkuTier']] tier: The tier of the SKU for Azure Dev Spaces Controller.
        """
        pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        The name of the SKU for Azure Dev Spaces Controller.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[Union[str, 'SkuTier']]]:
        """
        The tier of the SKU for Azure Dev Spaces Controller.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[Union[str, 'SkuTier']]]):
        pulumi.set(self, "tier", value)


