# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['WebAppSlotConfigurationNames']


class WebAppSlotConfigurationNames(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_setting_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 azure_storage_config_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 connection_string_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Slot Config names azure resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] app_setting_names: List of application settings names.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] azure_storage_config_names: List of external Azure storage account identifiers.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] connection_string_names: List of connection string names.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
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

            __props__['app_setting_names'] = app_setting_names
            __props__['azure_storage_config_names'] = azure_storage_config_names
            __props__['connection_string_names'] = connection_string_names
            __props__['kind'] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/latest:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20150801:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20160801:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20181101:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppSlotConfigurationNames"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppSlotConfigurationNames")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppSlotConfigurationNames, __self__).__init__(
            'azure-nextgen:web/v20200601:WebAppSlotConfigurationNames',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppSlotConfigurationNames':
        """
        Get an existing WebAppSlotConfigurationNames resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppSlotConfigurationNames(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appSettingNames")
    def app_setting_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of application settings names.
        """
        return pulumi.get(self, "app_setting_names")

    @property
    @pulumi.getter(name="azureStorageConfigNames")
    def azure_storage_config_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of external Azure storage account identifiers.
        """
        return pulumi.get(self, "azure_storage_config_names")

    @property
    @pulumi.getter(name="connectionStringNames")
    def connection_string_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of connection string names.
        """
        return pulumi.get(self, "connection_string_names")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

