# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *

__all__ = ['StorageSyncService']


class StorageSyncService(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 incoming_traffic_policy: Optional[pulumi.Input[Union[str, 'IncomingTrafficPolicy']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_sync_service_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Storage Sync Service object.
        API Version: 2020-03-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'IncomingTrafficPolicy']] incoming_traffic_policy: Incoming Traffic Policy
        :param pulumi.Input[str] location: Required. Gets or sets the location of the resource. This will be one of the supported and registered Azure Geo Regions (e.g. West US, East US, Southeast Asia, etc.). The geo region of a resource cannot be changed once it is created, but if an identical geo region is specified on update, the request will succeed.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] storage_sync_service_name: Name of Storage Sync Service resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets a list of key value pairs that describe the resource. These tags can be used for viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key with a length no greater than 128 characters and a value with a length no greater than 256 characters.
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

            __props__['incoming_traffic_policy'] = incoming_traffic_policy
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if storage_sync_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_sync_service_name'")
            __props__['storage_sync_service_name'] = storage_sync_service_name
            __props__['tags'] = tags
            __props__['last_operation_name'] = None
            __props__['last_workflow_id'] = None
            __props__['name'] = None
            __props__['private_endpoint_connections'] = None
            __props__['provisioning_state'] = None
            __props__['storage_sync_service_status'] = None
            __props__['storage_sync_service_uid'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storagesync/latest:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20170605preview:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20180402:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20180701:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20181001:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190201:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190301:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190601:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20191001:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20200301:StorageSyncService"), pulumi.Alias(type_="azure-nextgen:storagesync/v20200901:StorageSyncService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageSyncService, __self__).__init__(
            'azure-nextgen:storagesync:StorageSyncService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageSyncService':
        """
        Get an existing StorageSyncService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StorageSyncService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="incomingTrafficPolicy")
    def incoming_traffic_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Incoming Traffic Policy
        """
        return pulumi.get(self, "incoming_traffic_policy")

    @property
    @pulumi.getter(name="lastOperationName")
    def last_operation_name(self) -> pulumi.Output[str]:
        """
        Resource Last Operation Name
        """
        return pulumi.get(self, "last_operation_name")

    @property
    @pulumi.getter(name="lastWorkflowId")
    def last_workflow_id(self) -> pulumi.Output[str]:
        """
        StorageSyncService lastWorkflowId
        """
        return pulumi.get(self, "last_workflow_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        List of private endpoint connection associated with the specified storage sync service
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        StorageSyncService Provisioning State
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="storageSyncServiceStatus")
    def storage_sync_service_status(self) -> pulumi.Output[int]:
        """
        Storage Sync service status.
        """
        return pulumi.get(self, "storage_sync_service_status")

    @property
    @pulumi.getter(name="storageSyncServiceUid")
    def storage_sync_service_uid(self) -> pulumi.Output[str]:
        """
        Storage Sync service Uid
        """
        return pulumi.get(self, "storage_sync_service_uid")

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

