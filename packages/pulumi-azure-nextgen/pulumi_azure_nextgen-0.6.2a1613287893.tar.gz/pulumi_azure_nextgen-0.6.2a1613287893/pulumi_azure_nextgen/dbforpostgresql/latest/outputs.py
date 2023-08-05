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
    'PrivateEndpointPropertyResponse',
    'PrivateLinkServiceConnectionStatePropertyResponse',
    'ResourceIdentityResponse',
    'ServerPrivateEndpointConnectionPropertiesResponse',
    'ServerPrivateEndpointConnectionResponse',
    'ServerPrivateLinkServiceConnectionStatePropertyResponse',
    'SkuResponse',
    'StorageProfileResponse',
]

@pulumi.output_type
class PrivateEndpointPropertyResponse(dict):
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        :param str id: Resource id of the private endpoint.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource id of the private endpoint.
        """
        return pulumi.get(self, "id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PrivateLinkServiceConnectionStatePropertyResponse(dict):
    def __init__(__self__, *,
                 actions_required: str,
                 description: str,
                 status: str):
        """
        :param str actions_required: The actions required for private link service connection.
        :param str description: The private link service connection description.
        :param str status: The private link service connection status.
        """
        pulumi.set(__self__, "actions_required", actions_required)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> str:
        """
        The actions required for private link service connection.
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The private link service connection description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The private link service connection status.
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ResourceIdentityResponse(dict):
    """
    Azure Active Directory identity configuration for a resource.
    """
    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None):
        """
        Azure Active Directory identity configuration for a resource.
        :param str principal_id: The Azure Active Directory principal id.
        :param str tenant_id: The Azure Active Directory tenant id.
        :param str type: The identity type. Set this to 'SystemAssigned' in order to automatically create and assign an Azure Active Directory principal for the resource.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The Azure Active Directory principal id.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The Azure Active Directory tenant id.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The identity type. Set this to 'SystemAssigned' in order to automatically create and assign an Azure Active Directory principal for the resource.
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServerPrivateEndpointConnectionPropertiesResponse(dict):
    """
    Properties of a private endpoint connection.
    """
    def __init__(__self__, *,
                 provisioning_state: str,
                 private_endpoint: Optional['outputs.PrivateEndpointPropertyResponse'] = None,
                 private_link_service_connection_state: Optional['outputs.ServerPrivateLinkServiceConnectionStatePropertyResponse'] = None):
        """
        Properties of a private endpoint connection.
        :param str provisioning_state: State of the private endpoint connection.
        :param 'PrivateEndpointPropertyResponseArgs' private_endpoint: Private endpoint which the connection belongs to.
        :param 'ServerPrivateLinkServiceConnectionStatePropertyResponseArgs' private_link_service_connection_state: Connection state of the private endpoint connection.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if private_endpoint is not None:
            pulumi.set(__self__, "private_endpoint", private_endpoint)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        State of the private endpoint connection.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional['outputs.PrivateEndpointPropertyResponse']:
        """
        Private endpoint which the connection belongs to.
        """
        return pulumi.get(self, "private_endpoint")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional['outputs.ServerPrivateLinkServiceConnectionStatePropertyResponse']:
        """
        Connection state of the private endpoint connection.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServerPrivateEndpointConnectionResponse(dict):
    """
    A private endpoint connection under a server
    """
    def __init__(__self__, *,
                 id: str,
                 properties: 'outputs.ServerPrivateEndpointConnectionPropertiesResponse'):
        """
        A private endpoint connection under a server
        :param str id: Resource ID of the Private Endpoint Connection.
        :param 'ServerPrivateEndpointConnectionPropertiesResponseArgs' properties: Private endpoint connection properties
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID of the Private Endpoint Connection.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ServerPrivateEndpointConnectionPropertiesResponse':
        """
        Private endpoint connection properties
        """
        return pulumi.get(self, "properties")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServerPrivateLinkServiceConnectionStatePropertyResponse(dict):
    def __init__(__self__, *,
                 actions_required: str,
                 description: str,
                 status: str):
        """
        :param str actions_required: The actions required for private link service connection.
        :param str description: The private link service connection description.
        :param str status: The private link service connection status.
        """
        pulumi.set(__self__, "actions_required", actions_required)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> str:
        """
        The actions required for private link service connection.
        """
        return pulumi.get(self, "actions_required")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The private link service connection description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The private link service connection status.
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SkuResponse(dict):
    """
    Billing information related properties of a server.
    """
    def __init__(__self__, *,
                 name: str,
                 capacity: Optional[int] = None,
                 family: Optional[str] = None,
                 size: Optional[str] = None,
                 tier: Optional[str] = None):
        """
        Billing information related properties of a server.
        :param str name: The name of the sku, typically, tier + family + cores, e.g. B_Gen4_1, GP_Gen5_8.
        :param int capacity: The scale up/out capacity, representing server's compute units.
        :param str family: The family of hardware.
        :param str size: The size code, to be interpreted by resource as appropriate.
        :param str tier: The tier of the particular SKU, e.g. Basic.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the sku, typically, tier + family + cores, e.g. B_Gen4_1, GP_Gen5_8.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        The scale up/out capacity, representing server's compute units.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def family(self) -> Optional[str]:
        """
        The family of hardware.
        """
        return pulumi.get(self, "family")

    @property
    @pulumi.getter
    def size(self) -> Optional[str]:
        """
        The size code, to be interpreted by resource as appropriate.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        The tier of the particular SKU, e.g. Basic.
        """
        return pulumi.get(self, "tier")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StorageProfileResponse(dict):
    """
    Storage Profile properties of a server
    """
    def __init__(__self__, *,
                 backup_retention_days: Optional[int] = None,
                 geo_redundant_backup: Optional[str] = None,
                 storage_autogrow: Optional[str] = None,
                 storage_mb: Optional[int] = None):
        """
        Storage Profile properties of a server
        :param int backup_retention_days: Backup retention days for the server.
        :param str geo_redundant_backup: Enable Geo-redundant or not for server backup.
        :param str storage_autogrow: Enable Storage Auto Grow.
        :param int storage_mb: Max storage allowed for a server.
        """
        if backup_retention_days is not None:
            pulumi.set(__self__, "backup_retention_days", backup_retention_days)
        if geo_redundant_backup is not None:
            pulumi.set(__self__, "geo_redundant_backup", geo_redundant_backup)
        if storage_autogrow is not None:
            pulumi.set(__self__, "storage_autogrow", storage_autogrow)
        if storage_mb is not None:
            pulumi.set(__self__, "storage_mb", storage_mb)

    @property
    @pulumi.getter(name="backupRetentionDays")
    def backup_retention_days(self) -> Optional[int]:
        """
        Backup retention days for the server.
        """
        return pulumi.get(self, "backup_retention_days")

    @property
    @pulumi.getter(name="geoRedundantBackup")
    def geo_redundant_backup(self) -> Optional[str]:
        """
        Enable Geo-redundant or not for server backup.
        """
        return pulumi.get(self, "geo_redundant_backup")

    @property
    @pulumi.getter(name="storageAutogrow")
    def storage_autogrow(self) -> Optional[str]:
        """
        Enable Storage Auto Grow.
        """
        return pulumi.get(self, "storage_autogrow")

    @property
    @pulumi.getter(name="storageMB")
    def storage_mb(self) -> Optional[int]:
        """
        Max storage allowed for a server.
        """
        return pulumi.get(self, "storage_mb")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


