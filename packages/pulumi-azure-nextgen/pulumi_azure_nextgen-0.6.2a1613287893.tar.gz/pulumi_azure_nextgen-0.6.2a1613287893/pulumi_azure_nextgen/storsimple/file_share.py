# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from ._enums import *

__all__ = ['FileShare']


class FileShare(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_user: Optional[pulumi.Input[str]] = None,
                 data_policy: Optional[pulumi.Input['DataPolicy']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 file_server_name: Optional[pulumi.Input[str]] = None,
                 manager_name: Optional[pulumi.Input[str]] = None,
                 monitoring_status: Optional[pulumi.Input['MonitoringStatus']] = None,
                 provisioned_capacity_in_bytes: Optional[pulumi.Input[float]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 share_name: Optional[pulumi.Input[str]] = None,
                 share_status: Optional[pulumi.Input['ShareStatus']] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The File Share.
        API Version: 2016-10-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] admin_user: The user/group who will have full permission in this share. Active directory email address. Example: xyz@contoso.com or Contoso\\xyz.
        :param pulumi.Input['DataPolicy'] data_policy: The data policy
        :param pulumi.Input[str] description: Description for file share
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] file_server_name: The file server name.
        :param pulumi.Input[str] manager_name: The manager name
        :param pulumi.Input['MonitoringStatus'] monitoring_status: The monitoring status
        :param pulumi.Input[float] provisioned_capacity_in_bytes: The total provisioned capacity in Bytes
        :param pulumi.Input[str] resource_group_name: The resource group name
        :param pulumi.Input[str] share_name: The file share name.
        :param pulumi.Input['ShareStatus'] share_status: The Share Status
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

            if admin_user is None and not opts.urn:
                raise TypeError("Missing required property 'admin_user'")
            __props__['admin_user'] = admin_user
            if data_policy is None and not opts.urn:
                raise TypeError("Missing required property 'data_policy'")
            __props__['data_policy'] = data_policy
            __props__['description'] = description
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__['device_name'] = device_name
            if file_server_name is None and not opts.urn:
                raise TypeError("Missing required property 'file_server_name'")
            __props__['file_server_name'] = file_server_name
            if manager_name is None and not opts.urn:
                raise TypeError("Missing required property 'manager_name'")
            __props__['manager_name'] = manager_name
            if monitoring_status is None and not opts.urn:
                raise TypeError("Missing required property 'monitoring_status'")
            __props__['monitoring_status'] = monitoring_status
            if provisioned_capacity_in_bytes is None and not opts.urn:
                raise TypeError("Missing required property 'provisioned_capacity_in_bytes'")
            __props__['provisioned_capacity_in_bytes'] = provisioned_capacity_in_bytes
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if share_name is None and not opts.urn:
                raise TypeError("Missing required property 'share_name'")
            __props__['share_name'] = share_name
            if share_status is None and not opts.urn:
                raise TypeError("Missing required property 'share_status'")
            __props__['share_status'] = share_status
            __props__['local_used_capacity_in_bytes'] = None
            __props__['name'] = None
            __props__['type'] = None
            __props__['used_capacity_in_bytes'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storsimple/latest:FileShare"), pulumi.Alias(type_="azure-nextgen:storsimple/v20161001:FileShare")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FileShare, __self__).__init__(
            'azure-nextgen:storsimple:FileShare',
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
    @pulumi.getter(name="adminUser")
    def admin_user(self) -> pulumi.Output[str]:
        """
        The user/group who will have full permission in this share. Active directory email address. Example: xyz@contoso.com or Contoso\\xyz.
        """
        return pulumi.get(self, "admin_user")

    @property
    @pulumi.getter(name="dataPolicy")
    def data_policy(self) -> pulumi.Output[str]:
        """
        The data policy
        """
        return pulumi.get(self, "data_policy")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description for file share
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="localUsedCapacityInBytes")
    def local_used_capacity_in_bytes(self) -> pulumi.Output[float]:
        """
        The local used capacity in Bytes.
        """
        return pulumi.get(self, "local_used_capacity_in_bytes")

    @property
    @pulumi.getter(name="monitoringStatus")
    def monitoring_status(self) -> pulumi.Output[str]:
        """
        The monitoring status
        """
        return pulumi.get(self, "monitoring_status")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisionedCapacityInBytes")
    def provisioned_capacity_in_bytes(self) -> pulumi.Output[float]:
        """
        The total provisioned capacity in Bytes
        """
        return pulumi.get(self, "provisioned_capacity_in_bytes")

    @property
    @pulumi.getter(name="shareStatus")
    def share_status(self) -> pulumi.Output[str]:
        """
        The Share Status
        """
        return pulumi.get(self, "share_status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usedCapacityInBytes")
    def used_capacity_in_bytes(self) -> pulumi.Output[float]:
        """
        The used capacity in Bytes.
        """
        return pulumi.get(self, "used_capacity_in_bytes")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

