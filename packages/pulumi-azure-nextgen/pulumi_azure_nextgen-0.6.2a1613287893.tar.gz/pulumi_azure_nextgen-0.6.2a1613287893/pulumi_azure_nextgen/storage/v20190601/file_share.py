# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['FileShare']


class FileShare(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_tier: Optional[pulumi.Input[Union[str, 'ShareAccessTier']]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 enabled_protocols: Optional[pulumi.Input[Union[str, 'EnabledProtocols']]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 root_squash: Optional[pulumi.Input[Union[str, 'RootSquashType']]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 share_quota: Optional[pulumi.Input[int]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Properties of the file share, including Id, resource name, resource type, Etag.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'ShareAccessTier']] access_tier: Access tier for specific share. GpV2 account can choose between TransactionOptimized (default), Hot, and Cool. FileStorage account can choose Premium.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[Union[str, 'EnabledProtocols']] enabled_protocols: The authentication protocol that is used for the file share. Can only be specified when creating a share.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: A name-value pair to associate with the share as metadata.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[Union[str, 'RootSquashType']] root_squash: The property is for NFS share only. The default is NoRootSquash.
        :param pulumi.Input[str] share_name: The name of the file share within the specified storage account. File share names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
        :param pulumi.Input[int] share_quota: The maximum size of the share, in gigabytes. Must be greater than 0, and less than or equal to 5TB (5120). For Large File Shares, the maximum size is 102400.
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

            __props__['access_tier'] = access_tier
            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            __props__['enabled_protocols'] = enabled_protocols
            __props__['metadata'] = metadata
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['root_squash'] = root_squash
            if share_name is None and not opts.urn:
                raise TypeError("Missing required property 'share_name'")
            __props__['share_name'] = share_name
            __props__['share_quota'] = share_quota
            __props__['access_tier_change_time'] = None
            __props__['access_tier_status'] = None
            __props__['deleted'] = None
            __props__['deleted_time'] = None
            __props__['etag'] = None
            __props__['last_modified_time'] = None
            __props__['name'] = None
            __props__['remaining_retention_days'] = None
            __props__['share_usage_bytes'] = None
            __props__['type'] = None
            __props__['version'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storage:FileShare"), pulumi.Alias(type_="azure-nextgen:storage/latest:FileShare"), pulumi.Alias(type_="azure-nextgen:storage/v20190401:FileShare"), pulumi.Alias(type_="azure-nextgen:storage/v20200801preview:FileShare")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FileShare, __self__).__init__(
            'azure-nextgen:storage/v20190601:FileShare',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FileShare':
        """
        Get an existing FileShare resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return FileShare(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessTier")
    def access_tier(self) -> pulumi.Output[Optional[str]]:
        """
        Access tier for specific share. GpV2 account can choose between TransactionOptimized (default), Hot, and Cool. FileStorage account can choose Premium.
        """
        return pulumi.get(self, "access_tier")

    @property
    @pulumi.getter(name="accessTierChangeTime")
    def access_tier_change_time(self) -> pulumi.Output[str]:
        """
        Indicates the last modification time for share access tier.
        """
        return pulumi.get(self, "access_tier_change_time")

    @property
    @pulumi.getter(name="accessTierStatus")
    def access_tier_status(self) -> pulumi.Output[str]:
        """
        Indicates if there is a pending transition for access tier.
        """
        return pulumi.get(self, "access_tier_status")

    @property
    @pulumi.getter
    def deleted(self) -> pulumi.Output[bool]:
        """
        Indicates whether the share was deleted.
        """
        return pulumi.get(self, "deleted")

    @property
    @pulumi.getter(name="deletedTime")
    def deleted_time(self) -> pulumi.Output[str]:
        """
        The deleted time if the share was deleted.
        """
        return pulumi.get(self, "deleted_time")

    @property
    @pulumi.getter(name="enabledProtocols")
    def enabled_protocols(self) -> pulumi.Output[Optional[str]]:
        """
        The authentication protocol that is used for the file share. Can only be specified when creating a share.
        """
        return pulumi.get(self, "enabled_protocols")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Resource Etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Returns the date and time the share was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A name-value pair to associate with the share as metadata.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="remainingRetentionDays")
    def remaining_retention_days(self) -> pulumi.Output[int]:
        """
        Remaining retention days for share that was soft deleted.
        """
        return pulumi.get(self, "remaining_retention_days")

    @property
    @pulumi.getter(name="rootSquash")
    def root_squash(self) -> pulumi.Output[Optional[str]]:
        """
        The property is for NFS share only. The default is NoRootSquash.
        """
        return pulumi.get(self, "root_squash")

    @property
    @pulumi.getter(name="shareQuota")
    def share_quota(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum size of the share, in gigabytes. Must be greater than 0, and less than or equal to 5TB (5120). For Large File Shares, the maximum size is 102400.
        """
        return pulumi.get(self, "share_quota")

    @property
    @pulumi.getter(name="shareUsageBytes")
    def share_usage_bytes(self) -> pulumi.Output[float]:
        """
        The approximate size of the data stored on the share. Note that this value may not include all recently created or recently resized files.
        """
        return pulumi.get(self, "share_usage_bytes")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The version of the share.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

