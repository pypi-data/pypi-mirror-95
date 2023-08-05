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

__all__ = ['StreamingEndpoint']


class StreamingEndpoint(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_control: Optional[pulumi.Input[pulumi.InputType['StreamingEndpointAccessControlArgs']]] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 auto_start: Optional[pulumi.Input[bool]] = None,
                 availability_set_name: Optional[pulumi.Input[str]] = None,
                 cdn_enabled: Optional[pulumi.Input[bool]] = None,
                 cdn_profile: Optional[pulumi.Input[str]] = None,
                 cdn_provider: Optional[pulumi.Input[str]] = None,
                 cross_site_access_policies: Optional[pulumi.Input[pulumi.InputType['CrossSiteAccessPoliciesArgs']]] = None,
                 custom_host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_cache_age: Optional[pulumi.Input[float]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scale_units: Optional[pulumi.Input[int]] = None,
                 streaming_endpoint_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The streaming endpoint.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['StreamingEndpointAccessControlArgs']] access_control: The access control definition of the streaming endpoint.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[bool] auto_start: The flag indicates if the resource should be automatically started on creation.
        :param pulumi.Input[str] availability_set_name: This feature is deprecated, do not set a value for this property.
        :param pulumi.Input[bool] cdn_enabled: The CDN enabled flag.
        :param pulumi.Input[str] cdn_profile: The CDN profile name.
        :param pulumi.Input[str] cdn_provider: The CDN provider name.
        :param pulumi.Input[pulumi.InputType['CrossSiteAccessPoliciesArgs']] cross_site_access_policies: The streaming endpoint access policies.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] custom_host_names: The custom host names of the streaming endpoint
        :param pulumi.Input[str] description: The streaming endpoint description.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[float] max_cache_age: Max cache age
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[int] scale_units: The number of scale units. Use the Scale operation to adjust this value.
        :param pulumi.Input[str] streaming_endpoint_name: The name of the streaming endpoint, maximum length is 24.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
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

            __props__['access_control'] = access_control
            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            __props__['auto_start'] = auto_start
            __props__['availability_set_name'] = availability_set_name
            __props__['cdn_enabled'] = cdn_enabled
            __props__['cdn_profile'] = cdn_profile
            __props__['cdn_provider'] = cdn_provider
            __props__['cross_site_access_policies'] = cross_site_access_policies
            __props__['custom_host_names'] = custom_host_names
            __props__['description'] = description
            __props__['location'] = location
            __props__['max_cache_age'] = max_cache_age
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if scale_units is None and not opts.urn:
                raise TypeError("Missing required property 'scale_units'")
            __props__['scale_units'] = scale_units
            if streaming_endpoint_name is None and not opts.urn:
                raise TypeError("Missing required property 'streaming_endpoint_name'")
            __props__['streaming_endpoint_name'] = streaming_endpoint_name
            __props__['tags'] = tags
            __props__['created'] = None
            __props__['free_trial_end_time'] = None
            __props__['host_name'] = None
            __props__['last_modified'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['resource_state'] = None
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:media:StreamingEndpoint"), pulumi.Alias(type_="azure-nextgen:media/latest:StreamingEndpoint"), pulumi.Alias(type_="azure-nextgen:media/v20180330preview:StreamingEndpoint"), pulumi.Alias(type_="azure-nextgen:media/v20180601preview:StreamingEndpoint"), pulumi.Alias(type_="azure-nextgen:media/v20180701:StreamingEndpoint"), pulumi.Alias(type_="azure-nextgen:media/v20190501preview:StreamingEndpoint")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StreamingEndpoint, __self__).__init__(
            'azure-nextgen:media/v20200501:StreamingEndpoint',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StreamingEndpoint':
        """
        Get an existing StreamingEndpoint resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StreamingEndpoint(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessControl")
    def access_control(self) -> pulumi.Output[Optional['outputs.StreamingEndpointAccessControlResponse']]:
        """
        The access control definition of the streaming endpoint.
        """
        return pulumi.get(self, "access_control")

    @property
    @pulumi.getter(name="availabilitySetName")
    def availability_set_name(self) -> pulumi.Output[Optional[str]]:
        """
        This feature is deprecated, do not set a value for this property.
        """
        return pulumi.get(self, "availability_set_name")

    @property
    @pulumi.getter(name="cdnEnabled")
    def cdn_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        The CDN enabled flag.
        """
        return pulumi.get(self, "cdn_enabled")

    @property
    @pulumi.getter(name="cdnProfile")
    def cdn_profile(self) -> pulumi.Output[Optional[str]]:
        """
        The CDN profile name.
        """
        return pulumi.get(self, "cdn_profile")

    @property
    @pulumi.getter(name="cdnProvider")
    def cdn_provider(self) -> pulumi.Output[Optional[str]]:
        """
        The CDN provider name.
        """
        return pulumi.get(self, "cdn_provider")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        The exact time the streaming endpoint was created.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="crossSiteAccessPolicies")
    def cross_site_access_policies(self) -> pulumi.Output[Optional['outputs.CrossSiteAccessPoliciesResponse']]:
        """
        The streaming endpoint access policies.
        """
        return pulumi.get(self, "cross_site_access_policies")

    @property
    @pulumi.getter(name="customHostNames")
    def custom_host_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The custom host names of the streaming endpoint
        """
        return pulumi.get(self, "custom_host_names")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The streaming endpoint description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="freeTrialEndTime")
    def free_trial_end_time(self) -> pulumi.Output[str]:
        """
        The free trial expiration time.
        """
        return pulumi.get(self, "free_trial_end_time")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        The streaming endpoint host name.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> pulumi.Output[str]:
        """
        The exact time the streaming endpoint was last modified.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxCacheAge")
    def max_cache_age(self) -> pulumi.Output[Optional[float]]:
        """
        Max cache age
        """
        return pulumi.get(self, "max_cache_age")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the streaming endpoint.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        The resource state of the streaming endpoint.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter(name="scaleUnits")
    def scale_units(self) -> pulumi.Output[int]:
        """
        The number of scale units. Use the Scale operation to adjust this value.
        """
        return pulumi.get(self, "scale_units")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

