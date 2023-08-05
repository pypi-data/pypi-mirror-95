# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['EventSubscription']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:eventgrid:EventSubscription'.""", DeprecationWarning)


class EventSubscription(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:eventgrid:EventSubscription'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dead_letter_destination: Optional[pulumi.Input[pulumi.InputType['StorageBlobDeadLetterDestinationArgs']]] = None,
                 destination: Optional[pulumi.Input[Union[pulumi.InputType['AzureFunctionEventSubscriptionDestinationArgs'], pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['HybridConnectionEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusQueueEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusTopicEventSubscriptionDestinationArgs'], pulumi.InputType['StorageQueueEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]]] = None,
                 event_delivery_schema: Optional[pulumi.Input[Union[str, 'EventDeliverySchema']]] = None,
                 event_subscription_name: Optional[pulumi.Input[str]] = None,
                 expiration_time_utc: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']]] = None,
                 labels: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 retry_policy: Optional[pulumi.Input[pulumi.InputType['RetryPolicyArgs']]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Event Subscription
        Latest API Version: 2020-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StorageBlobDeadLetterDestinationArgs']] dead_letter_destination: The DeadLetter destination of the event subscription.
        :param pulumi.Input[Union[pulumi.InputType['AzureFunctionEventSubscriptionDestinationArgs'], pulumi.InputType['EventHubEventSubscriptionDestinationArgs'], pulumi.InputType['HybridConnectionEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusQueueEventSubscriptionDestinationArgs'], pulumi.InputType['ServiceBusTopicEventSubscriptionDestinationArgs'], pulumi.InputType['StorageQueueEventSubscriptionDestinationArgs'], pulumi.InputType['WebHookEventSubscriptionDestinationArgs']]] destination: Information about the destination where events have to be delivered for the event subscription.
        :param pulumi.Input[Union[str, 'EventDeliverySchema']] event_delivery_schema: The event delivery schema for the event subscription.
        :param pulumi.Input[str] event_subscription_name: Name of the event subscription. Event subscription names must be between 3 and 64 characters in length and should use alphanumeric letters only.
        :param pulumi.Input[str] expiration_time_utc: Expiration time of the event subscription.
        :param pulumi.Input[pulumi.InputType['EventSubscriptionFilterArgs']] filter: Information about the filter for the event subscription.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] labels: List of user defined labels.
        :param pulumi.Input[pulumi.InputType['RetryPolicyArgs']] retry_policy: The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        :param pulumi.Input[str] scope: The identifier of the resource to which the event subscription needs to be created or updated. The scope can be a subscription, or a resource group, or a top level resource belonging to a resource provider namespace, or an EventGrid topic. For example, use '/subscriptions/{subscriptionId}/' for a subscription, '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}' for a resource group, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}' for a resource, and '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}' for an EventGrid topic.
        """
        pulumi.log.warn("EventSubscription is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:eventgrid:EventSubscription'.")
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['dead_letter_destination'] = dead_letter_destination
            __props__['destination'] = destination
            __props__['event_delivery_schema'] = event_delivery_schema
            if event_subscription_name is None and not opts.urn:
                raise TypeError("Missing required property 'event_subscription_name'")
            __props__['event_subscription_name'] = event_subscription_name
            __props__['expiration_time_utc'] = expiration_time_utc
            __props__['filter'] = filter
            __props__['labels'] = labels
            __props__['retry_policy'] = retry_policy
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['topic'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:eventgrid:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20170615preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20170915preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20180101:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20180501preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20180915preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20190101:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20190201preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20190601:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20200101preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20200401preview:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20200601:EventSubscription"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20201015preview:EventSubscription")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EventSubscription, __self__).__init__(
            'azure-nextgen:eventgrid/latest:EventSubscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EventSubscription':
        """
        Get an existing EventSubscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return EventSubscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deadLetterDestination")
    def dead_letter_destination(self) -> pulumi.Output[Optional['outputs.StorageBlobDeadLetterDestinationResponse']]:
        """
        The DeadLetter destination of the event subscription.
        """
        return pulumi.get(self, "dead_letter_destination")

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Output[Optional[Any]]:
        """
        Information about the destination where events have to be delivered for the event subscription.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="eventDeliverySchema")
    def event_delivery_schema(self) -> pulumi.Output[Optional[str]]:
        """
        The event delivery schema for the event subscription.
        """
        return pulumi.get(self, "event_delivery_schema")

    @property
    @pulumi.getter(name="expirationTimeUtc")
    def expiration_time_utc(self) -> pulumi.Output[Optional[str]]:
        """
        Expiration time of the event subscription.
        """
        return pulumi.get(self, "expiration_time_utc")

    @property
    @pulumi.getter
    def filter(self) -> pulumi.Output[Optional['outputs.EventSubscriptionFilterResponse']]:
        """
        Information about the filter for the event subscription.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of user defined labels.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the event subscription.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="retryPolicy")
    def retry_policy(self) -> pulumi.Output[Optional['outputs.RetryPolicyResponse']]:
        """
        The retry policy for events. This can be used to configure maximum number of delivery attempts and time to live for events.
        """
        return pulumi.get(self, "retry_policy")

    @property
    @pulumi.getter
    def topic(self) -> pulumi.Output[str]:
        """
        Name of the topic of the event subscription.
        """
        return pulumi.get(self, "topic")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

