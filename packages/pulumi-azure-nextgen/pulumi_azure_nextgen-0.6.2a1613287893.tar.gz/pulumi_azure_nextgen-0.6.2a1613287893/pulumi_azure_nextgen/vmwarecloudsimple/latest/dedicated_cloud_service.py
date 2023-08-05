# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['DedicatedCloudService']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:vmwarecloudsimple:DedicatedCloudService'.""", DeprecationWarning)


class DedicatedCloudService(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:vmwarecloudsimple:DedicatedCloudService'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dedicated_cloud_service_name: Optional[pulumi.Input[str]] = None,
                 gateway_subnet: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Dedicated cloud service model
        Latest API Version: 2019-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dedicated_cloud_service_name: dedicated cloud Service name
        :param pulumi.Input[str] gateway_subnet: gateway Subnet for the account. It will collect the subnet address and always treat it as /28
        :param pulumi.Input[str] location: Azure region
        :param pulumi.Input[str] resource_group_name: The name of the resource group
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The list of tags
        """
        pulumi.log.warn("DedicatedCloudService is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:vmwarecloudsimple:DedicatedCloudService'.")
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

            if dedicated_cloud_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'dedicated_cloud_service_name'")
            __props__['dedicated_cloud_service_name'] = dedicated_cloud_service_name
            if gateway_subnet is None and not opts.urn:
                raise TypeError("Missing required property 'gateway_subnet'")
            __props__['gateway_subnet'] = gateway_subnet
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['is_account_onboarded'] = None
            __props__['name'] = None
            __props__['nodes'] = None
            __props__['service_url'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:vmwarecloudsimple:DedicatedCloudService"), pulumi.Alias(type_="azure-nextgen:vmwarecloudsimple/v20190401:DedicatedCloudService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DedicatedCloudService, __self__).__init__(
            'azure-nextgen:vmwarecloudsimple/latest:DedicatedCloudService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DedicatedCloudService':
        """
        Get an existing DedicatedCloudService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DedicatedCloudService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="gatewaySubnet")
    def gateway_subnet(self) -> pulumi.Output[str]:
        """
        gateway Subnet for the account. It will collect the subnet address and always treat it as /28
        """
        return pulumi.get(self, "gateway_subnet")

    @property
    @pulumi.getter(name="isAccountOnboarded")
    def is_account_onboarded(self) -> pulumi.Output[str]:
        """
        indicates whether account onboarded or not in a given region
        """
        return pulumi.get(self, "is_account_onboarded")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Azure region
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        {dedicatedCloudServiceName}
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def nodes(self) -> pulumi.Output[int]:
        """
        total nodes purchased
        """
        return pulumi.get(self, "nodes")

    @property
    @pulumi.getter(name="serviceURL")
    def service_url(self) -> pulumi.Output[str]:
        """
        link to a service management web portal
        """
        return pulumi.get(self, "service_url")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The list of tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        {resourceProviderNamespace}/{resourceType}
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

