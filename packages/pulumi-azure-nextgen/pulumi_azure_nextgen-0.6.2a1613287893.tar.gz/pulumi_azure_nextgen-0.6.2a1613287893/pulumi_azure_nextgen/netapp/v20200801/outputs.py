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
    'ActiveDirectoryResponse',
    'DailyScheduleResponse',
    'ExportPolicyRuleResponse',
    'HourlyScheduleResponse',
    'MonthlyScheduleResponse',
    'MountTargetPropertiesResponse',
    'ReplicationObjectResponse',
    'VolumeBackupPropertiesResponse',
    'VolumeBackupsResponse',
    'VolumePropertiesResponseDataProtection',
    'VolumePropertiesResponseExportPolicy',
    'VolumeSnapshotPropertiesResponse',
    'WeeklyScheduleResponse',
]

@pulumi.output_type
class ActiveDirectoryResponse(dict):
    """
    Active Directory
    """
    def __init__(__self__, *,
                 status: str,
                 status_details: str,
                 active_directory_id: Optional[str] = None,
                 ad_name: Optional[str] = None,
                 aes_encryption: Optional[bool] = None,
                 backup_operators: Optional[Sequence[str]] = None,
                 dns: Optional[str] = None,
                 domain: Optional[str] = None,
                 kdc_ip: Optional[str] = None,
                 ldap_signing: Optional[bool] = None,
                 organizational_unit: Optional[str] = None,
                 password: Optional[str] = None,
                 server_root_ca_certificate: Optional[str] = None,
                 site: Optional[str] = None,
                 smb_server_name: Optional[str] = None,
                 username: Optional[str] = None):
        """
        Active Directory
        :param str status: Status of the Active Directory
        :param str status_details: Any details in regards to the Status of the Active Directory
        :param str active_directory_id: Id of the Active Directory
        :param str ad_name: Name of the active directory machine. This optional parameter is used only while creating kerberos volume
        :param bool aes_encryption: If enabled, AES encryption will be enabled for SMB communication.
        :param Sequence[str] backup_operators: Users to be added to the Built-in Backup Operator active directory group. A list of unique usernames without domain specifier
        :param str dns: Comma separated list of DNS server IP addresses (IPv4 only) for the Active Directory domain
        :param str domain: Name of the Active Directory domain
        :param str kdc_ip: kdc server IP addresses for the active directory machine. This optional parameter is used only while creating kerberos volume.
        :param bool ldap_signing: Specifies whether or not the LDAP traffic needs to be signed.
        :param str organizational_unit: The Organizational Unit (OU) within the Windows Active Directory
        :param str password: Plain text password of Active Directory domain administrator, value is masked in the response
        :param str server_root_ca_certificate: When LDAP over SSL/TLS is enabled, the LDAP client is required to have base64 encoded Active Directory Certificate Service's self-signed root CA certificate, this optional parameter is used only for dual protocol with LDAP user-mapping volumes.
        :param str site: The Active Directory site the service will limit Domain Controller discovery to
        :param str smb_server_name: NetBIOS name of the SMB server. This name will be registered as a computer account in the AD and used to mount volumes
        :param str username: Username of Active Directory domain administrator
        """
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "status_details", status_details)
        if active_directory_id is not None:
            pulumi.set(__self__, "active_directory_id", active_directory_id)
        if ad_name is not None:
            pulumi.set(__self__, "ad_name", ad_name)
        if aes_encryption is not None:
            pulumi.set(__self__, "aes_encryption", aes_encryption)
        if backup_operators is not None:
            pulumi.set(__self__, "backup_operators", backup_operators)
        if dns is not None:
            pulumi.set(__self__, "dns", dns)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if kdc_ip is not None:
            pulumi.set(__self__, "kdc_ip", kdc_ip)
        if ldap_signing is not None:
            pulumi.set(__self__, "ldap_signing", ldap_signing)
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if server_root_ca_certificate is not None:
            pulumi.set(__self__, "server_root_ca_certificate", server_root_ca_certificate)
        if site is not None:
            pulumi.set(__self__, "site", site)
        if smb_server_name is not None:
            pulumi.set(__self__, "smb_server_name", smb_server_name)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Active Directory
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusDetails")
    def status_details(self) -> str:
        """
        Any details in regards to the Status of the Active Directory
        """
        return pulumi.get(self, "status_details")

    @property
    @pulumi.getter(name="activeDirectoryId")
    def active_directory_id(self) -> Optional[str]:
        """
        Id of the Active Directory
        """
        return pulumi.get(self, "active_directory_id")

    @property
    @pulumi.getter(name="adName")
    def ad_name(self) -> Optional[str]:
        """
        Name of the active directory machine. This optional parameter is used only while creating kerberos volume
        """
        return pulumi.get(self, "ad_name")

    @property
    @pulumi.getter(name="aesEncryption")
    def aes_encryption(self) -> Optional[bool]:
        """
        If enabled, AES encryption will be enabled for SMB communication.
        """
        return pulumi.get(self, "aes_encryption")

    @property
    @pulumi.getter(name="backupOperators")
    def backup_operators(self) -> Optional[Sequence[str]]:
        """
        Users to be added to the Built-in Backup Operator active directory group. A list of unique usernames without domain specifier
        """
        return pulumi.get(self, "backup_operators")

    @property
    @pulumi.getter
    def dns(self) -> Optional[str]:
        """
        Comma separated list of DNS server IP addresses (IPv4 only) for the Active Directory domain
        """
        return pulumi.get(self, "dns")

    @property
    @pulumi.getter
    def domain(self) -> Optional[str]:
        """
        Name of the Active Directory domain
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="kdcIP")
    def kdc_ip(self) -> Optional[str]:
        """
        kdc server IP addresses for the active directory machine. This optional parameter is used only while creating kerberos volume.
        """
        return pulumi.get(self, "kdc_ip")

    @property
    @pulumi.getter(name="ldapSigning")
    def ldap_signing(self) -> Optional[bool]:
        """
        Specifies whether or not the LDAP traffic needs to be signed.
        """
        return pulumi.get(self, "ldap_signing")

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[str]:
        """
        The Organizational Unit (OU) within the Windows Active Directory
        """
        return pulumi.get(self, "organizational_unit")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        Plain text password of Active Directory domain administrator, value is masked in the response
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="serverRootCACertificate")
    def server_root_ca_certificate(self) -> Optional[str]:
        """
        When LDAP over SSL/TLS is enabled, the LDAP client is required to have base64 encoded Active Directory Certificate Service's self-signed root CA certificate, this optional parameter is used only for dual protocol with LDAP user-mapping volumes.
        """
        return pulumi.get(self, "server_root_ca_certificate")

    @property
    @pulumi.getter
    def site(self) -> Optional[str]:
        """
        The Active Directory site the service will limit Domain Controller discovery to
        """
        return pulumi.get(self, "site")

    @property
    @pulumi.getter(name="smbServerName")
    def smb_server_name(self) -> Optional[str]:
        """
        NetBIOS name of the SMB server. This name will be registered as a computer account in the AD and used to mount volumes
        """
        return pulumi.get(self, "smb_server_name")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username of Active Directory domain administrator
        """
        return pulumi.get(self, "username")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DailyScheduleResponse(dict):
    """
    Daily Schedule properties
    """
    def __init__(__self__, *,
                 hour: Optional[int] = None,
                 minute: Optional[int] = None,
                 snapshots_to_keep: Optional[int] = None,
                 used_bytes: Optional[float] = None):
        """
        Daily Schedule properties
        :param int hour: Indicates which hour in UTC timezone a snapshot should be taken
        :param int minute: Indicates which minute snapshot should be taken
        :param int snapshots_to_keep: Daily snapshot count to keep
        :param float used_bytes: Resource size in bytes, current storage usage for the volume in bytes
        """
        if hour is not None:
            pulumi.set(__self__, "hour", hour)
        if minute is not None:
            pulumi.set(__self__, "minute", minute)
        if snapshots_to_keep is not None:
            pulumi.set(__self__, "snapshots_to_keep", snapshots_to_keep)
        if used_bytes is not None:
            pulumi.set(__self__, "used_bytes", used_bytes)

    @property
    @pulumi.getter
    def hour(self) -> Optional[int]:
        """
        Indicates which hour in UTC timezone a snapshot should be taken
        """
        return pulumi.get(self, "hour")

    @property
    @pulumi.getter
    def minute(self) -> Optional[int]:
        """
        Indicates which minute snapshot should be taken
        """
        return pulumi.get(self, "minute")

    @property
    @pulumi.getter(name="snapshotsToKeep")
    def snapshots_to_keep(self) -> Optional[int]:
        """
        Daily snapshot count to keep
        """
        return pulumi.get(self, "snapshots_to_keep")

    @property
    @pulumi.getter(name="usedBytes")
    def used_bytes(self) -> Optional[float]:
        """
        Resource size in bytes, current storage usage for the volume in bytes
        """
        return pulumi.get(self, "used_bytes")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ExportPolicyRuleResponse(dict):
    """
    Volume Export Policy Rule
    """
    def __init__(__self__, *,
                 allowed_clients: Optional[str] = None,
                 cifs: Optional[bool] = None,
                 has_root_access: Optional[bool] = None,
                 kerberos5_read_only: Optional[bool] = None,
                 kerberos5_read_write: Optional[bool] = None,
                 kerberos5i_read_only: Optional[bool] = None,
                 kerberos5i_read_write: Optional[bool] = None,
                 kerberos5p_read_only: Optional[bool] = None,
                 kerberos5p_read_write: Optional[bool] = None,
                 nfsv3: Optional[bool] = None,
                 nfsv41: Optional[bool] = None,
                 rule_index: Optional[int] = None,
                 unix_read_only: Optional[bool] = None,
                 unix_read_write: Optional[bool] = None):
        """
        Volume Export Policy Rule
        :param str allowed_clients: Client ingress specification as comma separated string with IPv4 CIDRs, IPv4 host addresses and host names
        :param bool cifs: Allows CIFS protocol
        :param bool has_root_access: Has root access to volume
        :param bool kerberos5_read_only: Kerberos5 Read only access. To be use with swagger version 2020-05-01 or later
        :param bool kerberos5_read_write: Kerberos5 Read and write access. To be use with swagger version 2020-05-01 or later
        :param bool kerberos5i_read_only: Kerberos5i Read only access. To be use with swagger version 2020-05-01 or later
        :param bool kerberos5i_read_write: Kerberos5i Read and write access. To be use with swagger version 2020-05-01 or later
        :param bool kerberos5p_read_only: Kerberos5p Read only access. To be use with swagger version 2020-05-01 or later
        :param bool kerberos5p_read_write: Kerberos5p Read and write access. To be use with swagger version 2020-05-01 or later
        :param bool nfsv3: Allows NFSv3 protocol. Enable only for NFSv3 type volumes
        :param bool nfsv41: Allows NFSv4.1 protocol. Enable only for NFSv4.1 type volumes
        :param int rule_index: Order index
        :param bool unix_read_only: Read only access
        :param bool unix_read_write: Read and write access
        """
        if allowed_clients is not None:
            pulumi.set(__self__, "allowed_clients", allowed_clients)
        if cifs is not None:
            pulumi.set(__self__, "cifs", cifs)
        if has_root_access is None:
            has_root_access = True
        if has_root_access is not None:
            pulumi.set(__self__, "has_root_access", has_root_access)
        if kerberos5_read_only is None:
            kerberos5_read_only = False
        if kerberos5_read_only is not None:
            pulumi.set(__self__, "kerberos5_read_only", kerberos5_read_only)
        if kerberos5_read_write is None:
            kerberos5_read_write = False
        if kerberos5_read_write is not None:
            pulumi.set(__self__, "kerberos5_read_write", kerberos5_read_write)
        if kerberos5i_read_only is None:
            kerberos5i_read_only = False
        if kerberos5i_read_only is not None:
            pulumi.set(__self__, "kerberos5i_read_only", kerberos5i_read_only)
        if kerberos5i_read_write is None:
            kerberos5i_read_write = False
        if kerberos5i_read_write is not None:
            pulumi.set(__self__, "kerberos5i_read_write", kerberos5i_read_write)
        if kerberos5p_read_only is None:
            kerberos5p_read_only = False
        if kerberos5p_read_only is not None:
            pulumi.set(__self__, "kerberos5p_read_only", kerberos5p_read_only)
        if kerberos5p_read_write is None:
            kerberos5p_read_write = False
        if kerberos5p_read_write is not None:
            pulumi.set(__self__, "kerberos5p_read_write", kerberos5p_read_write)
        if nfsv3 is not None:
            pulumi.set(__self__, "nfsv3", nfsv3)
        if nfsv41 is not None:
            pulumi.set(__self__, "nfsv41", nfsv41)
        if rule_index is not None:
            pulumi.set(__self__, "rule_index", rule_index)
        if unix_read_only is not None:
            pulumi.set(__self__, "unix_read_only", unix_read_only)
        if unix_read_write is not None:
            pulumi.set(__self__, "unix_read_write", unix_read_write)

    @property
    @pulumi.getter(name="allowedClients")
    def allowed_clients(self) -> Optional[str]:
        """
        Client ingress specification as comma separated string with IPv4 CIDRs, IPv4 host addresses and host names
        """
        return pulumi.get(self, "allowed_clients")

    @property
    @pulumi.getter
    def cifs(self) -> Optional[bool]:
        """
        Allows CIFS protocol
        """
        return pulumi.get(self, "cifs")

    @property
    @pulumi.getter(name="hasRootAccess")
    def has_root_access(self) -> Optional[bool]:
        """
        Has root access to volume
        """
        return pulumi.get(self, "has_root_access")

    @property
    @pulumi.getter(name="kerberos5ReadOnly")
    def kerberos5_read_only(self) -> Optional[bool]:
        """
        Kerberos5 Read only access. To be use with swagger version 2020-05-01 or later
        """
        return pulumi.get(self, "kerberos5_read_only")

    @property
    @pulumi.getter(name="kerberos5ReadWrite")
    def kerberos5_read_write(self) -> Optional[bool]:
        """
        Kerberos5 Read and write access. To be use with swagger version 2020-05-01 or later
        """
        return pulumi.get(self, "kerberos5_read_write")

    @property
    @pulumi.getter(name="kerberos5iReadOnly")
    def kerberos5i_read_only(self) -> Optional[bool]:
        """
        Kerberos5i Read only access. To be use with swagger version 2020-05-01 or later
        """
        return pulumi.get(self, "kerberos5i_read_only")

    @property
    @pulumi.getter(name="kerberos5iReadWrite")
    def kerberos5i_read_write(self) -> Optional[bool]:
        """
        Kerberos5i Read and write access. To be use with swagger version 2020-05-01 or later
        """
        return pulumi.get(self, "kerberos5i_read_write")

    @property
    @pulumi.getter(name="kerberos5pReadOnly")
    def kerberos5p_read_only(self) -> Optional[bool]:
        """
        Kerberos5p Read only access. To be use with swagger version 2020-05-01 or later
        """
        return pulumi.get(self, "kerberos5p_read_only")

    @property
    @pulumi.getter(name="kerberos5pReadWrite")
    def kerberos5p_read_write(self) -> Optional[bool]:
        """
        Kerberos5p Read and write access. To be use with swagger version 2020-05-01 or later
        """
        return pulumi.get(self, "kerberos5p_read_write")

    @property
    @pulumi.getter
    def nfsv3(self) -> Optional[bool]:
        """
        Allows NFSv3 protocol. Enable only for NFSv3 type volumes
        """
        return pulumi.get(self, "nfsv3")

    @property
    @pulumi.getter
    def nfsv41(self) -> Optional[bool]:
        """
        Allows NFSv4.1 protocol. Enable only for NFSv4.1 type volumes
        """
        return pulumi.get(self, "nfsv41")

    @property
    @pulumi.getter(name="ruleIndex")
    def rule_index(self) -> Optional[int]:
        """
        Order index
        """
        return pulumi.get(self, "rule_index")

    @property
    @pulumi.getter(name="unixReadOnly")
    def unix_read_only(self) -> Optional[bool]:
        """
        Read only access
        """
        return pulumi.get(self, "unix_read_only")

    @property
    @pulumi.getter(name="unixReadWrite")
    def unix_read_write(self) -> Optional[bool]:
        """
        Read and write access
        """
        return pulumi.get(self, "unix_read_write")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class HourlyScheduleResponse(dict):
    """
    Hourly Schedule properties
    """
    def __init__(__self__, *,
                 minute: Optional[int] = None,
                 snapshots_to_keep: Optional[int] = None,
                 used_bytes: Optional[float] = None):
        """
        Hourly Schedule properties
        :param int minute: Indicates which minute snapshot should be taken
        :param int snapshots_to_keep: Hourly snapshot count to keep
        :param float used_bytes: Resource size in bytes, current storage usage for the volume in bytes
        """
        if minute is not None:
            pulumi.set(__self__, "minute", minute)
        if snapshots_to_keep is not None:
            pulumi.set(__self__, "snapshots_to_keep", snapshots_to_keep)
        if used_bytes is not None:
            pulumi.set(__self__, "used_bytes", used_bytes)

    @property
    @pulumi.getter
    def minute(self) -> Optional[int]:
        """
        Indicates which minute snapshot should be taken
        """
        return pulumi.get(self, "minute")

    @property
    @pulumi.getter(name="snapshotsToKeep")
    def snapshots_to_keep(self) -> Optional[int]:
        """
        Hourly snapshot count to keep
        """
        return pulumi.get(self, "snapshots_to_keep")

    @property
    @pulumi.getter(name="usedBytes")
    def used_bytes(self) -> Optional[float]:
        """
        Resource size in bytes, current storage usage for the volume in bytes
        """
        return pulumi.get(self, "used_bytes")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MonthlyScheduleResponse(dict):
    """
    Monthly Schedule properties
    """
    def __init__(__self__, *,
                 days_of_month: Optional[str] = None,
                 hour: Optional[int] = None,
                 minute: Optional[int] = None,
                 snapshots_to_keep: Optional[int] = None,
                 used_bytes: Optional[float] = None):
        """
        Monthly Schedule properties
        :param str days_of_month: Indicates which days of the month snapshot should be taken. A comma delimited string.
        :param int hour: Indicates which hour in UTC timezone a snapshot should be taken
        :param int minute: Indicates which minute snapshot should be taken
        :param int snapshots_to_keep: Monthly snapshot count to keep
        :param float used_bytes: Resource size in bytes, current storage usage for the volume in bytes
        """
        if days_of_month is not None:
            pulumi.set(__self__, "days_of_month", days_of_month)
        if hour is not None:
            pulumi.set(__self__, "hour", hour)
        if minute is not None:
            pulumi.set(__self__, "minute", minute)
        if snapshots_to_keep is not None:
            pulumi.set(__self__, "snapshots_to_keep", snapshots_to_keep)
        if used_bytes is not None:
            pulumi.set(__self__, "used_bytes", used_bytes)

    @property
    @pulumi.getter(name="daysOfMonth")
    def days_of_month(self) -> Optional[str]:
        """
        Indicates which days of the month snapshot should be taken. A comma delimited string.
        """
        return pulumi.get(self, "days_of_month")

    @property
    @pulumi.getter
    def hour(self) -> Optional[int]:
        """
        Indicates which hour in UTC timezone a snapshot should be taken
        """
        return pulumi.get(self, "hour")

    @property
    @pulumi.getter
    def minute(self) -> Optional[int]:
        """
        Indicates which minute snapshot should be taken
        """
        return pulumi.get(self, "minute")

    @property
    @pulumi.getter(name="snapshotsToKeep")
    def snapshots_to_keep(self) -> Optional[int]:
        """
        Monthly snapshot count to keep
        """
        return pulumi.get(self, "snapshots_to_keep")

    @property
    @pulumi.getter(name="usedBytes")
    def used_bytes(self) -> Optional[float]:
        """
        Resource size in bytes, current storage usage for the volume in bytes
        """
        return pulumi.get(self, "used_bytes")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MountTargetPropertiesResponse(dict):
    """
    Mount target properties
    """
    def __init__(__self__, *,
                 file_system_id: str,
                 ip_address: str,
                 mount_target_id: str,
                 smb_server_fqdn: Optional[str] = None):
        """
        Mount target properties
        :param str file_system_id: UUID v4 used to identify the MountTarget
        :param str ip_address: The mount target's IPv4 address
        :param str mount_target_id: UUID v4 used to identify the MountTarget
        :param str smb_server_fqdn: The SMB server's Fully Qualified Domain Name, FQDN
        """
        pulumi.set(__self__, "file_system_id", file_system_id)
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "mount_target_id", mount_target_id)
        if smb_server_fqdn is not None:
            pulumi.set(__self__, "smb_server_fqdn", smb_server_fqdn)

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> str:
        """
        UUID v4 used to identify the MountTarget
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The mount target's IPv4 address
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="mountTargetId")
    def mount_target_id(self) -> str:
        """
        UUID v4 used to identify the MountTarget
        """
        return pulumi.get(self, "mount_target_id")

    @property
    @pulumi.getter(name="smbServerFqdn")
    def smb_server_fqdn(self) -> Optional[str]:
        """
        The SMB server's Fully Qualified Domain Name, FQDN
        """
        return pulumi.get(self, "smb_server_fqdn")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReplicationObjectResponse(dict):
    """
    Replication properties
    """
    def __init__(__self__, *,
                 remote_volume_resource_id: str,
                 replication_schedule: str,
                 endpoint_type: Optional[str] = None,
                 remote_volume_region: Optional[str] = None,
                 replication_id: Optional[str] = None):
        """
        Replication properties
        :param str remote_volume_resource_id: The resource ID of the remote volume.
        :param str replication_schedule: Schedule
        :param str endpoint_type: Indicates whether the local volume is the source or destination for the Volume Replication
        :param str remote_volume_region: The remote region for the other end of the Volume Replication.
        :param str replication_id: Id
        """
        pulumi.set(__self__, "remote_volume_resource_id", remote_volume_resource_id)
        pulumi.set(__self__, "replication_schedule", replication_schedule)
        if endpoint_type is not None:
            pulumi.set(__self__, "endpoint_type", endpoint_type)
        if remote_volume_region is not None:
            pulumi.set(__self__, "remote_volume_region", remote_volume_region)
        if replication_id is not None:
            pulumi.set(__self__, "replication_id", replication_id)

    @property
    @pulumi.getter(name="remoteVolumeResourceId")
    def remote_volume_resource_id(self) -> str:
        """
        The resource ID of the remote volume.
        """
        return pulumi.get(self, "remote_volume_resource_id")

    @property
    @pulumi.getter(name="replicationSchedule")
    def replication_schedule(self) -> str:
        """
        Schedule
        """
        return pulumi.get(self, "replication_schedule")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> Optional[str]:
        """
        Indicates whether the local volume is the source or destination for the Volume Replication
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="remoteVolumeRegion")
    def remote_volume_region(self) -> Optional[str]:
        """
        The remote region for the other end of the Volume Replication.
        """
        return pulumi.get(self, "remote_volume_region")

    @property
    @pulumi.getter(name="replicationId")
    def replication_id(self) -> Optional[str]:
        """
        Id
        """
        return pulumi.get(self, "replication_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class VolumeBackupPropertiesResponse(dict):
    """
    Volume Backup Properties
    """
    def __init__(__self__, *,
                 backup_enabled: Optional[bool] = None,
                 backup_policy_id: Optional[str] = None,
                 policy_enforced: Optional[bool] = None,
                 vault_id: Optional[str] = None):
        """
        Volume Backup Properties
        :param bool backup_enabled: Backup Enabled
        :param str backup_policy_id: Backup Policy Resource ID
        :param bool policy_enforced: Policy Enforced
        :param str vault_id: Vault Resource ID
        """
        if backup_enabled is not None:
            pulumi.set(__self__, "backup_enabled", backup_enabled)
        if backup_policy_id is not None:
            pulumi.set(__self__, "backup_policy_id", backup_policy_id)
        if policy_enforced is not None:
            pulumi.set(__self__, "policy_enforced", policy_enforced)
        if vault_id is not None:
            pulumi.set(__self__, "vault_id", vault_id)

    @property
    @pulumi.getter(name="backupEnabled")
    def backup_enabled(self) -> Optional[bool]:
        """
        Backup Enabled
        """
        return pulumi.get(self, "backup_enabled")

    @property
    @pulumi.getter(name="backupPolicyId")
    def backup_policy_id(self) -> Optional[str]:
        """
        Backup Policy Resource ID
        """
        return pulumi.get(self, "backup_policy_id")

    @property
    @pulumi.getter(name="policyEnforced")
    def policy_enforced(self) -> Optional[bool]:
        """
        Policy Enforced
        """
        return pulumi.get(self, "policy_enforced")

    @property
    @pulumi.getter(name="vaultId")
    def vault_id(self) -> Optional[str]:
        """
        Vault Resource ID
        """
        return pulumi.get(self, "vault_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class VolumeBackupsResponse(dict):
    """
    Volume details using the backup policy
    """
    def __init__(__self__, *,
                 backups_count: Optional[int] = None,
                 policy_enabled: Optional[bool] = None,
                 volume_name: Optional[str] = None):
        """
        Volume details using the backup policy
        :param int backups_count: Total count of backups for volume
        :param bool policy_enabled: Policy enabled
        :param str volume_name: Volume name
        """
        if backups_count is not None:
            pulumi.set(__self__, "backups_count", backups_count)
        if policy_enabled is not None:
            pulumi.set(__self__, "policy_enabled", policy_enabled)
        if volume_name is not None:
            pulumi.set(__self__, "volume_name", volume_name)

    @property
    @pulumi.getter(name="backupsCount")
    def backups_count(self) -> Optional[int]:
        """
        Total count of backups for volume
        """
        return pulumi.get(self, "backups_count")

    @property
    @pulumi.getter(name="policyEnabled")
    def policy_enabled(self) -> Optional[bool]:
        """
        Policy enabled
        """
        return pulumi.get(self, "policy_enabled")

    @property
    @pulumi.getter(name="volumeName")
    def volume_name(self) -> Optional[str]:
        """
        Volume name
        """
        return pulumi.get(self, "volume_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class VolumePropertiesResponseDataProtection(dict):
    """
    DataProtection type volumes include an object containing details of the replication
    """
    def __init__(__self__, *,
                 backup: Optional['outputs.VolumeBackupPropertiesResponse'] = None,
                 replication: Optional['outputs.ReplicationObjectResponse'] = None,
                 snapshot: Optional['outputs.VolumeSnapshotPropertiesResponse'] = None):
        """
        DataProtection type volumes include an object containing details of the replication
        :param 'VolumeBackupPropertiesResponseArgs' backup: Backup Properties
        :param 'ReplicationObjectResponseArgs' replication: Replication properties
        :param 'VolumeSnapshotPropertiesResponseArgs' snapshot: Snapshot properties.
        """
        if backup is not None:
            pulumi.set(__self__, "backup", backup)
        if replication is not None:
            pulumi.set(__self__, "replication", replication)
        if snapshot is not None:
            pulumi.set(__self__, "snapshot", snapshot)

    @property
    @pulumi.getter
    def backup(self) -> Optional['outputs.VolumeBackupPropertiesResponse']:
        """
        Backup Properties
        """
        return pulumi.get(self, "backup")

    @property
    @pulumi.getter
    def replication(self) -> Optional['outputs.ReplicationObjectResponse']:
        """
        Replication properties
        """
        return pulumi.get(self, "replication")

    @property
    @pulumi.getter
    def snapshot(self) -> Optional['outputs.VolumeSnapshotPropertiesResponse']:
        """
        Snapshot properties.
        """
        return pulumi.get(self, "snapshot")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class VolumePropertiesResponseExportPolicy(dict):
    """
    Set of export policy rules
    """
    def __init__(__self__, *,
                 rules: Optional[Sequence['outputs.ExportPolicyRuleResponse']] = None):
        """
        Set of export policy rules
        :param Sequence['ExportPolicyRuleResponseArgs'] rules: Export policy rule
        """
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.ExportPolicyRuleResponse']]:
        """
        Export policy rule
        """
        return pulumi.get(self, "rules")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class VolumeSnapshotPropertiesResponse(dict):
    """
    Volume Snapshot Properties
    """
    def __init__(__self__, *,
                 snapshot_policy_id: Optional[str] = None):
        """
        Volume Snapshot Properties
        :param str snapshot_policy_id: Snapshot Policy ResourceId
        """
        if snapshot_policy_id is not None:
            pulumi.set(__self__, "snapshot_policy_id", snapshot_policy_id)

    @property
    @pulumi.getter(name="snapshotPolicyId")
    def snapshot_policy_id(self) -> Optional[str]:
        """
        Snapshot Policy ResourceId
        """
        return pulumi.get(self, "snapshot_policy_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WeeklyScheduleResponse(dict):
    """
    Weekly Schedule properties, make a snapshot every week at a specific day or days
    """
    def __init__(__self__, *,
                 day: Optional[str] = None,
                 hour: Optional[int] = None,
                 minute: Optional[int] = None,
                 snapshots_to_keep: Optional[int] = None,
                 used_bytes: Optional[float] = None):
        """
        Weekly Schedule properties, make a snapshot every week at a specific day or days
        :param str day: Indicates which weekdays snapshot should be taken, accepts a comma separated list of week day names in english
        :param int hour: Indicates which hour in UTC timezone a snapshot should be taken
        :param int minute: Indicates which minute snapshot should be taken
        :param int snapshots_to_keep: Weekly snapshot count to keep
        :param float used_bytes: Resource size in bytes, current storage usage for the volume in bytes
        """
        if day is not None:
            pulumi.set(__self__, "day", day)
        if hour is not None:
            pulumi.set(__self__, "hour", hour)
        if minute is not None:
            pulumi.set(__self__, "minute", minute)
        if snapshots_to_keep is not None:
            pulumi.set(__self__, "snapshots_to_keep", snapshots_to_keep)
        if used_bytes is not None:
            pulumi.set(__self__, "used_bytes", used_bytes)

    @property
    @pulumi.getter
    def day(self) -> Optional[str]:
        """
        Indicates which weekdays snapshot should be taken, accepts a comma separated list of week day names in english
        """
        return pulumi.get(self, "day")

    @property
    @pulumi.getter
    def hour(self) -> Optional[int]:
        """
        Indicates which hour in UTC timezone a snapshot should be taken
        """
        return pulumi.get(self, "hour")

    @property
    @pulumi.getter
    def minute(self) -> Optional[int]:
        """
        Indicates which minute snapshot should be taken
        """
        return pulumi.get(self, "minute")

    @property
    @pulumi.getter(name="snapshotsToKeep")
    def snapshots_to_keep(self) -> Optional[int]:
        """
        Weekly snapshot count to keep
        """
        return pulumi.get(self, "snapshots_to_keep")

    @property
    @pulumi.getter(name="usedBytes")
    def used_bytes(self) -> Optional[float]:
        """
        Resource size in bytes, current storage usage for the volume in bytes
        """
        return pulumi.get(self, "used_bytes")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


