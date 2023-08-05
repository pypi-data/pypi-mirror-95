# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['Action']


class Action(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action_id: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 logic_app_resource_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 rule_id: Optional[pulumi.Input[str]] = None,
                 trigger_uri: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Action for alert rule.
        API Version: 2020-01-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action_id: Action ID
        :param pulumi.Input[str] etag: Etag of the azure resource
        :param pulumi.Input[str] logic_app_resource_id: Logic App Resource Id, /subscriptions/{my-subscription}/resourceGroups/{my-resource-group}/providers/Microsoft.Logic/workflows/{my-workflow-id}.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] rule_id: Alert rule ID
        :param pulumi.Input[str] trigger_uri: Logic App Callback URL for this specific workflow.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
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

            if action_id is None and not opts.urn:
                raise TypeError("Missing required property 'action_id'")
            __props__['action_id'] = action_id
            __props__['etag'] = etag
            if logic_app_resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'logic_app_resource_id'")
            __props__['logic_app_resource_id'] = logic_app_resource_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if rule_id is None and not opts.urn:
                raise TypeError("Missing required property 'rule_id'")
            __props__['rule_id'] = rule_id
            __props__['trigger_uri'] = trigger_uri
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__['workspace_name'] = workspace_name
            __props__['name'] = None
            __props__['type'] = None
            __props__['workflow_id'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:securityinsights/latest:Action"), pulumi.Alias(type_="azure-nextgen:securityinsights/v20200101:Action")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Action, __self__).__init__(
            'azure-nextgen:securityinsights:Action',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Action':
        """
        Get an existing Action resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Action(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the action.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="logicAppResourceId")
    def logic_app_resource_id(self) -> pulumi.Output[str]:
        """
        Logic App Resource Id, /subscriptions/{my-subscription}/resourceGroups/{my-resource-group}/providers/Microsoft.Logic/workflows/{my-workflow-id}.
        """
        return pulumi.get(self, "logic_app_resource_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workflowId")
    def workflow_id(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the logic app's workflow.
        """
        return pulumi.get(self, "workflow_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

