# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from ._enums import *

__all__ = [
    'DiskArgs',
    'HardwareProfileArgs',
    'IpAddressArgs',
    'NetworkProfileArgs',
    'OSProfileArgs',
    'StorageProfileArgs',
]

@pulumi.input_type
class DiskArgs:
    def __init__(__self__, *,
                 disk_size_gb: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Specifies the disk information fo the HANA instance
        :param pulumi.Input[int] disk_size_gb: Specifies the size of an empty data disk in gigabytes.
        :param pulumi.Input[str] name: The disk name.
        """
        if disk_size_gb is not None:
            pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the size of an empty data disk in gigabytes.
        """
        return pulumi.get(self, "disk_size_gb")

    @disk_size_gb.setter
    def disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "disk_size_gb", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The disk name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class HardwareProfileArgs:
    def __init__(__self__, *,
                 hana_instance_size: Optional[pulumi.Input[Union[str, 'HanaInstanceSizeNamesEnum']]] = None,
                 hardware_type: Optional[pulumi.Input[Union[str, 'HanaHardwareTypeNamesEnum']]] = None):
        """
        Specifies the hardware settings for the HANA instance.
        :param pulumi.Input[Union[str, 'HanaInstanceSizeNamesEnum']] hana_instance_size: Specifies the HANA instance SKU.
        :param pulumi.Input[Union[str, 'HanaHardwareTypeNamesEnum']] hardware_type: Name of the hardware type (vendor and/or their product name)
        """
        if hana_instance_size is not None:
            pulumi.set(__self__, "hana_instance_size", hana_instance_size)
        if hardware_type is not None:
            pulumi.set(__self__, "hardware_type", hardware_type)

    @property
    @pulumi.getter(name="hanaInstanceSize")
    def hana_instance_size(self) -> Optional[pulumi.Input[Union[str, 'HanaInstanceSizeNamesEnum']]]:
        """
        Specifies the HANA instance SKU.
        """
        return pulumi.get(self, "hana_instance_size")

    @hana_instance_size.setter
    def hana_instance_size(self, value: Optional[pulumi.Input[Union[str, 'HanaInstanceSizeNamesEnum']]]):
        pulumi.set(self, "hana_instance_size", value)

    @property
    @pulumi.getter(name="hardwareType")
    def hardware_type(self) -> Optional[pulumi.Input[Union[str, 'HanaHardwareTypeNamesEnum']]]:
        """
        Name of the hardware type (vendor and/or their product name)
        """
        return pulumi.get(self, "hardware_type")

    @hardware_type.setter
    def hardware_type(self, value: Optional[pulumi.Input[Union[str, 'HanaHardwareTypeNamesEnum']]]):
        pulumi.set(self, "hardware_type", value)


@pulumi.input_type
class IpAddressArgs:
    def __init__(__self__, *,
                 ip_address: Optional[pulumi.Input[str]] = None):
        """
        Specifies the IP address of the network interface.
        :param pulumi.Input[str] ip_address: Specifies the IP address of the network interface.
        """
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the IP address of the network interface.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)


@pulumi.input_type
class NetworkProfileArgs:
    def __init__(__self__, *,
                 circuit_id: Optional[pulumi.Input[str]] = None,
                 network_interfaces: Optional[pulumi.Input[Sequence[pulumi.Input['IpAddressArgs']]]] = None):
        """
        Specifies the network settings for the HANA instance disks.
        :param pulumi.Input[str] circuit_id: Specifies the circuit id for connecting to express route.
        :param pulumi.Input[Sequence[pulumi.Input['IpAddressArgs']]] network_interfaces: Specifies the network interfaces for the HANA instance.
        """
        if circuit_id is not None:
            pulumi.set(__self__, "circuit_id", circuit_id)
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)

    @property
    @pulumi.getter(name="circuitId")
    def circuit_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the circuit id for connecting to express route.
        """
        return pulumi.get(self, "circuit_id")

    @circuit_id.setter
    def circuit_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "circuit_id", value)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IpAddressArgs']]]]:
        """
        Specifies the network interfaces for the HANA instance.
        """
        return pulumi.get(self, "network_interfaces")

    @network_interfaces.setter
    def network_interfaces(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IpAddressArgs']]]]):
        pulumi.set(self, "network_interfaces", value)


@pulumi.input_type
class OSProfileArgs:
    def __init__(__self__, *,
                 computer_name: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 ssh_public_key: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Specifies the operating system settings for the HANA instance.
        :param pulumi.Input[str] computer_name: Specifies the host OS name of the HANA instance.
        :param pulumi.Input[str] os_type: This property allows you to specify the type of the OS.
        :param pulumi.Input[str] ssh_public_key: Specifies the SSH public key used to access the operating system.
        :param pulumi.Input[str] version: Specifies version of operating system.
        """
        if computer_name is not None:
            pulumi.set(__self__, "computer_name", computer_name)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if ssh_public_key is not None:
            pulumi.set(__self__, "ssh_public_key", ssh_public_key)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="computerName")
    def computer_name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the host OS name of the HANA instance.
        """
        return pulumi.get(self, "computer_name")

    @computer_name.setter
    def computer_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "computer_name", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[str]]:
        """
        This property allows you to specify the type of the OS.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="sshPublicKey")
    def ssh_public_key(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the SSH public key used to access the operating system.
        """
        return pulumi.get(self, "ssh_public_key")

    @ssh_public_key.setter
    def ssh_public_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssh_public_key", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies version of operating system.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class StorageProfileArgs:
    def __init__(__self__, *,
                 nfs_ip_address: Optional[pulumi.Input[str]] = None,
                 os_disks: Optional[pulumi.Input[Sequence[pulumi.Input['DiskArgs']]]] = None):
        """
        Specifies the storage settings for the HANA instance disks.
        :param pulumi.Input[str] nfs_ip_address: IP Address to connect to storage.
        :param pulumi.Input[Sequence[pulumi.Input['DiskArgs']]] os_disks: Specifies information about the operating system disk used by the hana instance.
        """
        if nfs_ip_address is not None:
            pulumi.set(__self__, "nfs_ip_address", nfs_ip_address)
        if os_disks is not None:
            pulumi.set(__self__, "os_disks", os_disks)

    @property
    @pulumi.getter(name="nfsIpAddress")
    def nfs_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        IP Address to connect to storage.
        """
        return pulumi.get(self, "nfs_ip_address")

    @nfs_ip_address.setter
    def nfs_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nfs_ip_address", value)

    @property
    @pulumi.getter(name="osDisks")
    def os_disks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DiskArgs']]]]:
        """
        Specifies information about the operating system disk used by the hana instance.
        """
        return pulumi.get(self, "os_disks")

    @os_disks.setter
    def os_disks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DiskArgs']]]]):
        pulumi.set(self, "os_disks", value)


