# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['NotificationHubAuthorizationRule']


class NotificationHubAuthorizationRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_rule_name: Optional[pulumi.Input[str]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 notification_hub_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['SharedAccessAuthorizationRulePropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Description of a Namespace AuthorizationRules.
        API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_rule_name: Authorization Rule Name.
        :param pulumi.Input[str] namespace_name: The namespace name.
        :param pulumi.Input[str] notification_hub_name: The notification hub name.
        :param pulumi.Input[pulumi.InputType['SharedAccessAuthorizationRulePropertiesArgs']] properties: Properties of the Namespace AuthorizationRules.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
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

            if authorization_rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'authorization_rule_name'")
            __props__['authorization_rule_name'] = authorization_rule_name
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            if notification_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'notification_hub_name'")
            __props__['notification_hub_name'] = notification_hub_name
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__['properties'] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['claim_type'] = None
            __props__['claim_value'] = None
            __props__['created_time'] = None
            __props__['key_name'] = None
            __props__['location'] = None
            __props__['modified_time'] = None
            __props__['name'] = None
            __props__['primary_key'] = None
            __props__['revision'] = None
            __props__['rights'] = None
            __props__['secondary_key'] = None
            __props__['sku'] = None
            __props__['tags'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:notificationhubs/latest:NotificationHubAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:notificationhubs/v20160301:NotificationHubAuthorizationRule"), pulumi.Alias(type_="azure-nextgen:notificationhubs/v20170401:NotificationHubAuthorizationRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NotificationHubAuthorizationRule, __self__).__init__(
            'azure-nextgen:notificationhubs:NotificationHubAuthorizationRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NotificationHubAuthorizationRule':
        """
        Get an existing NotificationHubAuthorizationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return NotificationHubAuthorizationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="claimType")
    def claim_type(self) -> pulumi.Output[str]:
        """
        A string that describes the claim type
        """
        return pulumi.get(self, "claim_type")

    @property
    @pulumi.getter(name="claimValue")
    def claim_value(self) -> pulumi.Output[str]:
        """
        A string that describes the claim value
        """
        return pulumi.get(self, "claim_value")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> pulumi.Output[str]:
        """
        The created time for this rule
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> pulumi.Output[str]:
        """
        A string that describes the authorization rule.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="modifiedTime")
    def modified_time(self) -> pulumi.Output[str]:
        """
        The last modified time for this rule
        """
        return pulumi.get(self, "modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> pulumi.Output[str]:
        """
        A base64-encoded 256-bit primary key for signing and validating the SAS token.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Output[int]:
        """
        The revision number for the rule
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def rights(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, "rights")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> pulumi.Output[str]:
        """
        A base64-encoded 256-bit primary key for signing and validating the SAS token.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the created namespace
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

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

