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
    'ContainerServiceCustomProfileArgs',
    'ContainerServiceDiagnosticsProfileArgs',
    'ContainerServiceLinuxProfileArgs',
    'ContainerServiceMasterProfileArgs',
    'ContainerServiceOrchestratorProfileArgs',
    'ContainerServiceServicePrincipalProfileArgs',
    'ContainerServiceSshConfigurationArgs',
    'ContainerServiceSshPublicKeyArgs',
    'ContainerServiceVMDiagnosticsArgs',
    'ContainerServiceWindowsProfileArgs',
]

@pulumi.input_type
class ContainerServiceAgentPoolProfileArgs:
    def __init__(__self__, *,
                 count: pulumi.Input[int],
                 dns_prefix: pulumi.Input[str],
                 name: pulumi.Input[str],
                 vm_size: pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']]):
        """
        Profile for the container service agent pool.
        :param pulumi.Input[int] count: Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        :param pulumi.Input[str] dns_prefix: DNS prefix to be used to create the FQDN for the agent pool.
        :param pulumi.Input[str] name: Unique name of the agent pool profile in the context of the subscription and resource group.
        :param pulumi.Input[Union[str, 'ContainerServiceVMSizeTypes']] vm_size: Size of agent VMs.
        """
        if count is None:
            count = 1
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "dns_prefix", dns_prefix)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter
    def count(self) -> pulumi.Input[int]:
        """
        Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: pulumi.Input[int]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter(name="dnsPrefix")
    def dns_prefix(self) -> pulumi.Input[str]:
        """
        DNS prefix to be used to create the FQDN for the agent pool.
        """
        return pulumi.get(self, "dns_prefix")

    @dns_prefix.setter
    def dns_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns_prefix", value)

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


@pulumi.input_type
class ContainerServiceCustomProfileArgs:
    def __init__(__self__, *,
                 orchestrator: pulumi.Input[str]):
        """
        Properties to configure a custom container service cluster.
        :param pulumi.Input[str] orchestrator: The name of the custom orchestrator to use.
        """
        pulumi.set(__self__, "orchestrator", orchestrator)

    @property
    @pulumi.getter
    def orchestrator(self) -> pulumi.Input[str]:
        """
        The name of the custom orchestrator to use.
        """
        return pulumi.get(self, "orchestrator")

    @orchestrator.setter
    def orchestrator(self, value: pulumi.Input[str]):
        pulumi.set(self, "orchestrator", value)


@pulumi.input_type
class ContainerServiceDiagnosticsProfileArgs:
    def __init__(__self__, *,
                 vm_diagnostics: pulumi.Input['ContainerServiceVMDiagnosticsArgs']):
        """
        :param pulumi.Input['ContainerServiceVMDiagnosticsArgs'] vm_diagnostics: Profile for the container service VM diagnostic agent.
        """
        pulumi.set(__self__, "vm_diagnostics", vm_diagnostics)

    @property
    @pulumi.getter(name="vmDiagnostics")
    def vm_diagnostics(self) -> pulumi.Input['ContainerServiceVMDiagnosticsArgs']:
        """
        Profile for the container service VM diagnostic agent.
        """
        return pulumi.get(self, "vm_diagnostics")

    @vm_diagnostics.setter
    def vm_diagnostics(self, value: pulumi.Input['ContainerServiceVMDiagnosticsArgs']):
        pulumi.set(self, "vm_diagnostics", value)


@pulumi.input_type
class ContainerServiceLinuxProfileArgs:
    def __init__(__self__, *,
                 admin_username: pulumi.Input[str],
                 ssh: pulumi.Input['ContainerServiceSshConfigurationArgs']):
        """
        Profile for Linux VMs in the container service cluster.
        :param pulumi.Input[str] admin_username: The administrator username to use for Linux VMs.
        :param pulumi.Input['ContainerServiceSshConfigurationArgs'] ssh: The ssh key configuration for Linux VMs.
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
        The ssh key configuration for Linux VMs.
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
        Profile for the container service master.
        :param pulumi.Input[str] dns_prefix: DNS prefix to be used to create the FQDN for master.
        :param pulumi.Input[int] count: Number of masters (VMs) in the container service cluster. Allowed values are 1, 3, and 5. The default value is 1.
        """
        pulumi.set(__self__, "dns_prefix", dns_prefix)
        if count is None:
            count = 1
        if count is not None:
            pulumi.set(__self__, "count", count)

    @property
    @pulumi.getter(name="dnsPrefix")
    def dns_prefix(self) -> pulumi.Input[str]:
        """
        DNS prefix to be used to create the FQDN for master.
        """
        return pulumi.get(self, "dns_prefix")

    @dns_prefix.setter
    def dns_prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns_prefix", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of masters (VMs) in the container service cluster. Allowed values are 1, 3, and 5. The default value is 1.
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)


@pulumi.input_type
class ContainerServiceOrchestratorProfileArgs:
    def __init__(__self__, *,
                 orchestrator_type: pulumi.Input['ContainerServiceOrchestratorTypes']):
        """
        Profile for the container service orchestrator.
        :param pulumi.Input['ContainerServiceOrchestratorTypes'] orchestrator_type: The orchestrator to use to manage container service cluster resources. Valid values are Swarm, DCOS, and Custom.
        """
        pulumi.set(__self__, "orchestrator_type", orchestrator_type)

    @property
    @pulumi.getter(name="orchestratorType")
    def orchestrator_type(self) -> pulumi.Input['ContainerServiceOrchestratorTypes']:
        """
        The orchestrator to use to manage container service cluster resources. Valid values are Swarm, DCOS, and Custom.
        """
        return pulumi.get(self, "orchestrator_type")

    @orchestrator_type.setter
    def orchestrator_type(self, value: pulumi.Input['ContainerServiceOrchestratorTypes']):
        pulumi.set(self, "orchestrator_type", value)


@pulumi.input_type
class ContainerServiceServicePrincipalProfileArgs:
    def __init__(__self__, *,
                 client_id: pulumi.Input[str],
                 secret: pulumi.Input[str]):
        """
        Information about a service principal identity for the cluster to use for manipulating Azure APIs.
        :param pulumi.Input[str] client_id: The ID for the service principal.
        :param pulumi.Input[str] secret: The secret password associated with the service principal.
        """
        pulumi.set(__self__, "client_id", client_id)
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
    @pulumi.getter
    def secret(self) -> pulumi.Input[str]:
        """
        The secret password associated with the service principal.
        """
        return pulumi.get(self, "secret")

    @secret.setter
    def secret(self, value: pulumi.Input[str]):
        pulumi.set(self, "secret", value)


@pulumi.input_type
class ContainerServiceSshConfigurationArgs:
    def __init__(__self__, *,
                 public_keys: pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]):
        """
        SSH configuration for Linux-based VMs running on Azure.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]] public_keys: the list of SSH public keys used to authenticate with Linux-based VMs.
        """
        pulumi.set(__self__, "public_keys", public_keys)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> pulumi.Input[Sequence[pulumi.Input['ContainerServiceSshPublicKeyArgs']]]:
        """
        the list of SSH public keys used to authenticate with Linux-based VMs.
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
class ContainerServiceVMDiagnosticsArgs:
    def __init__(__self__, *,
                 enabled: pulumi.Input[bool]):
        """
        Profile for diagnostics on the container service VMs.
        :param pulumi.Input[bool] enabled: Whether the VM diagnostic agent is provisioned on the VM.
        """
        pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        """
        Whether the VM diagnostic agent is provisioned on the VM.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class ContainerServiceWindowsProfileArgs:
    def __init__(__self__, *,
                 admin_password: pulumi.Input[str],
                 admin_username: pulumi.Input[str]):
        """
        Profile for Windows VMs in the container service cluster.
        :param pulumi.Input[str] admin_password: The administrator password to use for Windows VMs.
        :param pulumi.Input[str] admin_username: The administrator username to use for Windows VMs.
        """
        pulumi.set(__self__, "admin_password", admin_password)
        pulumi.set(__self__, "admin_username", admin_username)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> pulumi.Input[str]:
        """
        The administrator password to use for Windows VMs.
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> pulumi.Input[str]:
        """
        The administrator username to use for Windows VMs.
        """
        return pulumi.get(self, "admin_username")

    @admin_username.setter
    def admin_username(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_username", value)


