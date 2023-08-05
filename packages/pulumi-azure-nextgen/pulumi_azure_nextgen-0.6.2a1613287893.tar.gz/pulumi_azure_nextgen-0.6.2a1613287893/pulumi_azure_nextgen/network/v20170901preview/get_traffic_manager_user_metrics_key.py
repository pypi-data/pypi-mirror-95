# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetTrafficManagerUserMetricsKeyResult',
    'AwaitableGetTrafficManagerUserMetricsKeyResult',
    'get_traffic_manager_user_metrics_key',
]

@pulumi.output_type
class GetTrafficManagerUserMetricsKeyResult:
    """
    Class representing a Traffic Manager Real User Metrics key response.
    """
    def __init__(__self__, id=None, key=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The key returned by the Real User Metrics operation.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Network/trafficManagerProfiles.
        """
        return pulumi.get(self, "type")


class AwaitableGetTrafficManagerUserMetricsKeyResult(GetTrafficManagerUserMetricsKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTrafficManagerUserMetricsKeyResult(
            id=self.id,
            key=self.key,
            name=self.name,
            type=self.type)


def get_traffic_manager_user_metrics_key(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTrafficManagerUserMetricsKeyResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:network/v20170901preview:getTrafficManagerUserMetricsKey', __args__, opts=opts, typ=GetTrafficManagerUserMetricsKeyResult).value

    return AwaitableGetTrafficManagerUserMetricsKeyResult(
        id=__ret__.id,
        key=__ret__.key,
        name=__ret__.name,
        type=__ret__.type)
