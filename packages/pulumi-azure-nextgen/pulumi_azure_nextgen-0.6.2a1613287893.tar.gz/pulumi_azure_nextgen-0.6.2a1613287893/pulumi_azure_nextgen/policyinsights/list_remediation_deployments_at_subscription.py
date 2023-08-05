# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'ListRemediationDeploymentsAtSubscriptionResult',
    'AwaitableListRemediationDeploymentsAtSubscriptionResult',
    'list_remediation_deployments_at_subscription',
]

@pulumi.output_type
class ListRemediationDeploymentsAtSubscriptionResult:
    """
    List of deployments for a remediation.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> str:
        """
        The URL to get the next set of results.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.RemediationDeploymentResponseResult']:
        """
        Array of deployments for the remediation.
        """
        return pulumi.get(self, "value")


class AwaitableListRemediationDeploymentsAtSubscriptionResult(ListRemediationDeploymentsAtSubscriptionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListRemediationDeploymentsAtSubscriptionResult(
            next_link=self.next_link,
            value=self.value)


def list_remediation_deployments_at_subscription(remediation_name: Optional[str] = None,
                                                 top: Optional[int] = None,
                                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListRemediationDeploymentsAtSubscriptionResult:
    """
    Use this data source to access information about an existing resource.

    :param str remediation_name: The name of the remediation.
    :param int top: Maximum number of records to return.
    """
    __args__ = dict()
    __args__['remediationName'] = remediation_name
    __args__['top'] = top
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:policyinsights:listRemediationDeploymentsAtSubscription', __args__, opts=opts, typ=ListRemediationDeploymentsAtSubscriptionResult).value

    return AwaitableListRemediationDeploymentsAtSubscriptionResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
