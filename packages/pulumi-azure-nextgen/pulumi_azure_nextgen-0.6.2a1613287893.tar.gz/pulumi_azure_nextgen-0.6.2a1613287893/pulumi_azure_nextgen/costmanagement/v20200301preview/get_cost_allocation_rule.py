# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'GetCostAllocationRuleResult',
    'AwaitableGetCostAllocationRuleResult',
    'get_cost_allocation_rule',
]

@pulumi.output_type
class GetCostAllocationRuleResult:
    """
    The cost allocation rule model definition
    """
    def __init__(__self__, id=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure Resource Manager Id for the rule. This is a read ony value.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the rule. This is a read only value.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.CostAllocationRulePropertiesResponse':
        """
        Cost allocation rule properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type of the rule. This is a read only value of Microsoft.CostManagement/CostAllocationRule.
        """
        return pulumi.get(self, "type")


class AwaitableGetCostAllocationRuleResult(GetCostAllocationRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCostAllocationRuleResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_cost_allocation_rule(billing_account_id: Optional[str] = None,
                             rule_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCostAllocationRuleResult:
    """
    Use this data source to access information about an existing resource.

    :param str billing_account_id: BillingAccount ID
    :param str rule_name: Cost allocation rule name. The name cannot include spaces or any non alphanumeric characters other than '_' and '-'. The max length is 260 characters.
    """
    __args__ = dict()
    __args__['billingAccountId'] = billing_account_id
    __args__['ruleName'] = rule_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:costmanagement/v20200301preview:getCostAllocationRule', __args__, opts=opts, typ=GetCostAllocationRuleResult).value

    return AwaitableGetCostAllocationRuleResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)
