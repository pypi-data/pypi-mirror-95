# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from ._enums import *

__all__ = [
    'GatewayDetailsArgs',
    'IPv4FirewallRuleArgs',
    'IPv4FirewallSettingsArgs',
    'ResourceSkuArgs',
    'ServerAdministratorsArgs',
]

@pulumi.input_type
class GatewayDetailsArgs:
    def __init__(__self__, *,
                 gateway_resource_id: Optional[pulumi.Input[str]] = None):
        """
        The gateway details.
        :param pulumi.Input[str] gateway_resource_id: Gateway resource to be associated with the server.
        """
        if gateway_resource_id is not None:
            pulumi.set(__self__, "gateway_resource_id", gateway_resource_id)

    @property
    @pulumi.getter(name="gatewayResourceId")
    def gateway_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gateway resource to be associated with the server.
        """
        return pulumi.get(self, "gateway_resource_id")

    @gateway_resource_id.setter
    def gateway_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_resource_id", value)


@pulumi.input_type
class IPv4FirewallRuleArgs:
    def __init__(__self__, *,
                 firewall_rule_name: Optional[pulumi.Input[str]] = None,
                 range_end: Optional[pulumi.Input[str]] = None,
                 range_start: Optional[pulumi.Input[str]] = None):
        """
        The detail of firewall rule.
        :param pulumi.Input[str] firewall_rule_name: The rule name.
        :param pulumi.Input[str] range_end: The end range of IPv4.
        :param pulumi.Input[str] range_start: The start range of IPv4.
        """
        if firewall_rule_name is not None:
            pulumi.set(__self__, "firewall_rule_name", firewall_rule_name)
        if range_end is not None:
            pulumi.set(__self__, "range_end", range_end)
        if range_start is not None:
            pulumi.set(__self__, "range_start", range_start)

    @property
    @pulumi.getter(name="firewallRuleName")
    def firewall_rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        The rule name.
        """
        return pulumi.get(self, "firewall_rule_name")

    @firewall_rule_name.setter
    def firewall_rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "firewall_rule_name", value)

    @property
    @pulumi.getter(name="rangeEnd")
    def range_end(self) -> Optional[pulumi.Input[str]]:
        """
        The end range of IPv4.
        """
        return pulumi.get(self, "range_end")

    @range_end.setter
    def range_end(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "range_end", value)

    @property
    @pulumi.getter(name="rangeStart")
    def range_start(self) -> Optional[pulumi.Input[str]]:
        """
        The start range of IPv4.
        """
        return pulumi.get(self, "range_start")

    @range_start.setter
    def range_start(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "range_start", value)


@pulumi.input_type
class IPv4FirewallSettingsArgs:
    def __init__(__self__, *,
                 enable_power_bi_service: Optional[pulumi.Input[bool]] = None,
                 firewall_rules: Optional[pulumi.Input[Sequence[pulumi.Input['IPv4FirewallRuleArgs']]]] = None):
        """
        An array of firewall rules.
        :param pulumi.Input[bool] enable_power_bi_service: The indicator of enabling PBI service.
        :param pulumi.Input[Sequence[pulumi.Input['IPv4FirewallRuleArgs']]] firewall_rules: An array of firewall rules.
        """
        if enable_power_bi_service is not None:
            pulumi.set(__self__, "enable_power_bi_service", enable_power_bi_service)
        if firewall_rules is not None:
            pulumi.set(__self__, "firewall_rules", firewall_rules)

    @property
    @pulumi.getter(name="enablePowerBIService")
    def enable_power_bi_service(self) -> Optional[pulumi.Input[bool]]:
        """
        The indicator of enabling PBI service.
        """
        return pulumi.get(self, "enable_power_bi_service")

    @enable_power_bi_service.setter
    def enable_power_bi_service(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_power_bi_service", value)

    @property
    @pulumi.getter(name="firewallRules")
    def firewall_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IPv4FirewallRuleArgs']]]]:
        """
        An array of firewall rules.
        """
        return pulumi.get(self, "firewall_rules")

    @firewall_rules.setter
    def firewall_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IPv4FirewallRuleArgs']]]]):
        pulumi.set(self, "firewall_rules", value)


@pulumi.input_type
class ResourceSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 capacity: Optional[pulumi.Input[int]] = None,
                 tier: Optional[pulumi.Input[Union[str, 'SkuTier']]] = None):
        """
        Represents the SKU name and Azure pricing tier for Analysis Services resource.
        :param pulumi.Input[str] name: Name of the SKU level.
        :param pulumi.Input[int] capacity: The number of instances in the read only query pool.
        :param pulumi.Input[Union[str, 'SkuTier']] tier: The name of the Azure pricing tier to which the SKU applies.
        """
        pulumi.set(__self__, "name", name)
        if capacity is None:
            capacity = 1
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the SKU level.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The number of instances in the read only query pool.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[Union[str, 'SkuTier']]]:
        """
        The name of the Azure pricing tier to which the SKU applies.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[Union[str, 'SkuTier']]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class ServerAdministratorsArgs:
    def __init__(__self__, *,
                 members: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        An array of administrator user identities.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] members: An array of administrator user identities.
        """
        if members is not None:
            pulumi.set(__self__, "members", members)

    @property
    @pulumi.getter
    def members(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of administrator user identities.
        """
        return pulumi.get(self, "members")

    @members.setter
    def members(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "members", value)


