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

__all__ = [
    'GatewayDetailsResponse',
    'IPv4FirewallRuleResponse',
    'IPv4FirewallSettingsResponse',
    'ResourceSkuResponse',
    'ServerAdministratorsResponse',
]

@pulumi.output_type
class GatewayDetailsResponse(dict):
    """
    The gateway details.
    """
    def __init__(__self__, *,
                 dmts_cluster_uri: str,
                 gateway_object_id: str,
                 gateway_resource_id: Optional[str] = None):
        """
        The gateway details.
        :param str dmts_cluster_uri: Uri of the DMTS cluster.
        :param str gateway_object_id: Gateway object id from in the DMTS cluster for the gateway resource.
        :param str gateway_resource_id: Gateway resource to be associated with the server.
        """
        pulumi.set(__self__, "dmts_cluster_uri", dmts_cluster_uri)
        pulumi.set(__self__, "gateway_object_id", gateway_object_id)
        if gateway_resource_id is not None:
            pulumi.set(__self__, "gateway_resource_id", gateway_resource_id)

    @property
    @pulumi.getter(name="dmtsClusterUri")
    def dmts_cluster_uri(self) -> str:
        """
        Uri of the DMTS cluster.
        """
        return pulumi.get(self, "dmts_cluster_uri")

    @property
    @pulumi.getter(name="gatewayObjectId")
    def gateway_object_id(self) -> str:
        """
        Gateway object id from in the DMTS cluster for the gateway resource.
        """
        return pulumi.get(self, "gateway_object_id")

    @property
    @pulumi.getter(name="gatewayResourceId")
    def gateway_resource_id(self) -> Optional[str]:
        """
        Gateway resource to be associated with the server.
        """
        return pulumi.get(self, "gateway_resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IPv4FirewallRuleResponse(dict):
    """
    The detail of firewall rule.
    """
    def __init__(__self__, *,
                 firewall_rule_name: Optional[str] = None,
                 range_end: Optional[str] = None,
                 range_start: Optional[str] = None):
        """
        The detail of firewall rule.
        :param str firewall_rule_name: The rule name.
        :param str range_end: The end range of IPv4.
        :param str range_start: The start range of IPv4.
        """
        if firewall_rule_name is not None:
            pulumi.set(__self__, "firewall_rule_name", firewall_rule_name)
        if range_end is not None:
            pulumi.set(__self__, "range_end", range_end)
        if range_start is not None:
            pulumi.set(__self__, "range_start", range_start)

    @property
    @pulumi.getter(name="firewallRuleName")
    def firewall_rule_name(self) -> Optional[str]:
        """
        The rule name.
        """
        return pulumi.get(self, "firewall_rule_name")

    @property
    @pulumi.getter(name="rangeEnd")
    def range_end(self) -> Optional[str]:
        """
        The end range of IPv4.
        """
        return pulumi.get(self, "range_end")

    @property
    @pulumi.getter(name="rangeStart")
    def range_start(self) -> Optional[str]:
        """
        The start range of IPv4.
        """
        return pulumi.get(self, "range_start")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class IPv4FirewallSettingsResponse(dict):
    """
    An array of firewall rules.
    """
    def __init__(__self__, *,
                 enable_power_bi_service: Optional[bool] = None,
                 firewall_rules: Optional[Sequence['outputs.IPv4FirewallRuleResponse']] = None):
        """
        An array of firewall rules.
        :param bool enable_power_bi_service: The indicator of enabling PBI service.
        :param Sequence['IPv4FirewallRuleResponseArgs'] firewall_rules: An array of firewall rules.
        """
        if enable_power_bi_service is not None:
            pulumi.set(__self__, "enable_power_bi_service", enable_power_bi_service)
        if firewall_rules is not None:
            pulumi.set(__self__, "firewall_rules", firewall_rules)

    @property
    @pulumi.getter(name="enablePowerBIService")
    def enable_power_bi_service(self) -> Optional[bool]:
        """
        The indicator of enabling PBI service.
        """
        return pulumi.get(self, "enable_power_bi_service")

    @property
    @pulumi.getter(name="firewallRules")
    def firewall_rules(self) -> Optional[Sequence['outputs.IPv4FirewallRuleResponse']]:
        """
        An array of firewall rules.
        """
        return pulumi.get(self, "firewall_rules")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ResourceSkuResponse(dict):
    """
    Represents the SKU name and Azure pricing tier for Analysis Services resource.
    """
    def __init__(__self__, *,
                 name: str,
                 capacity: Optional[int] = None,
                 tier: Optional[str] = None):
        """
        Represents the SKU name and Azure pricing tier for Analysis Services resource.
        :param str name: Name of the SKU level.
        :param int capacity: The number of instances in the read only query pool.
        :param str tier: The name of the Azure pricing tier to which the SKU applies.
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
    def name(self) -> str:
        """
        Name of the SKU level.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        The number of instances in the read only query pool.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        The name of the Azure pricing tier to which the SKU applies.
        """
        return pulumi.get(self, "tier")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ServerAdministratorsResponse(dict):
    """
    An array of administrator user identities.
    """
    def __init__(__self__, *,
                 members: Optional[Sequence[str]] = None):
        """
        An array of administrator user identities.
        :param Sequence[str] members: An array of administrator user identities.
        """
        if members is not None:
            pulumi.set(__self__, "members", members)

    @property
    @pulumi.getter
    def members(self) -> Optional[Sequence[str]]:
        """
        An array of administrator user identities.
        """
        return pulumi.get(self, "members")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


