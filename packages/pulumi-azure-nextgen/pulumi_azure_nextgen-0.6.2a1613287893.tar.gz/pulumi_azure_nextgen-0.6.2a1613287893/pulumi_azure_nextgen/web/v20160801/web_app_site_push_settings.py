# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['WebAppSitePushSettings']


class WebAppSitePushSettings(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dynamic_tags_json: Optional[pulumi.Input[str]] = None,
                 is_push_enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tag_whitelist_json: Optional[pulumi.Input[str]] = None,
                 tags_requiring_auth: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Push settings for the App.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dynamic_tags_json: Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push registration endpoint.
        :param pulumi.Input[bool] is_push_enabled: Gets or sets a flag indicating whether the Push endpoint is enabled.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of web app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] tag_whitelist_json: Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
        :param pulumi.Input[str] tags_requiring_auth: Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push registration endpoint.
               Tags can consist of alphanumeric characters and the following:
               '_', '@', '#', '.', ':', '-'. 
               Validation should be performed at the PushRequestHandler.
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

            __props__['dynamic_tags_json'] = dynamic_tags_json
            if is_push_enabled is None and not opts.urn:
                raise TypeError("Missing required property 'is_push_enabled'")
            __props__['is_push_enabled'] = is_push_enabled
            __props__['kind'] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tag_whitelist_json'] = tag_whitelist_json
            __props__['tags_requiring_auth'] = tags_requiring_auth
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/latest:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/v20181101:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppSitePushSettings"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppSitePushSettings")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppSitePushSettings, __self__).__init__(
            'azure-nextgen:web/v20160801:WebAppSitePushSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppSitePushSettings':
        """
        Get an existing WebAppSitePushSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppSitePushSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dynamicTagsJson")
    def dynamic_tags_json(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a JSON string containing a list of dynamic tags that will be evaluated from user claims in the push registration endpoint.
        """
        return pulumi.get(self, "dynamic_tags_json")

    @property
    @pulumi.getter(name="isPushEnabled")
    def is_push_enabled(self) -> pulumi.Output[bool]:
        """
        Gets or sets a flag indicating whether the Push endpoint is enabled.
        """
        return pulumi.get(self, "is_push_enabled")

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
    @pulumi.getter(name="tagWhitelistJson")
    def tag_whitelist_json(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a JSON string containing a list of tags that are whitelisted for use by the push registration endpoint.
        """
        return pulumi.get(self, "tag_whitelist_json")

    @property
    @pulumi.getter(name="tagsRequiringAuth")
    def tags_requiring_auth(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets a JSON string containing a list of tags that require user authentication to be used in the push registration endpoint.
        Tags can consist of alphanumeric characters and the following:
        '_', '@', '#', '.', ':', '-'. 
        Validation should be performed at the PushRequestHandler.
        """
        return pulumi.get(self, "tags_requiring_auth")

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

