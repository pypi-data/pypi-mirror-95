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

__all__ = ['Cache']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:storagecache:Cache'.""", DeprecationWarning)


class Cache(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:storagecache:Cache'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cache_name: Optional[pulumi.Input[str]] = None,
                 cache_size_gb: Optional[pulumi.Input[int]] = None,
                 directory_services_settings: Optional[pulumi.Input[pulumi.InputType['CacheDirectorySettingsArgs']]] = None,
                 encryption_settings: Optional[pulumi.Input[pulumi.InputType['CacheEncryptionSettingsArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['CacheIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_settings: Optional[pulumi.Input[pulumi.InputType['CacheNetworkSettingsArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningStateType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 security_settings: Optional[pulumi.Input[pulumi.InputType['CacheSecuritySettingsArgs']]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['CacheSkuArgs']]] = None,
                 subnet: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A Cache instance. Follows Azure Resource Manager standards: https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/resource-api-reference.md
        Latest API Version: 2020-10-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cache_name: Name of Cache. Length of name must not be greater than 80 and chars must be from the [-0-9a-zA-Z_] char class.
        :param pulumi.Input[int] cache_size_gb: The size of this Cache, in GB.
        :param pulumi.Input[pulumi.InputType['CacheDirectorySettingsArgs']] directory_services_settings: Specifies Directory Services settings of the cache.
        :param pulumi.Input[pulumi.InputType['CacheEncryptionSettingsArgs']] encryption_settings: Specifies encryption settings of the cache.
        :param pulumi.Input[pulumi.InputType['CacheIdentityArgs']] identity: The identity of the cache, if configured.
        :param pulumi.Input[str] location: Region name string.
        :param pulumi.Input[pulumi.InputType['CacheNetworkSettingsArgs']] network_settings: Specifies network settings of the cache.
        :param pulumi.Input[Union[str, 'ProvisioningStateType']] provisioning_state: ARM provisioning state, see https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/Addendum.md#provisioningstate-property
        :param pulumi.Input[str] resource_group_name: Target resource group.
        :param pulumi.Input[pulumi.InputType['CacheSecuritySettingsArgs']] security_settings: Specifies security settings of the cache.
        :param pulumi.Input[pulumi.InputType['CacheSkuArgs']] sku: SKU for the Cache.
        :param pulumi.Input[str] subnet: Subnet used for the Cache.
        :param Any tags: ARM tags as name/value pairs.
        """
        pulumi.log.warn("Cache is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:storagecache:Cache'.")
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

            if cache_name is None and not opts.urn:
                raise TypeError("Missing required property 'cache_name'")
            __props__['cache_name'] = cache_name
            __props__['cache_size_gb'] = cache_size_gb
            __props__['directory_services_settings'] = directory_services_settings
            __props__['encryption_settings'] = encryption_settings
            __props__['identity'] = identity
            __props__['location'] = location
            __props__['network_settings'] = network_settings
            __props__['provisioning_state'] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['security_settings'] = security_settings
            __props__['sku'] = sku
            __props__['subnet'] = subnet
            __props__['tags'] = tags
            __props__['health'] = None
            __props__['mount_addresses'] = None
            __props__['name'] = None
            __props__['system_data'] = None
            __props__['type'] = None
            __props__['upgrade_status'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storagecache:Cache"), pulumi.Alias(type_="azure-nextgen:storagecache/v20190801preview:Cache"), pulumi.Alias(type_="azure-nextgen:storagecache/v20191101:Cache"), pulumi.Alias(type_="azure-nextgen:storagecache/v20200301:Cache"), pulumi.Alias(type_="azure-nextgen:storagecache/v20201001:Cache")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Cache, __self__).__init__(
            'azure-nextgen:storagecache/latest:Cache',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Cache':
        """
        Get an existing Cache resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Cache(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cacheSizeGB")
    def cache_size_gb(self) -> pulumi.Output[Optional[int]]:
        """
        The size of this Cache, in GB.
        """
        return pulumi.get(self, "cache_size_gb")

    @property
    @pulumi.getter(name="directoryServicesSettings")
    def directory_services_settings(self) -> pulumi.Output[Optional['outputs.CacheDirectorySettingsResponse']]:
        """
        Specifies Directory Services settings of the cache.
        """
        return pulumi.get(self, "directory_services_settings")

    @property
    @pulumi.getter(name="encryptionSettings")
    def encryption_settings(self) -> pulumi.Output[Optional['outputs.CacheEncryptionSettingsResponse']]:
        """
        Specifies encryption settings of the cache.
        """
        return pulumi.get(self, "encryption_settings")

    @property
    @pulumi.getter
    def health(self) -> pulumi.Output['outputs.CacheHealthResponse']:
        """
        Health of the Cache.
        """
        return pulumi.get(self, "health")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.CacheIdentityResponse']]:
        """
        The identity of the cache, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Region name string.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mountAddresses")
    def mount_addresses(self) -> pulumi.Output[Sequence[str]]:
        """
        Array of IP addresses that can be used by clients mounting this Cache.
        """
        return pulumi.get(self, "mount_addresses")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of Cache.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkSettings")
    def network_settings(self) -> pulumi.Output[Optional['outputs.CacheNetworkSettingsResponse']]:
        """
        Specifies network settings of the cache.
        """
        return pulumi.get(self, "network_settings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        ARM provisioning state, see https://github.com/Azure/azure-resource-manager-rpc/blob/master/v1.0/Addendum.md#provisioningstate-property
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="securitySettings")
    def security_settings(self) -> pulumi.Output[Optional['outputs.CacheSecuritySettingsResponse']]:
        """
        Specifies security settings of the cache.
        """
        return pulumi.get(self, "security_settings")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.CacheResponseSku']]:
        """
        SKU for the Cache.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def subnet(self) -> pulumi.Output[Optional[str]]:
        """
        Subnet used for the Cache.
        """
        return pulumi.get(self, "subnet")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        """
        ARM tags as name/value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the Cache; Microsoft.StorageCache/Cache
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="upgradeStatus")
    def upgrade_status(self) -> pulumi.Output[Optional['outputs.CacheUpgradeStatusResponse']]:
        """
        Upgrade status of the Cache.
        """
        return pulumi.get(self, "upgrade_status")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

