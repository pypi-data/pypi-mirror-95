# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['CustomDomain']


class CustomDomain(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 custom_domain_name: Optional[pulumi.Input[str]] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        CDN CustomDomain represents a mapping between a user specified domain name and a CDN endpoint. This is to use custom domain names to represent the URLs for branding purposes.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] custom_domain_name: Name of the custom domain within an endpoint.
        :param pulumi.Input[str] endpoint_name: Name of the endpoint within the CDN profile.
        :param pulumi.Input[str] host_name: The host name of the custom domain. Must be a domain name.
        :param pulumi.Input[str] profile_name: Name of the CDN profile within the resource group.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the Azure subscription.
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

            if custom_domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'custom_domain_name'")
            __props__['custom_domain_name'] = custom_domain_name
            if endpoint_name is None and not opts.urn:
                raise TypeError("Missing required property 'endpoint_name'")
            __props__['endpoint_name'] = endpoint_name
            if host_name is None and not opts.urn:
                raise TypeError("Missing required property 'host_name'")
            __props__['host_name'] = host_name
            if profile_name is None and not opts.urn:
                raise TypeError("Missing required property 'profile_name'")
            __props__['profile_name'] = profile_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['resource_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:cdn:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/latest:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20160402:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20161002:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20170402:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20171012:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20190415:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20190615:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20190615preview:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20191231:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20200331:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20200415:CustomDomain"), pulumi.Alias(type_="azure-nextgen:cdn/v20200901:CustomDomain")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(CustomDomain, __self__).__init__(
            'azure-nextgen:cdn/v20150601:CustomDomain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CustomDomain':
        """
        Get an existing CustomDomain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return CustomDomain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        The host name of the custom domain. Must be a domain name.
        """
        return pulumi.get(self, "host_name")

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
        Provisioning status of the custom domain.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        Resource status of the custom domain.
        """
        return pulumi.get(self, "resource_state")

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

