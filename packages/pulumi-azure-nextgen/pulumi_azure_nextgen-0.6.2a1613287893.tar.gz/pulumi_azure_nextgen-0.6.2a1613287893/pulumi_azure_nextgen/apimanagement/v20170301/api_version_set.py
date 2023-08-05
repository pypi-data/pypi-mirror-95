# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['ApiVersionSet']


class ApiVersionSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 version_header_name: Optional[pulumi.Input[str]] = None,
                 version_query_name: Optional[pulumi.Input[str]] = None,
                 version_set_id: Optional[pulumi.Input[str]] = None,
                 versioning_scheme: Optional[pulumi.Input[Union[str, 'VersioningScheme']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Api Version Set Contract details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of API Version Set.
        :param pulumi.Input[str] display_name: Name of API Version Set
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[str] version_header_name: Name of HTTP header parameter that indicates the API Version if versioningScheme is set to `header`.
        :param pulumi.Input[str] version_query_name: Name of query parameter that indicates the API Version if versioningScheme is set to `query`.
        :param pulumi.Input[str] version_set_id: Api Version Set identifier. Must be unique in the current API Management service instance.
        :param pulumi.Input[Union[str, 'VersioningScheme']] versioning_scheme: An value that determines where the API Version identifer will be located in a HTTP request.
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

            __props__['description'] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__['service_name'] = service_name
            __props__['version_header_name'] = version_header_name
            __props__['version_query_name'] = version_query_name
            if version_set_id is None and not opts.urn:
                raise TypeError("Missing required property 'version_set_id'")
            __props__['version_set_id'] = version_set_id
            if versioning_scheme is None and not opts.urn:
                raise TypeError("Missing required property 'versioning_scheme'")
            __props__['versioning_scheme'] = versioning_scheme
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:apimanagement:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/latest:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180101:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20180601preview:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20190101:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20191201preview:ApiVersionSet"), pulumi.Alias(type_="azure-nextgen:apimanagement/v20200601preview:ApiVersionSet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApiVersionSet, __self__).__init__(
            'azure-nextgen:apimanagement/v20170301:ApiVersionSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApiVersionSet':
        """
        Get an existing ApiVersionSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ApiVersionSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of API Version Set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Name of API Version Set
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
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="versionHeaderName")
    def version_header_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of HTTP header parameter that indicates the API Version if versioningScheme is set to `header`.
        """
        return pulumi.get(self, "version_header_name")

    @property
    @pulumi.getter(name="versionQueryName")
    def version_query_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of query parameter that indicates the API Version if versioningScheme is set to `query`.
        """
        return pulumi.get(self, "version_query_name")

    @property
    @pulumi.getter(name="versioningScheme")
    def versioning_scheme(self) -> pulumi.Output[str]:
        """
        An value that determines where the API Version identifer will be located in a HTTP request.
        """
        return pulumi.get(self, "versioning_scheme")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

