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

__all__ = ['Rule']


class Rule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['DeliveryRuleCacheExpirationActionArgs'], pulumi.InputType['DeliveryRuleCacheKeyQueryStringActionArgs'], pulumi.InputType['DeliveryRuleRequestHeaderActionArgs'], pulumi.InputType['DeliveryRuleResponseHeaderActionArgs'], pulumi.InputType['OriginGroupOverrideActionArgs'], pulumi.InputType['UrlRedirectActionArgs'], pulumi.InputType['UrlRewriteActionArgs'], pulumi.InputType['UrlSigningActionArgs']]]]]] = None,
                 conditions: Optional[pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['DeliveryRuleCookiesConditionArgs'], pulumi.InputType['DeliveryRuleHttpVersionConditionArgs'], pulumi.InputType['DeliveryRuleIsDeviceConditionArgs'], pulumi.InputType['DeliveryRulePostArgsConditionArgs'], pulumi.InputType['DeliveryRuleQueryStringConditionArgs'], pulumi.InputType['DeliveryRuleRemoteAddressConditionArgs'], pulumi.InputType['DeliveryRuleRequestBodyConditionArgs'], pulumi.InputType['DeliveryRuleRequestHeaderConditionArgs'], pulumi.InputType['DeliveryRuleRequestMethodConditionArgs'], pulumi.InputType['DeliveryRuleRequestSchemeConditionArgs'], pulumi.InputType['DeliveryRuleRequestUriConditionArgs'], pulumi.InputType['DeliveryRuleUrlFileExtensionConditionArgs'], pulumi.InputType['DeliveryRuleUrlFileNameConditionArgs'], pulumi.InputType['DeliveryRuleUrlPathConditionArgs']]]]]] = None,
                 match_processing_behavior: Optional[pulumi.Input[Union[str, 'MatchProcessingBehavior']]] = None,
                 order: Optional[pulumi.Input[int]] = None,
                 profile_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 rule_set_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Friendly Rules name mapping to the any Rules or secret related information.
        API Version: 2020-09-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['DeliveryRuleCacheExpirationActionArgs'], pulumi.InputType['DeliveryRuleCacheKeyQueryStringActionArgs'], pulumi.InputType['DeliveryRuleRequestHeaderActionArgs'], pulumi.InputType['DeliveryRuleResponseHeaderActionArgs'], pulumi.InputType['OriginGroupOverrideActionArgs'], pulumi.InputType['UrlRedirectActionArgs'], pulumi.InputType['UrlRewriteActionArgs'], pulumi.InputType['UrlSigningActionArgs']]]]] actions: A list of actions that are executed when all the conditions of a rule are satisfied.
        :param pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['DeliveryRuleCookiesConditionArgs'], pulumi.InputType['DeliveryRuleHttpVersionConditionArgs'], pulumi.InputType['DeliveryRuleIsDeviceConditionArgs'], pulumi.InputType['DeliveryRulePostArgsConditionArgs'], pulumi.InputType['DeliveryRuleQueryStringConditionArgs'], pulumi.InputType['DeliveryRuleRemoteAddressConditionArgs'], pulumi.InputType['DeliveryRuleRequestBodyConditionArgs'], pulumi.InputType['DeliveryRuleRequestHeaderConditionArgs'], pulumi.InputType['DeliveryRuleRequestMethodConditionArgs'], pulumi.InputType['DeliveryRuleRequestSchemeConditionArgs'], pulumi.InputType['DeliveryRuleRequestUriConditionArgs'], pulumi.InputType['DeliveryRuleUrlFileExtensionConditionArgs'], pulumi.InputType['DeliveryRuleUrlFileNameConditionArgs'], pulumi.InputType['DeliveryRuleUrlPathConditionArgs']]]]] conditions: A list of conditions that must be matched for the actions to be executed
        :param pulumi.Input[Union[str, 'MatchProcessingBehavior']] match_processing_behavior: If this rule is a match should the rules engine continue running the remaining rules or stop. If not present, defaults to Continue.
        :param pulumi.Input[int] order: The order in which the rules are applied for the endpoint. Possible values {0,1,2,3,………}. A rule with a lesser order will be applied before a rule with a greater order. Rule with order 0 is a special rule. It does not require any condition and actions listed in it will always be applied.
        :param pulumi.Input[str] profile_name: Name of the CDN profile which is unique within the resource group.
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] rule_name: Name of the delivery rule which is unique within the endpoint.
        :param pulumi.Input[str] rule_set_name: Name of the rule set under the profile.
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

            if actions is None and not opts.urn:
                raise TypeError("Missing required property 'actions'")
            __props__['actions'] = actions
            __props__['conditions'] = conditions
            __props__['match_processing_behavior'] = match_processing_behavior
            if order is None and not opts.urn:
                raise TypeError("Missing required property 'order'")
            __props__['order'] = order
            if profile_name is None and not opts.urn:
                raise TypeError("Missing required property 'profile_name'")
            __props__['profile_name'] = profile_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_name'")
            __props__['rule_name'] = rule_name
            if rule_set_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_set_name'")
            __props__['rule_set_name'] = rule_set_name
            __props__['deployment_status'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:cdn/latest:Rule"), pulumi.Alias(type_="azure-nextgen:cdn/v20200901:Rule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Rule, __self__).__init__(
            'azure-nextgen:cdn:Rule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Rule':
        """
        Get an existing Rule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Rule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Sequence[Any]]:
        """
        A list of actions that are executed when all the conditions of a rule are satisfied.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def conditions(self) -> pulumi.Output[Optional[Sequence[Any]]]:
        """
        A list of conditions that must be matched for the actions to be executed
        """
        return pulumi.get(self, "conditions")

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> pulumi.Output[str]:
        return pulumi.get(self, "deployment_status")

    @property
    @pulumi.getter(name="matchProcessingBehavior")
    def match_processing_behavior(self) -> pulumi.Output[Optional[str]]:
        """
        If this rule is a match should the rules engine continue running the remaining rules or stop. If not present, defaults to Continue.
        """
        return pulumi.get(self, "match_processing_behavior")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def order(self) -> pulumi.Output[int]:
        """
        The order in which the rules are applied for the endpoint. Possible values {0,1,2,3,………}. A rule with a lesser order will be applied before a rule with a greater order. Rule with order 0 is a special rule. It does not require any condition and actions listed in it will always be applied.
        """
        return pulumi.get(self, "order")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning status
        """
        return pulumi.get(self, "provisioning_state")

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

