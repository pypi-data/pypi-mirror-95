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
from ._inputs import *

__all__ = ['ManagedInstance']


class ManagedInstance(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_login: Optional[pulumi.Input[str]] = None,
                 administrator_login_password: Optional[pulumi.Input[str]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 dns_zone_partner: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ResourceIdentityArgs']]] = None,
                 instance_pool_id: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ManagedInstanceLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 managed_instance_create_mode: Optional[pulumi.Input[Union[str, 'ManagedServerCreateMode']]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 minimal_tls_version: Optional[pulumi.Input[str]] = None,
                 proxy_override: Optional[pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']]] = None,
                 public_data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 source_managed_instance_id: Optional[pulumi.Input[str]] = None,
                 storage_size_in_gb: Optional[pulumi.Input[int]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 timezone_id: Optional[pulumi.Input[str]] = None,
                 v_cores: Optional[pulumi.Input[int]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An Azure SQL managed instance.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_login: Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
        :param pulumi.Input[str] administrator_login_password: The administrator login password (required for managed instance creation).
        :param pulumi.Input[str] collation: Collation of the managed instance.
        :param pulumi.Input[str] dns_zone_partner: The resource id of another managed instance whose DNS zone this managed instance will share after creation.
        :param pulumi.Input[pulumi.InputType['ResourceIdentityArgs']] identity: The Azure Active Directory identity of the managed instance.
        :param pulumi.Input[str] instance_pool_id: The Id of the instance pool this managed server belongs to.
        :param pulumi.Input[Union[str, 'ManagedInstanceLicenseType']] license_type: The license type. Possible values are 'LicenseIncluded' (regular price inclusive of a new SQL license) and 'BasePrice' (discounted AHB price for bringing your own SQL licenses).
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] maintenance_configuration_id: Specifies maintenance configuration id to apply to this managed instance.
        :param pulumi.Input[Union[str, 'ManagedServerCreateMode']] managed_instance_create_mode: Specifies the mode of database creation.
               
               Default: Regular instance creation.
               
               Restore: Creates an instance by restoring a set of backups to specific point in time. RestorePointInTime and SourceManagedInstanceId must be specified.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] minimal_tls_version: Minimal TLS version. Allowed values: 'None', '1.0', '1.1', '1.2'
        :param pulumi.Input[Union[str, 'ManagedInstanceProxyOverride']] proxy_override: Connection type used for connecting to the instance.
        :param pulumi.Input[bool] public_data_endpoint_enabled: Whether or not the public data endpoint is enabled.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] restore_point_in_time: Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Managed instance SKU. Allowed values for sku.name: GP_Gen4, GP_Gen5, BC_Gen4, BC_Gen5
        :param pulumi.Input[str] source_managed_instance_id: The resource identifier of the source managed instance associated with create operation of this instance.
        :param pulumi.Input[int] storage_size_in_gb: Storage size in GB. Minimum value: 32. Maximum value: 8192. Increments of 32 GB allowed only.
        :param pulumi.Input[str] subnet_id: Subnet resource ID for the managed instance.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] timezone_id: Id of the timezone. Allowed values are timezones supported by Windows.
               Windows keeps details on supported timezones, including the id, in registry under
               KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones.
               You can get those registry values via SQL Server by querying SELECT name AS timezone_id FROM sys.time_zone_info.
               List of Ids can also be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell.
               An example of valid timezone id is "Pacific Standard Time" or "W. Europe Standard Time".
        :param pulumi.Input[int] v_cores: The number of vCores. Allowed values: 8, 16, 24, 32, 40, 64, 80.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['administrator_login'] = administrator_login
            __props__['administrator_login_password'] = administrator_login_password
            __props__['collation'] = collation
            __props__['dns_zone_partner'] = dns_zone_partner
            __props__['identity'] = identity
            __props__['instance_pool_id'] = instance_pool_id
            __props__['license_type'] = license_type
            __props__['location'] = location
            __props__['maintenance_configuration_id'] = maintenance_configuration_id
            __props__['managed_instance_create_mode'] = managed_instance_create_mode
            if managed_instance_name is None and not opts.urn:
                raise TypeError("Missing required property 'managed_instance_name'")
            __props__['managed_instance_name'] = managed_instance_name
            __props__['minimal_tls_version'] = minimal_tls_version
            __props__['proxy_override'] = proxy_override
            __props__['public_data_endpoint_enabled'] = public_data_endpoint_enabled
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['restore_point_in_time'] = restore_point_in_time
            __props__['sku'] = sku
            __props__['source_managed_instance_id'] = source_managed_instance_id
            __props__['storage_size_in_gb'] = storage_size_in_gb
            __props__['subnet_id'] = subnet_id
            __props__['tags'] = tags
            __props__['timezone_id'] = timezone_id
            __props__['v_cores'] = v_cores
            __props__['dns_zone'] = None
            __props__['fully_qualified_domain_name'] = None
            __props__['name'] = None
            __props__['state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql:ManagedInstance"), pulumi.Alias(type_="azure-nextgen:sql/v20180601preview:ManagedInstance"), pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:ManagedInstance"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:ManagedInstance")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedInstance, __self__).__init__(
            'azure-nextgen:sql/v20150501preview:ManagedInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedInstance':
        """
        Get an existing ManagedInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ManagedInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> pulumi.Output[Optional[str]]:
        """
        Administrator username for the managed instance. Can only be specified when the managed instance is being created (and is required for creation).
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter(name="administratorLoginPassword")
    def administrator_login_password(self) -> pulumi.Output[Optional[str]]:
        """
        The administrator login password (required for managed instance creation).
        """
        return pulumi.get(self, "administrator_login_password")

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[Optional[str]]:
        """
        Collation of the managed instance.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="dnsZone")
    def dns_zone(self) -> pulumi.Output[str]:
        """
        The Dns Zone that the managed instance is in.
        """
        return pulumi.get(self, "dns_zone")

    @property
    @pulumi.getter(name="dnsZonePartner")
    def dns_zone_partner(self) -> pulumi.Output[Optional[str]]:
        """
        The resource id of another managed instance whose DNS zone this managed instance will share after creation.
        """
        return pulumi.get(self, "dns_zone_partner")

    @property
    @pulumi.getter(name="fullyQualifiedDomainName")
    def fully_qualified_domain_name(self) -> pulumi.Output[str]:
        """
        The fully qualified domain name of the managed instance.
        """
        return pulumi.get(self, "fully_qualified_domain_name")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ResourceIdentityResponse']]:
        """
        The Azure Active Directory identity of the managed instance.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="instancePoolId")
    def instance_pool_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Id of the instance pool this managed server belongs to.
        """
        return pulumi.get(self, "instance_pool_id")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[Optional[str]]:
        """
        The license type. Possible values are 'LicenseIncluded' (regular price inclusive of a new SQL license) and 'BasePrice' (discounted AHB price for bringing your own SQL licenses).
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies maintenance configuration id to apply to this managed instance.
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter(name="managedInstanceCreateMode")
    def managed_instance_create_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the mode of database creation.
        
        Default: Regular instance creation.
        
        Restore: Creates an instance by restoring a set of backups to specific point in time. RestorePointInTime and SourceManagedInstanceId must be specified.
        """
        return pulumi.get(self, "managed_instance_create_mode")

    @property
    @pulumi.getter(name="minimalTlsVersion")
    def minimal_tls_version(self) -> pulumi.Output[Optional[str]]:
        """
        Minimal TLS version. Allowed values: 'None', '1.0', '1.1', '1.2'
        """
        return pulumi.get(self, "minimal_tls_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="proxyOverride")
    def proxy_override(self) -> pulumi.Output[Optional[str]]:
        """
        Connection type used for connecting to the instance.
        """
        return pulumi.get(self, "proxy_override")

    @property
    @pulumi.getter(name="publicDataEndpointEnabled")
    def public_data_endpoint_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not the public data endpoint is enabled.
        """
        return pulumi.get(self, "public_data_endpoint_enabled")

    @property
    @pulumi.getter(name="restorePointInTime")
    def restore_point_in_time(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        """
        return pulumi.get(self, "restore_point_in_time")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        Managed instance SKU. Allowed values for sku.name: GP_Gen4, GP_Gen5, BC_Gen4, BC_Gen5
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="sourceManagedInstanceId")
    def source_managed_instance_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource identifier of the source managed instance associated with create operation of this instance.
        """
        return pulumi.get(self, "source_managed_instance_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the managed instance.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageSizeInGB")
    def storage_size_in_gb(self) -> pulumi.Output[Optional[int]]:
        """
        Storage size in GB. Minimum value: 32. Maximum value: 8192. Increments of 32 GB allowed only.
        """
        return pulumi.get(self, "storage_size_in_gb")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        Subnet resource ID for the managed instance.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timezoneId")
    def timezone_id(self) -> pulumi.Output[Optional[str]]:
        """
        Id of the timezone. Allowed values are timezones supported by Windows.
        Windows keeps details on supported timezones, including the id, in registry under
        KEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Time Zones.
        You can get those registry values via SQL Server by querying SELECT name AS timezone_id FROM sys.time_zone_info.
        List of Ids can also be obtained by executing [System.TimeZoneInfo]::GetSystemTimeZones() in PowerShell.
        An example of valid timezone id is "Pacific Standard Time" or "W. Europe Standard Time".
        """
        return pulumi.get(self, "timezone_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vCores")
    def v_cores(self) -> pulumi.Output[Optional[int]]:
        """
        The number of vCores. Allowed values: 8, 16, 24, 32, 40, 64, 80.
        """
        return pulumi.get(self, "v_cores")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

