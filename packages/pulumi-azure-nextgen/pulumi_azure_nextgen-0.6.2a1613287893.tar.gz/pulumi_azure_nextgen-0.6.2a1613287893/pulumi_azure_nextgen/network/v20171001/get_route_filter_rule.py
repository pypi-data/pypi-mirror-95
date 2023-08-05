# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetRouteFilterRuleResult',
    'AwaitableGetRouteFilterRuleResult',
    'get_route_filter_rule',
]

@pulumi.output_type
class GetRouteFilterRuleResult:
    """
    Route Filter Rule Resource
    """
    def __init__(__self__, access=None, communities=None, etag=None, id=None, location=None, name=None, provisioning_state=None, route_filter_rule_type=None, tags=None):
        if access and not isinstance(access, str):
            raise TypeError("Expected argument 'access' to be a str")
        pulumi.set(__self__, "access", access)
        if communities and not isinstance(communities, list):
            raise TypeError("Expected argument 'communities' to be a list")
        pulumi.set(__self__, "communities", communities)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if route_filter_rule_type and not isinstance(route_filter_rule_type, str):
            raise TypeError("Expected argument 'route_filter_rule_type' to be a str")
        pulumi.set(__self__, "route_filter_rule_type", route_filter_rule_type)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def access(self) -> str:
        """
        The access type of the rule. Valid values are: 'Allow', 'Deny'
        """
        return pulumi.get(self, "access")

    @property
    @pulumi.getter
    def communities(self) -> Sequence[str]:
        """
        The collection for bgp community values to filter on. e.g. ['12076:5010','12076:5020']
        """
        return pulumi.get(self, "communities")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource. Possible values are: 'Updating', 'Deleting', 'Succeeded' and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="routeFilterRuleType")
    def route_filter_rule_type(self) -> str:
        """
        The rule type of the rule. Valid value is: 'Community'
        """
        return pulumi.get(self, "route_filter_rule_type")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRouteFilterRuleResult(GetRouteFilterRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRouteFilterRuleResult(
            access=self.access,
            communities=self.communities,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            route_filter_rule_type=self.route_filter_rule_type,
            tags=self.tags)


def get_route_filter_rule(resource_group_name: Optional[str] = None,
                          route_filter_name: Optional[str] = None,
                          rule_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRouteFilterRuleResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_group_name: The name of the resource group.
    :param str route_filter_name: The name of the route filter.
    :param str rule_name: The name of the rule.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['routeFilterName'] = route_filter_name
    __args__['ruleName'] = rule_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:network/v20171001:getRouteFilterRule', __args__, opts=opts, typ=GetRouteFilterRuleResult).value

    return AwaitableGetRouteFilterRuleResult(
        access=__ret__.access,
        communities=__ret__.communities,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        route_filter_rule_type=__ret__.route_filter_rule_type,
        tags=__ret__.tags)
