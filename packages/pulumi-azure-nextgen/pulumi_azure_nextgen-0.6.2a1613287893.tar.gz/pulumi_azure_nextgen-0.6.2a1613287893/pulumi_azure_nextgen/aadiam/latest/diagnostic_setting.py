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

__all__ = ['DiagnosticSetting']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:aadiam:DiagnosticSetting'.""", DeprecationWarning)


class DiagnosticSetting(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:aadiam:DiagnosticSetting'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 event_hub_authorization_rule_id: Optional[pulumi.Input[str]] = None,
                 event_hub_name: Optional[pulumi.Input[str]] = None,
                 logs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LogSettingsArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service_bus_rule_id: Optional[pulumi.Input[str]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The diagnostic setting resource.
        Latest API Version: 2017-04-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] event_hub_authorization_rule_id: The resource Id for the event hub authorization rule.
        :param pulumi.Input[str] event_hub_name: The name of the event hub. If none is specified, the default event hub will be selected.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LogSettingsArgs']]]] logs: The list of logs settings.
        :param pulumi.Input[str] name: The name of the diagnostic setting.
        :param pulumi.Input[str] service_bus_rule_id: The service bus rule Id of the diagnostic setting. This is here to maintain backwards compatibility.
        :param pulumi.Input[str] storage_account_id: The resource ID of the storage account to which you would like to send Diagnostic Logs.
        :param pulumi.Input[str] workspace_id: The workspace ID (resource ID of a Log Analytics workspace) for a Log Analytics workspace to which you would like to send Diagnostic Logs. Example: /subscriptions/4b9e8510-67ab-4e9a-95a9-e2f1e570ea9c/resourceGroups/insights-integration/providers/Microsoft.OperationalInsights/workspaces/viruela2
        """
        pulumi.log.warn("DiagnosticSetting is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:aadiam:DiagnosticSetting'.")
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

            __props__['event_hub_authorization_rule_id'] = event_hub_authorization_rule_id
            __props__['event_hub_name'] = event_hub_name
            __props__['logs'] = logs
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['service_bus_rule_id'] = service_bus_rule_id
            __props__['storage_account_id'] = storage_account_id
            __props__['workspace_id'] = workspace_id
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:aadiam:DiagnosticSetting"), pulumi.Alias(type_="azure-nextgen:aadiam/v20170401:DiagnosticSetting")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DiagnosticSetting, __self__).__init__(
            'azure-nextgen:aadiam/latest:DiagnosticSetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DiagnosticSetting':
        """
        Get an existing DiagnosticSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DiagnosticSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="eventHubAuthorizationRuleId")
    def event_hub_authorization_rule_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource Id for the event hub authorization rule.
        """
        return pulumi.get(self, "event_hub_authorization_rule_id")

    @property
    @pulumi.getter(name="eventHubName")
    def event_hub_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the event hub. If none is specified, the default event hub will be selected.
        """
        return pulumi.get(self, "event_hub_name")

    @property
    @pulumi.getter
    def logs(self) -> pulumi.Output[Optional[Sequence['outputs.LogSettingsResponse']]]:
        """
        The list of logs settings.
        """
        return pulumi.get(self, "logs")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceBusRuleId")
    def service_bus_rule_id(self) -> pulumi.Output[Optional[str]]:
        """
        The service bus rule Id of the diagnostic setting. This is here to maintain backwards compatibility.
        """
        return pulumi.get(self, "service_bus_rule_id")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource ID of the storage account to which you would like to send Diagnostic Logs.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        The workspace ID (resource ID of a Log Analytics workspace) for a Log Analytics workspace to which you would like to send Diagnostic Logs. Example: /subscriptions/4b9e8510-67ab-4e9a-95a9-e2f1e570ea9c/resourceGroups/insights-integration/providers/Microsoft.OperationalInsights/workspaces/viruela2
        """
        return pulumi.get(self, "workspace_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

