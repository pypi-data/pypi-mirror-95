# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['WebAppFunction']


class WebAppFunction(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[Any] = None,
                 config_href: Optional[pulumi.Input[str]] = None,
                 files: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 function_app_id: Optional[pulumi.Input[str]] = None,
                 function_name: Optional[pulumi.Input[str]] = None,
                 href: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 script_href: Optional[pulumi.Input[str]] = None,
                 script_root_path_href: Optional[pulumi.Input[str]] = None,
                 secrets_file_href: Optional[pulumi.Input[str]] = None,
                 test_data: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Web Job Information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param Any config: Config information.
        :param pulumi.Input[str] config_href: Config URI.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] files: File list.
        :param pulumi.Input[str] function_app_id: Function App ID.
        :param pulumi.Input[str] function_name: Function name.
        :param pulumi.Input[str] href: Function URI.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Site name.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] script_href: Script URI.
        :param pulumi.Input[str] script_root_path_href: Script root path URI.
        :param pulumi.Input[str] secrets_file_href: Secrets file URI.
        :param pulumi.Input[str] test_data: Test data used when testing via the Azure Portal.
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

            __props__['config'] = config
            __props__['config_href'] = config_href
            __props__['files'] = files
            __props__['function_app_id'] = function_app_id
            if function_name is None and not opts.urn:
                raise TypeError("Missing required property 'function_name'")
            __props__['function_name'] = function_name
            __props__['href'] = href
            __props__['kind'] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['script_href'] = script_href
            __props__['script_root_path_href'] = script_root_path_href
            __props__['secrets_file_href'] = secrets_file_href
            __props__['test_data'] = test_data
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/latest:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/v20160801:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppFunction"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppFunction")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppFunction, __self__).__init__(
            'azure-nextgen:web/v20181101:WebAppFunction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppFunction':
        """
        Get an existing WebAppFunction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppFunction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output[Optional[Any]]:
        """
        Config information.
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="configHref")
    def config_href(self) -> pulumi.Output[Optional[str]]:
        """
        Config URI.
        """
        return pulumi.get(self, "config_href")

    @property
    @pulumi.getter
    def files(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        File list.
        """
        return pulumi.get(self, "files")

    @property
    @pulumi.getter(name="functionAppId")
    def function_app_id(self) -> pulumi.Output[Optional[str]]:
        """
        Function App ID.
        """
        return pulumi.get(self, "function_app_id")

    @property
    @pulumi.getter
    def href(self) -> pulumi.Output[Optional[str]]:
        """
        Function URI.
        """
        return pulumi.get(self, "href")

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
    @pulumi.getter(name="scriptHref")
    def script_href(self) -> pulumi.Output[Optional[str]]:
        """
        Script URI.
        """
        return pulumi.get(self, "script_href")

    @property
    @pulumi.getter(name="scriptRootPathHref")
    def script_root_path_href(self) -> pulumi.Output[Optional[str]]:
        """
        Script root path URI.
        """
        return pulumi.get(self, "script_root_path_href")

    @property
    @pulumi.getter(name="secretsFileHref")
    def secrets_file_href(self) -> pulumi.Output[Optional[str]]:
        """
        Secrets file URI.
        """
        return pulumi.get(self, "secrets_file_href")

    @property
    @pulumi.getter(name="testData")
    def test_data(self) -> pulumi.Output[Optional[str]]:
        """
        Test data used when testing via the Azure Portal.
        """
        return pulumi.get(self, "test_data")

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

