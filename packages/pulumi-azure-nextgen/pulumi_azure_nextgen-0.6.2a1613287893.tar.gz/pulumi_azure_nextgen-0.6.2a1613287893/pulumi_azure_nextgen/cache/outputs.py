# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *

__all__ = [
    'ModuleResponse',
    'PrivateEndpointConnectionResponse',
    'PrivateEndpointResponse',
    'PrivateLinkServiceConnectionStateResponse',
    'RedisAccessKeysResponse',
    'RedisInstanceDetailsResponse',
    'RedisLinkedServerResponse',
    'ScheduleEntryResponse',
    'SkuResponse',
]

@pulumi.output_type
class ModuleResponse(dict):
    """
    Specifies configuration of a redis module
    """
    def __init__(__self__, *,
                 name: str,
                 version: str,
                 args: Optional[str] = None):
        """
        Specifies configuration of a redis module
        :param str name: The name of the module, e.g. 'RedisBloom', 'RediSearch', 'RedisTimeSeries'
        :param str version: The version of the module, e.g. '1.0'.
        :param str args: Configuration options for the module, e.g. 'ERROR_RATE 0.00 INITIAL_SIZE 400'.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "version", version)
        if args is not None:
            pulumi.set(__self__, "args", args)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the module, e.g. 'RedisBloom', 'RediSearch', 'RedisTimeSeries'
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the module, e.g. '1.0'.
        """
        return pulumi.get(self, "version")

    @property
    @pulumi.getter
    def args(self) -> Optional[str]:
        """
        Configuration options for the module, e.g. 'ERROR_RATE 0.00 INITIAL_SIZE 400'.
        """
        return pulumi.get(self, "args")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PrivateEndpointConnectionResponse(dict):
    """
    The Private Endpoint Connection resource.
    """
    def __init__(__self__, *,
                 id: str,
                 name: str,
                 private_link_service_connection_state: 'outputs.PrivateLinkServiceConnectionStateResponse',
                 provisioning_state: str,
                 type: str,
                 private_endpoint: Optional['outputs.PrivateEndpointResponse'] = None):
        """
        The Private Endpoint Connection resource.
        :param str id: Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        :param str name: The name of the resource
        :param 'PrivateLinkServiceConnectionStateResponseArgs' private_link_service_connection_state: A collection of information about the state of the connection between service consumer and provider.
        :param str provisioning_state: The provisioning state of the private endpoint connection resource.
        :param str type: The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        :param 'PrivateEndpointResponseArgs' private_endpoint: The resource of private end point.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "type", type)
        if private_endpoint is not None:
            pulumi.set(__self__, "private_endpoint", private_endpoint)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> 'outputs.PrivateLinkServiceConnectionStateResponse':
        """
        A collection of information about the state of the connection between service consumer and provider.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the private endpoint connection resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointResponse']:
        """
        The resource of private end point.
        """
        return pulumi.get(self, "private_endpoint")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PrivateEndpointResponse(dict):
    """
    The Private Endpoint resource.
    """
    def __init__(__self__, *,
                 id: str):
        """
        The Private Endpoint resource.
        :param str id: The ARM identifier for Private Endpoint
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ARM identifier for Private Endpoint
        """
        return pulumi.get(self, "id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PrivateLinkServiceConnectionStateResponse(dict):
    """
    A collection of information about the state of the connection between service consumer and provider.
    """
    def __init__(__self__, *,
                 actions_required: Optional[str] = None,
                 description: Optional[str] = None,
                 status: Optional[str] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param str actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param str description: The reason for approval/rejection of the connection.
        :param str status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[str]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RedisAccessKeysResponse(dict):
    """
    Redis cache access keys.
    """
    def __init__(__self__, *,
                 primary_key: str,
                 secondary_key: str):
        """
        Redis cache access keys.
        :param str primary_key: The current primary key that clients can use to authenticate with Redis cache.
        :param str secondary_key: The current secondary key that clients can use to authenticate with Redis cache.
        """
        pulumi.set(__self__, "primary_key", primary_key)
        pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> str:
        """
        The current primary key that clients can use to authenticate with Redis cache.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> str:
        """
        The current secondary key that clients can use to authenticate with Redis cache.
        """
        return pulumi.get(self, "secondary_key")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RedisInstanceDetailsResponse(dict):
    """
    Details of single instance of redis.
    """
    def __init__(__self__, *,
                 is_master: bool,
                 non_ssl_port: int,
                 shard_id: int,
                 ssl_port: int,
                 zone: str):
        """
        Details of single instance of redis.
        :param bool is_master: Specifies whether the instance is a master node.
        :param int non_ssl_port: If enableNonSslPort is true, provides Redis instance Non-SSL port.
        :param int shard_id: If clustering is enabled, the Shard ID of Redis Instance
        :param int ssl_port: Redis instance SSL port.
        :param str zone: If the Cache uses availability zones, specifies availability zone where this instance is located.
        """
        pulumi.set(__self__, "is_master", is_master)
        pulumi.set(__self__, "non_ssl_port", non_ssl_port)
        pulumi.set(__self__, "shard_id", shard_id)
        pulumi.set(__self__, "ssl_port", ssl_port)
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="isMaster")
    def is_master(self) -> bool:
        """
        Specifies whether the instance is a master node.
        """
        return pulumi.get(self, "is_master")

    @property
    @pulumi.getter(name="nonSslPort")
    def non_ssl_port(self) -> int:
        """
        If enableNonSslPort is true, provides Redis instance Non-SSL port.
        """
        return pulumi.get(self, "non_ssl_port")

    @property
    @pulumi.getter(name="shardId")
    def shard_id(self) -> int:
        """
        If clustering is enabled, the Shard ID of Redis Instance
        """
        return pulumi.get(self, "shard_id")

    @property
    @pulumi.getter(name="sslPort")
    def ssl_port(self) -> int:
        """
        Redis instance SSL port.
        """
        return pulumi.get(self, "ssl_port")

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        If the Cache uses availability zones, specifies availability zone where this instance is located.
        """
        return pulumi.get(self, "zone")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RedisLinkedServerResponse(dict):
    """
    Linked server Id
    """
    def __init__(__self__, *,
                 id: str):
        """
        Linked server Id
        :param str id: Linked server Id.
        """
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Linked server Id.
        """
        return pulumi.get(self, "id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ScheduleEntryResponse(dict):
    """
    Patch schedule entry for a Premium Redis Cache.
    """
    def __init__(__self__, *,
                 day_of_week: str,
                 start_hour_utc: int,
                 maintenance_window: Optional[str] = None):
        """
        Patch schedule entry for a Premium Redis Cache.
        :param str day_of_week: Day of the week when a cache can be patched.
        :param int start_hour_utc: Start hour after which cache patching can start.
        :param str maintenance_window: ISO8601 timespan specifying how much time cache patching can take. 
        """
        pulumi.set(__self__, "day_of_week", day_of_week)
        pulumi.set(__self__, "start_hour_utc", start_hour_utc)
        if maintenance_window is not None:
            pulumi.set(__self__, "maintenance_window", maintenance_window)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> str:
        """
        Day of the week when a cache can be patched.
        """
        return pulumi.get(self, "day_of_week")

    @property
    @pulumi.getter(name="startHourUtc")
    def start_hour_utc(self) -> int:
        """
        Start hour after which cache patching can start.
        """
        return pulumi.get(self, "start_hour_utc")

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> Optional[str]:
        """
        ISO8601 timespan specifying how much time cache patching can take. 
        """
        return pulumi.get(self, "maintenance_window")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SkuResponse(dict):
    """
    SKU parameters supplied to the create RedisEnterprise operation.
    """
    def __init__(__self__, *,
                 name: str,
                 capacity: Optional[int] = None):
        """
        SKU parameters supplied to the create RedisEnterprise operation.
        :param str name: The type of RedisEnterprise cluster to deploy. Possible values: (Enterprise_E10, EnterpriseFlash_F300 etc.)
        :param int capacity: The size of the RedisEnterprise cluster. Defaults to 2 or 3 depending on SKU. Valid values are (2, 4, 6, ...) for Enterprise SKUs and (3, 9, 15, ...) for Flash SKUs.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The type of RedisEnterprise cluster to deploy. Possible values: (Enterprise_E10, EnterpriseFlash_F300 etc.)
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        The size of the RedisEnterprise cluster. Defaults to 2 or 3 depending on SKU. Valid values are (2, 4, 6, ...) for Enterprise SKUs and (3, 9, 15, ...) for Flash SKUs.
        """
        return pulumi.get(self, "capacity")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


