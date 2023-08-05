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
    'ContainerServiceDiagnosticsProfileArgs',
    'ContainerServiceLinuxProfileArgs',
    'ContainerServiceMasterProfileArgs',
    'ContainerServiceOrchestratorProfileArgs',
    'ContainerServiceSshConfigurationArgs',
    'ContainerServiceSshPublicKeyArgs',
    'ContainerServiceVMDiagnosticsArgs',
    'ContainerServiceWindowsProfileArgs',
]

@pulumi.input_type
class ContainerServiceAgentPoolProfileArgs:
    def __init__(__self__, *,
                 dns_prefix: pulumi.Input[str],
                 name: pulumi.Input[str],
                 count: Optional[pulumi.Input[int]] = None,
                 vm_size: Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]] = None):
        """
        Profile for container service agent pool
        :param pulumi.Input[str] dns_prefix: DNS prefix to be used to create FQDN for this agent pool
        :param pulumi.Input[str] name: Unique name of the agent pool profile within the context of the subscription and resource group
        :param pulumi.Input[int] count: No. of agents (VMs) that will host docker containers
        :param pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']] vm_size: Size of agent VMs
        """
        pulumi.set(__self__, "dns_prefix", dns_prefix)
        pulumi.set(__self__, "name", name)
        if count is not None:
            pulumi.set(__self__, "count", count)
        if vm_size is not None:
            pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter(name="dnsPrefix")
    def dns_prefix(self) -> pulumi.Input[str]:
        """
        DNS prefix to be used to create FQDN for this agent pool
        """
        return pulumi.get(self, "dns_prefix")

    @dns_prefix.setter
    def dns_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns_prefix", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Unique name of the agent pool profile within the context of the subscription and resource group
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        No. of agents (VMs) that will host docker containers
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]]:
        """
        Size of agent VMs
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: Optional[pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]]):
        pulumi.set(self, "vm_size", value)


@pulumi.input_type
class ContainerServiceDiagnosticsProfileArgs:
    def __init__(__self__, *,
                 vm_diagnostics: Optional[pulumi.Input['ContainerServiceVMDiagnosticsArgs']] = None):
        """
        :param pulumi.Input['ContainerServiceVMDiagnosticsArgs'] vm_diagnostics: Profile for container service VM diagnostic agent
        """
        if vm_diagnostics is not None:
            pulumi.set(__self__, "vm_diagnostics", vm_diagnostics)

    @property
    @pulumi.getter(name="vmDiagnostics")
    def vm_diagnostics(self) -> Optional[pulumi.Input['ContainerServiceVMDiagnosticsArgs']]:
        """
        Profile for container service VM diagnostic agent
        """
        return pulumi.get(self, "vm_diagnostics")

    @vm_diagnostics.setter
    def vm_diagnostics(self, value: Optional[pulumi.Input['ContainerServiceVMDiagnosticsArgs']]):
        pulumi.set(self, "vm_diagnostics", value)


@pulumi.input_type
class ContainerServiceLinuxProfileArgs:
    def __init__(__self__, *,
                 admin_username: pulumi.Input[str],
                 ssh: pulumi.Input['ContainerServiceSshConfigurationArgs']):
        """
        Profile for Linux VM
        :param pulumi.Input[str] admin_username: The administrator username to use for all Linux VMs
        :param pulumi.Input['ContainerServiceSshConfigurationArgs'] ssh: Specifies the ssh key configuration for Linux VMs
        """
        pulumi.set(__self__, "admin_username", admin_username)
        pulumi.set(__self__, "ssh", ssh)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> pulumi.Input[str]:
        """
        The administrator username to use for all Linux VMs
        """
        return pulumi.get(self, "admin_username")

    @admin_username.setter
    def admin_username(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_username", value)

    @property
    @pulumi.getter
    def ssh(self) -> pulumi.Input['ContainerServiceSshConfigurationArgs']:
        """
        Specifies the ssh key configuration for Linux VMs
        """
        return pulumi.get(self, "ssh")

    @ssh.setter
    def ssh(self, value: pulumi.Input['ContainerServiceSshConfigurationArgs']):
        pulumi.set(self, "ssh", value)


@pulumi.input_type
class ContainerServiceMasterProfileArgs:
    def __init__(__self__, *,
                 dns_prefix: pulumi.Input[str],
                 count: Optional[pulumi.Input[int]] = None):
        """
        Profile for container service master
        :param pulumi.Input[str] dns_prefix: DNS prefix to be used to create FQDN for master
        :param pulumi.Input[int] count: Number of masters (VMs) in the container cluster
        """
        pulumi.set(__self__, "dns_prefix", dns_prefix)
        if count is not None:
            pulumi.set(__self__, "count", count)

    @property
    @pulumi.getter(name="dnsPrefix")
    def dns_prefix(self) -> pulumi.Input[str]:
        """
        DNS prefix to be used to create FQDN for master
        """
        return pulumi.get(self, "dns_prefix")

    @dns_prefix.setter
    def dns_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns_prefix", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of masters (VMs) in the container cluster
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)


@pulumi.input_type
class ContainerServiceOrchestratorProfileArgs:
    def __init__(__self__, *,
                 orchestrator_type: Optional[pulumi.Input['ContainerServiceOchestratorTypes']] = None):
        """
        Profile for Orchestrator
        :param pulumi.Input['ContainerServiceOchestratorTypes'] orchestrator_type: Specifies what orchestrator will be used to manage container cluster resources.
        """
        if orchestrator_type is not None:
            pulumi.set(__self__, "orchestrator_type", orchestrator_type)

    @property
    @pulumi.getter(name="orchestratorType")
    def orchestrator_type(self) -> Optional[pulumi.Input['ContainerServiceOchestratorTypes']]:
        """
        Specifies what orchestrator will be used to manage container cluster resources.
        """
        return pulumi.get(self, "orchestrator_type")

    @orchestrator_type.setter
    def orchestrator_type(self, value: Optional[pulumi.Input['ContainerServiceOchestratorTypes']]):
        pulumi.set(self, "orchestrator_type", value)


@pulumi.input_type
class ContainerServiceSshConfigurationArgs:
    def __init__(__self__, *,
                 public_keys: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]] = None):
        """
        SSH configuration for Linux based VMs running on Azure
        :param pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]] public_keys: Gets or sets the list of SSH public keys used to authenticate with Linux based VMs
        """
        if public_keys is not None:
            pulumi.set(__self__, "public_keys", public_keys)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]]:
        """
        Gets or sets the list of SSH public keys used to authenticate with Linux based VMs
        """
        return pulumi.get(self, "public_keys")

    @public_keys.setter
    def public_keys(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]]):
        pulumi.set(self, "public_keys", value)


@pulumi.input_type
class ContainerServiceSshPublicKeyArgs:
    def __init__(__self__, *,
                 key_data: pulumi.Input[str]):
        """
        Contains information about SSH certificate public key data.
        :param pulumi.Input[str] key_data: Gets or sets Certificate public key used to authenticate with VM through SSH. The certificate must be in Pem format with or without headers.
        """
        pulumi.set(__self__, "key_data", key_data)

    @property
    @pulumi.getter(name="keyData")
    def key_data(self) -> pulumi.Input[str]:
        """
        Gets or sets Certificate public key used to authenticate with VM through SSH. The certificate must be in Pem format with or without headers.
        """
        return pulumi.get(self, "key_data")

    @key_data.setter
    def key_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_data", value)


@pulumi.input_type
class ContainerServiceVMDiagnosticsArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None):
        """
        Describes VM Diagnostics.
        :param pulumi.Input[bool] enabled: Gets or sets whether VM Diagnostic Agent should be provisioned on the Virtual Machine.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Gets or sets whether VM Diagnostic Agent should be provisioned on the Virtual Machine.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class ContainerServiceWindowsProfileArgs:
    def __init__(__self__, *,
                 admin_password: pulumi.Input[str],
                 admin_username: pulumi.Input[str]):
        """
        Profile for Windows jumpbox
        :param pulumi.Input[str] admin_password: The administrator password to use for Windows jumpbox
        :param pulumi.Input[str] admin_username: The administrator username to use for Windows jumpbox
        """
        pulumi.set(__self__, "admin_password", admin_password)
        pulumi.set(__self__, "admin_username", admin_username)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> pulumi.Input[str]:
        """
        The administrator password to use for Windows jumpbox
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> pulumi.Input[str]:
        """
        The administrator username to use for Windows jumpbox
        """
        return pulumi.get(self, "admin_username")

    @admin_username.setter
    def admin_username(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_username", value)


