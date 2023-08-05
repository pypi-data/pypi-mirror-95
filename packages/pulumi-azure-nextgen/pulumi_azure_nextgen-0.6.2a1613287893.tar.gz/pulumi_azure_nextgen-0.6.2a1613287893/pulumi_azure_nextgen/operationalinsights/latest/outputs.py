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
    'AssociatedWorkspaceResponse',
    'CapacityReservationPropertiesResponse',
    'ClusterSkuResponse',
    'IdentityResponse',
    'KeyVaultPropertiesResponse',
    'PrivateLinkScopedResourceResponse',
    'StorageAccountResponse',
    'StorageInsightStatusResponse',
    'TagResponse',
    'UserIdentityPropertiesResponse',
    'WorkspaceCappingResponse',
    'WorkspaceSkuResponse',
]

@pulumi.output_type
class AssociatedWorkspaceResponse(dict):
    """
    The list of Log Analytics workspaces associated with the cluster.
    """
    def __init__(__self__, *,
                 associate_date: str,
                 resource_id: str,
                 workspace_id: str,
                 workspace_name: str):
        """
        The list of Log Analytics workspaces associated with the cluster.
        :param str associate_date: The time of workspace association.
        :param str resource_id: The ResourceId id the assigned workspace.
        :param str workspace_id: The id of the assigned workspace.
        :param str workspace_name: The name id the assigned workspace.
        """
        pulumi.set(__self__, "associate_date", associate_date)
        pulumi.set(__self__, "resource_id", resource_id)
        pulumi.set(__self__, "workspace_id", workspace_id)
        pulumi.set(__self__, "workspace_name", workspace_name)

    @property
    @pulumi.getter(name="associateDate")
    def associate_date(self) -> str:
        """
        The time of workspace association.
        """
        return pulumi.get(self, "associate_date")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        The ResourceId id the assigned workspace.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        The id of the assigned workspace.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> str:
        """
        The name id the assigned workspace.
        """
        return pulumi.get(self, "workspace_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class CapacityReservationPropertiesResponse(dict):
    """
    The Capacity Reservation properties.
    """
    def __init__(__self__, *,
                 last_sku_update: str,
                 max_capacity: float,
                 min_capacity: float):
        """
        The Capacity Reservation properties.
        :param str last_sku_update: The last time Sku was updated.
        :param float max_capacity: Maximum CapacityReservation value in GB.
        :param float min_capacity: Minimum CapacityReservation value in GB.
        """
        pulumi.set(__self__, "last_sku_update", last_sku_update)
        pulumi.set(__self__, "max_capacity", max_capacity)
        pulumi.set(__self__, "min_capacity", min_capacity)

    @property
    @pulumi.getter(name="lastSkuUpdate")
    def last_sku_update(self) -> str:
        """
        The last time Sku was updated.
        """
        return pulumi.get(self, "last_sku_update")

    @property
    @pulumi.getter(name="maxCapacity")
    def max_capacity(self) -> float:
        """
        Maximum CapacityReservation value in GB.
        """
        return pulumi.get(self, "max_capacity")

    @property
    @pulumi.getter(name="minCapacity")
    def min_capacity(self) -> float:
        """
        Minimum CapacityReservation value in GB.
        """
        return pulumi.get(self, "min_capacity")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ClusterSkuResponse(dict):
    """
    The cluster sku definition.
    """
    def __init__(__self__, *,
                 capacity: Optional[float] = None,
                 name: Optional[str] = None):
        """
        The cluster sku definition.
        :param float capacity: The capacity value
        :param str name: The name of the SKU.
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[float]:
        """
        The capacity value
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IdentityResponse(dict):
    """
    Identity for the resource.
    """
    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.UserIdentityPropertiesResponse']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: Type of managed service identity.
        :param Mapping[str, 'UserIdentityPropertiesResponseArgs'] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of managed service identity.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.UserIdentityPropertiesResponse']]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class KeyVaultPropertiesResponse(dict):
    """
    The key vault properties.
    """
    def __init__(__self__, *,
                 key_name: Optional[str] = None,
                 key_rsa_size: Optional[int] = None,
                 key_vault_uri: Optional[str] = None,
                 key_version: Optional[str] = None):
        """
        The key vault properties.
        :param str key_name: The name of the key associated with the Log Analytics cluster.
        :param int key_rsa_size: Selected key minimum required size.
        :param str key_vault_uri: The Key Vault uri which holds they key associated with the Log Analytics cluster.
        :param str key_version: The version of the key associated with the Log Analytics cluster.
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_rsa_size is not None:
            pulumi.set(__self__, "key_rsa_size", key_rsa_size)
        if key_vault_uri is not None:
            pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[str]:
        """
        The name of the key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keyRsaSize")
    def key_rsa_size(self) -> Optional[int]:
        """
        Selected key minimum required size.
        """
        return pulumi.get(self, "key_rsa_size")

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> Optional[str]:
        """
        The Key Vault uri which holds they key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_vault_uri")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[str]:
        """
        The version of the key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_version")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class PrivateLinkScopedResourceResponse(dict):
    """
    The private link scope resource reference.
    """
    def __init__(__self__, *,
                 resource_id: Optional[str] = None,
                 scope_id: Optional[str] = None):
        """
        The private link scope resource reference.
        :param str resource_id: The full resource Id of the private link scope resource.
        :param str scope_id: The private link scope unique Identifier.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if scope_id is not None:
            pulumi.set(__self__, "scope_id", scope_id)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The full resource Id of the private link scope resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="scopeId")
    def scope_id(self) -> Optional[str]:
        """
        The private link scope unique Identifier.
        """
        return pulumi.get(self, "scope_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StorageAccountResponse(dict):
    """
    Describes a storage account connection.
    """
    def __init__(__self__, *,
                 id: str,
                 key: str):
        """
        Describes a storage account connection.
        :param str id: The Azure Resource Manager ID of the storage account resource.
        :param str key: The storage account key.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The Azure Resource Manager ID of the storage account resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The storage account key.
        """
        return pulumi.get(self, "key")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class StorageInsightStatusResponse(dict):
    """
    The status of the storage insight.
    """
    def __init__(__self__, *,
                 state: str,
                 description: Optional[str] = None):
        """
        The status of the storage insight.
        :param str state: The state of the storage insight connection to the workspace
        :param str description: Description of the state of the storage insight.
        """
        pulumi.set(__self__, "state", state)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the storage insight connection to the workspace
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the state of the storage insight.
        """
        return pulumi.get(self, "description")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class TagResponse(dict):
    """
    A tag of a saved search.
    """
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        A tag of a saved search.
        :param str name: The tag name.
        :param str value: The tag value.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The tag name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The tag value.
        """
        return pulumi.get(self, "value")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class UserIdentityPropertiesResponse(dict):
    """
    User assigned identity properties.
    """
    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        User assigned identity properties.
        :param str client_id: The client id of user assigned identity.
        :param str principal_id: The principal id of user assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WorkspaceCappingResponse(dict):
    """
    The daily volume cap for ingestion.
    """
    def __init__(__self__, *,
                 data_ingestion_status: str,
                 quota_next_reset_time: str,
                 daily_quota_gb: Optional[float] = None):
        """
        The daily volume cap for ingestion.
        :param str data_ingestion_status: The status of data ingestion for this workspace.
        :param str quota_next_reset_time: The time when the quota will be rest.
        :param float daily_quota_gb: The workspace daily quota for ingestion.
        """
        pulumi.set(__self__, "data_ingestion_status", data_ingestion_status)
        pulumi.set(__self__, "quota_next_reset_time", quota_next_reset_time)
        if daily_quota_gb is not None:
            pulumi.set(__self__, "daily_quota_gb", daily_quota_gb)

    @property
    @pulumi.getter(name="dataIngestionStatus")
    def data_ingestion_status(self) -> str:
        """
        The status of data ingestion for this workspace.
        """
        return pulumi.get(self, "data_ingestion_status")

    @property
    @pulumi.getter(name="quotaNextResetTime")
    def quota_next_reset_time(self) -> str:
        """
        The time when the quota will be rest.
        """
        return pulumi.get(self, "quota_next_reset_time")

    @property
    @pulumi.getter(name="dailyQuotaGb")
    def daily_quota_gb(self) -> Optional[float]:
        """
        The workspace daily quota for ingestion.
        """
        return pulumi.get(self, "daily_quota_gb")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WorkspaceSkuResponse(dict):
    """
    The SKU (tier) of a workspace.
    """
    def __init__(__self__, *,
                 last_sku_update: str,
                 max_capacity_reservation_level: int,
                 name: str,
                 capacity_reservation_level: Optional[int] = None):
        """
        The SKU (tier) of a workspace.
        :param str last_sku_update: The last time when the sku was updated.
        :param int max_capacity_reservation_level: The maximum capacity reservation level available for this workspace, when CapacityReservation sku is selected.
        :param str name: The name of the SKU.
        :param int capacity_reservation_level: The capacity reservation level for this workspace, when CapacityReservation sku is selected.
        """
        pulumi.set(__self__, "last_sku_update", last_sku_update)
        pulumi.set(__self__, "max_capacity_reservation_level", max_capacity_reservation_level)
        pulumi.set(__self__, "name", name)
        if capacity_reservation_level is not None:
            pulumi.set(__self__, "capacity_reservation_level", capacity_reservation_level)

    @property
    @pulumi.getter(name="lastSkuUpdate")
    def last_sku_update(self) -> str:
        """
        The last time when the sku was updated.
        """
        return pulumi.get(self, "last_sku_update")

    @property
    @pulumi.getter(name="maxCapacityReservationLevel")
    def max_capacity_reservation_level(self) -> int:
        """
        The maximum capacity reservation level available for this workspace, when CapacityReservation sku is selected.
        """
        return pulumi.get(self, "max_capacity_reservation_level")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="capacityReservationLevel")
    def capacity_reservation_level(self) -> Optional[int]:
        """
        The capacity reservation level for this workspace, when CapacityReservation sku is selected.
        """
        return pulumi.get(self, "capacity_reservation_level")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


