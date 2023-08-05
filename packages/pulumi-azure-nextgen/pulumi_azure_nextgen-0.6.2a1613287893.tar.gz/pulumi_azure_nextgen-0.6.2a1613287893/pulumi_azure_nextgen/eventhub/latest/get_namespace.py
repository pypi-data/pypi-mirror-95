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
    'GetNamespaceResult',
    'AwaitableGetNamespaceResult',
    'get_namespace',
]

@pulumi.output_type
class GetNamespaceResult:
    """
    Single Namespace item in List or Get Operation
    """
    def __init__(__self__, created_at=None, id=None, is_auto_inflate_enabled=None, kafka_enabled=None, location=None, maximum_throughput_units=None, metric_id=None, name=None, provisioning_state=None, service_bus_endpoint=None, sku=None, tags=None, type=None, updated_at=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_auto_inflate_enabled and not isinstance(is_auto_inflate_enabled, bool):
            raise TypeError("Expected argument 'is_auto_inflate_enabled' to be a bool")
        pulumi.set(__self__, "is_auto_inflate_enabled", is_auto_inflate_enabled)
        if kafka_enabled and not isinstance(kafka_enabled, bool):
            raise TypeError("Expected argument 'kafka_enabled' to be a bool")
        pulumi.set(__self__, "kafka_enabled", kafka_enabled)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maximum_throughput_units and not isinstance(maximum_throughput_units, int):
            raise TypeError("Expected argument 'maximum_throughput_units' to be a int")
        pulumi.set(__self__, "maximum_throughput_units", maximum_throughput_units)
        if metric_id and not isinstance(metric_id, str):
            raise TypeError("Expected argument 'metric_id' to be a str")
        pulumi.set(__self__, "metric_id", metric_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_bus_endpoint and not isinstance(service_bus_endpoint, str):
            raise TypeError("Expected argument 'service_bus_endpoint' to be a str")
        pulumi.set(__self__, "service_bus_endpoint", service_bus_endpoint)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The time the Namespace was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isAutoInflateEnabled")
    def is_auto_inflate_enabled(self) -> Optional[bool]:
        """
        Value that indicates whether AutoInflate is enabled for eventhub namespace.
        """
        return pulumi.get(self, "is_auto_inflate_enabled")

    @property
    @pulumi.getter(name="kafkaEnabled")
    def kafka_enabled(self) -> Optional[bool]:
        """
        Value that indicates whether Kafka is enabled for eventhub namespace.
        """
        return pulumi.get(self, "kafka_enabled")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maximumThroughputUnits")
    def maximum_throughput_units(self) -> Optional[int]:
        """
        Upper limit of throughput units when AutoInflate is enabled, value should be within 0 to 20 throughput units. ( '0' if AutoInflateEnabled = true)
        """
        return pulumi.get(self, "maximum_throughput_units")

    @property
    @pulumi.getter(name="metricId")
    def metric_id(self) -> str:
        """
        Identifier for Azure Insights metrics.
        """
        return pulumi.get(self, "metric_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Namespace.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceBusEndpoint")
    def service_bus_endpoint(self) -> str:
        """
        Endpoint you can use to perform Service Bus operations.
        """
        return pulumi.get(self, "service_bus_endpoint")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        Properties of sku resource
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The time the Namespace was updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetNamespaceResult(GetNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamespaceResult(
            created_at=self.created_at,
            id=self.id,
            is_auto_inflate_enabled=self.is_auto_inflate_enabled,
            kafka_enabled=self.kafka_enabled,
            location=self.location,
            maximum_throughput_units=self.maximum_throughput_units,
            metric_id=self.metric_id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            service_bus_endpoint=self.service_bus_endpoint,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            updated_at=self.updated_at)


def get_namespace(namespace_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamespaceResult:
    """
    Use this data source to access information about an existing resource.

    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:eventhub/latest:getNamespace', __args__, opts=opts, typ=GetNamespaceResult).value

    return AwaitableGetNamespaceResult(
        created_at=__ret__.created_at,
        id=__ret__.id,
        is_auto_inflate_enabled=__ret__.is_auto_inflate_enabled,
        kafka_enabled=__ret__.kafka_enabled,
        location=__ret__.location,
        maximum_throughput_units=__ret__.maximum_throughput_units,
        metric_id=__ret__.metric_id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        service_bus_endpoint=__ret__.service_bus_endpoint,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        updated_at=__ret__.updated_at)
