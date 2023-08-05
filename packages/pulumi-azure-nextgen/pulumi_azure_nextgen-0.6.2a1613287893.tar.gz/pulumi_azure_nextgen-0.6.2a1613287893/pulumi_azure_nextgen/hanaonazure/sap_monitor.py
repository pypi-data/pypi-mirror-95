# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables

__all__ = ['SapMonitor']


class SapMonitor(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_customer_analytics: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_arm_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_id: Optional[pulumi.Input[str]] = None,
                 log_analytics_workspace_shared_key: Optional[pulumi.Input[str]] = None,
                 monitor_subnet: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_monitor_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        SAP monitor info on Azure (ARM properties and SAP monitor properties)
        API Version: 2020-02-07-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable_customer_analytics: The value indicating whether to send analytics to Microsoft
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] log_analytics_workspace_arm_id: The ARM ID of the Log Analytics Workspace that is used for monitoring
        :param pulumi.Input[str] log_analytics_workspace_id: The workspace ID of the log analytics workspace to be used for monitoring
        :param pulumi.Input[str] log_analytics_workspace_shared_key: The shared key of the log analytics workspace that is used for monitoring
        :param pulumi.Input[str] monitor_subnet: The subnet which the SAP monitor will be deployed in
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
        :param pulumi.Input[str] sap_monitor_name: Name of the SAP monitor resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
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

            __props__['enable_customer_analytics'] = enable_customer_analytics
            __props__['location'] = location
            __props__['log_analytics_workspace_arm_id'] = log_analytics_workspace_arm_id
            __props__['log_analytics_workspace_id'] = log_analytics_workspace_id
            __props__['log_analytics_workspace_shared_key'] = log_analytics_workspace_shared_key
            __props__['monitor_subnet'] = monitor_subnet
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sap_monitor_name is None and not opts.urn:
                raise TypeError("Missing required property 'sap_monitor_name'")
            __props__['sap_monitor_name'] = sap_monitor_name
            __props__['tags'] = tags
            __props__['managed_resource_group_name'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['sap_monitor_collector_version'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:hanaonazure/v20200207preview:SapMonitor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SapMonitor, __self__).__init__(
            'azure-nextgen:hanaonazure:SapMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SapMonitor':
        """
        Get an existing SapMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SapMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="enableCustomerAnalytics")
    def enable_customer_analytics(self) -> pulumi.Output[Optional[bool]]:
        """
        The value indicating whether to send analytics to Microsoft
        """
        return pulumi.get(self, "enable_customer_analytics")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceArmId")
    def log_analytics_workspace_arm_id(self) -> pulumi.Output[Optional[str]]:
        """
        The ARM ID of the Log Analytics Workspace that is used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_arm_id")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> pulumi.Output[Optional[str]]:
        """
        The workspace ID of the log analytics workspace to be used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_id")

    @property
    @pulumi.getter(name="logAnalyticsWorkspaceSharedKey")
    def log_analytics_workspace_shared_key(self) -> pulumi.Output[Optional[str]]:
        """
        The shared key of the log analytics workspace that is used for monitoring
        """
        return pulumi.get(self, "log_analytics_workspace_shared_key")

    @property
    @pulumi.getter(name="managedResourceGroupName")
    def managed_resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group the SAP Monitor resources get deployed into.
        """
        return pulumi.get(self, "managed_resource_group_name")

    @property
    @pulumi.getter(name="monitorSubnet")
    def monitor_subnet(self) -> pulumi.Output[Optional[str]]:
        """
        The subnet which the SAP monitor will be deployed in
        """
        return pulumi.get(self, "monitor_subnet")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        State of provisioning of the HanaInstance
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sapMonitorCollectorVersion")
    def sap_monitor_collector_version(self) -> pulumi.Output[str]:
        """
        The version of the payload running in the Collector VM
        """
        return pulumi.get(self, "sap_monitor_collector_version")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

