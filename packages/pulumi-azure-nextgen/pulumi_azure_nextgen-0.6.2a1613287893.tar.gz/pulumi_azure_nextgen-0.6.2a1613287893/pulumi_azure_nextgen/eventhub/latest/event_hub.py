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

__all__ = ['EventHub']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:eventhub:EventHub'.""", DeprecationWarning)


class EventHub(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:eventhub:EventHub'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 capture_description: Optional[pulumi.Input[pulumi.InputType['CaptureDescriptionArgs']]] = None,
                 event_hub_name: Optional[pulumi.Input[str]] = None,
                 message_retention_in_days: Optional[pulumi.Input[float]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 partition_count: Optional[pulumi.Input[float]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['EntityStatus']] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Single item in List or Get Event Hub operation
        Latest API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['CaptureDescriptionArgs']] capture_description: Properties of capture description
        :param pulumi.Input[str] event_hub_name: The Event Hub name
        :param pulumi.Input[float] message_retention_in_days: Number of days to retain the events for this Event Hub, value should be 1 to 7 days
        :param pulumi.Input[str] namespace_name: The Namespace name
        :param pulumi.Input[float] partition_count: Number of partitions created for the Event Hub, allowed values are from 1 to 32 partitions.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input['EntityStatus'] status: Enumerates the possible values for the status of the Event Hub.
        """
        pulumi.log.warn("EventHub is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:eventhub:EventHub'.")
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

            __props__['capture_description'] = capture_description
            if event_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'event_hub_name'")
            __props__['event_hub_name'] = event_hub_name
            __props__['message_retention_in_days'] = message_retention_in_days
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            __props__['partition_count'] = partition_count
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['status'] = status
            __props__['created_at'] = None
            __props__['name'] = None
            __props__['partition_ids'] = None
            __props__['type'] = None
            __props__['updated_at'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:eventhub:EventHub"), pulumi.Alias(type_="azure-nextgen:eventhub/v20140901:EventHub"), pulumi.Alias(type_="azure-nextgen:eventhub/v20150801:EventHub"), pulumi.Alias(type_="azure-nextgen:eventhub/v20170401:EventHub"), pulumi.Alias(type_="azure-nextgen:eventhub/v20180101preview:EventHub")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(EventHub, __self__).__init__(
            'azure-nextgen:eventhub/latest:EventHub',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'EventHub':
        """
        Get an existing EventHub resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return EventHub(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="captureDescription")
    def capture_description(self) -> pulumi.Output[Optional['outputs.CaptureDescriptionResponse']]:
        """
        Properties of capture description
        """
        return pulumi.get(self, "capture_description")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Exact time the Event Hub was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="messageRetentionInDays")
    def message_retention_in_days(self) -> pulumi.Output[Optional[float]]:
        """
        Number of days to retain the events for this Event Hub, value should be 1 to 7 days
        """
        return pulumi.get(self, "message_retention_in_days")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partitionCount")
    def partition_count(self) -> pulumi.Output[Optional[float]]:
        """
        Number of partitions created for the Event Hub, allowed values are from 1 to 32 partitions.
        """
        return pulumi.get(self, "partition_count")

    @property
    @pulumi.getter(name="partitionIds")
    def partition_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        Current number of shards on the Event Hub.
        """
        return pulumi.get(self, "partition_ids")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Enumerates the possible values for the status of the Event Hub.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The exact time the message was updated.
        """
        return pulumi.get(self, "updated_at")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

