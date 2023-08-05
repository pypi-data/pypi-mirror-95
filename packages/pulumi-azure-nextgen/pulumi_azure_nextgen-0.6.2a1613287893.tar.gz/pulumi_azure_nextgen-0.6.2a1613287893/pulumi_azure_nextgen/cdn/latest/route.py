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
from ._inputs import *

__all__ = ['Route']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:cdn:Route'.""", DeprecationWarning)


class Route(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:cdn:Route'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 compression_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CompressionSettingsArgs']]]]] = None,
                 custom_domains: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceReferenceArgs']]]]] = None,
                 enabled_state: Optional[pulumi.Input[Union[str, 'EnabledState']]] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 forwarding_protocol: Optional[pulumi.Input[Union[str, 'ForwardingProtocol']]] = None,
                 https_redirect: Optional[pulumi.Input[Union[str, 'HttpsRedirect']]] = None,
                 link_to_default_domain: Optional[pulumi.Input[Union[str, 'LinkToDefaultDomain']]] = None,
                 origin_group: Optional[pulumi.Input[pulumi.InputType['ResourceReferenceArgs']]] = None,
                 origin_path: Optional[pulumi.Input[str]] = None,
                 patterns_to_match: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 query_string_caching_behavior: Optional[pulumi.Input['AfdQueryStringCachingBehavior']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 route_name: Optional[pulumi.Input[str]] = None,
                 rule_sets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceReferenceArgs']]]]] = None,
                 supported_protocols: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'AFDEndpointProtocols']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Friendly Routes name mapping to the any Routes or secret related information.
        Latest API Version: 2020-09-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CompressionSettingsArgs']]]] compression_settings: compression settings.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceReferenceArgs']]]] custom_domains: Domains referenced by this endpoint.
        :param pulumi.Input[Union[str, 'EnabledState']] enabled_state: Whether to enable use of this rule. Permitted values are 'Enabled' or 'Disabled'
        :param pulumi.Input[str] endpoint_name: Name of the endpoint under the profile which is unique globally.
        :param pulumi.Input[Union[str, 'ForwardingProtocol']] forwarding_protocol: Protocol this rule will use when forwarding traffic to backends.
        :param pulumi.Input[Union[str, 'HttpsRedirect']] https_redirect: Whether to automatically redirect HTTP traffic to HTTPS traffic. Note that this is a easy way to set up this rule and it will be the first rule that gets executed.
        :param pulumi.Input[Union[str, 'LinkToDefaultDomain']] link_to_default_domain: whether this route will be linked to the default endpoint domain.
        :param pulumi.Input[pulumi.InputType['ResourceReferenceArgs']] origin_group: A reference to the origin group.
        :param pulumi.Input[str] origin_path: A directory path on the origin that AzureFrontDoor can use to retrieve content from, e.g. contoso.cloudapp.net/originpath.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] patterns_to_match: The route patterns of the rule.
        :param pulumi.Input[str] profile_name: Name of the CDN profile which is unique within the resource group.
        :param pulumi.Input['AfdQueryStringCachingBehavior'] query_string_caching_behavior: Defines how CDN caches requests that include query strings. You can ignore any query strings when caching, bypass caching to prevent requests that contain query strings from being cached, or cache every request with a unique URL.
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] route_name: Name of the routing rule.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceReferenceArgs']]]] rule_sets: rule sets referenced by this endpoint.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'AFDEndpointProtocols']]]] supported_protocols: List of supported protocols for this route.
        """
        pulumi.log.warn("Route is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:cdn:Route'.")
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

            __props__['compression_settings'] = compression_settings
            __props__['custom_domains'] = custom_domains
            __props__['enabled_state'] = enabled_state
            if endpoint_name is None and not opts.urn:
                raise TypeError("Missing required property 'endpoint_name'")
            __props__['endpoint_name'] = endpoint_name
            __props__['forwarding_protocol'] = forwarding_protocol
            __props__['https_redirect'] = https_redirect
            __props__['link_to_default_domain'] = link_to_default_domain
            if origin_group is None and not opts.urn:
                raise TypeError("Missing required property 'origin_group'")
            __props__['origin_group'] = origin_group
            __props__['origin_path'] = origin_path
            __props__['patterns_to_match'] = patterns_to_match
            if profile_name is None and not opts.urn:
                raise TypeError("Missing required property 'profile_name'")
            __props__['profile_name'] = profile_name
            __props__['query_string_caching_behavior'] = query_string_caching_behavior
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if route_name is None and not opts.urn:
                raise TypeError("Missing required property 'route_name'")
            __props__['route_name'] = route_name
            __props__['rule_sets'] = rule_sets
            __props__['supported_protocols'] = supported_protocols
            __props__['deployment_status'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:cdn:Route"), pulumi.Alias(type_="azure-nextgen:cdn/v20200901:Route")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Route, __self__).__init__(
            'azure-nextgen:cdn/latest:Route',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Route':
        """
        Get an existing Route resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Route(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="compressionSettings")
    def compression_settings(self) -> pulumi.Output[Optional[Sequence['outputs.CompressionSettingsResponse']]]:
        """
        compression settings.
        """
        return pulumi.get(self, "compression_settings")

    @property
    @pulumi.getter(name="customDomains")
    def custom_domains(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceReferenceResponse']]]:
        """
        Domains referenced by this endpoint.
        """
        return pulumi.get(self, "custom_domains")

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> pulumi.Output[str]:
        return pulumi.get(self, "deployment_status")

    @property
    @pulumi.getter(name="enabledState")
    def enabled_state(self) -> pulumi.Output[Optional[str]]:
        """
        Whether to enable use of this rule. Permitted values are 'Enabled' or 'Disabled'
        """
        return pulumi.get(self, "enabled_state")

    @property
    @pulumi.getter(name="forwardingProtocol")
    def forwarding_protocol(self) -> pulumi.Output[Optional[str]]:
        """
        Protocol this rule will use when forwarding traffic to backends.
        """
        return pulumi.get(self, "forwarding_protocol")

    @property
    @pulumi.getter(name="httpsRedirect")
    def https_redirect(self) -> pulumi.Output[Optional[str]]:
        """
        Whether to automatically redirect HTTP traffic to HTTPS traffic. Note that this is a easy way to set up this rule and it will be the first rule that gets executed.
        """
        return pulumi.get(self, "https_redirect")

    @property
    @pulumi.getter(name="linkToDefaultDomain")
    def link_to_default_domain(self) -> pulumi.Output[Optional[str]]:
        """
        whether this route will be linked to the default endpoint domain.
        """
        return pulumi.get(self, "link_to_default_domain")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="originGroup")
    def origin_group(self) -> pulumi.Output['outputs.ResourceReferenceResponse']:
        """
        A reference to the origin group.
        """
        return pulumi.get(self, "origin_group")

    @property
    @pulumi.getter(name="originPath")
    def origin_path(self) -> pulumi.Output[Optional[str]]:
        """
        A directory path on the origin that AzureFrontDoor can use to retrieve content from, e.g. contoso.cloudapp.net/originpath.
        """
        return pulumi.get(self, "origin_path")

    @property
    @pulumi.getter(name="patternsToMatch")
    def patterns_to_match(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The route patterns of the rule.
        """
        return pulumi.get(self, "patterns_to_match")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning status
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="queryStringCachingBehavior")
    def query_string_caching_behavior(self) -> pulumi.Output[Optional[str]]:
        """
        Defines how CDN caches requests that include query strings. You can ignore any query strings when caching, bypass caching to prevent requests that contain query strings from being cached, or cache every request with a unique URL.
        """
        return pulumi.get(self, "query_string_caching_behavior")

    @property
    @pulumi.getter(name="ruleSets")
    def rule_sets(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceReferenceResponse']]]:
        """
        rule sets referenced by this endpoint.
        """
        return pulumi.get(self, "rule_sets")

    @property
    @pulumi.getter(name="supportedProtocols")
    def supported_protocols(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of supported protocols for this route.
        """
        return pulumi.get(self, "supported_protocols")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

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

