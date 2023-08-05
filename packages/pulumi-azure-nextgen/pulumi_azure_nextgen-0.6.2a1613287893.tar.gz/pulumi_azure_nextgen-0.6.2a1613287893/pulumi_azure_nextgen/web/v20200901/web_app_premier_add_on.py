# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = ['WebAppPremierAddOn']


class WebAppPremierAddOn(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 marketplace_offer: Optional[pulumi.Input[str]] = None,
                 marketplace_publisher: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 premier_add_on_name: Optional[pulumi.Input[str]] = None,
                 product: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vendor: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Premier add-on.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] marketplace_offer: Premier add on Marketplace offer.
        :param pulumi.Input[str] marketplace_publisher: Premier add on Marketplace publisher.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] premier_add_on_name: Add-on name.
        :param pulumi.Input[str] product: Premier add on Product.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] sku: Premier add on SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] vendor: Premier add on Vendor.
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

            __props__['kind'] = kind
            __props__['location'] = location
            __props__['marketplace_offer'] = marketplace_offer
            __props__['marketplace_publisher'] = marketplace_publisher
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if premier_add_on_name is None and not opts.urn:
                raise TypeError("Missing required property 'premier_add_on_name'")
            __props__['premier_add_on_name'] = premier_add_on_name
            __props__['product'] = product
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['vendor'] = vendor
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/latest:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20150801:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20160801:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20181101:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppPremierAddOn"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppPremierAddOn")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppPremierAddOn, __self__).__init__(
            'azure-nextgen:web/v20200901:WebAppPremierAddOn',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppPremierAddOn':
        """
        Get an existing WebAppPremierAddOn resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppPremierAddOn(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="marketplaceOffer")
    def marketplace_offer(self) -> pulumi.Output[Optional[str]]:
        """
        Premier add on Marketplace offer.
        """
        return pulumi.get(self, "marketplace_offer")

    @property
    @pulumi.getter(name="marketplacePublisher")
    def marketplace_publisher(self) -> pulumi.Output[Optional[str]]:
        """
        Premier add on Marketplace publisher.
        """
        return pulumi.get(self, "marketplace_publisher")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def product(self) -> pulumi.Output[Optional[str]]:
        """
        Premier add on Product.
        """
        return pulumi.get(self, "product")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional[str]]:
        """
        Premier add on SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

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
    @pulumi.getter
    def vendor(self) -> pulumi.Output[Optional[str]]:
        """
        Premier add on Vendor.
        """
        return pulumi.get(self, "vendor")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

