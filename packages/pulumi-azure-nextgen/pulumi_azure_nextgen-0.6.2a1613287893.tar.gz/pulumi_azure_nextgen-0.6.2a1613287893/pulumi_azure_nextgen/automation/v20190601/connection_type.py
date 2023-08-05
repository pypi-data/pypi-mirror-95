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

__all__ = ['ConnectionType']


class ConnectionType(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 connection_type_name: Optional[pulumi.Input[str]] = None,
                 field_definitions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['FieldDefinitionArgs']]]]] = None,
                 is_global: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Definition of the connection type.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] connection_type_name: The parameters supplied to the create or update connection type operation.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['FieldDefinitionArgs']]]] field_definitions: Gets or sets the field definitions of the connection type.
        :param pulumi.Input[bool] is_global: Gets or sets a Boolean value to indicate if the connection type is global.
        :param pulumi.Input[str] name: Gets or sets the name of the connection type.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
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
            if connection_type_name is None and not opts.urn:
                raise TypeError("Missing required property 'connection_type_name'")
            __props__['connection_type_name'] = connection_type_name
            if field_definitions is None and not opts.urn:
                raise TypeError("Missing required property 'field_definitions'")
            __props__['field_definitions'] = field_definitions
            __props__['is_global'] = is_global
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['creation_time'] = None
            __props__['description'] = None
            __props__['last_modified_time'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:automation:ConnectionType"), pulumi.Alias(type_="azure-nextgen:automation/latest:ConnectionType"), pulumi.Alias(type_="azure-nextgen:automation/v20151031:ConnectionType"), pulumi.Alias(type_="azure-nextgen:automation/v20200113preview:ConnectionType")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ConnectionType, __self__).__init__(
            'azure-nextgen:automation/v20190601:ConnectionType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConnectionType':
        """
        Get an existing ConnectionType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ConnectionType(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        Gets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fieldDefinitions")
    def field_definitions(self) -> pulumi.Output[Mapping[str, 'outputs.FieldDefinitionResponse']]:
        """
        Gets the field definitions of the connection type.
        """
        return pulumi.get(self, "field_definitions")

    @property
    @pulumi.getter(name="isGlobal")
    def is_global(self) -> pulumi.Output[Optional[bool]]:
        """
        Gets or sets a Boolean value to indicate if the connection type is global.
        """
        return pulumi.get(self, "is_global")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets the name of the connection type.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

