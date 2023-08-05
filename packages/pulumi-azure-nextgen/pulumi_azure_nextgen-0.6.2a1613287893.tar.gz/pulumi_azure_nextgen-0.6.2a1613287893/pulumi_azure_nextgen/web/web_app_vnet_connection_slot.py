# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = ['WebAppVnetConnectionSlot']


class WebAppVnetConnectionSlot(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cert_blob: Optional[pulumi.Input[str]] = None,
                 dns_servers: Optional[pulumi.Input[str]] = None,
                 is_swift: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 vnet_name: Optional[pulumi.Input[str]] = None,
                 vnet_resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Virtual Network information contract.
        API Version: 2020-10-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cert_blob: A certificate file (.cer) blob containing the public key of the private key used to authenticate a 
               Point-To-Site VPN connection.
        :param pulumi.Input[str] dns_servers: DNS servers to be used by this Virtual Network. This should be a comma-separated list of IP addresses.
        :param pulumi.Input[bool] is_swift: Flag that is used to denote if this is VNET injection
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of the deployment slot. If a slot is not specified, the API will add or update connections for the production slot.
        :param pulumi.Input[str] vnet_name: Name of an existing Virtual Network.
        :param pulumi.Input[str] vnet_resource_id: The Virtual Network's resource ID.
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

            __props__['cert_blob'] = cert_blob
            __props__['dns_servers'] = dns_servers
            __props__['is_swift'] = is_swift
            __props__['kind'] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__['slot'] = slot
            if vnet_name is None and not opts.urn:
                raise TypeError("Missing required property 'vnet_name'")
            __props__['vnet_name'] = vnet_name
            __props__['vnet_resource_id'] = vnet_resource_id
            __props__['cert_thumbprint'] = None
            __props__['resync_required'] = None
            __props__['routes'] = None
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web/latest:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20150801:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20160801:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20181101:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppVnetConnectionSlot"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppVnetConnectionSlot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppVnetConnectionSlot, __self__).__init__(
            'azure-nextgen:web:WebAppVnetConnectionSlot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppVnetConnectionSlot':
        """
        Get an existing WebAppVnetConnectionSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppVnetConnectionSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="certBlob")
    def cert_blob(self) -> pulumi.Output[Optional[str]]:
        """
        A certificate file (.cer) blob containing the public key of the private key used to authenticate a 
        Point-To-Site VPN connection.
        """
        return pulumi.get(self, "cert_blob")

    @property
    @pulumi.getter(name="certThumbprint")
    def cert_thumbprint(self) -> pulumi.Output[str]:
        """
        The client certificate thumbprint.
        """
        return pulumi.get(self, "cert_thumbprint")

    @property
    @pulumi.getter(name="dnsServers")
    def dns_servers(self) -> pulumi.Output[Optional[str]]:
        """
        DNS servers to be used by this Virtual Network. This should be a comma-separated list of IP addresses.
        """
        return pulumi.get(self, "dns_servers")

    @property
    @pulumi.getter(name="isSwift")
    def is_swift(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag that is used to denote if this is VNET injection
        """
        return pulumi.get(self, "is_swift")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resyncRequired")
    def resync_required(self) -> pulumi.Output[bool]:
        """
        <code>true</code> if a resync is required; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "resync_required")

    @property
    @pulumi.getter
    def routes(self) -> pulumi.Output[Sequence['outputs.VnetRouteResponse']]:
        """
        The routes that this Virtual Network connection uses.
        """
        return pulumi.get(self, "routes")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vnetResourceId")
    def vnet_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Virtual Network's resource ID.
        """
        return pulumi.get(self, "vnet_resource_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

