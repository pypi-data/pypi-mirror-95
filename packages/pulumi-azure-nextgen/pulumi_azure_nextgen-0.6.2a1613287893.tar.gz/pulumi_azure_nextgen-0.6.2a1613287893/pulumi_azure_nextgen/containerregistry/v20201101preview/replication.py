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

__all__ = ['Replication']


class Replication(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 region_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 replication_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundancy: Optional[pulumi.Input[Union[str, 'ZoneRedundancy']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An object that represents a replication for a container registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[bool] region_endpoint_enabled: Specifies whether the replication's regional endpoint is enabled. Requests will not be routed to a replication whose regional endpoint is disabled, however its data will continue to be synced with other replications.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] replication_name: The name of the replication.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[Union[str, 'ZoneRedundancy']] zone_redundancy: Whether or not zone redundancy is enabled for this container registry replication
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

            __props__['location'] = location
            if region_endpoint_enabled is None:
                region_endpoint_enabled = True
            __props__['region_endpoint_enabled'] = region_endpoint_enabled
            if registry_name is None and not opts.urn:
                raise TypeError("Missing required property 'registry_name'")
            __props__['registry_name'] = registry_name
            if replication_name is None and not opts.urn:
                raise TypeError("Missing required property 'replication_name'")
            __props__['replication_name'] = replication_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            if zone_redundancy is None:
                zone_redundancy = 'Disabled'
            __props__['zone_redundancy'] = zone_redundancy
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['status'] = None
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:containerregistry:Replication"), pulumi.Alias(type_="azure-nextgen:containerregistry/latest:Replication"), pulumi.Alias(type_="azure-nextgen:containerregistry/v20170601preview:Replication"), pulumi.Alias(type_="azure-nextgen:containerregistry/v20171001:Replication"), pulumi.Alias(type_="azure-nextgen:containerregistry/v20190501:Replication"), pulumi.Alias(type_="azure-nextgen:containerregistry/v20191201preview:Replication")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Replication, __self__).__init__(
            'azure-nextgen:containerregistry/v20201101preview:Replication',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Replication':
        """
        Get an existing Replication resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Replication(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the replication at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="regionEndpointEnabled")
    def region_endpoint_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the replication's regional endpoint is enabled. Requests will not be routed to a replication whose regional endpoint is disabled, however its data will continue to be synced with other replications.
        """
        return pulumi.get(self, "region_endpoint_enabled")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.StatusResponse']:
        """
        The status of the replication at the time the operation was called.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneRedundancy")
    def zone_redundancy(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not zone redundancy is enabled for this container registry replication
        """
        return pulumi.get(self, "zone_redundancy")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

