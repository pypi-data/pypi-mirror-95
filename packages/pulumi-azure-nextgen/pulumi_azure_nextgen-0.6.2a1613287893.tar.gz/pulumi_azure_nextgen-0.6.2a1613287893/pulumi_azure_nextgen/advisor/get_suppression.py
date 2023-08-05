# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = [
    'GetSuppressionResult',
    'AwaitableGetSuppressionResult',
    'get_suppression',
]

@pulumi.output_type
class GetSuppressionResult:
    """
    The details of the snoozed or dismissed rule; for example, the duration, name, and GUID associated with the rule.
    """
    def __init__(__self__, expiration_time_stamp=None, id=None, name=None, suppression_id=None, ttl=None, type=None):
        if expiration_time_stamp and not isinstance(expiration_time_stamp, str):
            raise TypeError("Expected argument 'expiration_time_stamp' to be a str")
        pulumi.set(__self__, "expiration_time_stamp", expiration_time_stamp)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if suppression_id and not isinstance(suppression_id, str):
            raise TypeError("Expected argument 'suppression_id' to be a str")
        pulumi.set(__self__, "suppression_id", suppression_id)
        if ttl and not isinstance(ttl, str):
            raise TypeError("Expected argument 'ttl' to be a str")
        pulumi.set(__self__, "ttl", ttl)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="expirationTimeStamp")
    def expiration_time_stamp(self) -> str:
        """
        Gets or sets the expiration time stamp.
        """
        return pulumi.get(self, "expiration_time_stamp")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="suppressionId")
    def suppression_id(self) -> Optional[str]:
        """
        The GUID of the suppression.
        """
        return pulumi.get(self, "suppression_id")

    @property
    @pulumi.getter
    def ttl(self) -> Optional[str]:
        """
        The duration for which the suppression is valid.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetSuppressionResult(GetSuppressionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSuppressionResult(
            expiration_time_stamp=self.expiration_time_stamp,
            id=self.id,
            name=self.name,
            suppression_id=self.suppression_id,
            ttl=self.ttl,
            type=self.type)


def get_suppression(name: Optional[str] = None,
                    recommendation_id: Optional[str] = None,
                    resource_uri: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSuppressionResult:
    """
    Use this data source to access information about an existing resource.

    :param str name: The name of the suppression.
    :param str recommendation_id: The recommendation ID.
    :param str resource_uri: The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['recommendationId'] = recommendation_id
    __args__['resourceUri'] = resource_uri
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:advisor:getSuppression', __args__, opts=opts, typ=GetSuppressionResult).value

    return AwaitableGetSuppressionResult(
        expiration_time_stamp=__ret__.expiration_time_stamp,
        id=__ret__.id,
        name=__ret__.name,
        suppression_id=__ret__.suppression_id,
        ttl=__ret__.ttl,
        type=__ret__.type)
