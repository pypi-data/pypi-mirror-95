# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetIotHubResourceEventHubConsumerGroupResult',
    'AwaitableGetIotHubResourceEventHubConsumerGroupResult',
    'get_iot_hub_resource_event_hub_consumer_group',
]

@pulumi.output_type
class GetIotHubResourceEventHubConsumerGroupResult:
    """
    The properties of the EventHubConsumerGroupInfo object.
    """
    def __init__(__self__, id=None, name=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The Event Hub-compatible consumer group identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The Event Hub-compatible consumer group name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags.
        """
        return pulumi.get(self, "tags")


class AwaitableGetIotHubResourceEventHubConsumerGroupResult(GetIotHubResourceEventHubConsumerGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIotHubResourceEventHubConsumerGroupResult(
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_iot_hub_resource_event_hub_consumer_group(event_hub_endpoint_name: Optional[str] = None,
                                                  name: Optional[str] = None,
                                                  resource_group_name: Optional[str] = None,
                                                  resource_name: Optional[str] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIotHubResourceEventHubConsumerGroupResult:
    """
    Use this data source to access information about an existing resource.

    :param str event_hub_endpoint_name: The name of the Event Hub-compatible endpoint in the IoT hub.
    :param str name: The name of the consumer group to retrieve.
    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    __args__ = dict()
    __args__['eventHubEndpointName'] = event_hub_endpoint_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:devices/v20160203:getIotHubResourceEventHubConsumerGroup', __args__, opts=opts, typ=GetIotHubResourceEventHubConsumerGroupResult).value

    return AwaitableGetIotHubResourceEventHubConsumerGroupResult(
        id=__ret__.id,
        name=__ret__.name,
        tags=__ret__.tags)
