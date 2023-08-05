# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['VpnSite']


class VpnSite(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_space: Optional[pulumi.Input[pulumi.InputType['AddressSpaceArgs']]] = None,
                 bgp_properties: Optional[pulumi.Input[pulumi.InputType['BgpSettingsArgs']]] = None,
                 device_properties: Optional[pulumi.Input[pulumi.InputType['DevicePropertiesArgs']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 is_security_site: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 site_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_wan: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 vpn_site_links: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpnSiteLinkArgs']]]]] = None,
                 vpn_site_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        VpnSite Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AddressSpaceArgs']] address_space: The AddressSpace that contains an array of IP address ranges.
        :param pulumi.Input[pulumi.InputType['BgpSettingsArgs']] bgp_properties: The set of bgp properties.
        :param pulumi.Input[pulumi.InputType['DevicePropertiesArgs']] device_properties: The device properties.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] ip_address: The ip-address for the vpn-site.
        :param pulumi.Input[bool] is_security_site: IsSecuritySite flag.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VpnSite.
        :param pulumi.Input[str] site_key: The key for vpn-site that can be used for connections.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] virtual_wan: The VirtualWAN to which the vpnSite belongs.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VpnSiteLinkArgs']]]] vpn_site_links: List of all vpn site links.
        :param pulumi.Input[str] vpn_site_name: The name of the VpnSite being created or updated.
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

            __props__['address_space'] = address_space
            __props__['bgp_properties'] = bgp_properties
            __props__['device_properties'] = device_properties
            __props__['id'] = id
            __props__['ip_address'] = ip_address
            __props__['is_security_site'] = is_security_site
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['site_key'] = site_key
            __props__['tags'] = tags
            __props__['virtual_wan'] = virtual_wan
            __props__['vpn_site_links'] = vpn_site_links
            if vpn_site_name is None and not opts.urn:
                raise TypeError("Missing required property 'vpn_site_name'")
            __props__['vpn_site_name'] = vpn_site_name
            __props__['etag'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/latest:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20180401:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20180601:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20180701:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20180801:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20181001:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20181101:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20181201:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20190201:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20190401:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20190601:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20190701:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20190901:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20191101:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20191201:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20200301:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20200401:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20200501:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20200601:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20200701:VpnSite"), pulumi.Alias(type_="azure-nextgen:network/v20200801:VpnSite")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VpnSite, __self__).__init__(
            'azure-nextgen:network/v20190801:VpnSite',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VpnSite':
        """
        Get an existing VpnSite resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VpnSite(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressSpace")
    def address_space(self) -> pulumi.Output[Optional['outputs.AddressSpaceResponse']]:
        """
        The AddressSpace that contains an array of IP address ranges.
        """
        return pulumi.get(self, "address_space")

    @property
    @pulumi.getter(name="bgpProperties")
    def bgp_properties(self) -> pulumi.Output[Optional['outputs.BgpSettingsResponse']]:
        """
        The set of bgp properties.
        """
        return pulumi.get(self, "bgp_properties")

    @property
    @pulumi.getter(name="deviceProperties")
    def device_properties(self) -> pulumi.Output[Optional['outputs.DevicePropertiesResponse']]:
        """
        The device properties.
        """
        return pulumi.get(self, "device_properties")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[Optional[str]]:
        """
        The ip-address for the vpn-site.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="isSecuritySite")
    def is_security_site(self) -> pulumi.Output[Optional[bool]]:
        """
        IsSecuritySite flag.
        """
        return pulumi.get(self, "is_security_site")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

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
        The provisioning state of the VPN site resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="siteKey")
    def site_key(self) -> pulumi.Output[Optional[str]]:
        """
        The key for vpn-site that can be used for connections.
        """
        return pulumi.get(self, "site_key")

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
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualWan")
    def virtual_wan(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The VirtualWAN to which the vpnSite belongs.
        """
        return pulumi.get(self, "virtual_wan")

    @property
    @pulumi.getter(name="vpnSiteLinks")
    def vpn_site_links(self) -> pulumi.Output[Optional[Sequence['outputs.VpnSiteLinkResponse']]]:
        """
        List of all vpn site links.
        """
        return pulumi.get(self, "vpn_site_links")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

