# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = ['ConfigurationAssignmentParent']


class ConfigurationAssignmentParent(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration_assignment_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_configuration_id: Optional[pulumi.Input[str]] = None,
                 provider_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 resource_parent_name: Optional[pulumi.Input[str]] = None,
                 resource_parent_type: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Configuration Assignment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] configuration_assignment_name: Configuration assignment name
        :param pulumi.Input[str] location: Location of the resource
        :param pulumi.Input[str] maintenance_configuration_id: The maintenance configuration Id
        :param pulumi.Input[str] provider_name: Resource provider name
        :param pulumi.Input[str] resource_group_name: Resource group name
        :param pulumi.Input[str] resource_id: The unique resourceId
        :param pulumi.Input[str] resource_name_: Resource identifier
        :param pulumi.Input[str] resource_parent_name: Resource parent identifier
        :param pulumi.Input[str] resource_parent_type: Resource parent type
        :param pulumi.Input[str] resource_type: Resource type
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

            if configuration_assignment_name is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_assignment_name'")
            __props__['configuration_assignment_name'] = configuration_assignment_name
            __props__['location'] = location
            __props__['maintenance_configuration_id'] = maintenance_configuration_id
            if provider_name is None and not opts.urn:
                raise TypeError("Missing required property 'provider_name'")
            __props__['provider_name'] = provider_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['resource_id'] = resource_id
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__['resource_name'] = resource_name_
            if resource_parent_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_parent_name'")
            __props__['resource_parent_name'] = resource_parent_name
            if resource_parent_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_parent_type'")
            __props__['resource_parent_type'] = resource_parent_type
            if resource_type is None and not opts.urn:
                raise TypeError("Missing required property 'resource_type'")
            __props__['resource_type'] = resource_type
            __props__['name'] = None
            __props__['system_data'] = None
            __props__['type'] = None
        super(ConfigurationAssignmentParent, __self__).__init__(
            'azure-nextgen:maintenance/v20210401preview:ConfigurationAssignmentParent',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConfigurationAssignmentParent':
        """
        Get an existing ConfigurationAssignmentParent resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ConfigurationAssignmentParent(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Location of the resource
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceConfigurationId")
    def maintenance_configuration_id(self) -> pulumi.Output[Optional[str]]:
        """
        The maintenance configuration Id
        """
        return pulumi.get(self, "maintenance_configuration_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The unique resourceId
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

