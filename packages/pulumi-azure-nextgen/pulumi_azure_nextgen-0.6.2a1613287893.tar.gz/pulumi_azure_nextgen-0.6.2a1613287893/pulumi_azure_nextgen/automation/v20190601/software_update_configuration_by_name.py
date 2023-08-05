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

__all__ = ['SoftwareUpdateConfigurationByName']


class SoftwareUpdateConfigurationByName(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 error: Optional[pulumi.Input[pulumi.InputType['ErrorResponseArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_info: Optional[pulumi.Input[pulumi.InputType['SUCSchedulePropertiesArgs']]] = None,
                 software_update_configuration_name: Optional[pulumi.Input[str]] = None,
                 tasks: Optional[pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTasksArgs']]] = None,
                 update_configuration: Optional[pulumi.Input[pulumi.InputType['UpdateConfigurationArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Software update configuration properties.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[pulumi.InputType['ErrorResponseArgs']] error: Details of provisioning error
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[pulumi.InputType['SUCSchedulePropertiesArgs']] schedule_info: Schedule information for the Software update configuration
        :param pulumi.Input[str] software_update_configuration_name: The name of the software update configuration to be created.
        :param pulumi.Input[pulumi.InputType['SoftwareUpdateConfigurationTasksArgs']] tasks: Tasks information for the Software update configuration.
        :param pulumi.Input[pulumi.InputType['UpdateConfigurationArgs']] update_configuration: update specific properties for the Software update configuration
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

            if automation_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_name'")
            __props__['automation_account_name'] = automation_account_name
            __props__['error'] = error
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if schedule_info is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_info'")
            __props__['schedule_info'] = schedule_info
            if software_update_configuration_name is None and not opts.urn:
                raise TypeError("Missing required property 'software_update_configuration_name'")
            __props__['software_update_configuration_name'] = software_update_configuration_name
            __props__['tasks'] = tasks
            if update_configuration is None and not opts.urn:
                raise TypeError("Missing required property 'update_configuration'")
            __props__['update_configuration'] = update_configuration
            __props__['created_by'] = None
            __props__['creation_time'] = None
            __props__['last_modified_by'] = None
            __props__['last_modified_time'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:automation:SoftwareUpdateConfigurationByName"), pulumi.Alias(type_="azure-nextgen:automation/latest:SoftwareUpdateConfigurationByName"), pulumi.Alias(type_="azure-nextgen:automation/v20170515preview:SoftwareUpdateConfigurationByName")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SoftwareUpdateConfigurationByName, __self__).__init__(
            'azure-nextgen:automation/v20190601:SoftwareUpdateConfigurationByName',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SoftwareUpdateConfigurationByName':
        """
        Get an existing SoftwareUpdateConfigurationByName resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SoftwareUpdateConfigurationByName(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> pulumi.Output[str]:
        """
        CreatedBy property, which only appears in the response.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        Creation time of the resource, which only appears in the response.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def error(self) -> pulumi.Output[Optional['outputs.ErrorResponseResponse']]:
        """
        Details of provisioning error
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> pulumi.Output[str]:
        """
        LastModifiedBy property, which only appears in the response.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Last time resource was modified, which only appears in the response.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state for the software update configuration, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="scheduleInfo")
    def schedule_info(self) -> pulumi.Output['outputs.SUCSchedulePropertiesResponse']:
        """
        Schedule information for the Software update configuration
        """
        return pulumi.get(self, "schedule_info")

    @property
    @pulumi.getter
    def tasks(self) -> pulumi.Output[Optional['outputs.SoftwareUpdateConfigurationTasksResponse']]:
        """
        Tasks information for the Software update configuration.
        """
        return pulumi.get(self, "tasks")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updateConfiguration")
    def update_configuration(self) -> pulumi.Output['outputs.UpdateConfigurationResponse']:
        """
        update specific properties for the Software update configuration
        """
        return pulumi.get(self, "update_configuration")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

