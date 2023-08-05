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
    'ListSiteIdentifiersAssignedToHostNameResult',
    'AwaitableListSiteIdentifiersAssignedToHostNameResult',
    'list_site_identifiers_assigned_to_host_name',
]

@pulumi.output_type
class ListSiteIdentifiersAssignedToHostNameResult:
    """
    Collection of identifiers.
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
        Link to next page of resources.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.IdentifierResponseResult']:
        """
        Collection of resources.
        """
        return pulumi.get(self, "value")


class AwaitableListSiteIdentifiersAssignedToHostNameResult(ListSiteIdentifiersAssignedToHostNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListSiteIdentifiersAssignedToHostNameResult(
            next_link=self.next_link,
            value=self.value)


def list_site_identifiers_assigned_to_host_name(name: Optional[str] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListSiteIdentifiersAssignedToHostNameResult:
    """
    Use this data source to access information about an existing resource.

    :param str name: Name of the object.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:web/v20160301:listSiteIdentifiersAssignedToHostName', __args__, opts=opts, typ=ListSiteIdentifiersAssignedToHostNameResult).value

    return AwaitableListSiteIdentifiersAssignedToHostNameResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
