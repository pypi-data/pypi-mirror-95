# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['RegistrationDefinition']


class RegistrationDefinition(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 plan: Optional[pulumi.Input[pulumi.InputType['PlanArgs']]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['RegistrationDefinitionPropertiesArgs']]] = None,
                 registration_definition_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Registration definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PlanArgs']] plan: Plan details for the managed services.
        :param pulumi.Input[pulumi.InputType['RegistrationDefinitionPropertiesArgs']] properties: Properties of a registration definition.
        :param pulumi.Input[str] registration_definition_id: Guid of the registration definition.
        :param pulumi.Input[str] scope: Scope of the resource.
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

            __props__['plan'] = plan
            __props__['properties'] = properties
            if registration_definition_id is None and not opts.urn:
                raise TypeError("Missing required property 'registration_definition_id'")
            __props__['registration_definition_id'] = registration_definition_id
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__['scope'] = scope
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:managedservices:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/latest:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20180601preview:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20190401preview:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20190901:RegistrationDefinition"), pulumi.Alias(type_="azure-nextgen:managedservices/v20200201preview:RegistrationDefinition")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RegistrationDefinition, __self__).__init__(
            'azure-nextgen:managedservices/v20190601:RegistrationDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RegistrationDefinition':
        """
        Get an existing RegistrationDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return RegistrationDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the registration definition.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def plan(self) -> pulumi.Output[Optional['outputs.PlanResponse']]:
        """
        Plan details for the managed services.
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.RegistrationDefinitionPropertiesResponse']:
        """
        Properties of a registration definition.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

