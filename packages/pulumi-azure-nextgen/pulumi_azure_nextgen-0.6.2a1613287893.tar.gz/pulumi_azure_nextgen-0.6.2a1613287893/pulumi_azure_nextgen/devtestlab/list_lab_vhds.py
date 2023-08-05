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
    'ListLabVhdsResult',
    'AwaitableListLabVhdsResult',
    'list_lab_vhds',
]

@pulumi.output_type
class ListLabVhdsResult:
    """
    The response of a list operation.
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
    def next_link(self) -> Optional[str]:
        """
        Link for next set of results.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.LabVhdResponseResult']]:
        """
        Results of the list operation.
        """
        return pulumi.get(self, "value")


class AwaitableListLabVhdsResult(ListLabVhdsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListLabVhdsResult(
            next_link=self.next_link,
            value=self.value)


def list_lab_vhds(name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListLabVhdsResult:
    """
    Use this data source to access information about an existing resource.

    :param str name: The name of the lab.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devtestlab:listLabVhds', __args__, opts=opts, typ=ListLabVhdsResult).value

    return AwaitableListLabVhdsResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
