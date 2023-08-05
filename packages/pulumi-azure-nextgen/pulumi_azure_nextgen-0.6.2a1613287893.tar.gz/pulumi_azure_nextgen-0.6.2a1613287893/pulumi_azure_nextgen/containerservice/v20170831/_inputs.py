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
    'ContainerServiceAgentPoolProfileArgs',
    'ContainerServiceLinuxProfileArgs',
    'ContainerServiceServicePrincipalProfileArgs',
    'ContainerServiceSshConfigurationArgs',
    'ContainerServiceSshPublicKeyArgs',
    'KeyVaultSecretRefArgs',
]

@pulumi.input_type
class ContainerServiceAgentPoolProfileArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 vm_size: pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']],
                 count: Optional[pulumi.Input[int]] = None,
                 dns_prefix: Optional[pulumi.Input[str]] = None,
                 os_disk_size_gb: Optional[pulumi.Input[int]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OSType']]] = None,
                 ports: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 storage_profile: Optional[pulumi.Input[Union[str, 'ContainerServiceStorageProfileTypes']]] = None,
                 vnet_subnet_id: Optional[pulumi.Input[str]] = None):
        """
        Profile for the container service agent pool.
        :param pulumi.Input[str] name: Unique name of the agent pool profile in the context of the subscription and resource group.
        :param pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']] vm_size: Size of agent VMs.
        :param pulumi.Input[int] count: Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        :param pulumi.Input[str] dns_prefix: DNS prefix to be used to create the FQDN for the agent pool.
        :param pulumi.Input[int] os_disk_size_gb: OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        :param pulumi.Input[Union[str, 'OSType']] os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] ports: Ports number array used to expose on this agent pool. The default opened ports are different based on your choice of orchestrator.
        :param pulumi.Input[Union[str, 'ContainerServiceStorageProfileTypes']] storage_profile: Storage profile specifies what kind of storage used. Choose from StorageAccount and ManagedDisks. Leave it empty, we will choose for you based on the orchestrator choice.
        :param pulumi.Input[str] vnet_subnet_id: VNet SubnetID specifies the VNet's subnet identifier.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "vm_size", vm_size)
        if count is None:
            count = 1
        if count is not None:
            pulumi.set(__self__, "count", count)
        if dns_prefix is not None:
            pulumi.set(__self__, "dns_prefix", dns_prefix)
        if os_disk_size_gb is not None:
            pulumi.set(__self__, "os_disk_size_gb", os_disk_size_gb)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if ports is not None:
            pulumi.set(__self__, "ports", ports)
        if storage_profile is not None:
            pulumi.set(__self__, "storage_profile", storage_profile)
        if vnet_subnet_id is not None:
            pulumi.set(__self__, "vnet_subnet_id", vnet_subnet_id)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name of the agent pool profile in the context of the subscription and resource group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]):
        pulumi.set(self, "vm_size", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter(name="dnsPrefix")
    def dns_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        DNS prefix to be used to create the FQDN for the agent pool.
        """
        return pulumi.get(self, "dns_prefix")

    @dns_prefix.setter
    def dns_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_prefix", value)

    @property
    @pulumi.getter(name="osDiskSizeGB")
    def os_disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        """
        return pulumi.get(self, "os_disk_size_gb")

    @os_disk_size_gb.setter
    def os_disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "os_disk_size_gb", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[Union[str, 'OSType']]]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[Union[str, 'OSType']]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        Ports number array used to expose on this agent pool. The default opened ports are different based on your choice of orchestrator.
        """
        return pulumi.get(self, "ports")

    @ports.setter
    def ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "ports", value)

    @property
    @pulumi.getter(name="storageProfile")
    def storage_profile(self) -> Optional[pulumi.Input[Union[str, 'ContainerServiceStorageProfileTypes']]]:
        """
        Storage profile specifies what kind of storage used. Choose from StorageAccount and ManagedDisks. Leave it empty, we will choose for you based on the orchestrator choice.
        """
        return pulumi.get(self, "storage_profile")

    @storage_profile.setter
    def storage_profile(self, value: Optional[pulumi.Input[Union[str, 'ContainerServiceStorageProfileTypes']]]):
        pulumi.set(self, "storage_profile", value)

    @property
    @pulumi.getter(name="vnetSubnetID")
    def vnet_subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        VNet SubnetID specifies the VNet's subnet identifier.
        """
        return pulumi.get(self, "vnet_subnet_id")

    @vnet_subnet_id.setter
    def vnet_subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vnet_subnet_id", value)


@pulumi.input_type
class ContainerServiceLinuxProfileArgs:
    def __init__(__self__, *,
                 admin_username: pulumi.Input[str],
                 ssh: pulumi.Input['ContainerServiceSshConfigurationArgs']):
        """
        Profile for Linux VMs in the container service cluster.
        :param pulumi.Input[str] admin_username: The administrator username to use for Linux VMs.
        :param pulumi.Input['ContainerServiceSshConfigurationArgs'] ssh: SSH configuration for Linux-based VMs running on Azure.
        """
        pulumi.set(__self__, "admin_username", admin_username)
        pulumi.set(__self__, "ssh", ssh)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> pulumi.Input[str]:
        """
        The administrator username to use for Linux VMs.
        """
        return pulumi.get(self, "admin_username")

    @admin_username.setter
    def admin_username(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_username", value)

    @property
    @pulumi.getter
    def ssh(self) -> pulumi.Input['ContainerServiceSshConfigurationArgs']:
        """
        SSH configuration for Linux-based VMs running on Azure.
        """
        return pulumi.get(self, "ssh")

    @ssh.setter
    def ssh(self, value: pulumi.Input['ContainerServiceSshConfigurationArgs']):
        pulumi.set(self, "ssh", value)


@pulumi.input_type
class ContainerServiceServicePrincipalProfileArgs:
    def __init__(__self__, *,
                 client_id: pulumi.Input[str],
                 key_vault_secret_ref: Optional[pulumi.Input['KeyVaultSecretRefArgs']] = None,
                 secret: Optional[pulumi.Input[str]] = None):
        """
        Information about a service principal identity for the cluster to use for manipulating Azure APIs. Either secret or keyVaultSecretRef must be specified.
        :param pulumi.Input[str] client_id: The ID for the service principal.
        :param pulumi.Input['KeyVaultSecretRefArgs'] key_vault_secret_ref: Reference to a secret stored in Azure Key Vault.
        :param pulumi.Input[str] secret: The secret password associated with the service principal in plain text.
        """
        pulumi.set(__self__, "client_id", client_id)
        if key_vault_secret_ref is not None:
            pulumi.set(__self__, "key_vault_secret_ref", key_vault_secret_ref)
        if secret is not None:
            pulumi.set(__self__, "secret", secret)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Input[str]:
        """
        The ID for the service principal.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="keyVaultSecretRef")
    def key_vault_secret_ref(self) -> Optional[pulumi.Input['KeyVaultSecretRefArgs']]:
        """
        Reference to a secret stored in Azure Key Vault.
        """
        return pulumi.get(self, "key_vault_secret_ref")

    @key_vault_secret_ref.setter
    def key_vault_secret_ref(self, value: Optional[pulumi.Input['KeyVaultSecretRefArgs']]):
        pulumi.set(self, "key_vault_secret_ref", value)

    @property
    @pulumi.getter
    def secret(self) -> Optional[pulumi.Input[str]]:
        """
        The secret password associated with the service principal in plain text.
        """
        return pulumi.get(self, "secret")

    @secret.setter
    def secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secret", value)


@pulumi.input_type
class ContainerServiceSshConfigurationArgs:
    def __init__(__self__, *,
                 public_keys: pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]):
        """
        SSH configuration for Linux-based VMs running on Azure.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]] public_keys: The list of SSH public keys used to authenticate with Linux-based VMs. Only expect one key specified.
        """
        pulumi.set(__self__, "public_keys", public_keys)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]:
        """
        The list of SSH public keys used to authenticate with Linux-based VMs. Only expect one key specified.
        """
        return pulumi.get(self, "public_keys")

    @public_keys.setter
    def public_keys(self, value: pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]):
        pulumi.set(self, "public_keys", value)


@pulumi.input_type
class ContainerServiceSshPublicKeyArgs:
    def __init__(__self__, *,
                 key_data: pulumi.Input[str]):
        """
        Contains information about SSH certificate public key data.
        :param pulumi.Input[str] key_data: Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or without headers.
        """
        pulumi.set(__self__, "key_data", key_data)

    @property
    @pulumi.getter(name="keyData")
    def key_data(self) -> pulumi.Input[str]:
        """
        Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or without headers.
        """
        return pulumi.get(self, "key_data")

    @key_data.setter
    def key_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_data", value)


@pulumi.input_type
class KeyVaultSecretRefArgs:
    def __init__(__self__, *,
                 secret_name: pulumi.Input[str],
                 vault_id: pulumi.Input[str],
                 version: Optional[pulumi.Input[str]] = None):
        """
        Reference to a secret stored in Azure Key Vault.
        :param pulumi.Input[str] secret_name: The secret name.
        :param pulumi.Input[str] vault_id: Key vault identifier.
        :param pulumi.Input[str] version: The secret version.
        """
        pulumi.set(__self__, "secret_name", secret_name)
        pulumi.set(__self__, "vault_id", vault_id)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="secretName")
    def secret_name(self) -> pulumi.Input[str]:
        """
        The secret name.
        """
        return pulumi.get(self, "secret_name")

    @secret_name.setter
    def secret_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "secret_name", value)

    @property
    @pulumi.getter(name="vaultID")
    def vault_id(self) -> pulumi.Input[str]:
        """
        Key vault identifier.
        """
        return pulumi.get(self, "vault_id")

    @vault_id.setter
    def vault_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vault_id", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The secret version.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


