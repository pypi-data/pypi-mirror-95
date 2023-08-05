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

__all__ = ['Connection']

warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:automation:Connection'.""", DeprecationWarning)


class Connection(pulumi.CustomResource):
    warnings.warn("""The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:automation:Connection'.""", DeprecationWarning)

    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 connection_type: Optional[pulumi.Input[pulumi.InputType['ConnectionTypeAssociationPropertyArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 field_definition_values: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Definition of the connection.
        Latest API Version: 2019-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] connection_name: The parameters supplied to the create or update connection operation.
        :param pulumi.Input[pulumi.InputType['ConnectionTypeAssociationPropertyArgs']] connection_type: Gets or sets the connectionType of the connection.
        :param pulumi.Input[str] description: Gets or sets the description of the connection.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] field_definition_values: Gets or sets the field definition properties of the connection.
        :param pulumi.Input[str] name: Gets or sets the name of the connection.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        """
        pulumi.log.warn("Connection is deprecated: The 'latest' version is deprecated. Please migrate to the resource in the top-level module: 'azure-nextgen:automation:Connection'.")
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
            if connection_name is None and not opts.urn:
                raise TypeError("Missing required property 'connection_name'")
            __props__['connection_name'] = connection_name
            if connection_type is None and not opts.urn:
                raise TypeError("Missing required property 'connection_type'")
            __props__['connection_type'] = connection_type
            __props__['description'] = description
            __props__['field_definition_values'] = field_definition_values
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['creation_time'] = None
            __props__['last_modified_time'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:automation:Connection"), pulumi.Alias(type_="azure-nextgen:automation/v20151031:Connection"), pulumi.Alias(type_="azure-nextgen:automation/v20190601:Connection"), pulumi.Alias(type_="azure-nextgen:automation/v20200113preview:Connection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Connection, __self__).__init__(
            'azure-nextgen:automation/latest:Connection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Connection':
        """
        Get an existing Connection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Connection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionType")
    def connection_type(self) -> pulumi.Output[Optional['outputs.ConnectionTypeAssociationPropertyResponse']]:
        """
        Gets or sets the connectionType of the connection.
        """
        return pulumi.get(self, "connection_type")

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
    @pulumi.getter(name="fieldDefinitionValues")
    def field_definition_values(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Gets the field definition values of the connection.
        """
        return pulumi.get(self, "field_definition_values")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Gets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

