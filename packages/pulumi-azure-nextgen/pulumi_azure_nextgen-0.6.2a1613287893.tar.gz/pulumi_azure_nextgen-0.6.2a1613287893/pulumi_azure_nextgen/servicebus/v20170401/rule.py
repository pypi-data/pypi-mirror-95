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

__all__ = ['Rule']


class Rule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[pulumi.InputType['ActionArgs']]] = None,
                 correlation_filter: Optional[pulumi.Input[pulumi.InputType['CorrelationFilterArgs']]] = None,
                 filter_type: Optional[pulumi.Input['FilterType']] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 sql_filter: Optional[pulumi.Input[pulumi.InputType['SqlFilterArgs']]] = None,
                 subscription_name: Optional[pulumi.Input[str]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Description of Rule Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ActionArgs']] action: Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        :param pulumi.Input[pulumi.InputType['CorrelationFilterArgs']] correlation_filter: Properties of correlationFilter
        :param pulumi.Input['FilterType'] filter_type: Filter type that is evaluated against a BrokeredMessage.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] rule_name: The rule name.
        :param pulumi.Input[pulumi.InputType['SqlFilterArgs']] sql_filter: Properties of sqlFilter
        :param pulumi.Input[str] subscription_name: The subscription name.
        :param pulumi.Input[str] topic_name: The topic name.
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

            __props__['action'] = action
            __props__['correlation_filter'] = correlation_filter
            __props__['filter_type'] = filter_type
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__['namespace_name'] = namespace_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'rule_name'")
            __props__['rule_name'] = rule_name
            __props__['sql_filter'] = sql_filter
            if subscription_name is None and not opts.urn:
                raise TypeError("Missing required property 'subscription_name'")
            __props__['subscription_name'] = subscription_name
            if topic_name is None and not opts.urn:
                raise TypeError("Missing required property 'topic_name'")
            __props__['topic_name'] = topic_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:servicebus:Rule"), pulumi.Alias(type_="azure-nextgen:servicebus/latest:Rule"), pulumi.Alias(type_="azure-nextgen:servicebus/v20180101preview:Rule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Rule, __self__).__init__(
            'azure-nextgen:servicebus/v20170401:Rule',
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
    def action(self) -> pulumi.Output[Optional['outputs.ActionResponse']]:
        """
        Represents the filter actions which are allowed for the transformation of a message that have been matched by a filter expression.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="correlationFilter")
    def correlation_filter(self) -> pulumi.Output[Optional['outputs.CorrelationFilterResponse']]:
        """
        Properties of correlationFilter
        """
        return pulumi.get(self, "correlation_filter")

    @property
    @pulumi.getter(name="filterType")
    def filter_type(self) -> pulumi.Output[Optional[str]]:
        """
        Filter type that is evaluated against a BrokeredMessage.
        """
        return pulumi.get(self, "filter_type")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sqlFilter")
    def sql_filter(self) -> pulumi.Output[Optional['outputs.SqlFilterResponse']]:
        """
        Properties of sqlFilter
        """
        return pulumi.get(self, "sql_filter")

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

