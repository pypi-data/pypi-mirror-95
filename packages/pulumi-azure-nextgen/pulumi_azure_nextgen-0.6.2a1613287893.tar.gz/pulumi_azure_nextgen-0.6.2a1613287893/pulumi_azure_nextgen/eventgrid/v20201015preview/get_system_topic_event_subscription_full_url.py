# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetSystemTopicEventSubscriptionFullUrlResult',
    'AwaitableGetSystemTopicEventSubscriptionFullUrlResult',
    'get_system_topic_event_subscription_full_url',
]

@pulumi.output_type
class GetSystemTopicEventSubscriptionFullUrlResult:
    """
    Full endpoint url of an event subscription
    """
    def __init__(__self__, endpoint_url=None):
        if endpoint_url and not isinstance(endpoint_url, str):
            raise TypeError("Expected argument 'endpoint_url' to be a str")
        pulumi.set(__self__, "endpoint_url", endpoint_url)

    @property
    @pulumi.getter(name="endpointUrl")
    def endpoint_url(self) -> Optional[str]:
        """
        The URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_url")


class AwaitableGetSystemTopicEventSubscriptionFullUrlResult(GetSystemTopicEventSubscriptionFullUrlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSystemTopicEventSubscriptionFullUrlResult(
            endpoint_url=self.endpoint_url)


def get_system_topic_event_subscription_full_url(event_subscription_name: Optional[str] = None,
                                                 resource_group_name: Optional[str] = None,
                                                 system_topic_name: Optional[str] = None,
                                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSystemTopicEventSubscriptionFullUrlResult:
    """
    Use this data source to access information about an existing resource.

    :param str event_subscription_name: Name of the event subscription to be created. Event subscription names must be between 3 and 100 characters in length and use alphanumeric letters only.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    :param str system_topic_name: Name of the system topic.
    """
    __args__ = dict()
    __args__['eventSubscriptionName'] = event_subscription_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['systemTopicName'] = system_topic_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:eventgrid/v20201015preview:getSystemTopicEventSubscriptionFullUrl', __args__, opts=opts, typ=GetSystemTopicEventSubscriptionFullUrlResult).value

    return AwaitableGetSystemTopicEventSubscriptionFullUrlResult(
        endpoint_url=__ret__.endpoint_url)
