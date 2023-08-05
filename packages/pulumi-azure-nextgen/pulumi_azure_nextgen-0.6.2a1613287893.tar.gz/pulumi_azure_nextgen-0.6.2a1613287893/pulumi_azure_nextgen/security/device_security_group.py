# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['DeviceSecurityGroup']


class DeviceSecurityGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allowlist_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowlistCustomAlertRuleArgs']]]]] = None,
                 denylist_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DenylistCustomAlertRuleArgs']]]]] = None,
                 device_security_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 threshold_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThresholdCustomAlertRuleArgs']]]]] = None,
                 time_window_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeWindowCustomAlertRuleArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The device security group resource
        API Version: 2019-08-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AllowlistCustomAlertRuleArgs']]]] allowlist_rules: The allow-list custom alert rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DenylistCustomAlertRuleArgs']]]] denylist_rules: The deny-list custom alert rules.
        :param pulumi.Input[str] device_security_group_name: The name of the device security group. Note that the name of the device security group is case insensitive.
        :param pulumi.Input[str] resource_id: The identifier of the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ThresholdCustomAlertRuleArgs']]]] threshold_rules: The list of custom alert threshold rules.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TimeWindowCustomAlertRuleArgs']]]] time_window_rules: The list of custom alert time-window rules.
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

            __props__['allowlist_rules'] = allowlist_rules
            __props__['denylist_rules'] = denylist_rules
            if device_security_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_security_group_name'")
            __props__['device_security_group_name'] = device_security_group_name
            if resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'resource_id'")
            __props__['resource_id'] = resource_id
            __props__['threshold_rules'] = threshold_rules
            __props__['time_window_rules'] = time_window_rules
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:security/latest:DeviceSecurityGroup"), pulumi.Alias(type_="azure-nextgen:security/v20170801preview:DeviceSecurityGroup"), pulumi.Alias(type_="azure-nextgen:security/v20190801:DeviceSecurityGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DeviceSecurityGroup, __self__).__init__(
            'azure-nextgen:security:DeviceSecurityGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DeviceSecurityGroup':
        """
        Get an existing DeviceSecurityGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DeviceSecurityGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowlistRules")
    def allowlist_rules(self) -> pulumi.Output[Optional[Sequence['outputs.AllowlistCustomAlertRuleResponse']]]:
        """
        The allow-list custom alert rules.
        """
        return pulumi.get(self, "allowlist_rules")

    @property
    @pulumi.getter(name="denylistRules")
    def denylist_rules(self) -> pulumi.Output[Optional[Sequence['outputs.DenylistCustomAlertRuleResponse']]]:
        """
        The deny-list custom alert rules.
        """
        return pulumi.get(self, "denylist_rules")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="thresholdRules")
    def threshold_rules(self) -> pulumi.Output[Optional[Sequence['outputs.ThresholdCustomAlertRuleResponse']]]:
        """
        The list of custom alert threshold rules.
        """
        return pulumi.get(self, "threshold_rules")

    @property
    @pulumi.getter(name="timeWindowRules")
    def time_window_rules(self) -> pulumi.Output[Optional[Sequence['outputs.TimeWindowCustomAlertRuleResponse']]]:
        """
        The list of custom alert time-window rules.
        """
        return pulumi.get(self, "time_window_rules")

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

