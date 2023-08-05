# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['Favorite']


class Favorite(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 config: Optional[pulumi.Input[str]] = None,
                 favorite_id: Optional[pulumi.Input[str]] = None,
                 favorite_type: Optional[pulumi.Input['FavoriteType']] = None,
                 is_generated_from_template: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 source_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Properties that define a favorite that is associated to an Application Insights component.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category: Favorite category, as defined by the user at creation time.
        :param pulumi.Input[str] config: Configuration of this particular favorite, which are driven by the Azure portal UX. Configuration data is a string containing valid JSON
        :param pulumi.Input[str] favorite_id: The Id of a specific favorite defined in the Application Insights component
        :param pulumi.Input['FavoriteType'] favorite_type: Enum indicating if this favorite definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        :param pulumi.Input[bool] is_generated_from_template: Flag denoting wether or not this favorite was generated from a template.
        :param pulumi.Input[str] name: The user-defined name of the favorite.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the Application Insights component resource.
        :param pulumi.Input[str] source_type: The source of the favorite definition.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of 0 or more tags that are associated with this favorite definition
        :param pulumi.Input[str] version: This instance's version of the data model. This can change as new features are added that can be marked favorite. Current examples include MetricsExplorer (ME) and Search.
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

            __props__['category'] = category
            __props__['config'] = config
            if favorite_id is None and not opts.urn:
                raise TypeError("Missing required property 'favorite_id'")
            __props__['favorite_id'] = favorite_id
            __props__['favorite_type'] = favorite_type
            __props__['is_generated_from_template'] = is_generated_from_template
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__['resource_name'] = resource_name_
            __props__['source_type'] = source_type
            __props__['tags'] = tags
            __props__['version'] = version
            __props__['time_modified'] = None
            __props__['user_id'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:insights:Favorite"), pulumi.Alias(type_="azure-nextgen:insights/latest:Favorite")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Favorite, __self__).__init__(
            'azure-nextgen:insights/v20150501:Favorite',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Favorite':
        """
        Get an existing Favorite resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Favorite(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Output[Optional[str]]:
        """
        Favorite category, as defined by the user at creation time.
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output[Optional[str]]:
        """
        Configuration of this particular favorite, which are driven by the Azure portal UX. Configuration data is a string containing valid JSON
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="favoriteId")
    def favorite_id(self) -> pulumi.Output[str]:
        """
        Internally assigned unique id of the favorite definition.
        """
        return pulumi.get(self, "favorite_id")

    @property
    @pulumi.getter(name="favoriteType")
    def favorite_type(self) -> pulumi.Output[Optional[str]]:
        """
        Enum indicating if this favorite definition is owned by a specific user or is shared between all users with access to the Application Insights component.
        """
        return pulumi.get(self, "favorite_type")

    @property
    @pulumi.getter(name="isGeneratedFromTemplate")
    def is_generated_from_template(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag denoting wether or not this favorite was generated from a template.
        """
        return pulumi.get(self, "is_generated_from_template")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The user-defined name of the favorite.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sourceType")
    def source_type(self) -> pulumi.Output[Optional[str]]:
        """
        The source of the favorite definition.
        """
        return pulumi.get(self, "source_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of 0 or more tags that are associated with this favorite definition
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeModified")
    def time_modified(self) -> pulumi.Output[str]:
        """
        Date and time in UTC of the last modification that was made to this favorite definition.
        """
        return pulumi.get(self, "time_modified")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        Unique user id of the specific user that owns this favorite.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        This instance's version of the data model. This can change as new features are added that can be marked favorite. Current examples include MetricsExplorer (ME) and Search.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

