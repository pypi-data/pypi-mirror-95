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

__all__ = ['SmartDetectorAlertRule']


class SmartDetectorAlertRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action_groups: Optional[pulumi.Input[pulumi.InputType['ActionGroupsInformationArgs']]] = None,
                 alert_rule_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 detector: Optional[pulumi.Input[pulumi.InputType['DetectorArgs']]] = None,
                 frequency: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 severity: Optional[pulumi.Input[Union[str, 'Severity']]] = None,
                 state: Optional[pulumi.Input[Union[str, 'AlertRuleState']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 throttling: Optional[pulumi.Input[pulumi.InputType['ThrottlingInformationArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The alert rule information
        API Version: 2019-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ActionGroupsInformationArgs']] action_groups: The alert rule actions.
        :param pulumi.Input[str] alert_rule_name: The name of the alert rule.
        :param pulumi.Input[str] description: The alert rule description.
        :param pulumi.Input[pulumi.InputType['DetectorArgs']] detector: The alert rule's detector.
        :param pulumi.Input[str] frequency: The alert rule frequency in ISO8601 format. The time granularity must be in minutes and minimum value is 5 minutes.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] scope: The alert rule resources scope.
        :param pulumi.Input[Union[str, 'Severity']] severity: The alert rule severity.
        :param pulumi.Input[Union[str, 'AlertRuleState']] state: The alert rule state.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[pulumi.InputType['ThrottlingInformationArgs']] throttling: The alert rule throttling information.
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

            if action_groups is None and not opts.urn:
                raise TypeError("Missing required property 'action_groups'")
            __props__['action_groups'] = action_groups
            if alert_rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'alert_rule_name'")
            __props__['alert_rule_name'] = alert_rule_name
            __props__['description'] = description
            if detector is None and not opts.urn:
                raise TypeError("Missing required property 'detector'")
            __props__['detector'] = detector
            if frequency is None and not opts.urn:
                raise TypeError("Missing required property 'frequency'")
            __props__['frequency'] = frequency
            if location is None:
                location = 'global'
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            if severity is None and not opts.urn:
                raise TypeError("Missing required property 'severity'")
            __props__['severity'] = severity
            if state is None and not opts.urn:
                raise TypeError("Missing required property 'state'")
            __props__['state'] = state
            __props__['tags'] = tags
            __props__['throttling'] = throttling
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:alertsmanagement/latest:SmartDetectorAlertRule"), pulumi.Alias(type_="azure-nextgen:alertsmanagement/v20190301:SmartDetectorAlertRule"), pulumi.Alias(type_="azure-nextgen:alertsmanagement/v20190601:SmartDetectorAlertRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SmartDetectorAlertRule, __self__).__init__(
            'azure-nextgen:alertsmanagement:SmartDetectorAlertRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SmartDetectorAlertRule':
        """
        Get an existing SmartDetectorAlertRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SmartDetectorAlertRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="actionGroups")
    def action_groups(self) -> pulumi.Output['outputs.ActionGroupsInformationResponse']:
        """
        The alert rule actions.
        """
        return pulumi.get(self, "action_groups")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The alert rule description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def detector(self) -> pulumi.Output['outputs.DetectorResponse']:
        """
        The alert rule's detector.
        """
        return pulumi.get(self, "detector")

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Output[str]:
        """
        The alert rule frequency in ISO8601 format. The time granularity must be in minutes and minimum value is 5 minutes.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Output[Sequence[str]]:
        """
        The alert rule resources scope.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def severity(self) -> pulumi.Output[str]:
        """
        The alert rule severity.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The alert rule state.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def throttling(self) -> pulumi.Output[Optional['outputs.ThrottlingInformationResponse']]:
        """
        The alert rule throttling information.
        """
        return pulumi.get(self, "throttling")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

