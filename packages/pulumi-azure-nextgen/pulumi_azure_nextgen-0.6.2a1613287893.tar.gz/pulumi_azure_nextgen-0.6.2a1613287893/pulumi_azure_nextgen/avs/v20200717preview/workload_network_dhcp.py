# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['WorkloadNetworkDhcp']


class WorkloadNetworkDhcp(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dhcp_id: Optional[pulumi.Input[str]] = None,
                 dhcp_type: Optional[pulumi.Input[Union[str, 'DhcpTypeEnum']]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[float]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        NSX DHCP

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dhcp_id: NSX DHCP identifier. Generally the same as the DHCP display name
        :param pulumi.Input[Union[str, 'DhcpTypeEnum']] dhcp_type: Type of DHCP: SERVER or RELAY.
        :param pulumi.Input[str] display_name: Display name of the DHCP entity.
        :param pulumi.Input[str] private_cloud_name: Name of the private cloud
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[float] revision: NSX revision number.
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

            if dhcp_id is None and not opts.urn:
                raise TypeError("Missing required property 'dhcp_id'")
            __props__['dhcp_id'] = dhcp_id
            if dhcp_type is None and not opts.urn:
                raise TypeError("Missing required property 'dhcp_type'")
            __props__['dhcp_type'] = dhcp_type
            __props__['display_name'] = display_name
            if private_cloud_name is None and not opts.urn:
                raise TypeError("Missing required property 'private_cloud_name'")
            __props__['private_cloud_name'] = private_cloud_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['revision'] = revision
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['segments'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:avs:WorkloadNetworkDhcp")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WorkloadNetworkDhcp, __self__).__init__(
            'azure-nextgen:avs/v20200717preview:WorkloadNetworkDhcp',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WorkloadNetworkDhcp':
        """
        Get an existing WorkloadNetworkDhcp resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WorkloadNetworkDhcp(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dhcpType")
    def dhcp_type(self) -> pulumi.Output[str]:
        """
        Type of DHCP: SERVER or RELAY.
        """
        return pulumi.get(self, "dhcp_type")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Display name of the DHCP entity.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Output[Optional[float]]:
        """
        NSX revision number.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def segments(self) -> pulumi.Output[Sequence[str]]:
        """
        NSX Segments consuming DHCP.
        """
        return pulumi.get(self, "segments")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

