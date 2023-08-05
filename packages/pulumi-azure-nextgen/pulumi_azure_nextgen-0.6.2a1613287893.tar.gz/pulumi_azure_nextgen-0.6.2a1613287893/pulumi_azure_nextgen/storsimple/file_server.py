# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['FileServer']


class FileServer(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_schedule_group_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 file_server_name: Optional[pulumi.Input[str]] = None,
                 manager_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_domain_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The file server.
        API Version: 2016-10-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_schedule_group_id: The backup policy id.
        :param pulumi.Input[str] description: The description of the file server
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] domain_name: Domain of the file server
        :param pulumi.Input[str] file_server_name: The file server name.
        :param pulumi.Input[str] manager_name: The manager name
        :param pulumi.Input[str] resource_group_name: The resource group name
        :param pulumi.Input[str] storage_domain_id: The storage domain id.
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

            if backup_schedule_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'backup_schedule_group_id'")
            __props__['backup_schedule_group_id'] = backup_schedule_group_id
            __props__['description'] = description
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__['device_name'] = device_name
            if domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'domain_name'")
            __props__['domain_name'] = domain_name
            if file_server_name is None and not opts.urn:
                raise TypeError("Missing required property 'file_server_name'")
            __props__['file_server_name'] = file_server_name
            if manager_name is None and not opts.urn:
                raise TypeError("Missing required property 'manager_name'")
            __props__['manager_name'] = manager_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if storage_domain_id is None and not opts.urn:
                raise TypeError("Missing required property 'storage_domain_id'")
            __props__['storage_domain_id'] = storage_domain_id
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storsimple/latest:FileServer"), pulumi.Alias(type_="azure-nextgen:storsimple/v20161001:FileServer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FileServer, __self__).__init__(
            'azure-nextgen:storsimple:FileServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FileServer':
        """
        Get an existing FileServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return FileServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupScheduleGroupId")
    def backup_schedule_group_id(self) -> pulumi.Output[str]:
        """
        The backup policy id.
        """
        return pulumi.get(self, "backup_schedule_group_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the file server
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        Domain of the file server
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="storageDomainId")
    def storage_domain_id(self) -> pulumi.Output[str]:
        """
        The storage domain id.
        """
        return pulumi.get(self, "storage_domain_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

