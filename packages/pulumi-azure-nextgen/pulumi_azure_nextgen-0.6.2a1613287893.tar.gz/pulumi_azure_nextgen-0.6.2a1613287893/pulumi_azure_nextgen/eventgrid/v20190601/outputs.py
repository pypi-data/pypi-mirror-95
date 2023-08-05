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

__all__ = [
    'BoolEqualsAdvancedFilterResponse',
    'EventHubEventSubscriptionDestinationResponse',
    'EventSubscriptionFilterResponse',
    'HybridConnectionEventSubscriptionDestinationResponse',
    'NumberGreaterThanAdvancedFilterResponse',
    'NumberGreaterThanOrEqualsAdvancedFilterResponse',
    'NumberInAdvancedFilterResponse',
    'NumberLessThanAdvancedFilterResponse',
    'NumberLessThanOrEqualsAdvancedFilterResponse',
    'NumberNotInAdvancedFilterResponse',
    'RetryPolicyResponse',
    'ServiceBusQueueEventSubscriptionDestinationResponse',
    'StorageBlobDeadLetterDestinationResponse',
    'StorageQueueEventSubscriptionDestinationResponse',
    'StringBeginsWithAdvancedFilterResponse',
    'StringContainsAdvancedFilterResponse',
    'StringEndsWithAdvancedFilterResponse',
    'StringInAdvancedFilterResponse',
    'StringNotInAdvancedFilterResponse',
    'WebHookEventSubscriptionDestinationResponse',
]

@pulumi.output_type
class BoolEqualsAdvancedFilterResponse(dict):
    """
    BoolEquals Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 value: Optional[bool] = None):
        """
        BoolEquals Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'BoolEquals'.
        :param str key: The field/property in the event based on which you want to filter.
        :param bool value: The boolean filter value.
        """
        pulumi.set(__self__, "operator_type", 'BoolEquals')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'BoolEquals'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[bool]:
        """
        The boolean filter value.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EventHubEventSubscriptionDestinationResponse(dict):
    """
    Information about the event hub destination for an event subscription
    """
    def __init__(__self__, *,
                 endpoint_type: str,
                 resource_id: Optional[str] = None):
        """
        Information about the event hub destination for an event subscription
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'EventHub'.
        :param str resource_id: The Azure Resource Id that represents the endpoint of an Event Hub destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'EventHub')
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'EventHub'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource Id that represents the endpoint of an Event Hub destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EventSubscriptionFilterResponse(dict):
    """
    Filter for the Event Subscription.
    """
    def __init__(__self__, *,
                 advanced_filters: Optional[Sequence[Any]] = None,
                 included_event_types: Optional[Sequence[str]] = None,
                 is_subject_case_sensitive: Optional[bool] = None,
                 subject_begins_with: Optional[str] = None,
                 subject_ends_with: Optional[str] = None):
        """
        Filter for the Event Subscription.
        :param Sequence[Union['BoolEqualsAdvancedFilterResponseArgs', 'NumberGreaterThanAdvancedFilterResponseArgs', 'NumberGreaterThanOrEqualsAdvancedFilterResponseArgs', 'NumberInAdvancedFilterResponseArgs', 'NumberLessThanAdvancedFilterResponseArgs', 'NumberLessThanOrEqualsAdvancedFilterResponseArgs', 'NumberNotInAdvancedFilterResponseArgs', 'StringBeginsWithAdvancedFilterResponseArgs', 'StringContainsAdvancedFilterResponseArgs', 'StringEndsWithAdvancedFilterResponseArgs', 'StringInAdvancedFilterResponseArgs', 'StringNotInAdvancedFilterResponseArgs']] advanced_filters: An array of advanced filters that are used for filtering event subscriptions.
        :param Sequence[str] included_event_types: A list of applicable event types that need to be part of the event subscription. If it is desired to subscribe to all default event types, set the IncludedEventTypes to null.
        :param bool is_subject_case_sensitive: Specifies if the SubjectBeginsWith and SubjectEndsWith properties of the filter 
               should be compared in a case sensitive manner.
        :param str subject_begins_with: An optional string to filter events for an event subscription based on a resource path prefix.
               The format of this depends on the publisher of the events. 
               Wildcard characters are not supported in this path.
        :param str subject_ends_with: An optional string to filter events for an event subscription based on a resource path suffix.
               Wildcard characters are not supported in this path.
        """
        if advanced_filters is not None:
            pulumi.set(__self__, "advanced_filters", advanced_filters)
        if included_event_types is not None:
            pulumi.set(__self__, "included_event_types", included_event_types)
        if is_subject_case_sensitive is None:
            is_subject_case_sensitive = False
        if is_subject_case_sensitive is not None:
            pulumi.set(__self__, "is_subject_case_sensitive", is_subject_case_sensitive)
        if subject_begins_with is not None:
            pulumi.set(__self__, "subject_begins_with", subject_begins_with)
        if subject_ends_with is not None:
            pulumi.set(__self__, "subject_ends_with", subject_ends_with)

    @property
    @pulumi.getter(name="advancedFilters")
    def advanced_filters(self) -> Optional[Sequence[Any]]:
        """
        An array of advanced filters that are used for filtering event subscriptions.
        """
        return pulumi.get(self, "advanced_filters")

    @property
    @pulumi.getter(name="includedEventTypes")
    def included_event_types(self) -> Optional[Sequence[str]]:
        """
        A list of applicable event types that need to be part of the event subscription. If it is desired to subscribe to all default event types, set the IncludedEventTypes to null.
        """
        return pulumi.get(self, "included_event_types")

    @property
    @pulumi.getter(name="isSubjectCaseSensitive")
    def is_subject_case_sensitive(self) -> Optional[bool]:
        """
        Specifies if the SubjectBeginsWith and SubjectEndsWith properties of the filter 
        should be compared in a case sensitive manner.
        """
        return pulumi.get(self, "is_subject_case_sensitive")

    @property
    @pulumi.getter(name="subjectBeginsWith")
    def subject_begins_with(self) -> Optional[str]:
        """
        An optional string to filter events for an event subscription based on a resource path prefix.
        The format of this depends on the publisher of the events. 
        Wildcard characters are not supported in this path.
        """
        return pulumi.get(self, "subject_begins_with")

    @property
    @pulumi.getter(name="subjectEndsWith")
    def subject_ends_with(self) -> Optional[str]:
        """
        An optional string to filter events for an event subscription based on a resource path suffix.
        Wildcard characters are not supported in this path.
        """
        return pulumi.get(self, "subject_ends_with")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class HybridConnectionEventSubscriptionDestinationResponse(dict):
    """
    Information about the HybridConnection destination for an event subscription.
    """
    def __init__(__self__, *,
                 endpoint_type: str,
                 resource_id: Optional[str] = None):
        """
        Information about the HybridConnection destination for an event subscription.
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'HybridConnection'.
        :param str resource_id: The Azure Resource ID of an hybrid connection that is the destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'HybridConnection')
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'HybridConnection'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource ID of an hybrid connection that is the destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NumberGreaterThanAdvancedFilterResponse(dict):
    """
    NumberGreaterThan Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 value: Optional[float] = None):
        """
        NumberGreaterThan Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'NumberGreaterThan'.
        :param str key: The field/property in the event based on which you want to filter.
        :param float value: The filter value.
        """
        pulumi.set(__self__, "operator_type", 'NumberGreaterThan')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'NumberGreaterThan'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        """
        The filter value.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NumberGreaterThanOrEqualsAdvancedFilterResponse(dict):
    """
    NumberGreaterThanOrEquals Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 value: Optional[float] = None):
        """
        NumberGreaterThanOrEquals Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'NumberGreaterThanOrEquals'.
        :param str key: The field/property in the event based on which you want to filter.
        :param float value: The filter value.
        """
        pulumi.set(__self__, "operator_type", 'NumberGreaterThanOrEquals')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'NumberGreaterThanOrEquals'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        """
        The filter value.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NumberInAdvancedFilterResponse(dict):
    """
    NumberIn Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[float]] = None):
        """
        NumberIn Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'NumberIn'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[float] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'NumberIn')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'NumberIn'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[float]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NumberLessThanAdvancedFilterResponse(dict):
    """
    NumberLessThan Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 value: Optional[float] = None):
        """
        NumberLessThan Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'NumberLessThan'.
        :param str key: The field/property in the event based on which you want to filter.
        :param float value: The filter value.
        """
        pulumi.set(__self__, "operator_type", 'NumberLessThan')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'NumberLessThan'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        """
        The filter value.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NumberLessThanOrEqualsAdvancedFilterResponse(dict):
    """
    NumberLessThanOrEquals Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 value: Optional[float] = None):
        """
        NumberLessThanOrEquals Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'NumberLessThanOrEquals'.
        :param str key: The field/property in the event based on which you want to filter.
        :param float value: The filter value.
        """
        pulumi.set(__self__, "operator_type", 'NumberLessThanOrEquals')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'NumberLessThanOrEquals'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        """
        The filter value.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class NumberNotInAdvancedFilterResponse(dict):
    """
    NumberNotIn Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[float]] = None):
        """
        NumberNotIn Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'NumberNotIn'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[float] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'NumberNotIn')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'NumberNotIn'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[float]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RetryPolicyResponse(dict):
    """
    Information about the retry policy for an event subscription.
    """
    def __init__(__self__, *,
                 event_time_to_live_in_minutes: Optional[int] = None,
                 max_delivery_attempts: Optional[int] = None):
        """
        Information about the retry policy for an event subscription.
        :param int event_time_to_live_in_minutes: Time To Live (in minutes) for events.
        :param int max_delivery_attempts: Maximum number of delivery retry attempts for events.
        """
        if event_time_to_live_in_minutes is not None:
            pulumi.set(__self__, "event_time_to_live_in_minutes", event_time_to_live_in_minutes)
        if max_delivery_attempts is not None:
            pulumi.set(__self__, "max_delivery_attempts", max_delivery_attempts)

    @property
    @pulumi.getter(name="eventTimeToLiveInMinutes")
    def event_time_to_live_in_minutes(self) -> Optional[int]:
        """
        Time To Live (in minutes) for events.
        """
        return pulumi.get(self, "event_time_to_live_in_minutes")

    @property
    @pulumi.getter(name="maxDeliveryAttempts")
    def max_delivery_attempts(self) -> Optional[int]:
        """
        Maximum number of delivery retry attempts for events.
        """
        return pulumi.get(self, "max_delivery_attempts")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServiceBusQueueEventSubscriptionDestinationResponse(dict):
    """
    Information about the service bus destination for an event subscription
    """
    def __init__(__self__, *,
                 endpoint_type: str,
                 resource_id: Optional[str] = None):
        """
        Information about the service bus destination for an event subscription
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'ServiceBusQueue'.
        :param str resource_id: The Azure Resource Id that represents the endpoint of the Service Bus destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'ServiceBusQueue')
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'ServiceBusQueue'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource Id that represents the endpoint of the Service Bus destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StorageBlobDeadLetterDestinationResponse(dict):
    """
    Information about the storage blob based dead letter destination.
    """
    def __init__(__self__, *,
                 endpoint_type: str,
                 blob_container_name: Optional[str] = None,
                 resource_id: Optional[str] = None):
        """
        Information about the storage blob based dead letter destination.
        :param str endpoint_type: Type of the endpoint for the dead letter destination
               Expected value is 'StorageBlob'.
        :param str blob_container_name: The name of the Storage blob container that is the destination of the deadletter events
        :param str resource_id: The Azure Resource ID of the storage account that is the destination of the deadletter events
        """
        pulumi.set(__self__, "endpoint_type", 'StorageBlob')
        if blob_container_name is not None:
            pulumi.set(__self__, "blob_container_name", blob_container_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the dead letter destination
        Expected value is 'StorageBlob'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="blobContainerName")
    def blob_container_name(self) -> Optional[str]:
        """
        The name of the Storage blob container that is the destination of the deadletter events
        """
        return pulumi.get(self, "blob_container_name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource ID of the storage account that is the destination of the deadletter events
        """
        return pulumi.get(self, "resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StorageQueueEventSubscriptionDestinationResponse(dict):
    """
    Information about the storage queue destination for an event subscription.
    """
    def __init__(__self__, *,
                 endpoint_type: str,
                 queue_name: Optional[str] = None,
                 resource_id: Optional[str] = None):
        """
        Information about the storage queue destination for an event subscription.
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'StorageQueue'.
        :param str queue_name: The name of the Storage queue under a storage account that is the destination of an event subscription.
        :param str resource_id: The Azure Resource ID of the storage account that contains the queue that is the destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_type", 'StorageQueue')
        if queue_name is not None:
            pulumi.set(__self__, "queue_name", queue_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'StorageQueue'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="queueName")
    def queue_name(self) -> Optional[str]:
        """
        The name of the Storage queue under a storage account that is the destination of an event subscription.
        """
        return pulumi.get(self, "queue_name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The Azure Resource ID of the storage account that contains the queue that is the destination of an event subscription.
        """
        return pulumi.get(self, "resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StringBeginsWithAdvancedFilterResponse(dict):
    """
    StringBeginsWith Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[str]] = None):
        """
        StringBeginsWith Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'StringBeginsWith'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[str] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'StringBeginsWith')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'StringBeginsWith'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StringContainsAdvancedFilterResponse(dict):
    """
    StringContains Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[str]] = None):
        """
        StringContains Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'StringContains'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[str] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'StringContains')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'StringContains'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StringEndsWithAdvancedFilterResponse(dict):
    """
    StringEndsWith Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[str]] = None):
        """
        StringEndsWith Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'StringEndsWith'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[str] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'StringEndsWith')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'StringEndsWith'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StringInAdvancedFilterResponse(dict):
    """
    StringIn Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[str]] = None):
        """
        StringIn Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'StringIn'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[str] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'StringIn')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'StringIn'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StringNotInAdvancedFilterResponse(dict):
    """
    StringNotIn Advanced Filter.
    """
    def __init__(__self__, *,
                 operator_type: str,
                 key: Optional[str] = None,
                 values: Optional[Sequence[str]] = None):
        """
        StringNotIn Advanced Filter.
        :param str operator_type: The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
               Expected value is 'StringNotIn'.
        :param str key: The field/property in the event based on which you want to filter.
        :param Sequence[str] values: The set of filter values.
        """
        pulumi.set(__self__, "operator_type", 'StringNotIn')
        if key is not None:
            pulumi.set(__self__, "key", key)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> str:
        """
        The operator type used for filtering, e.g., NumberIn, StringContains, BoolEquals and others.
        Expected value is 'StringNotIn'.
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The field/property in the event based on which you want to filter.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def values(self) -> Optional[Sequence[str]]:
        """
        The set of filter values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebHookEventSubscriptionDestinationResponse(dict):
    """
    Information about the webhook destination for an event subscription
    """
    def __init__(__self__, *,
                 endpoint_base_url: str,
                 endpoint_type: str,
                 endpoint_url: Optional[str] = None):
        """
        Information about the webhook destination for an event subscription
        :param str endpoint_base_url: The base URL that represents the endpoint of the destination of an event subscription.
        :param str endpoint_type: Type of the endpoint for the event subscription destination
               Expected value is 'WebHook'.
        :param str endpoint_url: The URL that represents the endpoint of the destination of an event subscription.
        """
        pulumi.set(__self__, "endpoint_base_url", endpoint_base_url)
        pulumi.set(__self__, "endpoint_type", 'WebHook')
        if endpoint_url is not None:
            pulumi.set(__self__, "endpoint_url", endpoint_url)

    @property
    @pulumi.getter(name="endpointBaseUrl")
    def endpoint_base_url(self) -> str:
        """
        The base URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_base_url")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> str:
        """
        Type of the endpoint for the event subscription destination
        Expected value is 'WebHook'.
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="endpointUrl")
    def endpoint_url(self) -> Optional[str]:
        """
        The URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_url")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


