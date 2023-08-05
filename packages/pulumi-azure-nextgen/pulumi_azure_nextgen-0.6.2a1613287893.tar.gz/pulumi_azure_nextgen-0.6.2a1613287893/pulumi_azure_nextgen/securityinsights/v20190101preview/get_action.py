# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetActionResult',
    'AwaitableGetActionResult',
    'get_action',
]

@pulumi.output_type
class GetActionResult:
    """
    Action for alert rule.
    """
    def __init__(__self__, etag=None, id=None, logic_app_resource_id=None, name=None, type=None, workflow_id=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if logic_app_resource_id and not isinstance(logic_app_resource_id, str):
            raise TypeError("Expected argument 'logic_app_resource_id' to be a str")
        pulumi.set(__self__, "logic_app_resource_id", logic_app_resource_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if workflow_id and not isinstance(workflow_id, str):
            raise TypeError("Expected argument 'workflow_id' to be a str")
        pulumi.set(__self__, "workflow_id", workflow_id)

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the action.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="logicAppResourceId")
    def logic_app_resource_id(self) -> Optional[str]:
        """
        Logic App Resource Id, /subscriptions/{my-subscription}/resourceGroups/{my-resource-group}/providers/Microsoft.Logic/workflows/{my-workflow-id}.
        """
        return pulumi.get(self, "logic_app_resource_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workflowId")
    def workflow_id(self) -> Optional[str]:
        """
        The name of the logic app's workflow.
        """
        return pulumi.get(self, "workflow_id")


class AwaitableGetActionResult(GetActionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActionResult(
            etag=self.etag,
            id=self.id,
            logic_app_resource_id=self.logic_app_resource_id,
            name=self.name,
            type=self.type,
            workflow_id=self.workflow_id)


def get_action(action_id: Optional[str] = None,
               operational_insights_resource_provider: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               rule_id: Optional[str] = None,
               workspace_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActionResult:
    """
    Use this data source to access information about an existing resource.

    :param str action_id: Action ID
    :param str operational_insights_resource_provider: The namespace of workspaces resource provider- Microsoft.OperationalInsights.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['actionId'] = action_id
    __args__['operationalInsightsResourceProvider'] = operational_insights_resource_provider
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleId'] = rule_id
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:securityinsights/v20190101preview:getAction', __args__, opts=opts, typ=GetActionResult).value

    return AwaitableGetActionResult(
        etag=__ret__.etag,
        id=__ret__.id,
        logic_app_resource_id=__ret__.logic_app_resource_id,
        name=__ret__.name,
        type=__ret__.type,
        workflow_id=__ret__.workflow_id)
