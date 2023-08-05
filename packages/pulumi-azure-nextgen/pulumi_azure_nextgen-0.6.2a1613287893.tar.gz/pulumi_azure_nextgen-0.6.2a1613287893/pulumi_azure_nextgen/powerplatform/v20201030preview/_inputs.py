# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = [
    'EnterprisePolicyIdentityArgs',
    'KeyPropertiesArgs',
    'KeyVaultPropertiesArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'PropertiesEncryptionArgs',
]

@pulumi.input_type
class EnterprisePolicyIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        The identity of the EnterprisePolicy.
        :param pulumi.Input['ResourceIdentityType'] type: The type of identity used for the EnterprisePolicy. Currently, the only supported type is 'SystemAssigned', which implicitly creates an identity.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The type of identity used for the EnterprisePolicy. Currently, the only supported type is 'SystemAssigned', which implicitly creates an identity.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class KeyPropertiesArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Url and version of the KeyVault Secret
        :param pulumi.Input[str] name: The identifier of the key vault key used to encrypt data.
        :param pulumi.Input[str] version: The version of the identity which will be used to access key vault.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the key vault key used to encrypt data.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the identity which will be used to access key vault.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class KeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input['KeyPropertiesArgs']] = None):
        """
        Settings concerning key vault encryption for a configuration store.
        :param pulumi.Input[str] id: Uri of KeyVault
        :param pulumi.Input['KeyPropertiesArgs'] key: Identity of the secret that includes name and version.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if key is not None:
            pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Uri of KeyVault
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input['KeyPropertiesArgs']]:
        """
        Identity of the secret that includes name and version.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input['KeyPropertiesArgs']]):
        pulumi.set(self, "key", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class PropertiesEncryptionArgs:
    def __init__(__self__, *,
                 key_vault_properties: Optional[pulumi.Input['KeyVaultPropertiesArgs']] = None):
        """
        The encryption settings for a configuration store.
        :param pulumi.Input['KeyVaultPropertiesArgs'] key_vault_properties: Key vault properties.
        """
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional[pulumi.Input['KeyVaultPropertiesArgs']]:
        """
        Key vault properties.
        """
        return pulumi.get(self, "key_vault_properties")

    @key_vault_properties.setter
    def key_vault_properties(self, value: Optional[pulumi.Input['KeyVaultPropertiesArgs']]):
        pulumi.set(self, "key_vault_properties", value)


