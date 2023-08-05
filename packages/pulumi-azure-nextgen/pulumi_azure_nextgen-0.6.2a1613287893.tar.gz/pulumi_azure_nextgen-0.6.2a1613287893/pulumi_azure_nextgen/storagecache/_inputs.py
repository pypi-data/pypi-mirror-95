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
    'CacheActiveDirectorySettingsArgs',
    'CacheActiveDirectorySettingsCredentialsArgs',
    'CacheDirectorySettingsArgs',
    'CacheEncryptionSettingsArgs',
    'CacheIdentityArgs',
    'CacheNetworkSettingsArgs',
    'CacheSecuritySettingsArgs',
    'CacheSkuArgs',
    'CacheUsernameDownloadSettingsArgs',
    'CacheUsernameDownloadSettingsCredentialsArgs',
    'ClfsTargetArgs',
    'KeyVaultKeyReferenceArgs',
    'KeyVaultKeyReferenceSourceVaultArgs',
    'NamespaceJunctionArgs',
    'Nfs3TargetArgs',
    'NfsAccessPolicyArgs',
    'NfsAccessRuleArgs',
    'UnknownTargetArgs',
]

@pulumi.input_type
class CacheActiveDirectorySettingsArgs:
    def __init__(__self__, *,
                 cache_net_bios_name: pulumi.Input[str],
                 domain_name: pulumi.Input[str],
                 domain_net_bios_name: pulumi.Input[str],
                 primary_dns_ip_address: pulumi.Input[str],
                 credentials: Optional[pulumi.Input['CacheActiveDirectorySettingsCredentialsArgs']] = None,
                 secondary_dns_ip_address: Optional[pulumi.Input[str]] = None):
        """
        Active Directory settings used to join a cache to a domain.
        :param pulumi.Input[str] cache_net_bios_name: The NetBIOS name to assign to the HPC Cache when it joins the Active Directory domain as a server. Length must 1-15 characters from the class [-0-9a-zA-Z].
        :param pulumi.Input[str] domain_name: The fully qualified domain name of the Active Directory domain controller.
        :param pulumi.Input[str] domain_net_bios_name: The Active Directory domain's NetBIOS name.
        :param pulumi.Input[str] primary_dns_ip_address: Primary DNS IP address used to resolve the Active Directory domain controller's fully qualified domain name.
        :param pulumi.Input['CacheActiveDirectorySettingsCredentialsArgs'] credentials: Active Directory admin credentials used to join the HPC Cache to a domain.
        :param pulumi.Input[str] secondary_dns_ip_address: Secondary DNS IP address used to resolve the Active Directory domain controller's fully qualified domain name.
        """
        pulumi.set(__self__, "cache_net_bios_name", cache_net_bios_name)
        pulumi.set(__self__, "domain_name", domain_name)
        pulumi.set(__self__, "domain_net_bios_name", domain_net_bios_name)
        pulumi.set(__self__, "primary_dns_ip_address", primary_dns_ip_address)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if secondary_dns_ip_address is not None:
            pulumi.set(__self__, "secondary_dns_ip_address", secondary_dns_ip_address)

    @property
    @pulumi.getter(name="cacheNetBiosName")
    def cache_net_bios_name(self) -> pulumi.Input[str]:
        """
        The NetBIOS name to assign to the HPC Cache when it joins the Active Directory domain as a server. Length must 1-15 characters from the class [-0-9a-zA-Z].
        """
        return pulumi.get(self, "cache_net_bios_name")

    @cache_net_bios_name.setter
    def cache_net_bios_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cache_net_bios_name", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Input[str]:
        """
        The fully qualified domain name of the Active Directory domain controller.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="domainNetBiosName")
    def domain_net_bios_name(self) -> pulumi.Input[str]:
        """
        The Active Directory domain's NetBIOS name.
        """
        return pulumi.get(self, "domain_net_bios_name")

    @domain_net_bios_name.setter
    def domain_net_bios_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_net_bios_name", value)

    @property
    @pulumi.getter(name="primaryDnsIpAddress")
    def primary_dns_ip_address(self) -> pulumi.Input[str]:
        """
        Primary DNS IP address used to resolve the Active Directory domain controller's fully qualified domain name.
        """
        return pulumi.get(self, "primary_dns_ip_address")

    @primary_dns_ip_address.setter
    def primary_dns_ip_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "primary_dns_ip_address", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['CacheActiveDirectorySettingsCredentialsArgs']]:
        """
        Active Directory admin credentials used to join the HPC Cache to a domain.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['CacheActiveDirectorySettingsCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="secondaryDnsIpAddress")
    def secondary_dns_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Secondary DNS IP address used to resolve the Active Directory domain controller's fully qualified domain name.
        """
        return pulumi.get(self, "secondary_dns_ip_address")

    @secondary_dns_ip_address.setter
    def secondary_dns_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_dns_ip_address", value)


@pulumi.input_type
class CacheActiveDirectorySettingsCredentialsArgs:
    def __init__(__self__, *,
                 password: pulumi.Input[str],
                 username: pulumi.Input[str]):
        """
        Active Directory admin credentials used to join the HPC Cache to a domain.
        :param pulumi.Input[str] password: Plain text password of the Active Directory domain administrator. This value is stored encrypted and not returned on response.
        :param pulumi.Input[str] username: Username of the Active Directory domain administrator. This value is stored encrypted and not returned on response.
        """
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        """
        Plain text password of the Active Directory domain administrator. This value is stored encrypted and not returned on response.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        Username of the Active Directory domain administrator. This value is stored encrypted and not returned on response.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class CacheDirectorySettingsArgs:
    def __init__(__self__, *,
                 active_directory: Optional[pulumi.Input['CacheActiveDirectorySettingsArgs']] = None,
                 username_download: Optional[pulumi.Input['CacheUsernameDownloadSettingsArgs']] = None):
        """
        Cache Directory Services settings.
        :param pulumi.Input['CacheActiveDirectorySettingsArgs'] active_directory: Specifies settings for joining the HPC Cache to an Active Directory domain.
        :param pulumi.Input['CacheUsernameDownloadSettingsArgs'] username_download: Specifies settings for Extended Groups. Extended Groups allows users to be members of more than 16 groups.
        """
        if active_directory is not None:
            pulumi.set(__self__, "active_directory", active_directory)
        if username_download is not None:
            pulumi.set(__self__, "username_download", username_download)

    @property
    @pulumi.getter(name="activeDirectory")
    def active_directory(self) -> Optional[pulumi.Input['CacheActiveDirectorySettingsArgs']]:
        """
        Specifies settings for joining the HPC Cache to an Active Directory domain.
        """
        return pulumi.get(self, "active_directory")

    @active_directory.setter
    def active_directory(self, value: Optional[pulumi.Input['CacheActiveDirectorySettingsArgs']]):
        pulumi.set(self, "active_directory", value)

    @property
    @pulumi.getter(name="usernameDownload")
    def username_download(self) -> Optional[pulumi.Input['CacheUsernameDownloadSettingsArgs']]:
        """
        Specifies settings for Extended Groups. Extended Groups allows users to be members of more than 16 groups.
        """
        return pulumi.get(self, "username_download")

    @username_download.setter
    def username_download(self, value: Optional[pulumi.Input['CacheUsernameDownloadSettingsArgs']]):
        pulumi.set(self, "username_download", value)


@pulumi.input_type
class CacheEncryptionSettingsArgs:
    def __init__(__self__, *,
                 key_encryption_key: Optional[pulumi.Input['KeyVaultKeyReferenceArgs']] = None):
        """
        Cache encryption settings.
        :param pulumi.Input['KeyVaultKeyReferenceArgs'] key_encryption_key: Specifies the location of the key encryption key in Key Vault.
        """
        if key_encryption_key is not None:
            pulumi.set(__self__, "key_encryption_key", key_encryption_key)

    @property
    @pulumi.getter(name="keyEncryptionKey")
    def key_encryption_key(self) -> Optional[pulumi.Input['KeyVaultKeyReferenceArgs']]:
        """
        Specifies the location of the key encryption key in Key Vault.
        """
        return pulumi.get(self, "key_encryption_key")

    @key_encryption_key.setter
    def key_encryption_key(self, value: Optional[pulumi.Input['KeyVaultKeyReferenceArgs']]):
        pulumi.set(self, "key_encryption_key", value)


@pulumi.input_type
class CacheIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['CacheIdentityType']] = None):
        """
        Cache identity properties.
        :param pulumi.Input['CacheIdentityType'] type: The type of identity used for the cache
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['CacheIdentityType']]:
        """
        The type of identity used for the cache
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['CacheIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class CacheNetworkSettingsArgs:
    def __init__(__self__, *,
                 mtu: Optional[pulumi.Input[int]] = None):
        """
        Cache network settings.
        :param pulumi.Input[int] mtu: The IPv4 maximum transmission unit configured for the subnet.
        """
        if mtu is None:
            mtu = 1500
        if mtu is not None:
            pulumi.set(__self__, "mtu", mtu)

    @property
    @pulumi.getter
    def mtu(self) -> Optional[pulumi.Input[int]]:
        """
        The IPv4 maximum transmission unit configured for the subnet.
        """
        return pulumi.get(self, "mtu")

    @mtu.setter
    def mtu(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "mtu", value)


@pulumi.input_type
class CacheSecuritySettingsArgs:
    def __init__(__self__, *,
                 access_policies: Optional[pulumi.Input[Sequence[pulumi.Input['NfsAccessPolicyArgs']]]] = None):
        """
        Cache security settings.
        :param pulumi.Input[Sequence[pulumi.Input['NfsAccessPolicyArgs']]] access_policies: NFS access policies defined for this cache.
        """
        if access_policies is not None:
            pulumi.set(__self__, "access_policies", access_policies)

    @property
    @pulumi.getter(name="accessPolicies")
    def access_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NfsAccessPolicyArgs']]]]:
        """
        NFS access policies defined for this cache.
        """
        return pulumi.get(self, "access_policies")

    @access_policies.setter
    def access_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NfsAccessPolicyArgs']]]]):
        pulumi.set(self, "access_policies", value)


@pulumi.input_type
class CacheSkuArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None):
        """
        SKU for the Cache.
        :param pulumi.Input[str] name: SKU name for this Cache.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        SKU name for this Cache.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class CacheUsernameDownloadSettingsArgs:
    def __init__(__self__, *,
                 auto_download_certificate: Optional[pulumi.Input[bool]] = None,
                 ca_certificate_uri: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input['CacheUsernameDownloadSettingsCredentialsArgs']] = None,
                 encrypt_ldap_connection: Optional[pulumi.Input[bool]] = None,
                 extended_groups: Optional[pulumi.Input[bool]] = None,
                 group_file_uri: Optional[pulumi.Input[str]] = None,
                 ldap_base_dn: Optional[pulumi.Input[str]] = None,
                 ldap_server: Optional[pulumi.Input[str]] = None,
                 require_valid_certificate: Optional[pulumi.Input[bool]] = None,
                 user_file_uri: Optional[pulumi.Input[str]] = None,
                 username_source: Optional[pulumi.Input[Union[str, 'UsernameSource']]] = None):
        """
        Settings for Extended Groups username and group download.
        :param pulumi.Input[bool] auto_download_certificate: Determines if the certificate should be automatically downloaded. This applies to 'caCertificateURI' only if 'requireValidCertificate' is true.
        :param pulumi.Input[str] ca_certificate_uri: The URI of the CA certificate to validate the LDAP secure connection. This field must be populated when 'requireValidCertificate' is set to true.
        :param pulumi.Input['CacheUsernameDownloadSettingsCredentialsArgs'] credentials: When present, these are the credentials for the secure LDAP connection.
        :param pulumi.Input[bool] encrypt_ldap_connection: Whether or not the LDAP connection should be encrypted.
        :param pulumi.Input[bool] extended_groups: Whether or not Extended Groups is enabled.
        :param pulumi.Input[str] group_file_uri: The URI of the file containing group information (in /etc/group file format). This field must be populated when 'usernameSource' is set to 'File'.
        :param pulumi.Input[str] ldap_base_dn: The base distinguished name for the LDAP domain.
        :param pulumi.Input[str] ldap_server: The fully qualified domain name or IP address of the LDAP server to use.
        :param pulumi.Input[bool] require_valid_certificate: Determines if the certificates must be validated by a certificate authority. When true, caCertificateURI must be provided.
        :param pulumi.Input[str] user_file_uri: The URI of the file containing user information (in /etc/passwd file format). This field must be populated when 'usernameSource' is set to 'File'.
        :param pulumi.Input[Union[str, 'UsernameSource']] username_source: This setting determines how the cache gets username and group names for clients.
        """
        if auto_download_certificate is not None:
            pulumi.set(__self__, "auto_download_certificate", auto_download_certificate)
        if ca_certificate_uri is not None:
            pulumi.set(__self__, "ca_certificate_uri", ca_certificate_uri)
        if credentials is not None:
            pulumi.set(__self__, "credentials", credentials)
        if encrypt_ldap_connection is not None:
            pulumi.set(__self__, "encrypt_ldap_connection", encrypt_ldap_connection)
        if extended_groups is not None:
            pulumi.set(__self__, "extended_groups", extended_groups)
        if group_file_uri is not None:
            pulumi.set(__self__, "group_file_uri", group_file_uri)
        if ldap_base_dn is not None:
            pulumi.set(__self__, "ldap_base_dn", ldap_base_dn)
        if ldap_server is not None:
            pulumi.set(__self__, "ldap_server", ldap_server)
        if require_valid_certificate is not None:
            pulumi.set(__self__, "require_valid_certificate", require_valid_certificate)
        if user_file_uri is not None:
            pulumi.set(__self__, "user_file_uri", user_file_uri)
        if username_source is None:
            username_source = 'None'
        if username_source is not None:
            pulumi.set(__self__, "username_source", username_source)

    @property
    @pulumi.getter(name="autoDownloadCertificate")
    def auto_download_certificate(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if the certificate should be automatically downloaded. This applies to 'caCertificateURI' only if 'requireValidCertificate' is true.
        """
        return pulumi.get(self, "auto_download_certificate")

    @auto_download_certificate.setter
    def auto_download_certificate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_download_certificate", value)

    @property
    @pulumi.getter(name="caCertificateURI")
    def ca_certificate_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the CA certificate to validate the LDAP secure connection. This field must be populated when 'requireValidCertificate' is set to true.
        """
        return pulumi.get(self, "ca_certificate_uri")

    @ca_certificate_uri.setter
    def ca_certificate_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ca_certificate_uri", value)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[pulumi.Input['CacheUsernameDownloadSettingsCredentialsArgs']]:
        """
        When present, these are the credentials for the secure LDAP connection.
        """
        return pulumi.get(self, "credentials")

    @credentials.setter
    def credentials(self, value: Optional[pulumi.Input['CacheUsernameDownloadSettingsCredentialsArgs']]):
        pulumi.set(self, "credentials", value)

    @property
    @pulumi.getter(name="encryptLdapConnection")
    def encrypt_ldap_connection(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not the LDAP connection should be encrypted.
        """
        return pulumi.get(self, "encrypt_ldap_connection")

    @encrypt_ldap_connection.setter
    def encrypt_ldap_connection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypt_ldap_connection", value)

    @property
    @pulumi.getter(name="extendedGroups")
    def extended_groups(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not Extended Groups is enabled.
        """
        return pulumi.get(self, "extended_groups")

    @extended_groups.setter
    def extended_groups(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "extended_groups", value)

    @property
    @pulumi.getter(name="groupFileURI")
    def group_file_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the file containing group information (in /etc/group file format). This field must be populated when 'usernameSource' is set to 'File'.
        """
        return pulumi.get(self, "group_file_uri")

    @group_file_uri.setter
    def group_file_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_file_uri", value)

    @property
    @pulumi.getter(name="ldapBaseDN")
    def ldap_base_dn(self) -> Optional[pulumi.Input[str]]:
        """
        The base distinguished name for the LDAP domain.
        """
        return pulumi.get(self, "ldap_base_dn")

    @ldap_base_dn.setter
    def ldap_base_dn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ldap_base_dn", value)

    @property
    @pulumi.getter(name="ldapServer")
    def ldap_server(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified domain name or IP address of the LDAP server to use.
        """
        return pulumi.get(self, "ldap_server")

    @ldap_server.setter
    def ldap_server(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ldap_server", value)

    @property
    @pulumi.getter(name="requireValidCertificate")
    def require_valid_certificate(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines if the certificates must be validated by a certificate authority. When true, caCertificateURI must be provided.
        """
        return pulumi.get(self, "require_valid_certificate")

    @require_valid_certificate.setter
    def require_valid_certificate(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "require_valid_certificate", value)

    @property
    @pulumi.getter(name="userFileURI")
    def user_file_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the file containing user information (in /etc/passwd file format). This field must be populated when 'usernameSource' is set to 'File'.
        """
        return pulumi.get(self, "user_file_uri")

    @user_file_uri.setter
    def user_file_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_file_uri", value)

    @property
    @pulumi.getter(name="usernameSource")
    def username_source(self) -> Optional[pulumi.Input[Union[str, 'UsernameSource']]]:
        """
        This setting determines how the cache gets username and group names for clients.
        """
        return pulumi.get(self, "username_source")

    @username_source.setter
    def username_source(self, value: Optional[pulumi.Input[Union[str, 'UsernameSource']]]):
        pulumi.set(self, "username_source", value)


@pulumi.input_type
class CacheUsernameDownloadSettingsCredentialsArgs:
    def __init__(__self__, *,
                 bind_dn: Optional[pulumi.Input[str]] = None,
                 bind_password: Optional[pulumi.Input[str]] = None):
        """
        When present, these are the credentials for the secure LDAP connection.
        :param pulumi.Input[str] bind_dn: The Bind Distinguished Name identity to be used in the secure LDAP connection. This value is stored encrypted and not returned on response.
        :param pulumi.Input[str] bind_password: The Bind password to be used in the secure LDAP connection. This value is stored encrypted and not returned on response.
        """
        if bind_dn is not None:
            pulumi.set(__self__, "bind_dn", bind_dn)
        if bind_password is not None:
            pulumi.set(__self__, "bind_password", bind_password)

    @property
    @pulumi.getter(name="bindDn")
    def bind_dn(self) -> Optional[pulumi.Input[str]]:
        """
        The Bind Distinguished Name identity to be used in the secure LDAP connection. This value is stored encrypted and not returned on response.
        """
        return pulumi.get(self, "bind_dn")

    @bind_dn.setter
    def bind_dn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bind_dn", value)

    @property
    @pulumi.getter(name="bindPassword")
    def bind_password(self) -> Optional[pulumi.Input[str]]:
        """
        The Bind password to be used in the secure LDAP connection. This value is stored encrypted and not returned on response.
        """
        return pulumi.get(self, "bind_password")

    @bind_password.setter
    def bind_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bind_password", value)


@pulumi.input_type
class ClfsTargetArgs:
    def __init__(__self__, *,
                 target: Optional[pulumi.Input[str]] = None):
        """
        Properties pertaining to the ClfsTarget
        :param pulumi.Input[str] target: Resource ID of storage container.
        """
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID of storage container.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)


@pulumi.input_type
class KeyVaultKeyReferenceArgs:
    def __init__(__self__, *,
                 key_url: pulumi.Input[str],
                 source_vault: pulumi.Input['KeyVaultKeyReferenceSourceVaultArgs']):
        """
        Describes a reference to Key Vault Key.
        :param pulumi.Input[str] key_url: The URL referencing a key encryption key in Key Vault.
        :param pulumi.Input['KeyVaultKeyReferenceSourceVaultArgs'] source_vault: Describes a resource Id to source Key Vault.
        """
        pulumi.set(__self__, "key_url", key_url)
        pulumi.set(__self__, "source_vault", source_vault)

    @property
    @pulumi.getter(name="keyUrl")
    def key_url(self) -> pulumi.Input[str]:
        """
        The URL referencing a key encryption key in Key Vault.
        """
        return pulumi.get(self, "key_url")

    @key_url.setter
    def key_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_url", value)

    @property
    @pulumi.getter(name="sourceVault")
    def source_vault(self) -> pulumi.Input['KeyVaultKeyReferenceSourceVaultArgs']:
        """
        Describes a resource Id to source Key Vault.
        """
        return pulumi.get(self, "source_vault")

    @source_vault.setter
    def source_vault(self, value: pulumi.Input['KeyVaultKeyReferenceSourceVaultArgs']):
        pulumi.set(self, "source_vault", value)


@pulumi.input_type
class KeyVaultKeyReferenceSourceVaultArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None):
        """
        Describes a resource Id to source Key Vault.
        :param pulumi.Input[str] id: Resource Id.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class NamespaceJunctionArgs:
    def __init__(__self__, *,
                 namespace_path: Optional[pulumi.Input[str]] = None,
                 nfs_access_policy: Optional[pulumi.Input[str]] = None,
                 nfs_export: Optional[pulumi.Input[str]] = None,
                 target_path: Optional[pulumi.Input[str]] = None):
        """
        A namespace junction.
        :param pulumi.Input[str] namespace_path: Namespace path on a Cache for a Storage Target.
        :param pulumi.Input[str] nfs_access_policy: Name of the access policy applied to this junction.
        :param pulumi.Input[str] nfs_export: NFS export where targetPath exists.
        :param pulumi.Input[str] target_path: Path in Storage Target to which namespacePath points.
        """
        if namespace_path is not None:
            pulumi.set(__self__, "namespace_path", namespace_path)
        if nfs_access_policy is not None:
            pulumi.set(__self__, "nfs_access_policy", nfs_access_policy)
        if nfs_export is not None:
            pulumi.set(__self__, "nfs_export", nfs_export)
        if target_path is not None:
            pulumi.set(__self__, "target_path", target_path)

    @property
    @pulumi.getter(name="namespacePath")
    def namespace_path(self) -> Optional[pulumi.Input[str]]:
        """
        Namespace path on a Cache for a Storage Target.
        """
        return pulumi.get(self, "namespace_path")

    @namespace_path.setter
    def namespace_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_path", value)

    @property
    @pulumi.getter(name="nfsAccessPolicy")
    def nfs_access_policy(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the access policy applied to this junction.
        """
        return pulumi.get(self, "nfs_access_policy")

    @nfs_access_policy.setter
    def nfs_access_policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nfs_access_policy", value)

    @property
    @pulumi.getter(name="nfsExport")
    def nfs_export(self) -> Optional[pulumi.Input[str]]:
        """
        NFS export where targetPath exists.
        """
        return pulumi.get(self, "nfs_export")

    @nfs_export.setter
    def nfs_export(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nfs_export", value)

    @property
    @pulumi.getter(name="targetPath")
    def target_path(self) -> Optional[pulumi.Input[str]]:
        """
        Path in Storage Target to which namespacePath points.
        """
        return pulumi.get(self, "target_path")

    @target_path.setter
    def target_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_path", value)


@pulumi.input_type
class Nfs3TargetArgs:
    def __init__(__self__, *,
                 target: Optional[pulumi.Input[str]] = None,
                 usage_model: Optional[pulumi.Input[str]] = None):
        """
        Properties pertaining to the Nfs3Target
        :param pulumi.Input[str] target: IP address or host name of an NFSv3 host (e.g., 10.0.44.44).
        :param pulumi.Input[str] usage_model: Identifies the usage model to be used for this Storage Target. Get choices from .../usageModels
        """
        if target is not None:
            pulumi.set(__self__, "target", target)
        if usage_model is not None:
            pulumi.set(__self__, "usage_model", usage_model)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        IP address or host name of an NFSv3 host (e.g., 10.0.44.44).
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="usageModel")
    def usage_model(self) -> Optional[pulumi.Input[str]]:
        """
        Identifies the usage model to be used for this Storage Target. Get choices from .../usageModels
        """
        return pulumi.get(self, "usage_model")

    @usage_model.setter
    def usage_model(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "usage_model", value)


@pulumi.input_type
class NfsAccessPolicyArgs:
    def __init__(__self__, *,
                 access_rules: pulumi.Input[Sequence[pulumi.Input['NfsAccessRuleArgs']]],
                 name: pulumi.Input[str]):
        """
        A set of rules describing access policies applied to NFSv3 clients of the cache.
        :param pulumi.Input[Sequence[pulumi.Input['NfsAccessRuleArgs']]] access_rules: The set of rules describing client accesses allowed under this policy.
        :param pulumi.Input[str] name: Name identifying this policy. Access Policy names are not case sensitive.
        """
        pulumi.set(__self__, "access_rules", access_rules)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="accessRules")
    def access_rules(self) -> pulumi.Input[Sequence[pulumi.Input['NfsAccessRuleArgs']]]:
        """
        The set of rules describing client accesses allowed under this policy.
        """
        return pulumi.get(self, "access_rules")

    @access_rules.setter
    def access_rules(self, value: pulumi.Input[Sequence[pulumi.Input['NfsAccessRuleArgs']]]):
        pulumi.set(self, "access_rules", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name identifying this policy. Access Policy names are not case sensitive.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class NfsAccessRuleArgs:
    def __init__(__self__, *,
                 access: pulumi.Input[Union[str, 'NfsAccessRuleAccess']],
                 scope: pulumi.Input[Union[str, 'NfsAccessRuleScope']],
                 anonymous_gid: Optional[pulumi.Input[str]] = None,
                 anonymous_uid: Optional[pulumi.Input[str]] = None,
                 filter: Optional[pulumi.Input[str]] = None,
                 root_squash: Optional[pulumi.Input[bool]] = None,
                 submount_access: Optional[pulumi.Input[bool]] = None,
                 suid: Optional[pulumi.Input[bool]] = None):
        """
        Rule to place restrictions on portions of the cache namespace being presented to clients.
        :param pulumi.Input[Union[str, 'NfsAccessRuleAccess']] access: Access allowed by this rule.
        :param pulumi.Input[Union[str, 'NfsAccessRuleScope']] scope: Scope for this rule. The scope and filter determine which clients match the rule.
        :param pulumi.Input[str] anonymous_gid: GID value that replaces 0 when rootSquash is true.
        :param pulumi.Input[str] anonymous_uid: UID value that replaces 0 when rootSquash is true.
        :param pulumi.Input[str] filter: Filter applied to the scope for this rule. The filter's format depends on its scope. 'default' scope matches all clients and has no filter value. 'network' scope takes a filter in CIDR format (for example, 10.99.1.0/24). 'host' takes an IP address or fully qualified domain name as filter. If a client does not match any filter rule and there is no default rule, access is denied.
        :param pulumi.Input[bool] root_squash: Map root accesses to anonymousUID and anonymousGID.
        :param pulumi.Input[bool] submount_access: For the default policy, allow access to subdirectories under the root export. If this is set to no, clients can only mount the path '/'. If set to yes, clients can mount a deeper path, like '/a/b'.
        :param pulumi.Input[bool] suid: Allow SUID semantics.
        """
        pulumi.set(__self__, "access", access)
        pulumi.set(__self__, "scope", scope)
        if anonymous_gid is None:
            anonymous_gid = '-2'
        if anonymous_gid is not None:
            pulumi.set(__self__, "anonymous_gid", anonymous_gid)
        if anonymous_uid is None:
            anonymous_uid = '-2'
        if anonymous_uid is not None:
            pulumi.set(__self__, "anonymous_uid", anonymous_uid)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if root_squash is not None:
            pulumi.set(__self__, "root_squash", root_squash)
        if submount_access is not None:
            pulumi.set(__self__, "submount_access", submount_access)
        if suid is not None:
            pulumi.set(__self__, "suid", suid)

    @property
    @pulumi.getter
    def access(self) -> pulumi.Input[Union[str, 'NfsAccessRuleAccess']]:
        """
        Access allowed by this rule.
        """
        return pulumi.get(self, "access")

    @access.setter
    def access(self, value: pulumi.Input[Union[str, 'NfsAccessRuleAccess']]):
        pulumi.set(self, "access", value)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[Union[str, 'NfsAccessRuleScope']]:
        """
        Scope for this rule. The scope and filter determine which clients match the rule.
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[Union[str, 'NfsAccessRuleScope']]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter(name="anonymousGID")
    def anonymous_gid(self) -> Optional[pulumi.Input[str]]:
        """
        GID value that replaces 0 when rootSquash is true.
        """
        return pulumi.get(self, "anonymous_gid")

    @anonymous_gid.setter
    def anonymous_gid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "anonymous_gid", value)

    @property
    @pulumi.getter(name="anonymousUID")
    def anonymous_uid(self) -> Optional[pulumi.Input[str]]:
        """
        UID value that replaces 0 when rootSquash is true.
        """
        return pulumi.get(self, "anonymous_uid")

    @anonymous_uid.setter
    def anonymous_uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "anonymous_uid", value)

    @property
    @pulumi.getter
    def filter(self) -> Optional[pulumi.Input[str]]:
        """
        Filter applied to the scope for this rule. The filter's format depends on its scope. 'default' scope matches all clients and has no filter value. 'network' scope takes a filter in CIDR format (for example, 10.99.1.0/24). 'host' takes an IP address or fully qualified domain name as filter. If a client does not match any filter rule and there is no default rule, access is denied.
        """
        return pulumi.get(self, "filter")

    @filter.setter
    def filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter", value)

    @property
    @pulumi.getter(name="rootSquash")
    def root_squash(self) -> Optional[pulumi.Input[bool]]:
        """
        Map root accesses to anonymousUID and anonymousGID.
        """
        return pulumi.get(self, "root_squash")

    @root_squash.setter
    def root_squash(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "root_squash", value)

    @property
    @pulumi.getter(name="submountAccess")
    def submount_access(self) -> Optional[pulumi.Input[bool]]:
        """
        For the default policy, allow access to subdirectories under the root export. If this is set to no, clients can only mount the path '/'. If set to yes, clients can mount a deeper path, like '/a/b'.
        """
        return pulumi.get(self, "submount_access")

    @submount_access.setter
    def submount_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "submount_access", value)

    @property
    @pulumi.getter
    def suid(self) -> Optional[pulumi.Input[bool]]:
        """
        Allow SUID semantics.
        """
        return pulumi.get(self, "suid")

    @suid.setter
    def suid(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "suid", value)


@pulumi.input_type
class UnknownTargetArgs:
    def __init__(__self__, *,
                 unknown_map: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Properties pertaining to the UnknownTarget
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] unknown_map: Dictionary of string->string pairs containing information about the Storage Target.
        """
        if unknown_map is not None:
            pulumi.set(__self__, "unknown_map", unknown_map)

    @property
    @pulumi.getter(name="unknownMap")
    def unknown_map(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Dictionary of string->string pairs containing information about the Storage Target.
        """
        return pulumi.get(self, "unknown_map")

    @unknown_map.setter
    def unknown_map(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "unknown_map", value)


