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
    'GetEntityResult',
    'AwaitableGetEntityResult',
    'get_entity',
]

@pulumi.output_type
class GetEntityResult:
    """
    Describes the result of the request to view entities.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> str:
        """
        The URL to use for getting the next set of results.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.EntityInfoResponseResult']]:
        """
        The list of entities.
        """
        return pulumi.get(self, "value")


class AwaitableGetEntityResult(GetEntityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEntityResult(
            next_link=self.next_link,
            value=self.value)


def get_entity(group_name: Optional[str] = None,
               skiptoken: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEntityResult:
    """
    Use this data source to access information about an existing resource.

    :param str group_name: A filter which allows the call to be filtered for a specific group.
    :param str skiptoken: Page continuation token is only used if a previous operation returned a partial result. 
           If a previous response contains a nextLink element, the value of the nextLink element will include a token parameter that specifies a starting point to use for subsequent calls.
    """
    __args__ = dict()
    __args__['groupName'] = group_name
    __args__['skiptoken'] = skiptoken
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:management/v20180101preview:getEntity', __args__, opts=opts, typ=GetEntityResult).value

    return AwaitableGetEntityResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
