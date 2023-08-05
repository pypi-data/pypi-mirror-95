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

__all__ = ['StorageAccount']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:storage:StorageAccount'.""", DeprecationWarning)


class StorageAccount(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:storage:StorageAccount'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_tier: Optional[pulumi.Input['AccessTier']] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 allow_blob_public_access: Optional[pulumi.Input[bool]] = None,
                 allow_shared_key_access: Optional[pulumi.Input[bool]] = None,
                 azure_files_identity_based_authentication: Optional[pulumi.Input[pulumi.InputType['AzureFilesIdentityBasedAuthenticationArgs']]] = None,
                 custom_domain: Optional[pulumi.Input[pulumi.InputType['CustomDomainArgs']]] = None,
                 enable_https_traffic_only: Optional[pulumi.Input[bool]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['EncryptionArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 is_hns_enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'Kind']]] = None,
                 large_file_shares_state: Optional[pulumi.Input[Union[str, 'LargeFileSharesState']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 minimum_tls_version: Optional[pulumi.Input[Union[str, 'MinimumTlsVersion']]] = None,
                 network_rule_set: Optional[pulumi.Input[pulumi.InputType['NetworkRuleSetArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_preference: Optional[pulumi.Input[pulumi.InputType['RoutingPreferenceArgs']]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The storage account.
        Latest API Version: 2019-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['AccessTier'] access_tier: Required for storage accounts where kind = BlobStorage. The access tier used for billing.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[bool] allow_blob_public_access: Allow or disallow public access to all blobs or containers in the storage account. The default interpretation is true for this property.
        :param pulumi.Input[bool] allow_shared_key_access: Indicates whether the storage account permits requests to be authorized with the account access key via Shared Key. If false, then all requests, including shared access signatures, must be authorized with Azure Active Directory (Azure AD). The default value is null, which is equivalent to true.
        :param pulumi.Input[pulumi.InputType['AzureFilesIdentityBasedAuthenticationArgs']] azure_files_identity_based_authentication: Provides the identity based authentication settings for Azure Files.
        :param pulumi.Input[pulumi.InputType['CustomDomainArgs']] custom_domain: User domain assigned to the storage account. Name is the CNAME source. Only one custom domain is supported per storage account at this time. To clear the existing custom domain, use an empty string for the custom domain name property.
        :param pulumi.Input[bool] enable_https_traffic_only: Allows https traffic only to storage service if sets to true. The default value is true since API version 2019-04-01.
        :param pulumi.Input[pulumi.InputType['EncryptionArgs']] encryption: Not applicable. Azure Storage encryption is enabled for all storage accounts and cannot be disabled.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: The identity of the resource.
        :param pulumi.Input[bool] is_hns_enabled: Account HierarchicalNamespace enabled if sets to true.
        :param pulumi.Input[Union[str, 'Kind']] kind: Required. Indicates the type of storage account.
        :param pulumi.Input[Union[str, 'LargeFileSharesState']] large_file_shares_state: Allow large file shares if sets to Enabled. It cannot be disabled once it is enabled.
        :param pulumi.Input[str] location: Required. Gets or sets the location of the resource. This will be one of the supported and registered Azure Geo Regions (e.g. West US, East US, Southeast Asia, etc.). The geo region of a resource cannot be changed once it is created, but if an identical geo region is specified on update, the request will succeed.
        :param pulumi.Input[Union[str, 'MinimumTlsVersion']] minimum_tls_version: Set the minimum TLS version to be permitted on requests to storage. The default interpretation is TLS 1.0 for this property.
        :param pulumi.Input[pulumi.InputType['NetworkRuleSetArgs']] network_rule_set: Network rule set
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['RoutingPreferenceArgs']] routing_preference: Maintains information about the network routing choice opted by the user for data transfer
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Required. Gets or sets the SKU name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets a list of key value pairs that describe the resource. These tags can be used for viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key with a length no greater than 128 characters and a value with a length no greater than 256 characters.
        """
        pulumi.log.warn("StorageAccount is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:storage:StorageAccount'.")
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

            __props__['access_tier'] = access_tier
            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            __props__['allow_blob_public_access'] = allow_blob_public_access
            __props__['allow_shared_key_access'] = allow_shared_key_access
            __props__['azure_files_identity_based_authentication'] = azure_files_identity_based_authentication
            __props__['custom_domain'] = custom_domain
            __props__['enable_https_traffic_only'] = enable_https_traffic_only
            __props__['encryption'] = encryption
            __props__['identity'] = identity
            __props__['is_hns_enabled'] = is_hns_enabled
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__['kind'] = kind
            __props__['large_file_shares_state'] = large_file_shares_state
            __props__['location'] = location
            __props__['minimum_tls_version'] = minimum_tls_version
            __props__['network_rule_set'] = network_rule_set
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['routing_preference'] = routing_preference
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['blob_restore_status'] = None
            __props__['creation_time'] = None
            __props__['failover_in_progress'] = None
            __props__['geo_replication_stats'] = None
            __props__['last_geo_failover_time'] = None
            __props__['name'] = None
            __props__['primary_endpoints'] = None
            __props__['primary_location'] = None
            __props__['private_endpoint_connections'] = None
            __props__['provisioning_state'] = None
            __props__['secondary_endpoints'] = None
            __props__['secondary_location'] = None
            __props__['status_of_primary'] = None
            __props__['status_of_secondary'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storage:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20150501preview:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20150615:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20160101:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20160501:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20161201:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20170601:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20171001:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20180201:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20180301preview:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20180701:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20181101:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20190401:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20190601:StorageAccount"), pulumi.Alias(type_="azure-nextgen:storage/v20200801preview:StorageAccount")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageAccount, __self__).__init__(
            'azure-nextgen:storage/latest:StorageAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageAccount':
        """
        Get an existing StorageAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StorageAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> pulumi.Output[str]:
        """
        Required for storage accounts where kind = BlobStorage. The access tier used for billing.
        """
        return pulumi.get(self, "access_tier")

    @property
    @pulumi.getter(name="allowBlobPublicAccess")
    def allow_blob_public_access(self) -> pulumi.Output[Optional[bool]]:
        """
        Allow or disallow public access to all blobs or containers in the storage account. The default interpretation is true for this property.
        """
        return pulumi.get(self, "allow_blob_public_access")

    @property
    @pulumi.getter(name="allowSharedKeyAccess")
    def allow_shared_key_access(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the storage account permits requests to be authorized with the account access key via Shared Key. If false, then all requests, including shared access signatures, must be authorized with Azure Active Directory (Azure AD). The default value is null, which is equivalent to true.
        """
        return pulumi.get(self, "allow_shared_key_access")

    @property
    @pulumi.getter(name="azureFilesIdentityBasedAuthentication")
    def azure_files_identity_based_authentication(self) -> pulumi.Output[Optional['outputs.AzureFilesIdentityBasedAuthenticationResponse']]:
        """
        Provides the identity based authentication settings for Azure Files.
        """
        return pulumi.get(self, "azure_files_identity_based_authentication")

    @property
    @pulumi.getter(name="blobRestoreStatus")
    def blob_restore_status(self) -> pulumi.Output['outputs.BlobRestoreStatusResponse']:
        """
        Blob restore status
        """
        return pulumi.get(self, "blob_restore_status")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        Gets the creation date and time of the storage account in UTC.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="customDomain")
    def custom_domain(self) -> pulumi.Output['outputs.CustomDomainResponse']:
        """
        Gets the custom domain the user assigned to this storage account.
        """
        return pulumi.get(self, "custom_domain")

    @property
    @pulumi.getter(name="enableHttpsTrafficOnly")
    def enable_https_traffic_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Allows https traffic only to storage service if sets to true.
        """
        return pulumi.get(self, "enable_https_traffic_only")

    @property
    @pulumi.getter
    def encryption(self) -> pulumi.Output['outputs.EncryptionResponse']:
        """
        Gets the encryption settings on the account. If unspecified, the account is unencrypted.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter(name="failoverInProgress")
    def failover_in_progress(self) -> pulumi.Output[bool]:
        """
        If the failover is in progress, the value will be true, otherwise, it will be null.
        """
        return pulumi.get(self, "failover_in_progress")

    @property
    @pulumi.getter(name="geoReplicationStats")
    def geo_replication_stats(self) -> pulumi.Output['outputs.GeoReplicationStatsResponse']:
        """
        Geo Replication Stats
        """
        return pulumi.get(self, "geo_replication_stats")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="isHnsEnabled")
    def is_hns_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Account HierarchicalNamespace enabled if sets to true.
        """
        return pulumi.get(self, "is_hns_enabled")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Gets the Kind.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="largeFileSharesState")
    def large_file_shares_state(self) -> pulumi.Output[Optional[str]]:
        """
        Allow large file shares if sets to Enabled. It cannot be disabled once it is enabled.
        """
        return pulumi.get(self, "large_file_shares_state")

    @property
    @pulumi.getter(name="lastGeoFailoverTime")
    def last_geo_failover_time(self) -> pulumi.Output[str]:
        """
        Gets the timestamp of the most recent instance of a failover to the secondary location. Only the most recent timestamp is retained. This element is not returned if there has never been a failover instance. Only available if the accountType is Standard_GRS or Standard_RAGRS.
        """
        return pulumi.get(self, "last_geo_failover_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="minimumTlsVersion")
    def minimum_tls_version(self) -> pulumi.Output[Optional[str]]:
        """
        Set the minimum TLS version to be permitted on requests to storage. The default interpretation is TLS 1.0 for this property.
        """
        return pulumi.get(self, "minimum_tls_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkRuleSet")
    def network_rule_set(self) -> pulumi.Output['outputs.NetworkRuleSetResponse']:
        """
        Network rule set
        """
        return pulumi.get(self, "network_rule_set")

    @property
    @pulumi.getter(name="primaryEndpoints")
    def primary_endpoints(self) -> pulumi.Output['outputs.EndpointsResponse']:
        """
        Gets the URLs that are used to perform a retrieval of a public blob, queue, or table object. Note that Standard_ZRS and Premium_LRS accounts only return the blob endpoint.
        """
        return pulumi.get(self, "primary_endpoints")

    @property
    @pulumi.getter(name="primaryLocation")
    def primary_location(self) -> pulumi.Output[str]:
        """
        Gets the location of the primary data center for the storage account.
        """
        return pulumi.get(self, "primary_location")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        List of private endpoint connection associated with the specified storage account
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Gets the status of the storage account at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="routingPreference")
    def routing_preference(self) -> pulumi.Output[Optional['outputs.RoutingPreferenceResponse']]:
        """
        Maintains information about the network routing choice opted by the user for data transfer
        """
        return pulumi.get(self, "routing_preference")

    @property
    @pulumi.getter(name="secondaryEndpoints")
    def secondary_endpoints(self) -> pulumi.Output['outputs.EndpointsResponse']:
        """
        Gets the URLs that are used to perform a retrieval of a public blob, queue, or table object from the secondary location of the storage account. Only available if the SKU name is Standard_RAGRS.
        """
        return pulumi.get(self, "secondary_endpoints")

    @property
    @pulumi.getter(name="secondaryLocation")
    def secondary_location(self) -> pulumi.Output[str]:
        """
        Gets the location of the geo-replicated secondary for the storage account. Only available if the accountType is Standard_GRS or Standard_RAGRS.
        """
        return pulumi.get(self, "secondary_location")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        Gets the SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="statusOfPrimary")
    def status_of_primary(self) -> pulumi.Output[str]:
        """
        Gets the status indicating whether the primary location of the storage account is available or unavailable.
        """
        return pulumi.get(self, "status_of_primary")

    @property
    @pulumi.getter(name="statusOfSecondary")
    def status_of_secondary(self) -> pulumi.Output[str]:
        """
        Gets the status indicating whether the secondary location of the storage account is available or unavailable. Only available if the SKU name is Standard_GRS or Standard_RAGRS.
        """
        return pulumi.get(self, "status_of_secondary")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

