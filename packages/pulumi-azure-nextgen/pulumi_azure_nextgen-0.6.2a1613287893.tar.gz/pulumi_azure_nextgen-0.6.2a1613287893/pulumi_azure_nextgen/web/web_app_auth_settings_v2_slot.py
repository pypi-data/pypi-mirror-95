# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from .. import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['WebAppAuthSettingsV2Slot']


class WebAppAuthSettingsV2Slot(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_validation: Optional[pulumi.Input[pulumi.InputType['GlobalValidationArgs']]] = None,
                 http_settings: Optional[pulumi.Input[pulumi.InputType['HttpSettingsArgs']]] = None,
                 identity_providers: Optional[pulumi.Input[pulumi.InputType['IdentityProvidersArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 login: Optional[pulumi.Input[pulumi.InputType['LoginArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[pulumi.InputType['AuthPlatformArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        API Version: 2020-10-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of web app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of web app slot. If not specified then will default to production slot.
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

            __props__['global_validation'] = global_validation
            __props__['http_settings'] = http_settings
            __props__['identity_providers'] = identity_providers
            __props__['kind'] = kind
            __props__['login'] = login
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['platform'] = platform
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__['slot'] = slot
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web/latest:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-nextgen:web/v20201001:WebAppAuthSettingsV2Slot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppAuthSettingsV2Slot, __self__).__init__(
            'azure-nextgen:web:WebAppAuthSettingsV2Slot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppAuthSettingsV2Slot':
        """
        Get an existing WebAppAuthSettingsV2Slot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppAuthSettingsV2Slot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="globalValidation")
    def global_validation(self) -> pulumi.Output[Optional['outputs.GlobalValidationResponse']]:
        return pulumi.get(self, "global_validation")

    @property
    @pulumi.getter(name="httpSettings")
    def http_settings(self) -> pulumi.Output[Optional['outputs.HttpSettingsResponse']]:
        return pulumi.get(self, "http_settings")

    @property
    @pulumi.getter(name="identityProviders")
    def identity_providers(self) -> pulumi.Output[Optional['outputs.IdentityProvidersResponse']]:
        return pulumi.get(self, "identity_providers")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def login(self) -> pulumi.Output[Optional['outputs.LoginResponse']]:
        return pulumi.get(self, "login")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> pulumi.Output[Optional['outputs.AuthPlatformResponse']]:
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

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

