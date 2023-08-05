# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'SkuResponse',
]

@pulumi.output_type
class SkuResponse(dict):
    """
    The SKU to be applied for this resource
    """
    def __init__(__self__, *,
                 name: Optional[str] = None):
        """
        The SKU to be applied for this resource
        :param str name: Name of the SKU to be applied
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the SKU to be applied
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


