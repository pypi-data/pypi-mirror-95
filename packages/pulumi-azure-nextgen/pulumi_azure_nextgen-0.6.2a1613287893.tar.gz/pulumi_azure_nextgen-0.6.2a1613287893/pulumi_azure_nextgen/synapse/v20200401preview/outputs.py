# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'SkuResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class SkuResponse(dict):
    """
    An ARM Resource SKU.
    """
    def __init__(__self__, *,
                 name: str,
                 tier: Optional[str] = None):
        """
        An ARM Resource SKU.
        :param str name: The name of the SKU, typically, a letter + Number code, e.g. P3.
        :param str tier: The tier or edition of the particular SKU, e.g. Basic, Premium.
        """
        pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU, typically, a letter + Number code, e.g. P3.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        The tier or edition of the particular SKU, e.g. Basic, Premium.
        """
        return pulumi.get(self, "tier")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SystemDataResponse(dict):
    """
    ARM System Data.
    """
    def __init__(__self__, *,
                 created_at: str,
                 created_by: str,
                 created_by_type: str,
                 last_modified_at: str,
                 last_modified_by: str,
                 last_modified_by_type: str):
        """
        ARM System Data.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: A string identifier for the identity that created the resource.
        :param str created_by_type: The type of identity that created the resource: <User|Application|ManagedIdentity|Key>
        :param str last_modified_at: The timestamp of last modification (UTC).
        :param str last_modified_by: A string identifier for the identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource: <User|Application|ManagedIdentity|Key>
        """
        pulumi.set(__self__, "created_at", created_at)
        pulumi.set(__self__, "created_by", created_by)
        pulumi.set(__self__, "created_by_type", created_by_type)
        pulumi.set(__self__, "last_modified_at", last_modified_at)
        pulumi.set(__self__, "last_modified_by", last_modified_by)
        pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> str:
        """
        A string identifier for the identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> str:
        """
        The type of identity that created the resource: <User|Application|ManagedIdentity|Key>
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> str:
        """
        The timestamp of last modification (UTC).
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> str:
        """
        A string identifier for the identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> str:
        """
        The type of identity that last modified the resource: <User|Application|ManagedIdentity|Key>
        """
        return pulumi.get(self, "last_modified_by_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


