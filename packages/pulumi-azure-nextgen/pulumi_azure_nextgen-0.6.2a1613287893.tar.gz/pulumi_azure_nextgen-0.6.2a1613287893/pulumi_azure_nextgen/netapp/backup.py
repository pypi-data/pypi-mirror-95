# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Backup']


class Backup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 backup_name: Optional[pulumi.Input[str]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 pool_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 volume_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Backup of a Volume
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] backup_name: The name of the backup
        :param pulumi.Input[str] label: Label for backup
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] pool_name: The name of the capacity pool
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] volume_name: The name of the volume
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

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            if backup_name is None and not opts.urn:
                raise TypeError("Missing required property 'backup_name'")
            __props__['backup_name'] = backup_name
            __props__['label'] = label
            __props__['location'] = location
            if pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'pool_name'")
            __props__['pool_name'] = pool_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if volume_name is None and not opts.urn:
                raise TypeError("Missing required property 'volume_name'")
            __props__['volume_name'] = volume_name
            __props__['backup_id'] = None
            __props__['backup_type'] = None
            __props__['creation_date'] = None
            __props__['failure_reason'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['size'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:netapp/latest:Backup"), pulumi.Alias(type_="azure-nextgen:netapp/v20200501:Backup"), pulumi.Alias(type_="azure-nextgen:netapp/v20200601:Backup"), pulumi.Alias(type_="azure-nextgen:netapp/v20200701:Backup"), pulumi.Alias(type_="azure-nextgen:netapp/v20200801:Backup"), pulumi.Alias(type_="azure-nextgen:netapp/v20200901:Backup"), pulumi.Alias(type_="azure-nextgen:netapp/v20201101:Backup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Backup, __self__).__init__(
            'azure-nextgen:netapp:Backup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Backup':
        """
        Get an existing Backup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Backup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupId")
    def backup_id(self) -> pulumi.Output[str]:
        """
        UUID v4 used to identify the Backup
        """
        return pulumi.get(self, "backup_id")

    @property
    @pulumi.getter(name="backupType")
    def backup_type(self) -> pulumi.Output[str]:
        """
        Type of backup adhoc or scheduled
        """
        return pulumi.get(self, "backup_type")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of the backup
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> pulumi.Output[str]:
        """
        Failure reason
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter
    def label(self) -> pulumi.Output[Optional[str]]:
        """
        Label for backup
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[float]:
        """
        Size of backup
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

